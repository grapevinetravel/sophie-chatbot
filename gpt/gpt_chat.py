import json
import logging
from openai import OpenAI
import os

from gpt.context_manager import manage_context, cleanup_old_conversations
from gpt.router import handle_function_call
from gpt.short_circuits.short_circuits import ShortCircuit
from schemas import all_schemas

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

short_circuit = ShortCircuit()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_chat(user_message: str, conversation_id: str, session_store: dict,
    context_strategy="smart_compression", max_context_tokens=100000):
  """
    Run chat with context management

    Args:
        user_message: User's input message
        conversation_id: Unique conversation identifier
        session_store: Dictionary storing all conversations
        context_strategy: Strategy for managing context size
        max_context_tokens: Maximum tokens to keep in context
    """

  # Initialize conversation if not exists
  if conversation_id not in session_store:
    session_store[conversation_id] = [{
      "role": "system",
      "content": (
        "You are a corporate travel assistant for business travelers. Your role is to help users find and book hotels for upcoming trips. "
        "Follow the workflow below precisely and avoid off-topic or creative responses.\n\n"

        "Behavior Rules:\n"
        "- Do not generate code, poems, jokes, stories, or creative content.\n"
        "- Do not engage in small talk or answer unrelated topics (sports, news, history, entertainment).\n"
        "- Always respond concisely, professionally, and task-focused.\n"
        "- Do not assume or fabricate details. Do not invent examples.\n"
        "- Do not return hotels that don't meet rating or other user criteria.\n\n"
        "- Do not help with anything but travel related content.\n\n"
        
        "Workflow:\n"
        "2. If both last name and email are provided, call `resolve_user_and_trips(email, last_name)`:\n"
        "   - If `user_uuid` is empty, do not mention lookup failure. Continue with manual support.\n"
        "   - If trips are found, display them using this format:\n"
        "     <ul>\n"
        "     <li><strong>Flight:</strong> {flight_number}<br />"
        "<strong>Destination:</strong> {destination}<br />"
        "<strong>Arrival:</strong> {arrival_date}</li>\n"
        "     </ul>\n"
        "     Ask the user to select one for hotel suggestions.\n"
        "3. If the user has not provided both email and last name, do not ask. Continue based on any given destination, dates, or preferences.\n"
        "4. When a trip is selected:\n"
        "   - Use `mapbox_search(destination)` to get coordinates and city name. Do your best to call with country code `mapbox_search(destination, country_code)` \n"
        "   - Call `get_hotels_by_corporate_geo(corporate_id, lat, long, radius_meters)`.\n"
        "   - If past stays are found for that destination city (case-insensitive match), display them like this:\n"
        "     <ul>\n"
        "     <li><strong>{hotel_name}</strong><br />{location}<br /><strong>Date:</strong> {date}</li>\n"
        "     </ul>\n"
        "   - Ask the user if they want to stay at one of them or see other options.\n"
        "5. If no past stays match the destination city, proceed without mentioning them.\n"
        "6. Gather check-in and check-out dates from the user only after a hotel is picked.\n"
        "   - You can suggest hotels without a check-in date, but ask for check-out to check availability.\n"
        "   - If a flight arrival date is known, use that as the check-in.\n"
        "   - Ask for hotel preferences: rating, brand, amenities, etc.\n"
        "7. To suggest hotels, use `search_hotels()`:\n"
        "   - Only return hotels that match the user's filters (e.g., rating).\n"
        "   - Use this display format:\n"
        "     <ul>\n"
        "     <li><strong>{name}</strong> ({rating}★) - {brand}<br />{address_line}, {city}<br />"
        "Price per night: {average_price}</li>\n"
        "     </ul>\n"
        "   - Ask if the user wants to check availability or see full details for any.\n"
        "8. If the user requests more information about a hotel, call `display_full_hotel_details(property_id)` (use expedia_id as the property_id).\n"
        "   - DO not call display_full_hotel_details(property_id) unless asked explicitly for full details of only one property, otherwise use the search_hotels.\n"
        "   - When asked explicitly for hotel images, use 'display_hotel_images(property_id)'\n"
        "9. If the user selects a hotel and provides check-in/check-out dates, call `check_availability(check-in, check-out, property_id)`:\n"
        "   - NEVER call `check_availability(check-in, check-out, property_id)` with a check-in or check-out value that is before 2025.\n"
        "   - Summarize room types and rates clearly.\n"
        "   - Ask if the user wants to proceed with booking or see more options.\n"
        "10. If the user asks about specific amenities (e.g., pool, gym, parking):\n"
        "    - Search the `vector_text` for keywords in the hotel's data.\n"
        "    - Only say 'not available' if no match is found in the description blocks.\n\n"
        "11. If the user asks to book a hotel:\n"
        "    - If the user provided his name and email, only ask for travel agent email\n\n"
        "    - If the user has not provided his name and email, ask for their travel agent email in order to send a reservation request. Also ask for their name and email to include in the mail, but only if they ask to book\n"
        "    - Call send_reservation_request with reservation details\n\n"
        "Formatting Guidelines:\n"
        "- Format all your responses as HTML. When using picture URLs make sure HTML is correct <img src= {url}> to render not display URL.\n"
        "- Use `<strong>` tags for labels like hotel name, rating, flight number, etc.\n"
        "- Keep output clean and easy to scan.\n\n"

        "Other:\n"
        "- Assume check-in is the flight arrival date unless specified. When year not specified, assume 2025.\n"
        "- Do not ask for last name or email, the user already know they'll receive better service if they provide them\n"
        "- Maintain a polite, helpful tone without unnecessary delays or filler phrases.\n"
        "- Always stay within the scope of business travel and hotel bookings.\n"
      )
    }]

  # Get current messages and add user message
  messages = session_store[conversation_id]
  messages.append({"role": "user", "content": user_message})

  # Apply context management BEFORE making API call
  messages = manage_context(
      messages,
      strategy=context_strategy,
      max_tokens=max_context_tokens
  )

  # Update session store with managed context
  session_store[conversation_id] = messages

  # Periodic cleanup of old conversations
  if len(session_store) > 100:  # Adjust threshold as needed
    cleanup_old_conversations(session_store, max_conversations=50)

  while True:
    try:
      response = client.chat.completions.create(
          model="gpt-4o",
          messages=messages,
          tools=[{"type": "function", "function": schema} for schema in all_schemas],
          tool_choice="auto"
      )

      message = response.choices[0].message

      # If a tool (function) needs to be called
      if hasattr(message, "tool_calls") and message.tool_calls:
        messages.append(message.model_dump())

        for tool_call in message.tool_calls:
          tool_name = tool_call.function.name
          arguments = json.loads(tool_call.function.arguments)

          result = handle_function_call(tool_name, arguments)
          reply = short_circuit.handle(tool_name, result)

          messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)[:10000]
          })

          if reply:
            messages.append({
              "role": "assistant",
              "content": reply
            })

            # Apply context management after tool responses
            messages = manage_context(
                messages,
                strategy=context_strategy,
                max_tokens=max_context_tokens
            )
            session_store[conversation_id] = messages
            return reply

        # Continue the loop for possible follow-up tool calls
        continue

      # If no tool call, this is the final assistant message
      final_reply = message.content
      messages.append({"role": "assistant", "content": final_reply})

      # Apply final context management
      messages = manage_context(
          messages,
          strategy=context_strategy,
          max_tokens=max_context_tokens
      )
      session_store[conversation_id] = messages
      return final_reply

    except Exception as e:
      logging.error(f"Error in chat completion: {e}")
      # Try context reduction on error (might be token limit)
      messages = manage_context(
          messages,
          strategy="truncate",  # Use more aggressive strategy
          max_tokens=max_context_tokens // 2
      )
      session_store[conversation_id] = messages

      # If still failing after context reduction, raise the error
      if len(messages) <= 2:  # Only system + user message left
        raise e