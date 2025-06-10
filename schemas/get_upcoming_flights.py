resolve_user_and_trips_schema = {
    "name": "resolve_user_and_trips",
    "description": "Checks if the user exists and retrieves any upcoming flights/train rides",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string"},
            "last_name": {"type": "string"}
        },
        "required": ["email", "last_name"]
    }
}