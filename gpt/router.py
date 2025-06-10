from service.email_service import send_reservation_request
from service.expedia_client import ExpediaRapidClient
from service.user_service import UserService
from service.mapbox_service import MapboxService
from service.rate_service import HotelAvailabilityService
from service.hotel_service import HotelSearch
import logging
import time

hotel_service = HotelSearch()
mapbox_service = MapboxService()
user_service = UserService()
hotel_avail_service = HotelAvailabilityService()
expedia_service = ExpediaRapidClient()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def handle_function_call(name, arguments):
  """
    Handles function calls by name and provides logging of start, end, and elapsed time.
    """
  start_time = time.time()
  logging.info(f"Function '{name}' started with arguments: {arguments}")

  result = None
  if name == "resolve_user_and_trips":
    result = user_service.resolve_user_and_trips(**arguments)
  elif name == "mapbox_search":
    result = mapbox_service.mapbox_search(**arguments)
  elif name == "get_hotels_by_corporate_geo":
    result = user_service.get_hotels_by_corporate_geo(**arguments)
  elif name == "search_hotels":
    result = hotel_service.search_hotels(**arguments)
  elif name == "check_availability":
    result = hotel_avail_service.check_availability(**arguments)
  elif name == "get_full_hotel_details":
    result = expedia_service.getStaticContent(**arguments)
  elif name == "display_full_hotel_details":
    result = expedia_service.getStaticContent(**arguments)
  elif name == "display_hotel_images":
    result = expedia_service.getStaticImages(**arguments)
  elif name == "send_reservation_request":
    result = send_reservation_request(**arguments)
  else:
    result = {"error": "Unknown function"}

  end_time = time.time()
  elapsed_time = end_time - start_time
  logging.info(f"Function '{name}' returned result: '{result}'")
  logging.info(f"Function '{name}' ended. Elapsed time: {elapsed_time:.2f} seconds.")

  return result
