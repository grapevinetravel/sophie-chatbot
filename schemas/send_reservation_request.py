send_reservation_request_schema = {
    "name": "send_reservation_request",
    "description": "Sends a reservation request for a hotel stay based on provided details.",
    "parameters": {
        "type": "object",
        "properties": {
            "hotel_name": {"type": "string"},
            "check_in": {"type": "string", "format": "date"},  # 'YYYY-MM-DD' format
            "check_out": {"type": "string", "format": "date"},  # 'YYYY-MM-DD' format
            "traveler_name": {"type": "string"},
            "traveler_email": {"type": "string", "format": "email"}
        },
        "required": ["hotel_name", "check_in", "check_out"]
    }
}