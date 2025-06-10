def send_reservation_request(hotel_name: str, check_in: str, check_out: str, traveler_name: str = None, traveler_email: str = None):
  """
    Sends a reservation request (currently just prints the input).

    :param hotel_name: The name of the hotel for the reservation.
    :param check_in: The check-in date in YYYY-MM-DD format.
    :param check_out: The check-out date in YYYY-MM-DD format.
    :param traveler_name: (Optional) The name of the traveler making the reservation.
    :param traveler_email: (Optional) The email of the traveler making the reservation.
    """
  print(f"Hotel Name: {hotel_name}")
  print(f"Check-In Date: {check_in}")
  print(f"Check-Out Date: {check_out}")

  if traveler_name:
    print(f"Traveler Name: {traveler_name}")
  else:
    print("Traveler Name: Not provided")

  if traveler_email:
    print(f"Traveler Email: {traveler_email}")
  else:
    print("Traveler Email: Not provided")

  return "Success"