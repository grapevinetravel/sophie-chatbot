check_availability_schema = {
    "name": "check_availability",
    "description": "Get room rate and availability information for a hotel given its property ID and check-in/check-out dates.",
    "parameters": {
        "type": "object",
        "properties": {
            "in_date": {
                "type": "string",
                "description": "Check-in date in YYYY-MM-DD format"
            },
            "out_date": {
                "type": "string",
                "description": "Check-out date in YYYY-MM-DD format"
            },
            "property_id": {
                "type": "string",
                "description": "Hotel property ID as returned by hotel search"
            }
        },
        "required": ["in_date", "out_date", "property_id"]
    }
}