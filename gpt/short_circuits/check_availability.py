import html


def handle_hotel_availability(availability_data):
  """
  Handle hotel availability check results - show 5 rates: lowest, highest, and 3 in middle
  """
  if not availability_data:
    return (
      '<div class="alert alert-warning">'
      '<span class="icon">📅</span>'
      "I couldn't check availability for those dates. Please try different dates or contact the hotel directly."
      '</div>'
    )

  # Extract availability data
  availability_list = availability_data.get('availability', [])

  if not availability_list:
    return '''
      <div class="alert alert-info">
          <span class="icon">😔</span>
          Unfortunately, this hotel doesn't have availability for your selected dates. 
          Would you like me to check other hotels or suggest alternative dates?
      </div>
      '''

  # Get rates and sort by total price
  rates = availability_list[0].get('rates', [])

  if not rates:
    return '''
      <div class="alert alert-info">
          <span class="icon">😔</span>
          No rooms are currently available for your selected dates. 
          Would you like me to check other hotels or suggest alternative dates?
      </div>
      '''

  # Sort rates by total price
  sorted_rates = sorted(rates, key=lambda x: x.get('total_price', 0))

  # Select 5 rates: lowest, highest, and 3 in middle
  selected_rates = []
  if len(sorted_rates) <= 5:
    selected_rates = sorted_rates
  else:
    # Lowest
    selected_rates.append(sorted_rates[0])

    # 3 from middle
    middle_start = len(sorted_rates) // 4
    middle_indices = [
      middle_start,
      len(sorted_rates) // 2,
      len(sorted_rates) - middle_start - 1
    ]
    for idx in middle_indices:
      if idx < len(sorted_rates) - 1:  # Don't duplicate the highest
        selected_rates.append(sorted_rates[idx])

    # Highest
    selected_rates.append(sorted_rates[-1])

  room_cards = ""
  for i, rate in enumerate(selected_rates):
    room_desc = rate.get('room_description', 'Standard Room')
    total_price = rate.get('total_price', 0)
    currency = rate.get('currency', 'GBP')
    refundable = rate.get('refundable', False)
    rate_id = rate.get('rate_id', '')

    currency_symbol = '£' if currency == 'GBP' else currency

    # Badge for lowest/highest
    badge = ""
    if i == 0:
      badge = '<span style="background: #22c55e; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; font-weight: 500;">Lowest Price</span>'
    elif i == len(selected_rates) - 1 and len(sorted_rates) > 1:
      badge = '<span style="background: #7c3aed; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; font-weight: 500;">Premium Option</span>'

    # Cancellation status
    cancellation_icon = "✅" if refundable else "❌"
    cancellation_text = "Refundable" if refundable else "Non-refundable"
    cancellation_color = "#22c55e" if refundable else "#dc2626"

    room_cards += f'''
      <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin: 12px 0; background: #fff;">
          <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
              <div style="flex: 1;">
                  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                      <h4 style="margin: 0; color: #374151; font-size: 1em;">{room_desc}</h4>
                      {badge}
                  </div>
                  <div style="color: {cancellation_color}; font-size: 0.85em;">
                      {cancellation_icon} {cancellation_text}
                  </div>
              </div>
              <div style="text-align: right;">
                  <div style="font-weight: 600; color: #4f46e5; font-size: 1.3em;">{currency_symbol}{total_price:.0f}</div>
                  <div style="font-size: 0.8em; color: #6b7280;">per night</div>
              </div>
          </div>
          <button onclick="selectRoom('{rate_id}', '{html.escape(room_desc)}', {total_price})" 
                  style="width: 100%; background: #4f46e5; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: 500; cursor: pointer;">
              Book This Room
          </button>
      </div>
      '''

  min_price = sorted_rates[0].get('total_price', 0)
  max_price = sorted_rates[-1].get('total_price', 0)
  currency_symbol = '£' if sorted_rates[0].get('currency') == 'GBP' else sorted_rates[0].get('currency', 'GBP')

  return f'''
  <div style="background: #f0fdf4; border: 1px solid #22c55e; border-radius: 8px; padding: 16px; margin: 12px 0;">
      <h3 style="color: #166534; margin: 0 0 8px 0;">✅ Available Rooms</h3>
      <p style="color: #166534; margin: 0;">
          {len(rates)} rooms available • {currency_symbol}{min_price:.0f} - {currency_symbol}{max_price:.0f} per night
      </p>
  </div>
  {room_cards}
  '''