import uuid
from datetime import datetime, timedelta
import random


class MockUserService:
  def __init__(self):
    # Mock user data - 4 users with UK trips
    self.mock_users = {
      ("james.mitchell@salesforce-corp.com", "mitchell"): {
        "user_uuid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "corporation_id": 275071,
        "upcoming_flights": [
          {
            "arrival_time": "2025-07-15T14:30:00Z",
            "staying_until": "2025-07-18T10:00:00Z",
            "origin": "London, GB (LHR)",
            "destination": "Manchester, GB (MAN)",
            "destination_lat": 53.3537,
            "destination_lon": -2.2750
          },
          {
            "arrival_time": "2025-08-22T09:15:00Z",
            "staying_until": "2025-08-25T16:30:00Z",
            "origin": "London, GB (LGW)",
            "destination": "Edinburgh, GB (EDI)",
            "destination_lat": 55.9500,
            "destination_lon": -3.3725
          }
        ]
      },
      ("sarah.chen@nextstep-ventures.com", "chen"): {
        "user_uuid": "b2c3d4e5-f6g7-8901-2345-678901bcdef0",
        "corporation_id": 275071,
        "upcoming_flights": [
          {
            "arrival_time": "2025-06-28T16:45:00Z",
            "staying_until": "2025-06-30T12:00:00Z",
            "origin": "Birmingham, GB (BHX)",
            "destination": "London, GB (LHR)",
            "destination_lat": 51.4700,
            "destination_lon": -0.4543
          },
          {
            "arrival_time": "2025-09-10T11:20:00Z",
            "staying_until": "2025-09-15T14:45:00Z",
            "origin": "Manchester, GB (MAN)",
            "destination": "Glasgow, GB (GLA)",
            "destination_lat": 55.8719,
            "destination_lon": -4.4331
          }
        ]
      },
      ("david.rodriguez@mckinsey-consulting.com", "rodriguez"): {
        "user_uuid": "c3d4e5f6-g7h8-9012-3456-789012cdef01",
        "corporation_id": 275071,
        "upcoming_flights": [
          {
            "arrival_time": "2025-07-03T13:10:00Z",
            "staying_until": "2025-07-07T11:30:00Z",
            "origin": "London, GB (STN)",
            "destination": "Newcastle, GB (NCL)",
            "destination_lat": 55.0375,
            "destination_lon": -1.6917
          },
          {
            "arrival_time": "2025-08-18T17:35:00Z",
            "staying_until": "2025-08-22T09:20:00Z",
            "origin": "London, GB (LTN)",
            "destination": "Belfast, GB (BFS)",
            "destination_lat": 54.6575,
            "destination_lon": -6.2158
          }
        ]
      },
      ("emily.park@techcorp-innovations.com", "park"): {
        "user_uuid": "d4e5f6g7-h8i9-0123-4567-890123def012",
        "corporation_id": 275071,
        "upcoming_flights": [
          {
            "arrival_time": "2025-06-20T12:00:00Z",
            "staying_until": "2025-06-24T15:30:00Z",
            "origin": "Liverpool, GB (LPL)",
            "destination": "London, GB (LHR)",
            "destination_lat": 51.4700,
            "destination_lon": -0.4543
          },
          {
            "arrival_time": "2025-07-25T15:25:00Z",
            "staying_until": "2025-07-28T13:15:00Z",
            "origin": "Aberdeen, GB (ABZ)",
            "destination": "Birmingham, GB (BHX)",
            "destination_lat": 52.4539,
            "destination_lon": -1.7480
          }
        ]
      }
    }

    # Mock hotel data for different UK locations
    self.mock_hotels = {
      # London area hotels
      "london": [
        {
          "hotel_id": "8035714",
          "name": "The Shard Hotel",
          "address": "31 St Thomas Street, London SE1 9QU",
          "latitude": 51.5045,
          "longitude": -0.0865,
          "booking_count": 245,
          "rating": 4.8,
          "average_daily_rate": 320
        },
        {
          "hotel_id": "11785569",
          "name": "Premier Inn London County Hall",
          "address": "Belvedere Road, London SE1 7PB",
          "latitude": 51.5016,
          "longitude": -0.1134,
          "booking_count": 198,
          "rating": 4.3,
          "average_daily_rate": 125
        },
        {
          "hotel_id": "1532724",
          "name": "Hilton London Tower Bridge",
          "address": "5 More London Place, London SE1 2BY",
          "latitude": 51.5055,
          "longitude": -0.0834,
          "booking_count": 167,
          "rating": 4.5,
          "average_daily_rate": 280
        }
      ],
      # Manchester area hotels
      "manchester": [
        {
          "hotel_id": "691209",
          "name": "The Lowry Hotel",
          "address": "50 Dearmans Place, Manchester M3 5LH",
          "latitude": 53.4808,
          "longitude": -2.2426,
          "booking_count": 156,
          "rating": 4.6,
          "average_daily_rate": 195
        },
        {
          "hotel_id": "1044199",
          "name": "Radisson Blu Edwardian Manchester",
          "address": "Free Trade Hall, Peter Street, Manchester M2 5GP",
          "latitude": 53.4776,
          "longitude": -2.2463,
          "booking_count": 134,
          "rating": 4.4,
          "average_daily_rate": 165
        }
      ],
      # Edinburgh area hotels
      "edinburgh": [
        {
          "hotel_id": "570820",
          "name": "The Scotsman Hotel",
          "address": "20 North Bridge, Edinburgh EH1 1TR",
          "latitude": 55.9533,
          "longitude": -3.1883,
          "booking_count": 142,
          "rating": 4.7,
          "average_daily_rate": 210
        },
        {
          "hotel_id": "7728219",
          "name": "Hotel du Vin Edinburgh",
          "address": "11 Bristo Place, Edinburgh EH1 1EZ",
          "latitude": 55.9467,
          "longitude": -3.1925,
          "booking_count": 118,
          "rating": 4.2,
          "average_daily_rate": 155
        }
      ],
      # Birmingham area hotels
      "birmingham": [
        {
          "hotel_id": "7727274",
          "name": "Hotel du Vin Birmingham",
          "address": "25 Church Street, Birmingham B3 2NR",
          "latitude": 52.4862,
          "longitude": -1.8904,
          "booking_count": 127,
          "rating": 4.3,
          "average_daily_rate": 145
        },
        {
          "hotel_id": "787701",
          "name": "AC Hotel by Marriott Birmingham",
          "address": "81-87 Snow Hill, Birmingham B4 6HH",
          "latitude": 52.4834,
          "longitude": -1.8998,
          "booking_count": 103,
          "rating": 4.1,
          "average_daily_rate": 125
        }
      ],
      # Newcastle area hotels
      "newcastle": [
        {
          "hotel_id": "7728462",
          "name": "Hotel du Vin Newcastle",
          "address": "City Road, Newcastle upon Tyne NE1 2BE",
          "latitude": 54.9783,
          "longitude": -1.6178,
          "booking_count": 89,
          "rating": 4.4,
          "average_daily_rate": 135
        },
        {
          "hotel_id": "9610649",
          "name": "Crowne Plaza Newcastle",
          "address": "Stephenson Quarter, Newcastle upon Tyne NE1 3SA",
          "latitude": 54.9689,
          "longitude": -1.6062,
          "booking_count": 76,
          "rating": 4.1,
          "average_daily_rate": 110
        }
      ],
      # Belfast area hotels
      "belfast": [
        {
          "hotel_id": "1406421",
          "name": "The Merchant Hotel",
          "address": "16 Skipper Street, Belfast BT1 2DZ",
          "latitude": 54.6014,
          "longitude": -5.9302,
          "booking_count": 93,
          "rating": 4.7,
          "average_daily_rate": 180
        },
        {
          "hotel_id": "79018",
          "name": "Europa Hotel Belfast",
          "address": "Great Victoria Street, Belfast BT2 7AP",
          "latitude": 54.5947,
          "longitude": -5.9341,
          "booking_count": 71,
          "rating": 4.2,
          "average_daily_rate": 95
        }
      ],
      # Glasgow area hotels
      "glasgow": [
        {
          "hotel_id": "7728220",
          "name": "Hotel du Vin Glasgow",
          "address": "1 Devonshire Gardens, Glasgow G12 0UX",
          "latitude": 55.8750,
          "longitude": -4.2894,
          "booking_count": 86,
          "rating": 4.5,
          "average_daily_rate": 165
        },
        {
          "hotel_id": "894917",
          "name": "Radisson Blu Hotel Glasgow",
          "address": "301 Argyle Street, Glasgow G2 8DL",
          "latitude": 55.8578,
          "longitude": -4.2692,
          "booking_count": 68,
          "rating": 4.3,
          "average_daily_rate": 125
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
    # Determine location based on coordinates (rough UK city mapping)
    if 51.4 <= lat <= 51.6 and -0.5 <= long <= 0.1:  # London area
      hotels = self.mock_hotels["london"]
    elif 53.3 <= lat <= 53.4 and -2.3 <= long <= -2.2:  # Manchester area
      hotels = self.mock_hotels["manchester"]
    elif 55.9 <= lat <= 56.0 and -3.4 <= long <= -3.1:  # Edinburgh area
      hotels = self.mock_hotels["edinburgh"]
    elif 52.4 <= lat <= 52.5 and -1.95 <= long <= -1.7:  # Birmingham area
      hotels = self.mock_hotels["birmingham"]
    elif 54.9 <= lat <= 55.1 and -1.7 <= long <= -1.6:  # Newcastle area
      hotels = self.mock_hotels["newcastle"]
    elif 54.6 <= lat <= 54.7 and -6.3 <= long <= -5.9:  # Belfast area
      hotels = self.mock_hotels["belfast"]
    elif 55.8 <= lat <= 55.9 and -4.5 <= long <= -4.2:  # Glasgow area
      hotels = self.mock_hotels["glasgow"]
    else:
      # Default to London hotels if coordinates don't match known areas
      hotels = self.mock_hotels["london"]

    # Return top 5 hotels sorted by booking_count (already sorted in mock data)
    return hotels[:5]

  def get_all_mock_users(self):
    """Helper method to get all mock user emails and last names for testing"""
    return list(self.mock_users.keys())
