from datetime import datetime


class HotelAvailabilityService:
  def __init__(self):
    self.url = "https://europe-west1-grapevine-v2-feb-2025.cloudfunctions.net/hotel-availability-service-dev/availability"
    self.headers = {"Content-Type": "application/json"}

  def adjust_dates_if_in_past(self, in_date: str, out_date: str) -> tuple:
    # Parse the input dates
    in_date_obj = datetime.strptime(in_date, "%d-%m-%Y")
    out_date_obj = datetime.strptime(out_date, "%d-%m-%Y")

    # Get current date
    now = datetime.now()

    # Adjust dates if they are in the past
    if in_date_obj < now:
      in_date_obj = in_date_obj.replace(year=2025)
    if out_date_obj < now:
      out_date_obj = out_date_obj.replace(year=2025)

    # Convert back to string in the required format
    return in_date_obj.strftime("%d-%m-%Y"), out_date_obj.strftime("%d-%m-%Y")

  def check_availability(self, in_date: str, out_date: str, property_id: str):
    # Adjust the dates if necessary
    in_date, out_date = self.adjust_dates_if_in_past(in_date, out_date)

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