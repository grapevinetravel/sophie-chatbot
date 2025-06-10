get_full_hotel_details_schema = {
    "name": "get_full_hotel_details",
    "description": "Get full details about a hotel.",
    "parameters": {
        "type": "object",
        "properties": {
            "property_id": {
                "type": "string",
                "description": "Hotel property ID as returned by hotel search"
            }
        },
        "required": ["property_id"]
    }
}