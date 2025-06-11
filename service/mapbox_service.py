import os
import requests

ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")


class MapboxService:
  def __init__(self):
    self.base_url = "https://api.mapbox.com/search/searchbox/v1/forward"
    self.access_token = ACCESS_TOKEN

  def mapbox_search(self, query: str, country: str = None) -> dict:
    # Construct query parameters
    params = {
      "q": query,
      "access_token": self.access_token,
    }
    if country:
      params["country"] = country

    try:
      # Make the GET request
      response = requests.get(self.base_url, params=params)

      # Check if the request was successful
      if response.status_code == 200:
        return extract_coords_and_name(response.json())
      else:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response: {response.text}")
        return {"error": "Failed request", "details": response.text}
    except requests.RequestException as e:
      # Handle exceptions gracefully
      print(f"An error occurred: {e}")
      return {"error": "Request exception", "details": str(e)}

  def get_location(self, location_input):
    # If already has coordinates, return as-is
    if isinstance(location_input, dict) and 'lat' in location_input and 'lng' in location_input:
      return {
        'lat': location_input['lat'],
        'lng': location_input['lng'],
        'name': location_input.get('name', 'Unknown Location')
      }

    # Extract search query and country
    if isinstance(location_input, dict):
      query = location_input.get('location', '')
      country = location_input.get('country', None)
    elif isinstance(location_input, str):
      query = location_input
      country = None
    else:
      raise ValueError("Invalid location input format")

    if not query:
      raise ValueError("Location query cannot be empty")

    # Search for location
    search_result = self.mapbox_search(query, country)

    if 'error' in search_result:
      raise ValueError(f"Could not find location '{query}': {search_result['error']}")

    # Convert to expected format
    return {
      'lat': search_result['coords']['latitude'],
      'lng': search_result['coords']['longitude'],
      'name': search_result['name']
    }

  def get_directions(self, origin, destination, mode="walking"):

    try:
      # Resolve both locations using get_location
      resolved_origin = self.get_location(origin)
      resolved_destination = self.get_location(destination)

      return {
        'origin': resolved_origin,
        'destination': resolved_destination,
        'mode': mode
      }
    except Exception as e:
      raise ValueError(f"Failed to get directions: {str(e)}")


def extract_coords_and_name(data):
  if data.get("features") and len(data["features"]) > 0:
    first_feature = data["features"][0]
    name = first_feature["properties"].get("name")
    coords = {
      "latitude": first_feature["geometry"]["coordinates"][1],
      "longitude": first_feature["geometry"]["coordinates"][0],
    }
    return {"name": name, "coords": coords}
  else:
    return {"error": "No features available"}