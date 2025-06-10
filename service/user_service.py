import os

import requests

TINYBIRD_TOKEN = os.getenv('TINYBIRD_TOKEN')

class UserService:

  def resolve_user_and_trips(self, email: str, last_name: str):
    uuid = self.user_exists(email, last_name)
    upcoming_flights, corporation_id = self.get_upcoming_flights(uuid)
    if uuid:
      return {
        "user_uuid": uuid,
        # "corporation_id": corporation_id,
        "corporation_id": 275071,
        "upcoming_flights": upcoming_flights
      }
    else:
      return {}

  def user_exists(self, email: str, last_name: str) -> str:
    # URL for the API endpoint
    url = "https://europe-west1-grapevine-v2-feb-2025.cloudfunctions.net/suggestion-engine-production/getUserGUID"

    # Construct the JSON payload
    payload = {
      "email": email,
      "last_name": last_name
    }

    # HTTP headers
    headers = {
      "Content-Type": "application/json"
    }

    try:
      # Make the POST request
      response = requests.post(url, json=payload, headers=headers)

      # Check if the response status code is 200 (OK)
      if response.status_code == 200:
        # Return the raw text of the response (GUID or empty string)
        return response.text.strip()
      else:
        # Log the error and return an empty string
        print(f"Error: Received status code {response.status_code} with response: {response.text}")
        return ""
    except requests.RequestException as e:
      # Handle exceptions (e.g., network issues)
      print(f"An error occurred during the HTTP request: {e}")
      return ""

  def get_upcoming_flights(self, user_uuid):
    # URL for the API endpoint
    url = "https://api.tinybird.co/v0/pipes/get_upcoming_trips_with_flights_lightning.json"

    # HTTP Headers
    headers = {
      "Authorization": f"Bearer {TINYBIRD_TOKEN}"
    }

    # Parameters for the GET request
    params = {
      "user_guid": user_uuid
    }

    try:
      # Make the GET request
      response = requests.get(url, headers=headers, params=params)

      # Check if the response is successful
      if response.status_code == 200:
        # Parse JSON response
        json_response = response.json()

        # Extract the "data" field
        data = json_response.get("data", [])

        seen = set()
        filtered_trips = []
        corporation_id = None

        for trip in data:
          if corporation_id is None:
            corporation_id = trip['corporation_id']
          # Create a tuple of the fields to identify duplicates
          unique_key = (trip['origin'], trip['trip_id'], trip['destination'])

          if unique_key not in seen:
            # Add the unique key to the set and keep the trip in the result
            seen.add(unique_key)
            filtered_trips.append(trip)

        # Transform and filter the data
        formatted_data = [
          {
            "arrival_time": item["latest_travel_date"],
            "origin": item["origin"],
            "destination": item["destination"]
          }
          for item in filtered_trips
        ]



        # Return only the formatted data
        return formatted_data, corporation_id
      else:
        # Log error message and return None
        print(f"Error: Received status code {response.status_code} with response: {response.text}")
        return None
    except requests.RequestException as e:
      # Handle exceptions (e.g., network issues)
      print(f"An error occurred during the HTTP request: {e}")
      return None

  def get_hotels_by_corporate_geo(self, lat, long, corporate_id, radius_meters=5000):
    # API Endpoint and Authorization Header
    url = "https://api.tinybird.co/v0/pipes/get_hotels_by_corporate_geo.json"
    headers = {
      "Authorization": f"Bearer {TINYBIRD_TOKEN}"
    }

    # Parameters for the GET request
    params = {
      "in_lat": lat,
      "in_long": long,
      "in_comporate_id": corporate_id,
      "in_radius_meters": radius_meters
    }

    try:
      # Make the GET request
      response = requests.get(url, headers=headers, params=params)

      # Check if the response is successful
      if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract data field
        hotels = json_response.get("data", [])

        # Sort hotels by booking_count in descending order and take the first 5
        top_hotels = sorted(hotels, key=lambda x: x["booking_count"], reverse=True)[:5]

        # Return the top 5 hotels
        return top_hotels
      else:
        # Log error message and return None
        print(f"Error: Received status code {response.status_code} with response: {response.text}")
        return []
    except requests.RequestException as e:
      # Handle exceptions (e.g., network issues)
      print(f"An error occurred during the HTTP request: {e}")
      return []

