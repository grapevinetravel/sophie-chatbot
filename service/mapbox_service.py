import os

import requests

ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

class MapboxService:
  def __init__(self):
    """
        Initializes the MapboxService with an access token and a session token.

        Args:
            access_token (str): The access token for accessing the Mapbox API.
            session_token (str): A unique token for the current session.
        """
    self.base_url = "https://api.mapbox.com/search/searchbox/v1/forward"
    self.access_token = ACCESS_TOKEN

  def mapbox_search(self, query: str, country: str = None) -> dict:
    """
        Makes a request to the Mapbox Search API to retrieve suggestions based on the query and optional country.

        Args:
            query (str): The search query.
            country (str, optional): The country filter (e.g., "GB"). Defaults to None.

        Returns:
            dict: The API response as a JSON dictionary.
        """
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
        return extract_coords_and_name(response.json())  # Return the response JSON as a dictionary
      else:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response: {response.text}")
        return {"error": "Failed request", "details": response.text}
    except requests.RequestException as e:
      # Handle exceptions gracefully
      print(f"An error occurred: {e}")
      return {"error": "Request exception", "details": str(e)}


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
