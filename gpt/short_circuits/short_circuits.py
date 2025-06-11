import html
from datetime import datetime

from gpt.short_circuits.check_availability import handle_hotel_availability
from gpt.short_circuits.display_hotel_images import handle_display_hotel_images
from gpt.short_circuits.hotel_booking import handle_hotel_booking
from gpt.short_circuits.hotel_search import search_hotels_result
from gpt.short_circuits.display_directions import display_directions, display_location
from gpt.short_circuits.upcoming_trips import handle_resolve_user_and_trips
from gpt.short_circuits.past_trips import handle_hotel_recommendations
from gpt.short_circuits.display_full_hotel import handle_display_full_hotel_details


class ShortCircuit:
  def handle(self, func_name, result):
    """
    Main handler that routes to specific function handlers
    """
    if func_name == "resolve_user_and_trips":
      return handle_resolve_user_and_trips(result)
    elif func_name == "get_hotels_by_corporate_geo":
      return handle_hotel_recommendations(result)
    elif func_name == "search_hotels":
      return search_hotels_result(result)
    elif func_name == "check_availability":
      return handle_hotel_availability(result)
    elif func_name == "display_full_hotel_details":
      return handle_display_full_hotel_details(result)
    elif func_name == "display_hotel_images":
      return handle_display_hotel_images(result)
    elif func_name == "send_reservation_request":
      return handle_hotel_booking()
    elif func_name == "get_directions":
      return display_directions(result)
    elif func_name == "get_location":
      return display_location(result)
    # Add more handlers as needed
    return None