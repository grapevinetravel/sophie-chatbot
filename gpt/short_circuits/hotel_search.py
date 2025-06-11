def search_hotels_result(hotels_data):
  """
  Handle general hotel search results display - with inline styles
  """
  if not hotels_data or len(hotels_data) == 0:
    return (
      '<div style="padding: 14px 16px; border-radius: 8px; display: flex; align-items: center; gap: 10px; margin: 12px 0; font-size: 0.9em; background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe;">'
      '<span style="font-size: 1.1em;">🔍</span>'
      "I couldn't find any hotels for your search criteria. Try adjusting your location or dates."
      '</div>'
    )

  # Sort hotels by rank (lower rank = better)
  sorted_hotels = sorted(hotels_data, key=lambda x: x.get('rank', float('inf')))

  # Get search statistics
  total_hotels = len(sorted_hotels)

  # Get location from first hotel
  location = sorted_hotels[0].get('location', {}) if sorted_hotels else {}
  city = location.get('city', 'your destination')

  hotel_cards = ""
  for i, hotel in enumerate(sorted_hotels, 1):
    # Extract hotel details
    name = hotel.get('name', 'Hotel Name')
    brand_name = hotel.get('brand_name', '')
    chain_name = hotel.get('chain_name', '')
    rating = hotel.get('rating', 0)
    expedia_id = hotel.get('expedia_id', '')
    hotel_id = hotel.get('hotel_id', '')

    # Price formatting
    price_str = hotel.get('average_price', 'Unknown')
    if price_str == 'Unknown':
      price_amount = 0
    else:
      price_amount = float(price_str.replace(' GBP', ''))

    # Location details
    hotel_location = hotel.get('location', {})
    address_line1 = hotel_location.get('line_1', '')
    address_line2 = hotel_location.get('line_2', '')
    postal_code = hotel_location.get('postal_code', '')

    # Build address string
    address_parts = [address_line1]
    if address_line2:
      address_parts.append(address_line2)
    if postal_code:
      address_parts.append(postal_code)
    address = ', '.join(filter(None, address_parts))

    # Rating stars
    rating_stars = "⭐" * int(rating) if rating else "Not rated"

    # Brand/Chain display
    brand_info = ""
    if brand_name and chain_name and brand_name != chain_name:
      brand_info = f"{brand_name} ({chain_name})"
    elif brand_name:
      brand_info = brand_name
    elif chain_name:
      brand_info = chain_name

    # Price category badge
    price_category = ""
    price_color = "#6b7280"
    if price_amount == 0:
      price_category = "💰 Price available on booking"
      price_color = "#6b7280"
    elif price_amount <= 100:
      price_category = "💰 Budget Friendly"
      price_color = "#059669"
    elif price_amount <= 150:
      price_category = "💼 Mid-Range"
      price_color = "#ea580c"
    elif price_amount <= 200:
      price_category = "✨ Premium"
      price_color = "#7c3aed"
    else:
      price_category = "👑 Luxury"
      price_color = "#dc2626"

    # Rank badge
    rank_badge = ""
    if i <= 3:
      rank_badge = f'<span style="background: #22c55e; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; font-weight: 500; margin-left: 8px;">#{i} Top Choice</span>'
    elif hotel.get('rank', float('inf')) < 5000:
      rank_badge = f'<span style="background: #3b82f6; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; font-weight: 500; margin-left: 8px;">Highly Rated</span>'

    # Escape quotes for JavaScript
    name_escaped = name.replace("'", "\\'")
    address_escaped = address.replace("'", "\\'") if address else name_escaped

    hotel_cards += f'''
        <div onclick="selectSearchHotel('{expedia_id}', '{name_escaped}', '{hotel_id}')" style="
            border: 1px solid #e5e7eb; 
            border-radius: 12px; 
            padding: 18px; 
            margin: 14px 0; 
            background: #fff; 
            transition: all 0.2s ease; 
            cursor: pointer;
            font-family: inherit;
        " onmouseover="this.style.boxShadow='0 4px 12px rgba(79, 70, 229, 0.1)'; this.style.borderColor='#4f46e5'"
           onmouseout="this.style.boxShadow='none'; this.style.borderColor='#e5e7eb'">

            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap;">
                        <h4 style="margin: 0; color: #374151; font-size: 1.15em; font-weight: 600;">{name}</h4>
                        {rank_badge}
                    </div>

                    <div style="margin-bottom: 8px;">
                        <div style="color: #6b7280; font-size: 0.9em; margin-bottom: 2px;">{brand_info}</div>
                        <div style="color: {price_color}; font-size: 0.85em; font-weight: 500;">{price_category}</div>
                    </div>

                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        <span style="color: #f59e0b; font-size: 0.9em;">{rating_stars}</span>
                        {f'<span style="color: #6b7280; font-size: 0.85em;">({rating}/5)</span>' if rating else ''}
                    </div>
                </div>

                <div style="text-align: right; margin-left: 16px;">
                    <div style="font-weight: 700; color: #4f46e5; font-size: 1.4em;">{'£' + str(int(price_amount)) if price_amount > 0 else 'TBD'}</div>
                    <div style="font-size: 0.8em; color: #6b7280;">avg per night</div>
                </div>
            </div>

            <div style="border-top: 1px solid #f3f4f6; padding-top: 12px; margin-bottom: 14px;">
                <div style="color: #6b7280; font-size: 0.85em; line-height: 1.4;">
                    📍 {address or city}
                </div>
            </div>

            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <button onclick="event.stopPropagation(); selectSearchHotel('{expedia_id}', '{name_escaped}', '{hotel_id}')" style="
                    flex: 1;
                    min-width: 140px;
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
                    Check Availability & Rates
                </button>

                <button onclick="event.stopPropagation(); showHotelFullInfo('{expedia_id}', '{name_escaped}', '{hotel_id}')" style="
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

                <button onclick="event.stopPropagation(); showHotelLocation('{name_escaped}', '{address_escaped}')" style="
                    background: transparent; 
                    border: 2px solid #3b82f6; 
                    color: #3b82f6; 
                    padding: 12px 16px; 
                    border-radius: 8px; 
                    font-weight: 600; 
                    cursor: pointer; 
                    transition: all 0.2s ease; 
                    font-size: 0.95em;
                    font-family: inherit;
                    white-space: nowrap;
                " onmouseover="this.style.background='#3b82f6'; this.style.color='white'"
                   onmouseout="this.style.background='transparent'; this.style.color='#3b82f6'">
                    📍 Location
                </button>
            </div>
        </div>
        '''

  return f'''
    <div style="margin: 10px 0; font-family: inherit;">
        <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 12px; padding: 18px; margin: 16px 0;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="font-size: 1.3em;">🏨</span>
                <h3 style="color: #0369a1; margin: 0; font-size: 1.3em;">Hotels in {city}</h3>
            </div>
            <div style="color: #0c4a6e; font-size: 0.9em; margin-top: 8px;">
                <strong>{total_hotels}</strong> hotels found
            </div>
        </div>

        <div>
            {hotel_cards}
        </div>

        <div style="background: #f8fafc; border-radius: 8px; padding: 16px; margin-top: 16px; text-align: center;">
            <p style="color: #6b7280; font-size: 0.9em; margin: 0 0 12px 0;">
                💡 Prices are estimated averages. Click any hotel to check real-time availability and current rates.
            </p>
            <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
                <button onclick="refineCentralitySearch()" style="
                    background: transparent; 
                    border: 2px solid #4f46e5; 
                    color: #4f46e5; 
                    padding: 8px 16px; 
                    border-radius: 6px; 
                    cursor: pointer; 
                    font-weight: 500; 
                    font-size: 0.9em;
                    font-family: inherit;
                " onmouseover="this.style.background='#4f46e5'; this.style.color='white'"
                   onmouseout="this.style.background='transparent'; this.style.color='#4f46e5'">
                    Show City Center Only
                </button>
                <button onclick="refineSearchByPrice()" style="
                    background: transparent; 
                    border: 2px solid #059669; 
                    color: #059669; 
                    padding: 8px 16px; 
                    border-radius: 6px; 
                    cursor: pointer; 
                    font-weight: 500; 
                    font-size: 0.9em;
                    font-family: inherit;
                " onmouseover="this.style.background='#059669'; this.style.color='white'"
                   onmouseout="this.style.background='transparent'; this.style.color='#059669'">
                    Budget Friendly Hotels
                </button>
            </div>
        </div>
    </div>
    '''