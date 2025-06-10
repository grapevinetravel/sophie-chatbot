def handle_resolve_user_and_trips(result):
  """
  Handle user trips display with rich formatting - with inline styles for reliability
  """
  user_uuid = result.get("user_uuid")
  trips = result.get("upcoming_flights", [])

  if not user_uuid:
    return (
      '<div class="alert alert-warning">'
      '<span class="icon">⚠️</span>'
      "I couldn't find any company subscription linked to your details. "
      "Would you like to continue by manually providing your travel details?"
      '</div>'
    )

  if not trips:
    return (
      '<div class="alert alert-info">'
      '<span class="icon">ℹ️</span>'
      "I found your company profile but there are no upcoming trips. "
      "Please tell me your travel destination and dates so I can suggest hotels."
      '</div>'
    )

  # Generate trip cards with inline styles for reliability
  trip_cards = ""
  for i, trip in enumerate(trips, 1):
    # Parse the datetime for better formatting
    try:
      from datetime import datetime
      arrival_dt = datetime.fromisoformat(trip['arrival_time'].replace('Z', '+00:00'))
      formatted_date = arrival_dt.strftime('%B %d, %Y')
      formatted_time = arrival_dt.strftime('%I:%M %p')
    except:
      # Fallback if datetime parsing fails
      formatted_date = trip.get('arrival_time', '').split(' ')[0] if trip.get('arrival_time') else 'Date TBD'
      formatted_time = trip.get('arrival_time', '').split(' ')[1] if ' ' in trip.get('arrival_time', '') else ''

    # Extract airport codes and clean up destination names
    origin = trip.get('origin', '')
    destination = trip.get('destination', '')

    origin_parts = origin.split(' (')
    destination_parts = destination.split(' (')

    origin_city = origin_parts[0].strip().replace(' APT', '').replace(', GB', '')
    origin_code = origin_parts[1].replace(')', '') if len(origin_parts) > 1 else ''

    destination_city = destination_parts[0].strip().replace(' APT', '').replace(', GB', '')
    destination_code = destination_parts[1].replace(')', '') if len(destination_parts) > 1 else ''

    trip_cards += f'''
        <div onclick="selectTrip({i})" style="
            background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            color: white;
            box-shadow: 0 3px 10px rgba(79, 70, 229, 0.2);
            transition: all 0.2s ease;
            cursor: pointer;
            font-family: inherit;
        " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 15px rgba(79, 70, 229, 0.3)'" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 3px 10px rgba(79, 70, 229, 0.2)'">

            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-weight: 600; font-size: 1em;">Trip {i}</span>
                <span style="
                    background: rgba(255,255,255,0.2);
                    padding: 3px 10px;
                    border-radius: 15px;
                    font-size: 0.8em;
                    font-weight: 500;
                ">{origin_code} → {destination_code}</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                <div style="text-align: center; flex: 1;">
                    <span style="display: block; font-size: 1em; font-weight: 600; margin-bottom: 3px;">{origin_city}</span>
                    <span style="display: block; font-size: 0.8em; opacity: 0.8;">{origin_code}</span>
                </div>
                <div style="font-size: 1.1em; margin: 0 15px;">✈️</div>
                <div style="text-align: center; flex: 1;">
                    <span style="display: block; font-size: 1em; font-weight: 600; margin-bottom: 3px;">{destination_city}</span>
                    <span style="display: block; font-size: 0.8em; opacity: 0.8;">{destination_code}</span>
                </div>
            </div>

            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
                padding-top: 8px;
                border-top: 1px solid rgba(255,255,255,0.2);
            ">
                <span style="font-weight: 500; font-size: 0.9em;">{formatted_date}</span>
                <span style="font-size: 0.85em; opacity: 0.9;">{formatted_time}</span>
            </div>

            <button onclick="event.stopPropagation(); selectTrip({i})" style="
                width: 100%;
                background: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
                padding: 8px 14px;
                border-radius: 6px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 0.9em;
                font-family: inherit;
            " onmouseover="this.style.background='rgba(255,255,255,0.3)'; this.style.borderColor='rgba(255,255,255,0.5)'"
               onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.borderColor='rgba(255,255,255,0.3)'">
                Select for Hotel Search
            </button>
        </div>
        '''

  return f'''
    <div style="margin: 10px 0; font-family: inherit;">
        <div style="text-align: center; margin-bottom: 16px;">
            <h3 style="margin: 0 0 6px 0; color: #374151; font-size: 1.2em; font-weight: 600;">Your Upcoming Trips</h3>
            <p style="margin: 0; color: #6b7280; font-size: 0.85em;">Click on a trip to get hotel recommendations</p>
        </div>
        {trip_cards}
    </div>
    '''


# Alternative version with better mobile responsiveness
def handle_resolve_user_and_trips_mobile_optimized(self, result):
  """
  Mobile-optimized version with responsive inline styles
  """
  user_uuid = result.get("user_uuid")
  trips = result.get("upcoming_flights", [])

  if not user_uuid:
    return (
      '<div style="padding: 14px 16px; border-radius: 8px; display: flex; align-items: center; gap: 10px; margin: 12px 0; font-size: 0.9em; background: #fef3c7; color: #92400e; border: 1px solid #fde68a;">'
      '<span style="font-size: 1.1em;">⚠️</span>'
      "I couldn't find any company subscription linked to your details. "
      "Would you like to continue by manually providing your travel details?"
      '</div>'
    )

  if not trips:
    return (
      '<div style="padding: 14px 16px; border-radius: 8px; display: flex; align-items: center; gap: 10px; margin: 12px 0; font-size: 0.9em; background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe;">'
      '<span style="font-size: 1.1em;">ℹ️</span>'
      "I found your company profile but there are no upcoming trips. "
      "Please tell me your travel destination and dates so I can suggest hotels."
      '</div>'
    )

  # Generate trip cards with mobile-first responsive design
  trip_cards = ""
  for i, trip in enumerate(trips, 1):
    # Parse the datetime for better formatting
    try:
      from datetime import datetime
      arrival_dt = datetime.fromisoformat(trip['arrival_time'].replace('Z', '+00:00'))
      formatted_date = arrival_dt.strftime('%B %d, %Y')
      formatted_time = arrival_dt.strftime('%I:%M %p')
    except:
      formatted_date = trip.get('arrival_time', '').split(' ')[0] if trip.get('arrival_time') else 'Date TBD'
      formatted_time = trip.get('arrival_time', '').split(' ')[1] if ' ' in trip.get('arrival_time', '') else ''

    # Extract airport codes and clean up destination names
    origin = trip.get('origin', '')
    destination = trip.get('destination', '')

    origin_parts = origin.split(' (')
    destination_parts = destination.split(' (')

    origin_city = origin_parts[0].strip().replace(' APT', '').replace(', GB', '')
    origin_code = origin_parts[1].replace(')', '') if len(origin_parts) > 1 else ''

    destination_city = destination_parts[0].strip().replace(' APT', '').replace(', GB', '')
    destination_code = destination_parts[1].replace(')', '') if len(destination_parts) > 1 else ''

    trip_cards += f'''
        <div onclick="selectTrip({i})" style="
            background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            border-radius: 12px;
            padding: 16px;
            margin: 12px 0;
            color: white;
            box-shadow: 0 3px 10px rgba(79, 70, 229, 0.2);
            cursor: pointer;
            font-family: inherit;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(79, 70, 229, 0.3)'" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 3px 10px rgba(79, 70, 229, 0.2)'">

            <!-- Trip Header -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span style="font-weight: 600; font-size: 1.1em;">Trip {i}</span>
                <span style="
                    background: rgba(255,255,255,0.25);
                    padding: 4px 12px;
                    border-radius: 16px;
                    font-size: 0.85em;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                ">{origin_code} → {destination_code}</span>
            </div>

            <!-- Route Display -->
            <div style="margin-bottom: 14px;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 8px;">
                    <div style="text-align: center;">
                        <div style="font-size: 1.1em; font-weight: 700; margin-bottom: 2px;">{origin_city}</div>
                        <div style="font-size: 0.8em; opacity: 0.85; font-weight: 500;">{origin_code}</div>
                    </div>
                    <div style="font-size: 1.3em; opacity: 0.9;">✈️</div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.1em; font-weight: 700; margin-bottom: 2px;">{destination_city}</div>
                        <div style="font-size: 0.8em; opacity: 0.85; font-weight: 500;">{destination_code}</div>
                    </div>
                </div>
            </div>

            <!-- Date/Time Info -->
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
                padding: 10px 0;
                border-top: 1px solid rgba(255,255,255,0.25);
                border-bottom: 1px solid rgba(255,255,255,0.25);
            ">
                <span style="font-weight: 600; font-size: 0.95em;">📅 {formatted_date}</span>
                <span style="font-size: 0.9em; opacity: 0.9; font-weight: 500;">🕒 {formatted_time}</span>
            </div>

            <!-- Action Button -->
            <button onclick="event.stopPropagation(); selectTrip({i})" style="
                width: 100%;
                background: rgba(255,255,255,0.2);
                color: white;
                border: 2px solid rgba(255,255,255,0.3);
                padding: 12px 16px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                font-size: 0.95em;
                font-family: inherit;
                transition: all 0.2s ease;
            " onmouseover="this.style.background='rgba(255,255,255,0.35)'; this.style.borderColor='rgba(255,255,255,0.6)'; this.style.transform='translateY(-1px)'"
               onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.borderColor='rgba(255,255,255,0.3)'; this.style.transform='translateY(0)'">
                ✨ Select for Hotel Search
            </button>
        </div>
        '''

  return f'''
    <div style="margin: 15px 0; font-family: inherit; max-width: 100%;">
        <div style="text-align: center; margin-bottom: 20px; padding: 0 10px;">
            <h3 style="margin: 0 0 8px 0; color: #1f2937; font-size: 1.4em; font-weight: 700;">✈️ Your Upcoming Trips</h3>
            <p style="margin: 0; color: #6b7280; font-size: 0.9em; line-height: 1.4;">Click on any trip to get personalized hotel recommendations</p>
        </div>
        {trip_cards}
        <div style="text-align: center; margin-top: 16px; padding: 0 10px;">
            <p style="color: #9ca3af; font-size: 0.8em; margin: 0;">💡 Sophie will find hotels based on your company's booking history</p>
        </div>
    </div>
    '''