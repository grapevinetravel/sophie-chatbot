def handle_display_full_hotel_details(result):
  """
  Display comprehensive hotel details with rich formatting
  """
  if not result:
    return (
      '<div style="padding: 14px 16px; border-radius: 8px; display: flex; align-items: center; gap: 10px; margin: 12px 0; font-size: 0.9em; background: #fef3c7; color: #92400e; border: 1px solid #fde68a;">'
      '<span style="font-size: 1.1em;">⚠️</span>'
      "Hotel details not available at the moment. Please try again later."
      '</div>'
    )

  # Extract main hotel data (assuming single property)
  property_id = list(result.keys())[0] if result else None
  if not property_id:
    return "No hotel details found."

  hotel = result[property_id]

  # Extract basic information
  name = hotel.get('name', 'Hotel Name Not Available')
  address = hotel.get('address', {})
  location = hotel.get('location', {})
  ratings = hotel.get('ratings', {}).get('property', {})
  amenities = hotel.get('amenities', {})
  images = hotel.get('images', [])
  rooms = hotel.get('rooms', {})
  descriptions = hotel.get('descriptions', {})
  statistics = hotel.get('statistics', {})
  brand = hotel.get('brand', {})
  chain = hotel.get('chain', {})

  # Format address
  address_parts = []
  if address.get('line_1'):
    address_parts.append(address['line_1'])
  if address.get('city'):
    address_parts.append(address['city'])
  if address.get('postal_code'):
    address_parts.append(address['postal_code'])
  full_address = ', '.join(address_parts)

  # Format rating
  rating = float(ratings.get('rating', 0)) if ratings.get('rating') else 0
  rating_stars = "⭐" * int(rating) if rating > 0 else "Not rated"
  rating_type = ratings.get('type', 'Star')

  # Get hero image
  hero_image = None
  for img in images:
    if img.get('hero_image'):
      hero_image = img.get('links', {}).get('350px', {}).get('href')
      break

  # Format amenities (top 10 most relevant)
  key_amenities = []
  amenity_icons = {
    'Free WiFi': '📶',
    'Parking': '🚗',
    'Breakfast': '🍳',
    'Fitness': '💪',
    'Pool': '🏊',
    'Air conditioning': '❄️',
    'Pet': '🐕',
    'Bar': '🍸',
    'Restaurant': '🍽️',
    'Room service': '🛎️',
    'Elevator': '🛗',
    'Wheelchair': '♿',
    'WiFi': '📶',
    'Smoke-free': '🚭',
    'Front desk': '🏨'
  }

  for amenity_id, amenity_data in list(amenities.items())[:10]:
    amenity_name = amenity_data.get('name', '')
    icon = '✨'
    for key, emoji in amenity_icons.items():
      if key.lower() in amenity_name.lower():
        icon = emoji
        break
    key_amenities.append(f"{icon} {amenity_name}")

  # Room types summary
  room_summary = []
  for room_id, room_data in list(rooms.items())[:3]:  # Show top 3 room types
    room_name = room_data.get('name', 'Room')
    area = room_data.get('area', {})
    sq_feet = area.get('square_feet', 0)
    bed_groups = room_data.get('bed_groups', {})

    bed_info = ""
    for bed_group in bed_groups.values():
      bed_info = bed_group.get('description', '')
      break

    room_info = f"🛏️ {room_name}"
    if bed_info:
      room_info += f" ({bed_info})"
    if sq_feet:
      room_info += f" - {int(sq_feet)} sq ft"
    room_summary.append(room_info)

  # Hotel statistics
  year_built = ""
  total_rooms = ""
  floors = ""

  for stat in statistics.values():
    stat_name = stat.get('name', '')
    if 'Year Built' in stat_name:
      year_built = stat.get('value', '')
    elif 'Total number of rooms' in stat_name:
      total_rooms = stat.get('value', '')
    elif 'Number of floors' in stat_name:
      floors = stat.get('value', '')

  return f'''
    <div style="margin: 15px 0; font-family: inherit; max-width: 100%;">
        <!-- Hotel Header -->
        <div style="
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            position: relative;
            overflow: hidden;
        ">
            <div style="position: relative; z-index: 2;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <h2 style="margin: 0; font-size: 1.5em; font-weight: 700;">{name}</h2>
                    {f'<span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 16px; font-size: 0.8em; font-weight: 500;">{brand.get("name", "")}</span>' if brand.get("name") else ''}
                </div>

                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px; flex-wrap: wrap;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="font-size: 1em;">{rating_stars}</span>
                        {f'<span style="font-size: 0.9em; opacity: 0.9;">({rating}/5 {rating_type})</span>' if rating > 0 else ''}
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="font-size: 1em;">📍</span>
                        <span style="font-size: 0.9em; opacity: 0.9;">{full_address}</span>
                    </div>
                </div>

                {f'<div style="display: flex; gap: 16px; font-size: 0.85em; opacity: 0.9; flex-wrap: wrap;">' +
                 (f'<span>🏢 {total_rooms} rooms</span>' if total_rooms else '') +
                 (f'<span>📅 Built {year_built}</span>' if year_built else '') +
                 (f'<span>🏗️ {floors} floors</span>' if floors else '') +
                 '</div>' if any([total_rooms, year_built, floors]) else ''}
            </div>

            {f'<img src="{hero_image}" style="position: absolute; top: 0; right: 0; width: 120px; height: 80px; object-fit: cover; border-radius: 8px; opacity: 0.3;" />' if hero_image else ''}
        </div>

        <!-- Quick Info Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-bottom: 16px;">

            <!-- Amenities Card -->
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px;">
                <h3 style="margin: 0 0 12px 0; color: #374151; font-size: 1.1em; display: flex; align-items: center; gap: 8px;">
                    ✨ Key Amenities
                </h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.85em;">
                    {chr(10).join(f'<div style="color: #6b7280;">{amenity}</div>' for amenity in key_amenities[:8])}
                </div>
                {f'<div style="margin-top: 8px; font-size: 0.8em; color: #9ca3af;">+{len(key_amenities) - 8} more amenities</div>' if len(key_amenities) > 8 else ''}
            </div>

            <!-- Room Types Card -->
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px;">
                <h3 style="margin: 0 0 12px 0; color: #374151; font-size: 1.1em; display: flex; align-items: center; gap: 8px;">
                    🏨 Available Rooms
                </h3>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.85em;">
                    {chr(10).join(f'<div style="color: #6b7280; padding: 4px 0; border-bottom: 1px solid #f3f4f6;">{room}</div>' for room in room_summary[:4])}
                </div>
                {f'<div style="margin-top: 8px; font-size: 0.8em; color: #9ca3af;">+{len(rooms) - 4} more room types</div>' if len(rooms) > 4 else ''}
            </div>
        </div>

        <!-- Description Section -->
        {f"""
        <div style="background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 18px; margin-bottom: 16px;">
            <h3 style="margin: 0 0 12px 0; color: #374151; font-size: 1.1em; display: flex; align-items: center; gap: 8px;">
                📋 About This Hotel
            </h3>
            {f'<div style="margin-bottom: 12px;"><strong style="color: #4f46e5;">Location:</strong> <span style="color: #6b7280; font-size: 0.9em; line-height: 1.4;">{descriptions.get("location", "")}</span></div>' if descriptions.get("location") else ''}
            {f'<div style="margin-bottom: 12px;"><strong style="color: #4f46e5;">Overview:</strong> <span style="color: #6b7280; font-size: 0.9em; line-height: 1.4;">{descriptions.get("amenities", "")}</span></div>' if descriptions.get("amenities") else ''}
            {f'<div style="margin-bottom: 12px;"><strong style="color: #4f46e5;">Dining:</strong> <span style="color: #6b7280; font-size: 0.9em; line-height: 1.4;">{descriptions.get("dining", "")}</span></div>' if descriptions.get("dining") else ''}
        </div>
        """ if any(descriptions.get(key) for key in ["location", "amenities", "dining"]) else ''}

        <!-- Action Buttons -->
        <div style="display: flex; gap: 12px; margin-top: 20px; flex-wrap: wrap;">
            <button onclick="checkAvailability('{property_id}', '{name.replace("'", " ")}'); return false;" style="
                flex: 1;
                min-width: 200px;
                background: linear-gradient(135deg, #22c55e, #16a34a);
                color: white;
                border: none;
                padding: 14px 20px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 1em;
                font-family: inherit;
            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(34, 197, 94, 0.3)'"
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                🎯 Check Availability & Rates
            </button>

            <button onclick="viewHotelImages('{property_id}', '{name.replace("'", " ")}'); return false;" style="
                background: transparent;
                color: #059669;
                border: 2px solid #059669;
                padding: 14px 20px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 1em;
                font-family: inherit;
            " onmouseover="this.style.background='#059669'; this.style.color='white'"
               onmouseout="this.style.background='transparent'; this.style.color='#059669'">
                📸 Photos ({len(images)})
            </button>
        </div>

        <!-- Footer Info -->
        <div style="background: #f8fafc; border-radius: 8px; padding: 16px; margin-top: 16px; text-align: center;">
            <p style="color: #6b7280; font-size: 0.85em; margin: 0;">
                💡 This information is updated regularly. Click "Check Availability" for real-time pricing and booking.
            </p>
        </div>
    </div>
    '''


# Additional JavaScript functions to add to your main HTML
def get_additional_javascript_functions():
  """
  Additional JavaScript functions for hotel details interactions
  """
  return '''
    // Additional functions for hotel details
    function checkAvailability(propertyId, hotelName) {
        addMessage('user', `Check availability for ${hotelName}`);
        sendToBackend({
            message: `Check availability for ${hotelName}`,
            check_availability: {
                property_id: propertyId,
                hotel_name: hotelName
            }
        });
    }

    function viewAllRooms(propertyId) {
        addMessage('user', 'Show me all available room types');
        sendToBackend({
            message: 'Show all room types',
            view_rooms: {
                property_id: propertyId
            }
        });
    }

    function viewHotelImages(propertyId) {
        addMessage('user', 'Show me hotel photos');
        sendToBackend({
            message: 'Show hotel photos',
            view_images: {
                property_id: propertyId
            }
        });
    }
    '''


# Room details handler (if you want to show individual room details)
def handle_display_room_details(rooms_data, property_id):
  """
  Display detailed room information
  """
  if not rooms_data:
    return "No room details available."

  room_cards = ""
  for room_id, room in rooms_data.items():
    name = room.get('name', 'Room')
    area = room.get('area', {})
    sq_feet = area.get('square_feet', 0)
    sq_meters = area.get('square_meters', 0)

    # Bed configuration
    bed_groups = room.get('bed_groups', {})
    bed_info = ""
    for bed_group in bed_groups.values():
      bed_info = bed_group.get('description', '')
      break

    # Amenities
    amenities = room.get('amenities', {})
    room_amenities = [amenity.get('name', '') for amenity in amenities.values()]

    # Occupancy
    occupancy = room.get('occupancy', {}).get('max_allowed', {})
    max_adults = occupancy.get('adults', 0)
    max_children = occupancy.get('children', 0)

    # Room image
    images = room.get('images', [])
    room_image = None
    if images:
      room_image = images[0].get('links', {}).get('350px', {}).get('href')

    room_cards += f'''
        <div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 18px; margin: 14px 0; background: #fff;">
            <div style="display: flex; gap: 16px;">
                {f'<img src="{room_image}" style="width: 120px; height: 80px; object-fit: cover; border-radius: 8px; flex-shrink: 0;" />' if room_image else ''}

                <div style="flex: 1;">
                    <h4 style="margin: 0 0 8px 0; color: #374151; font-size: 1.2em; font-weight: 600;">{name}</h4>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 12px; font-size: 0.9em;">
                        {f'<div><strong>🛏️ Beds:</strong> {bed_info}</div>' if bed_info else ''}
                        {f'<div><strong>📏 Size:</strong> {int(sq_feet)} sq ft ({sq_meters:.0f} m²)</div>' if sq_feet else ''}
                        <div><strong>👥 Occupancy:</strong> {max_adults + max_children} guests</div>
                    </div>

                    {(''.join([
                        '<div style="margin-bottom: 12px;">',
                        '<strong style="color: #4f46e5; font-size: 0.9em;">Room Features:</strong>',
                        '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 4px; margin-top: 4px; font-size: 0.8em; color: #6b7280;">',
                        chr(10).join([f'<div>• {amenity}</div>' for amenity in room_amenities[:6]]),
                        '</div>',
                        (f"<div style='font-size: 0.75em; color: #9ca3af; margin-top: 4px;'>+{len(room_amenities) - 6} more features</div>" if len(room_amenities) > 6 else ''),
                        '</div>',
                    ]) if room_amenities else '')}

                    <button onclick="selectRoomType('{room_id}', '{name.replace("'", " '")}', '{property_id}')" style="
                        background: linear-gradient(135deg, #4f46e5, #3b82f6);
                        color: white;
                        border: none;
                        padding: 10px 16px;
                        border-radius: 6px;
                        font-weight: 500;
                        cursor: pointer;
                        font-family: inherit;
                    ">
                        Check This Room Type
                    </button>
                </div>
            </div>
        </div>
        '''

  return f'''
    <div style="margin: 10px 0;">
        <h3 style="color: #374151; margin-bottom: 16px; font-size: 1.3em;">🏨 Available Room Types</h3>
        {room_cards}
    </div>
    '''