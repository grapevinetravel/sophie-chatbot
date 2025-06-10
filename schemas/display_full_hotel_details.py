display_full_hotel_details_schema = {
    "name": "display_full_hotel_details",
    "description": "Reply with full details about a single hotel.",
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