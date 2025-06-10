import requests


class HotelAvailabilityService:
  def __init__(self):
    self.url = "https://europe-west1-grapevine-v2-feb-2025.cloudfunctions.net/hotel-availability-service-dev/availability"
    self.headers = {"Content-Type": "application/json"}

  def check_availability(self, in_date: str, out_date: str, property_id: str):
    payload = {
      "currency": "GBP",
      "in_date": in_date,
      "out_date": out_date,
      "property_ids": [
        property_id
      ],
      "rate_limit": 10,
      "return_only_available_properties": True,
      "source": "expedia",
      "tax_included": True,
      "trace_id": "offers-backend"
    }

    try:
      response = requests.post(self.url, json=payload, headers=self.headers)
      response.raise_for_status()
      return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as error:
      print(f"An error occurred: {error}")
      return None  # Return None in case of error