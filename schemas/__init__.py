from schemas.check_availability import check_availability_schema
from schemas.display_hotel_images import display_hotel_images_schema
from schemas.get_full_hotel_details import get_full_hotel_details_schema
from schemas.get_hotels_by_corporate_geo import get_hotels_by_corporate_geo_schema
from schemas.get_upcoming_flights import resolve_user_and_trips_schema

from schemas.mapbox_search import mapbox_search_schema
from schemas.search_hotels import search_hotels_schema
from schemas.send_reservation_request import send_reservation_request_schema
from schemas.display_full_hotel_details import display_full_hotel_details_schema

all_schemas = [
  resolve_user_and_trips_schema,
  mapbox_search_schema,
  get_hotels_by_corporate_geo_schema,
  search_hotels_schema,
  check_availability_schema,
  get_full_hotel_details_schema,
  send_reservation_request_schema,
  display_full_hotel_details_schema,
  display_hotel_images_schema

  # Add the rest here
]
