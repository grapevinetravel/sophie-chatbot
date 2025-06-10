def handle_hotel_recommendations(hotels_data):
  """
  Handle hotel recommendations display with rich formatting - inline styles
  """
  if not hotels_data or len(hotels_data) == 0:
    return (
      '<div style="padding: 14px 16px; border-radius: 8px; display: flex; align-items: center; gap: 10px; margin: 12px 0; font-size: 0.9em; background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe;">'
      '<span style="font-size: 1.1em;">🏨</span>'
      "I couldn't find any hotels based on your company's past bookings for this destination. "
      "Would you like me to search for other available hotels in the area?"
      '</div>'
    )

  # Sort hotels by distance (closest first)
  sorted_hotels = sorted(hotels_data, key=lambda x: x.get('distance_meters', float('inf')))

  hotel_cards = ""
  for i, hotel in enumerate(sorted_hotels, 1):
    # Format distance
    distance_m = hotel.get('distance_meters', 0)
    if distance_m < 1000:
      distance_str = f"{distance_m}m"
    else:
      distance_km = distance_m / 1000
      distance_str = f"{distance_km:.1f}km"

    # Format price
    avg_rate = hotel.get('average_daily_rate', 0)
    price_str = f"£{avg_rate:.0f}" if avg_rate else "Price TBD"

    # Format last booking date
    latest_booking = hotel.get('latest_booking', '')
    try:
      from datetime import datetime
      booking_dt = datetime.fromisoformat(latest_booking.replace('Z', '+00:00'))
      formatted_date = booking_dt.strftime('%b %d, %Y')
    except:
      formatted_date = latest_booking.split(' ')[0] if latest_booking else 'Recently'

    # Booking popularity indicator
    booking_count = hotel.get('booking_count', 0)
    if booking_count >= 10:
      popularity = "🔥 Popular Choice"
      popularity_color = "#dc2626"
    elif booking_count >= 5:
      popularity = "⭐ Frequently Booked"
      popularity_color = "#ea580c"
    else:
      popularity = "✨ Available Option"
      popularity_color = "#059669"

    # Distance badge color
    if distance_m <= 500:
      distance_color = "#059669"  # Green for very close
      distance_icon = "📍"
    elif distance_m <= 2000:
      distance_color = "#ea580c"  # Orange for moderate distance
      distance_icon = "🚶"
    else:
      distance_color = "#6b7280"  # Gray for farther
      distance_icon = "🚗"

    # Escape single quotes in hotel name for JavaScript
    hotel_name_escaped = hotel.get('name', '').replace("'", "\\'")

    # Get hotel IDs for the buttons
    property_id = hotel.get('property_id', i)
    expedia_id = hotel.get('expedia_id', '')
    hotel_id = hotel.get('hotel_id', '')

    hotel_cards += f'''
      <div onclick="selectHotel({property_id}, '{hotel_name_escaped}')" style="
          background: white;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          padding: 16px;
          margin-bottom: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
          transition: all 0.2s ease;
          cursor: pointer;
          font-family: inherit;
      " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 15px rgba(79, 70, 229, 0.1)'; this.style.borderColor='#4f46e5'"
         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0, 0, 0, 0.04)'; this.style.borderColor='#e5e7eb'">

          <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
              <div style="flex: 1;">
                  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                      <h4 style="margin: 0; color: #374151; font-size: 1.1em; font-weight: 600; line-height: 1.2;">{hotel.get('name', 'Hotel Name')}</h4>
                  </div>
                  <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                      <span style="font-size: 0.8em; font-weight: 500; color: {popularity_color};">{popularity}</span>
                  </div>
              </div>

              <div style="text-align: right; margin-left: 16px;">
                  <span style="display: block; font-size: 0.75em; color: #6b7280; margin-bottom: 2px;">Avg Rate</span>
                  <span style="display: block; font-size: 1.3em; font-weight: 700; color: #4f46e5; line-height: 1;">{price_str}</span>
                  <span style="display: block; font-size: 0.75em; color: #6b7280; margin-top: 2px;">per night</span>
              </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px;">
              <div style="display: flex; align-items: center; gap: 8px; font-size: 0.9em; color: #6b7280;">
                  <span style="font-size: 1em; color: {distance_color};">{distance_icon}</span>
                  <span style="color: #6b7280;">Distance: <strong style="color: #374151;">{distance_str}</strong></span>
              </div>
              <div style="display: flex; align-items: center; gap: 8px; font-size: 0.9em; color: #6b7280;">
                  <span style="font-size: 1em;">📅</span>
                  <span style="color: #6b7280;">Last booked: <strong style="color: #374151;">{formatted_date}</strong></span>
              </div>
              <div style="display: flex; align-items: center; gap: 8px; font-size: 0.9em; color: #6b7280;">
                  <span style="font-size: 1em;">👥</span>
                  <span style="color: #6b7280;">Company bookings: <strong style="color: #374151;">{booking_count}</strong></span>
              </div>
          </div>

          <div style="display: flex; gap: 8px;">
              <button onclick="event.stopPropagation(); selectHotel({property_id}, '{hotel_name_escaped}')" style="
                  flex: 1;
                  background: linear-gradient(135deg, #4f46e5, #3b82f6);
                  color: white;
                  border: none;
                  padding: 12px 16px;
                  border-radius: 8px;
                  font-weight: 600;
                  cursor: pointer;
                  transition: all 0.2s ease;
                  font-size: 0.95em;
                  font-family: inherit;
              " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 12px rgba(79, 70, 229, 0.3)'"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                  Check Availability & Book
              </button>

              <button onclick="event.stopPropagation(); showHotelFullInfo('{expedia_id or property_id}', '{hotel_name_escaped}', '{hotel_id or property_id}')" style="
                  background: transparent; 
                  border: 2px solid #6b7280; 
                  color: #6b7280; 
                  padding: 12px 16px; 
                  border-radius: 8px; 
                  font-weight: 600; 
                  cursor: pointer; 
                  transition: all 0.2s ease; 
                  font-size: 0.95em;
                  font-family: inherit;
                  white-space: nowrap;
              " onmouseover="this.style.background='#6b7280'; this.style.color='white'"
                 onmouseout="this.style.background='transparent'; this.style.color='#6b7280'">
                  Full Info
              </button>
          </div>
      </div>
      '''

  return f'''
  <div style="margin: 10px 0; font-family: inherit;">
      <div style="background: #f0fdf4; border: 1px solid #22c55e; border-radius: 12px; padding: 18px; margin: 16px 0;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
              <span style="font-size: 1.3em;">🏨</span>
              <h3 style="color: #166534; margin: 0; font-size: 1.3em;">Recommended Hotels</h3>
          </div>
          <p style="color: #166534; margin: 0; font-size: 1em;">Based on your company's booking history</p>
      </div>

      <div>
          {hotel_cards}
      </div>

      <div style="margin-top: 16px;">
          <p style="color: #6b7280; font-size: 0.85em; text-align: center; margin-top: 16px;">
              💡 These hotels are popular with your colleagues. Want to see more options?
          </p>
          <div style="text-align: center; margin-top: 12px;">
              <button onclick="requestMoreHotels()" style="
                  background: transparent; 
                  border: 2px solid #4f46e5; 
                  color: #4f46e5; 
                  padding: 8px 16px; 
                  border-radius: 6px; 
                  cursor: pointer; 
                  font-weight: 500;
                  font-family: inherit;
              " onmouseover="this.style.background='#4f46e5'; this.style.color='white'"
                 onmouseout="this.style.background='transparent'; this.style.color='#4f46e5'">
                  Show More Hotels
              </button>
          </div>
      </div>
  </div>
  '''