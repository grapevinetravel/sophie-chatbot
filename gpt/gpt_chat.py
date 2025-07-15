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
        "- Pay attention to user name and email and call `resolve_user_and_trips` as soon as you get them\n\n"

        "Workflow:\n"
        "1. Check carefully for last name and email. If both name and email are provided, call `resolve_user_and_trips(email, last_name)`:\n"
        "   - If `user_uuid` is empty, do not mention lookup failure. Continue with manual support.\n"
        "2. If the user has not provided both email and last name, do not ask. Continue based on any given destination, dates, or preferences.\n"
        "3. When a trip is selected:\n"
        "   - If the destination_lat and destination_lon are missing, use `mapbox_search(destination)` to get coordinates and city name. Do your best to call with country code `mapbox_search(destination, country_code)` \n"
        "   - Call `get_hotels_by_corporate_geo(corporate_id, lat, long, radius_meters)`.\n"
        "   - Ask the user if they want to stay at one of them or see other options.\n"
        "4. If no past stays match the destination city, proceed without mentioning them.\n"
        "5. Gather check-in and check-out dates from the user only after a hotel is picked.\n"
        "   - If a flight arrival date is known, use that as the check-in.\n"
        "   - If a flight staying until date is known, use that as the check-out.\n"
        "   - Ask for hotel preferences: rating, brand, amenities, etc.\n"
        "6. To suggest hotels, use `search_hotels()`:\n"
        "   - Only return hotels that match the user's filters (e.g., rating).\n"
        "   - Use this display format:\n"
        "     <ul>\n"
        "     <li><strong>{name}</strong> ({rating}★) - {brand}<br />{address_line}, {city}<br />"
        "Price per night: {average_price}</li>\n"
        "     </ul>\n"
        "   - Ask if the user wants to check availability or see full details for any.\n"
        "7. If the user requests more information about a hotel, call `display_full_hotel_details(property_id)` (use expedia_id as the property_id).\n"
        "   - DO not call display_full_hotel_details(property_id) unless asked explicitly for full details of only one property, otherwise use the search_hotels.\n"
        "   - When asked explicitly for hotel images, use 'display_hotel_images(property_id)'\n"
        "8. If the user selects a hotel and provides check-in/check-out dates, call `check_availability(check-in, check-out, property_id)`:\n"
        "   - NEVER call `check_availability(check-in, check-out, property_id)` with a check-in or check-out value that is before 2025.\n"
        "   - If the hotel is chosen after an upcoming flight or trip is selected, ask if the user wants to use the arrival date and staying until date as check-in check out date, presenting the values\n"
        "   - Summarize room types and rates clearly.\n"
        "   - Ask if the user wants to proceed with booking or see more options.\n"
        "9. If the user asks about specific amenities (e.g., pool, gym, parking):\n"
        "    - Search the `vector_text` for keywords in the hotel's data.\n"
        "    - Only say 'not available' if no match is found in the description blocks.\n\n"
        "10. If the user asks to book a hotel:\n"
        "    - If the user provided his name and email, only ask for travel agent email\n\n"
        "    - If the user has not provided his name and email, ask for their travel agent email in order to send a reservation request. Also ask for their name and email to include in the mail, but only if they ask to book\n"
        "    - Call send_reservation_request with reservation details\n\n"
        "11. If the user asks about a hotel's location or wants to see where a hotel is located:\n"
        "    - Use `get_location(location_input)` with the hotel's address or coordinates if available\n"
        "    - `get_location` should be called with coordinates when possible, when not, use the hotel name\n"
        "    - This will display an interactive map showing the hotel's exact location\n\n"
        "12. If the user asks for directions from a hotel to a point of interest (POI) or location:\n"
        "    - Use `get_directions(origin, destination, mode)` with both locations\n"
        "    - For the hotel origin: use hotel name and city, or coordinates if available from hotel data\n"
        "    - For the destination: use the user's specified POI/location name\n"
        "    - Default to walking mode unless user specifies driving or cycling\n"
        "    - Examples:\n"
        "      - `get_directions(\"Marriott London County Hall\", \"Big Ben\", \"walking\")`\n"
        "      - `get_directions({\"location\": \"Hotel Name\", \"country\": \"GB\"}, \"Tower Bridge\", \"cycling\")`\n"
        "      - `get_directions({\"lat\": 51.5078, \"lng\": -0.0877, \"name\": \"Hotel Name\"}, \"Westminster Abbey\")`\n"
        "    - This will display an interactive map with route, distance, and estimated travel time\n\n"
        "13. Location and directions are travel-related services, so provide them when requested for hotels and nearby attractions.\n\n"

        "Formatting Guidelines:\n"
        "- Format all your responses as HTML. When using picture URLs make sure HTML is correct <img src= {url}> to render not display URL.\n"
        "- Use `<strong>` tags for labels like hotel name, rating, flight number, etc.\n"
        "- Keep output clean and easy to scan.\n\n"

        "Other:\n"
        "- Assume check-in is the flight arrival date unless specified. Check out is staying_until. When year not specified, assume 2025.\n"
        "- Do not ask for last name or email, the user already know they'll receive better service if they provide them\n"
        "- Maintain a polite but friendly and informal, helpful tone without unnecessary delays\n"
        "- Always stay within the scope of business travel and hotel bookings.\n"
      )
    }]

  # Get current messages and add user message
  messages = session_store[conversation_id]
  initial_mock = False
  if "I would like to use mock travel history for demonstration purposes." in user_message:
    user_message = user_message.replace("I would like to use mock travel history for demonstration purposes.", "").strip()
    initial_mock = True
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

          try:
            # Safely handle the function call
            result = handle_function_call(tool_name, arguments, initial_mock)
          except Exception as e:
            # If an error occurs, set result to "error"
            result = "error"

          try:
            # Safely process short_circuit handling
            reply = short_circuit.handle(tool_name, result)
          except Exception as e:
            # If an error occurs during reply creation, set reply to None
            reply = None

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