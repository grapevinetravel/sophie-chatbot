import html


def handle_hotel_availability(availability_data):
  """
  Handle hotel availability check results - show 5 rates: lowest, highest, and 3 in middle
  """
  if not availability_data:
    return (
      '<div style="background: #fef3cd; border: 1px solid #f59e0b; border-radius: 12px; padding: 20px; margin: 16px 0; display: flex; align-items: center; gap: 12px;">'
      '<span style="font-size: 1.5em;">📅</span>'
      '<div style="color: #92400e; font-weight: 500;">I couldn\'t check availability for those dates. Please try different dates or contact the hotel directly.</div>'
      '</div>'
    )

  # Extract availability data
  availability_list = availability_data.get('availability', [])

  if not availability_list:
    return '''
      <div style="background: #dbeafe; border: 1px solid #3b82f6; border-radius: 12px; padding: 20px; margin: 16px 0; display: flex; align-items: center; gap: 12px;">
          <span style="font-size: 1.5em;">😔</span>
          <div style="color: #1e40af; font-weight: 500;">
              Unfortunately, this hotel doesn't have availability for your selected dates. 
              Would you like me to check other hotels or suggest alternative dates?
          </div>
      </div>
      '''

  # Get rates and sort by total price
  rates = availability_list[0].get('rates', [])

  if not rates:
    return '''
      <div style="background: #dbeafe; border: 1px solid #3b82f6; border-radius: 12px; padding: 20px; margin: 16px 0; display: flex; align-items: center; gap: 12px;">
          <span style="font-size: 1.5em;">😔</span>
          <div style="color: #1e40af; font-weight: 500;">
              No rooms are currently available for your selected dates. 
              Would you like me to check other hotels or suggest alternative dates?
          </div>
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
    nightly_rate = rate.get('average_nightly_rate', 0)
    currency = rate.get('currency', 'GBP')
    refundable = rate.get('refundable', False)
    rate_id = rate.get('rate_id', '')

    currency_symbol = '£' if currency == 'GBP' else currency

    # Badge for lowest/highest
    badge = ""
    if i == 0:
      badge = '<span style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.75em; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);">Best Price</span>'
    elif i == len(selected_rates) - 1 and len(sorted_rates) > 1:
      badge = '<span style="background: linear-gradient(135deg, #8b5cf6, #7c3aed); color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.75em; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);">Premium</span>'

    # Cancellation status
    cancellation_icon = "✅" if refundable else "❌"
    cancellation_text = "Free cancellation" if refundable else "Non-refundable"
    cancellation_color = "#059669" if refundable else "#dc2626"
    cancellation_bg = "#ecfdf5" if refundable else "#fef2f2"

    # Card gradient border for best price
    border_style = "border: 2px solid transparent; background: linear-gradient(white, white) padding-box, linear-gradient(135deg, #10b981, #059669) border-box;" if i == 0 else "border: 1px solid #e5e7eb;"

    room_cards += f'''
      <div style="{border_style} border-radius: 16px; padding: 24px; margin: 16px 0; background: white; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); transition: all 0.2s ease;">
          <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
              <div style="flex: 1;">
                  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                      <h4 style="margin: 0; color: #111827; font-size: 1.1em; font-weight: 600;">{room_desc}</h4>
                      {badge}
                  </div>
                  <div style="background: {cancellation_bg}; color: {cancellation_color}; padding: 8px 12px; border-radius: 8px; font-size: 0.85em; font-weight: 500; display: inline-flex; align-items: center; gap: 6px;">
                      <span>{cancellation_icon}</span>
                      <span>{cancellation_text}</span>
                  </div>
              </div>
              <div style="text-align: right; margin-left: 20px;">
                  <div style="font-weight: 700; color: #1f2937; font-size: 1.8em; line-height: 1.2;">{currency_symbol}{nightly_rate:.0f}</div>
                  <div style="font-size: 0.9em; color: #6b7280; margin-bottom: 4px;">per night</div>
                  <div style="font-size: 0.8em; color: #9ca3af; padding: 4px 8px; background: #f9fafb; border-radius: 6px;">
                      {currency_symbol}{total_price:.0f} total stay
                  </div>
              </div>
          </div>
          <button onclick="selectRoom('{rate_id}', '{html.escape(room_desc)}', {total_price})" 
                  style="width: 100%; background: linear-gradient(135deg, #4f46e5, #4338ca); color: white; border: none; padding: 14px 20px; border-radius: 12px; font-weight: 600; font-size: 1em; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3);"
                  onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 6px 12px -2px rgba(79, 70, 229, 0.4)';"
                  onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px -1px rgba(79, 70, 229, 0.3)';">
              Book This Room
          </button>
      </div>
      '''

  min_price = sorted_rates[0].get('total_price', 0)
  max_price = sorted_rates[-1].get('total_price', 0)
  min_nightly = sorted_rates[0].get('average_nightly_rate', 0)
  max_nightly = sorted_rates[-1].get('average_nightly_rate', 0)
  currency_symbol = '£' if sorted_rates[0].get('currency') == 'GBP' else sorted_rates[0].get('currency', 'GBP')

  return f'''
  <div style="background: linear-gradient(135deg, #ecfdf5, #d1fae5); border: 2px solid #10b981; border-radius: 16px; padding: 20px; margin: 16px 0; box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1);">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
          <span style="font-size: 1.5em;">✅</span>
          <h3 style="color: #065f46; margin: 0; font-size: 1.3em; font-weight: 700;">Available Rooms</h3>
      </div>
      <p style="color: #047857; margin: 0; font-size: 1.05em; font-weight: 500;">
          {len(rates)} rooms available • {currency_symbol}{min_nightly:.0f} - {currency_symbol}{max_nightly:.0f} per night
      </p>
  </div>
  {room_cards}
  '''