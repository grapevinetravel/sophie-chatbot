get_hotels_by_corporate_geo_schema = {
    "name": "get_hotels_by_corporate_geo",
    "description": "Find hotels frequently booked by a corporation near a geographic location.",
    "parameters": {
        "type": "object",
        "properties": {
            "corporate_id": {
                "type": "integer",
                "description": "The unique ID of the corporation."
            },
            "lat": {
                "type": "number",
                "description": "Latitude of the destination."
            },
            "long": {
                "type": "number",
                "description": "Longitude of the destination."
            },
            "radius_meters": {
                "type": "number",
                "description": "Search radius in meters.",
                "default": 7000
            }
        },
        "required": ["corporate_id", "lat", "long"]
    }
}