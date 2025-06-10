def handle_hotel_booking():
  """
  Return a static HTML confirmation message indicating booking is confirmed.
  """
  return '''
      <div style="background: #f0fdf4; border: 2px solid #22c55e; border-radius: 12px; padding: 20px; margin: 16px 0;">
          <div style="text-align: center; margin-bottom: 16px;">
              <span style="font-size: 2em;">✅</span>
              <h3 style="color: #166534; margin: 8px 0;">Booking Confirmed</h3>
          </div>

          <p style="color: #166534; font-size: 1em; text-align: center;">
              Your booking has been successfully confirmed. We look forward to welcoming you soon!
          </p>
      </div>
  '''