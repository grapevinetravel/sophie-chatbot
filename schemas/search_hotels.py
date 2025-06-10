search_hotels_schema = {
    "name": "search_hotels",
    "description": (
        "Search hotels near a location that match the user's preferences. "
        "You can filter by chain, star rating, and proximity. "
        "Preferences should be a free-text description of hotel features the user wants."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "preference_text": {
                "type": "string",
                "description": "Free-text description of hotel preferences, e.g. 'quiet modern hotel with a gym and breakfast'"
            },
            "coords": {
                "type": "object",
                "description": "Geographic coordinates of the search center",
                "properties": {
                    "latitude": { "type": "number" },
                    "longitude": { "type": "number" }
                },
                "required": ["latitude", "longitude"]
            },
            "radius_km": {
                "type": "number",
                "description": "Optional search radius in kilometers around the location",
                "default": 10
            },
            "chain": {
                "type": "string",
                "description": "Optional hotel chain filter (e.g., 'Hilton')"
            },
            "min_rating": {
                "type": "number",
                "description": "Minimum star rating (e.g., 4.0)"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of hotels to return",
                "default": 10
            }
        },
        "required": ["preference_text"]
    }
}