def display_location(location_data):
  """
  Display location information with coordinates and map pin.

  Args:
      location_data (dict): Location data with {'lat': float, 'lng': float, 'name': str}

  Returns:
      str: HTML string displaying location information
  """
  import random

  # Generate unique map ID for location display
  map_id = f"location_{random.randint(1000, 9999)}"

  return f'''
  <div style="margin: 15px 0; font-family: inherit;">
      <div style="background: #f0fdf4; border: 1px solid #22c55e; border-radius: 12px; padding: 18px; margin: 16px 0;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
              <span style="font-size: 1.3em;">📍</span>
              <h3 style="color: #15803d; margin: 0; font-size: 1.3em;">Location Found</h3>
          </div>
          <div style="color: #166534; font-size: 0.9em;">
              {location_data['name']}
          </div>
      </div>

      <div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); margin-bottom: 16px;">
          <div id="{map_id}" style="height: 400px; width: 100%;"></div>
      </div>

      <div style="background: #f8fafc; border-radius: 8px; padding: 16px;">
          <div style="color: #6b7280; font-size: 0.9em; margin-bottom: 8px;">
              <strong style="color: #374151;">📍 Location Details:</strong>
          </div>
          <div style="color: #6b7280; font-size: 0.85em; line-height: 1.4;">
              <div style="margin-bottom: 4px;"><strong>Name:</strong> {location_data['name']}</div>
              <div style="margin-bottom: 4px;"><strong>Latitude:</strong> {location_data['lat']:.6f}</div>
              <div><strong>Longitude:</strong> {location_data['lng']:.6f}</div>
          </div>
      </div>
  </div>

  <script>
      // Store location data for this map instance
      window.locationData_{map_id} = {{
          "lat": {location_data['lat']},
          "lng": {location_data['lng']},
          "name": "{location_data['name']}"
      }};

      // Initialize location map when DOM is ready
      setTimeout(function() {{
          if (typeof initializeLocationMap === 'function') {{
              initializeLocationMap('{map_id}', window.locationData_{map_id});
          }}
      }}, 100);
  </script>
  '''

def display_directions(route_config):
  """
  Returns HTML for displaying directions between two points with interactive map

  Args:
      route_config (dict): Configuration dictionary containing:
          - origin (dict): {'lat': float, 'lng': float, 'name': str}
          - destination (dict): {'lat': float, 'lng': float, 'name': str}
          - mode (str, optional): Travel mode - 'walking', 'driving', or 'cycling' (default: 'walking')

  Returns:
      str: HTML string with interactive map and directions interface
  """
  import random
  import json
  import math

  # Extract data from config
  origin = route_config.get('origin', {})
  destination = route_config.get('destination', {})
  mode = route_config.get('mode', 'walking')

  # Validate required fields
  required_origin_fields = ['lat', 'lng', 'name']
  required_destination_fields = ['lat', 'lng', 'name']

  for field in required_origin_fields:
    if field not in origin:
      raise ValueError(f"Missing required field 'origin.{field}' in route_config")

  for field in required_destination_fields:
    if field not in destination:
      raise ValueError(f"Missing required field 'destination.{field}' in route_config")

  # Validate mode
  valid_modes = ['walking', 'driving', 'cycling']
  if mode not in valid_modes:
    mode = 'walking'

  # Calculate approximate distance using Haversine formula
  def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)

    a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lng / 2) * math.sin(delta_lng / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

  # Calculate distance and estimated time
  distance_km = calculate_distance(origin['lat'], origin['lng'], destination['lat'], destination['lng'])

  # Estimate time based on mode
  if mode == 'walking':
    # Average walking speed: 5 km/h
    time_hours = distance_km / 5
    mode_icon = "🚶"
    mode_color = "#059669"
  elif mode == 'driving':
    # Average city driving speed: 30 km/h
    time_hours = distance_km / 30
    mode_icon = "🚗"
    mode_color = "#4f46e5"
  else:  # cycling
    # Average cycling speed: 15 km/h
    time_hours = distance_km / 15
    mode_icon = "🚴"
    mode_color = "#ea580c"

  # Format time
  if time_hours < 1:
    time_str = f"{int(time_hours * 60)} minutes"
  else:
    hours = int(time_hours)
    minutes = int((time_hours - hours) * 60)
    if minutes > 0:
      time_str = f"{hours}h {minutes}m"
    else:
      time_str = f"{hours}h"

  # Generate unique map ID
  map_id = f"map_{random.randint(1000, 9999)}"

  # Create route data for JavaScript
  route_data = {
    "origin": origin,
    "destination": destination,
    "mode": mode
  }

  # Get active button style for current mode
  def get_button_style(button_mode, current_mode):
    if button_mode == current_mode:
      if button_mode == 'walking':
        return f"background: #059669; border: 2px solid #059669; color: white;"
      elif button_mode == 'driving':
        return f"background: #4f46e5; border: 2px solid #4f46e5; color: white;"
      else:  # cycling
        return f"background: #ea580c; border: 2px solid #ea580c; color: white;"
    else:
      if button_mode == 'walking':
        color = "#059669"
      elif button_mode == 'driving':
        color = "#4f46e5"
      else:  # cycling
        color = "#ea580c"
      return f"background: transparent; border: 2px solid {color}; color: {color};"

  return f'''
    <div style="margin: 15px 0; font-family: inherit;">
        <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 12px; padding: 18px; margin: 16px 0;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="font-size: 1.3em;">{mode_icon}</span>
                <h3 style="color: #0369a1; margin: 0; font-size: 1.3em;">{mode.title()} Directions</h3>
            </div>
            <div style="color: #0c4a6e; font-size: 0.9em;">
                From {origin['name']} to {destination['name']} • Approximately {time_str}
            </div>
        </div>

        <div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); margin-bottom: 16px;">
            <div id="{map_id}" style="height: 400px; width: 100%;"></div>
        </div>

        <div style="background: #f8fafc; border-radius: 8px; padding: 16px;">
            <div style="color: #6b7280; font-size: 0.9em; margin-bottom: 8px;">
                <strong style="color: #374151;">{mode_icon} {mode.title()} Route Details:</strong>
            </div>
            <div style="color: #6b7280; font-size: 0.85em; line-height: 1.4;">
                <div style="margin-bottom: 4px;"><strong>From:</strong> {origin['name']}</div>
                <div style="margin-bottom: 4px;"><strong>To:</strong> {destination['name']}</div>
                <div style="margin-bottom: 4px;"><strong>Distance:</strong> ~{distance_km:.1f} km</div>
                <div><strong>Estimated Time:</strong> ~{time_str}</div>
            </div>
        </div>
    </div>

    <script>
        // Store route data for this map instance
        window.routeData_{map_id} = {json.dumps(route_data)};

        // Initialize map when DOM is ready
        setTimeout(function() {{
            if (typeof initializeDirectionsMap === 'function') {{
                initializeDirectionsMap('{map_id}', window.routeData_{map_id});
            }}
        }}, 100);
    </script>
    '''