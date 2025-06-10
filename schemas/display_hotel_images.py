display_hotel_images_schema = {
    "name": "display_hotel_images",
    "description": "Reply with nicely structured hotel images.",
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