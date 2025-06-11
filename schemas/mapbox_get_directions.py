get_location_schema = {
    "name": "get_location",
    "description": (
        "Resolve a single location input to coordinates. Accepts either coordinates directly or "
        "searches for a location by name. Returns standardized lat/lng coordinates with location name."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "location_input": {
                "oneOf": [
                    {
                        "type": "object",
                        "description": "Location specified by coordinates",
                        "properties": {
                            "lat": {
                                "type": "number",
                                "description": "Latitude coordinate",
                                "minimum": -90,
                                "maximum": 90
                            },
                            "lng": {
                                "type": "number",
                                "description": "Longitude coordinate",
                                "minimum": -180,
                                "maximum": 180
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name/description for the location"
                            }
                        },
                        "required": ["lat", "lng"],
                        "additionalProperties": False
                    },
                    {
                        "type": "object",
                        "description": "Location specified by name and optional country",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Place name, POI, or address to search for"
                            },
                            "country": {
                                "type": "string",
                                "description": "Optional 2-letter country code (e.g., 'FR', 'GB', 'US')",
                                "minLength": 2,
                                "maxLength": 2
                            }
                        },
                        "required": ["location"],
                        "additionalProperties": False
                    },
                    {
                        "type": "string",
                        "description": "Simple location name to search for (searches globally without country filter)"
                    }
                ]
            }
        },
        "required": ["location_input"]
    }
}

get_directions_schema = {
    "name": "get_directions",
    "description": (
        "Get directions between two locations with flexible input formats. "
        "Resolves both origin and destination to coordinates and returns route configuration."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "origin": {
                "oneOf": [
                    {
                        "type": "object",
                        "description": "Origin location specified by coordinates",
                        "properties": {
                            "lat": {
                                "type": "number",
                                "description": "Latitude coordinate",
                                "minimum": -90,
                                "maximum": 90
                            },
                            "lng": {
                                "type": "number",
                                "description": "Longitude coordinate",
                                "minimum": -180,
                                "maximum": 180
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name/description for the origin location"
                            }
                        },
                        "required": ["lat", "lng"],
                        "additionalProperties": False
                    },
                    {
                        "type": "object",
                        "description": "Origin location specified by name and optional country",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Place name, POI, or address to search for"
                            },
                            "country": {
                                "type": "string",
                                "description": "Optional 2-letter country code (e.g., 'FR', 'GB', 'US')",
                                "minLength": 2,
                                "maxLength": 2
                            }
                        },
                        "required": ["location"],
                        "additionalProperties": False
                    },
                    {
                        "type": "string",
                        "description": "Simple origin location name to search for"
                    }
                ]
            },
            "destination": {
                "oneOf": [
                    {
                        "type": "object",
                        "description": "Destination location specified by coordinates",
                        "properties": {
                            "lat": {
                                "type": "number",
                                "description": "Latitude coordinate",
                                "minimum": -90,
                                "maximum": 90
                            },
                            "lng": {
                                "type": "number",
                                "description": "Longitude coordinate",
                                "minimum": -180,
                                "maximum": 180
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name/description for the destination location"
                            }
                        },
                        "required": ["lat", "lng"],
                        "additionalProperties": False
                    },
                    {
                        "type": "object",
                        "description": "Destination location specified by name and optional country",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Place name, POI, or address to search for"
                            },
                            "country": {
                                "type": "string",
                                "description": "Optional 2-letter country code (e.g., 'FR', 'GB', 'US')",
                                "minLength": 2,
                                "maxLength": 2
                            }
                        },
                        "required": ["location"],
                        "additionalProperties": False
                    },
                    {
                        "type": "string",
                        "description": "Simple destination location name to search for"
                    }
                ]
            },
            "mode": {
                "type": "string",
                "description": "Travel mode for directions",
                "enum": ["walking", "driving", "cycling"],
                "default": "walking"
            }
        },
        "required": ["origin", "destination"]
    }
}