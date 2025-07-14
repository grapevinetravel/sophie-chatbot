import uuid
from datetime import datetime, timedelta
import random


class MockUserService:
  def __init__(self):
    # Mock user data - 4 users with US trips (including Denver)
    self.mock_users = {
      ("james.mitchell@salesforce-corp.com", "mitchell"): {
        "user_uuid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "corporation_id": 275071,
        "upcoming_flights": [
          {
            "arrival_time": "2025-08-04T14:30:00Z",
            "staying_until": "2025-08-07T10:00:00Z",
            "origin": "London, GB (LHR)",
            "destination": "Denver, US (DEN)",
            "destination_lat": 39.7392,
            "destination_lon": -104.9903
          },
          {
            "arrival_time": "2025-09-11T09:15:00Z",
            "staying_until": "2025-09-14T16:30:00Z",
            "origin": "London, GB (LGW)",
            "destination": "Austin, US (AUS)",
            "destination_lat": 30.2672,
            "destination_lon": -97.7431
          }
        ]
      },
      ("sarah.chen@nextstep-ventures.com", "chen"): {
        "user_uuid": "b2c3d4e5-f6g7-8901-2345-678901bcdef0",
        "corporation_id": 275071,
        "upcoming_flights": [
          {
            "arrival_time": "2025-07-18T16:45:00Z",
            "staying_until": "2025-07-20T12:00:00Z",
            "origin": "Birmingham, GB (BHX)",
            "destination": "New York, US (JFK)",
            "destination_lat": 40.7128,
            "destination_lon": -74.0060
          },
          {
            "arrival_time": "2025-09-30T11:20:00Z",
            "staying_until": "2025-10-05T14:45:00Z",
            "origin": "Manchester, GB (MAN)",
            "destination": "Seattle, US (SEA)",
            "destination_lat": 47.6062,
            "destination_lon": -122.3321
          }
        ]
      },
      ("david.rodriguez@mckinsey-consulting.com", "rodriguez"): {
        "user_uuid": "c3d4e5f6-g7h8-9012-3456-789012cdef01",
        "corporation_id": 275071,
        "upcoming_flights": [
          {
            "arrival_time": "2025-07-23T13:10:00Z",
            "staying_until": "2025-07-27T11:30:00Z",
            "origin": "London, GB (STN)",
            "destination": "San Francisco, US (SFO)",
            "destination_lat": 37.7749,
            "destination_lon": -122.4194
          },
          {
            "arrival_time": "2025-09-07T17:35:00Z",
            "staying_until": "2025-09-11T09:20:00Z",
            "origin": "London, GB (LTN)",
            "destination": "Chicago, US (ORD)",
            "destination_lat": 41.8781,
            "destination_lon": -87.6298
          }
        ]
      },
      ("emily.park@techcorp-innovations.com", "park"): {
        "user_uuid": "d4e5f6g7-h8i9-0123-4567-890123def012",
        "corporation_id": 275071,
        "upcoming_flights": [
          {
            "arrival_time": "2025-07-10T12:00:00Z",
            "staying_until": "2025-07-14T15:30:00Z",
            "origin": "Liverpool, GB (LPL)",
            "destination": "Boston, US (BOS)",
            "destination_lat": 42.3601,
            "destination_lon": -71.0589
          },
          {
            "arrival_time": "2025-08-14T15:25:00Z",
            "staying_until": "2025-08-17T13:15:00Z",
            "origin": "Aberdeen, GB (ABZ)",
            "destination": "Miami, US (MIA)",
            "destination_lat": 25.7617,
            "destination_lon": -80.1918
          }
        ]
      }
    }

    # Mock hotel data for different US locations
    self.mock_hotels = {
      # Denver area hotels
      "denver": [
        {
          "hotel_id": "8260654",
          "name": "The Crawford Hotel",
          "address": "1701 Wynkoop Street, Denver, CO 80202",
          "latitude": 39.7531,
          "longitude": -105.0017,
          "booking_count": 245,
          "rating": 4.8,
          "average_daily_rate": 285
        },
        {
          "hotel_id": "9726",
          "name": "Denver Marriott City Center",
          "address": "1701 California Street, Denver, CO 80202",
          "latitude": 39.7470,
          "longitude": -104.9913,
          "booking_count": 198,
          "rating": 4.3,
          "average_daily_rate": 165
        },
        {
          "hotel_id": "24031",
          "name": "Grand Hyatt Denver",
          "address": "1750 Welton Street, Denver, CO 80202",
          "latitude": 39.7449,
          "longitude": -104.9814,
          "booking_count": 167,
          "rating": 4.5,
          "average_daily_rate": 220
        }
      ],
      # New York area hotels
      "new_york": [
        {
          "hotel_id": "28044",
          "name": "The Plaza Hotel",
          "address": "768 5th Avenue, New York, NY 10019",
          "latitude": 40.7648,
          "longitude": -73.9754,
          "booking_count": 356,
          "rating": 4.6,
          "average_daily_rate": 495
        },
        {
          "hotel_id": "19681371",
          "name": "Pod Hotels Times Square",
          "address": "400 W 42nd Street, New York, NY 10036",
          "latitude": 40.7589,
          "longitude": -73.9928,
          "booking_count": 234,
          "rating": 4.1,
          "average_daily_rate": 185
        }
      ],
      # San Francisco area hotels
      "san_francisco": [
        {
          "hotel_id": "1321986",
          "name": "The St. Regis San Francisco",
          "address": "125 3rd Street, San Francisco, CA 94103",
          "latitude": 37.7854,
          "longitude": -122.4005,
          "booking_count": 142,
          "rating": 4.7,
          "average_daily_rate": 410
        },
        {
          "hotel_id": "9868852",
          "name": "Hotel Zephyr San Francisco",
          "address": "Pier 39, San Francisco, CA 94133",
          "latitude": 37.8098,
          "longitude": -122.4098,
          "booking_count": 118,
          "rating": 4.2,
          "average_daily_rate": 255
        }
      ],
      # Chicago area hotels
      "chicago": [
        {
          "hotel_id": "8079",
          "name": "The Palmer House Hilton",
          "address": "17 E Monroe Street, Chicago, IL 60603",
          "latitude": 41.8806,
          "longitude": -87.6267,
          "booking_count": 127,
          "rating": 4.3,
          "average_daily_rate": 195
        },
        {
          "hotel_id": "18035",
          "name": "Chicago Marriott Downtown",
          "address": "540 N Michigan Avenue, Chicago, IL 60611",
          "latitude": 41.8925,
          "longitude": -87.6244,
          "booking_count": 103,
          "rating": 4.1,
          "average_daily_rate": 165
        }
      ],
      # Boston area hotels
      "boston": [
        {
          "hotel_id": "2558",
          "name": "The Langham Boston",
          "address": "250 Franklin Street, Boston, MA 02110",
          "latitude": 42.3554,
          "longitude": -71.0640,
          "booking_count": 89,
          "rating": 4.4,
          "average_daily_rate": 335
        },
        {
          "hotel_id": "26146",
          "name": "Boston Harbor Hotel",
          "address": "70 Rowes Wharf, Boston, MA 02110",
          "latitude": 42.3570,
          "longitude": -71.0518,
          "booking_count": 76,
          "rating": 4.6,
          "average_daily_rate": 410
        }
      ],
      # Miami area hotels
      "miami": [
        {
          "hotel_id": "1126560",
          "name": "The Setai Miami Beach",
          "address": "2001 Collins Avenue, Miami Beach, FL 33139",
          "latitude": 25.7907,
          "longitude": -80.1300,
          "booking_count": 93,
          "rating": 4.7,
          "average_daily_rate": 480
        },
        {
          "hotel_id": "456566",
          "name": "JW Marriott Miami",
          "address": "1109 Brickell Avenue, Miami, FL 33131",
          "latitude": 25.7617,
          "longitude": -80.1918,
          "booking_count": 71,
          "rating": 4.2,
          "average_daily_rate": 295
        }
      ],
      # Seattle area hotels
      "seattle": [
        {
          "hotel_id": "20230",
          "name": "The Fairmont Olympic Hotel",
          "address": "411 University Street, Seattle, WA 98101",
          "latitude": 47.6089,
          "longitude": -122.3356,
          "booking_count": 86,
          "rating": 4.5,
          "average_daily_rate": 365
        },
        {
          "hotel_id": "16950",
          "name": "Hotel Andra Seattle",
          "address": "2000 4th Avenue, Seattle, WA 98121",
          "latitude": 47.6134,
          "longitude": -122.3414,
          "booking_count": 68,
          "rating": 4.3,
          "average_daily_rate": 225
        }
      ],
      # Austin area hotels
      "austin": [
        {
          "hotel_id": "10269315",
          "name": "Hotel Van Zandt",
          "address": "605 Davis Street, Austin, TX 78701",
          "latitude": 30.2638,
          "longitude": -97.7531,
          "booking_count": 95,
          "rating": 4.4,
          "average_daily_rate": 285
        },
        {
          "hotel_id": "8778760",
          "name": "JW Marriott Austin",
          "address": "110 E 2nd Street, Austin, TX 78701",
          "latitude": 30.2648,
          "longitude": -97.7404,
          "booking_count": 82,
          "rating": 4.2,
          "average_daily_rate": 350
        }
      ]
    }

  def resolve_user_and_trips(self, initial_mock: bool, email: str, last_name: str):
    """Mock version of resolve_user_and_trips"""
    user_key = (email.lower(), last_name.lower())

    # If initial_mock is True, return any of the entries in mock_users
    if initial_mock:
      return next(iter(self.mock_users.values()), {})  # Get any entry or return an empty dictionary if mock_users is empty

    # Otherwise, resolve user normally
    if user_key in self.mock_users:
      return self.mock_users[user_key]
    else:
      return {}

  def user_exists(self, email: str, last_name: str) -> str:
    """Mock version of user_exists - returns UUID if user exists"""
    user_key = (email.lower(), last_name.lower())
    if user_key in self.mock_users:
      return self.mock_users[user_key]["user_uuid"]
    else:
      return ""

  def get_upcoming_flights(self, user_uuid: str):
    """Mock version of get_upcoming_flights"""
    for user_data in self.mock_users.values():
      if user_data["user_uuid"] == user_uuid:
        return user_data["upcoming_flights"], user_data["corporation_id"]
    return None, None

  def get_hotels_by_corporate_geo(self, lat: float, long: float, corporate_id: int, radius_meters: int = 5000):
    """Mock version of get_hotels_by_corporate_geo"""
    # Determine location based on coordinates (US city mapping)
    if 39.6 <= lat <= 39.8 and -105.1 <= long <= -104.9:  # Denver area
      hotels = self.mock_hotels["denver"]
    elif 40.6 <= lat <= 40.8 and -74.1 <= long <= -73.9:  # New York area
      hotels = self.mock_hotels["new_york"]
    elif 37.7 <= lat <= 37.8 and -122.5 <= long <= -122.3:  # San Francisco area
      hotels = self.mock_hotels["san_francisco"]
    elif 41.8 <= lat <= 41.9 and -87.7 <= long <= -87.6:  # Chicago area
      hotels = self.mock_hotels["chicago"]
    elif 42.3 <= lat <= 42.4 and -71.1 <= long <= -71.0:  # Boston area
      hotels = self.mock_hotels["boston"]
    elif 25.7 <= lat <= 25.8 and -80.2 <= long <= -80.1:  # Miami area
      hotels = self.mock_hotels["miami"]
    elif 47.5 <= lat <= 47.7 and -122.4 <= long <= -122.3:  # Seattle area
      hotels = self.mock_hotels["seattle"]
    elif 30.2 <= lat <= 30.3 and -97.8 <= long <= -97.7:  # Austin area
      hotels = self.mock_hotels["austin"]
    else:
      # Default to empty list if coordinates don't match known areas
      hotels = []

    # Return top 5 hotels sorted by booking_count (already sorted in mock data)
    return hotels[:5]

  def get_all_mock_users(self):
    """Helper method to get all mock user emails and last names for testing"""
    return list(self.mock_users.keys())