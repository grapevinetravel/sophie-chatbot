mapbox_search_schema = {
    "name": "mapbox_search",
    "description": (
        "Look up a geographic location or POI using a clear place name (not full sentence). "
        "Returns an array of suggestions with coordinates and context. "
        "Include a country code (ISO 3166-1 alpha-2) if known to improve accuracy."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "A clear place name, POI, or address — e.g., 'Marriott Berlin' or 'Gare du Nord'"
            },
            "country": {
                "type": "string",
                "description": "Optional 2-letter country code (e.g., 'FR', 'GB', 'US')",
                "minLength": 2,
                "maxLength": 2
            }
        },
        "required": ["query"]
    }
}