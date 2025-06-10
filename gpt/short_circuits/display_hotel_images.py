def handle_display_hotel_images(result):
  """
  Display hotel images with improved formatting and proper data handling
  """
  if not result:
    return (
      '<div style="padding: 14px 16px; border-radius: 8px; display: flex; align-items: center; gap: 10px; margin: 12px 0; font-size: 0.9em; background: #fef3c7; color: #92400e; border: 1px solid #fde68a;">'
      '<span style="font-size: 1.1em;">⚠️</span>'
      "Hotel images not available at the moment. Please try again later."
      '</div>'
    )

  # Handle different input formats
  if isinstance(result, list) and len(result) > 0:
    # Input is a list with hotel data
    hotel_data = result[0]
    hotel_name = hotel_data.get('hotel_name', 'Hotel Name Not Available')
    property_id = hotel_data.get('property_id', '')
    images = hotel_data.get('images', [])
  elif isinstance(result, dict):
    # Check if it's the old format with property_id as key
    property_id = list(result.keys())[0] if result else None
    if property_id and isinstance(result[property_id], dict):
      hotel_data = result[property_id]
      hotel_name = hotel_data.get('name', 'Hotel Name Not Available')
      images = hotel_data.get('images', [])
    else:
      # Direct format
      hotel_name = result.get('hotel_name', result.get('name', 'Hotel Name Not Available'))
      property_id = result.get('property_id', '')
      images = result.get('images', [])
  else:
    return "Invalid hotel data format."

  if not images:
    return f'''
        <div style="padding: 20px; text-align: center; border: 1px solid #e5e7eb; border-radius: 12px; background: #f9fafb;">
            <span style="font-size: 2em; display: block; margin-bottom: 10px;">📷</span>
            <p style="color: #6b7280; margin: 0;">No images available for {hotel_name}</p>
        </div>
        '''

  # Categorize images
  hero_images = []
  room_images = []
  lobby_images = []
  reception_images = []
  amenity_images = []
  other_images = []

  for img in images:
    category = img.get('category', 0)
    caption = img.get('caption', '').lower()

    if img.get('hero_image'):
      hero_images.append(img)
    elif category == 21001 or 'room' in caption:
      room_images.append(img)
    elif category == 10001 or 'lobby' in caption:
      lobby_images.append(img)
    elif category == 10002 or 'reception' in caption:
      reception_images.append(img)
    elif category == 22009 or 'amenity' in caption:
      amenity_images.append(img)
    else:
      other_images.append(img)

  def create_image_grid(image_list, title, icon, max_images=6):
    if not image_list:
      return ""

    grid_images = ""
    for i, img in enumerate(image_list[:max_images]):
      img_url = img.get('url', '')
      img_caption = img.get('caption', f'Image {i + 1}')
      room_name = img.get('room_name', '')

      # Create a descriptive title
      if room_name:
        img_title = room_name
      else:
        img_title = img_caption

      grid_images += f'''
                <div style="position: relative; border-radius: 8px; overflow: hidden; aspect-ratio: 4/3; background: #f3f4f6; cursor: pointer; transition: transform 0.2s ease;" 
                     onclick="openImageModal('{img_url}', '{img_title.replace("'", " ")}', '{hotel_name.replace("'", " ")}')">
                    <img src="{img_url}" 
                         alt="{img_title}" 
                         style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.2s ease;"
                         onmouseover="this.style.transform='scale(1.05)'"
                         onmouseout="this.style.transform='scale(1)'"
                         loading="lazy" />
                    <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.7)); color: white; padding: 8px; font-size: 0.8em;">
                        {img_title[:50]}{'...' if len(img_title) > 50 else ''}
                    </div>
                </div>
            '''

    more_count = len(image_list) - max_images
    if more_count > 0:
      grid_images += f'''
                <div style="position: relative; border-radius: 8px; overflow: hidden; aspect-ratio: 4/3; background: linear-gradient(135deg, #4f46e5, #3b82f6); cursor: pointer; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600;"
                     onclick="showMoreImages('{title.lower()}', '{property_id}')">
                    <div style="text-align: center;">
                        <div style="font-size: 1.5em; margin-bottom: 4px;">+{more_count}</div>
                        <div style="font-size: 0.9em;">More {title}</div>
                    </div>
                </div>
            '''

    return f'''
            <div style="margin-bottom: 24px;">
                <h3 style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; color: #374151; font-size: 1.1em;">
                    {icon} {title} ({len(image_list)})
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px;">
                    {grid_images}
                </div>
            </div>
        '''

  # Create the main hero section
  hero_section = ""
  if hero_images:
    main_hero = hero_images[0]
    hero_url = main_hero.get('url', '')
    hero_section = f'''
            <div style="position: relative; margin-bottom: 20px; border-radius: 12px; overflow: hidden; height: 300px; background: #f3f4f6; cursor: pointer;"
                 onclick="openImageModal('{hero_url}', 'Main Hotel Image', '{hotel_name.replace("'", " ")}')">
                <img src="{hero_url}" 
                     alt="Main hotel image" 
                     style="width: 100%; height: 100%; object-fit: cover;" />
                <div style="position: absolute; top: 16px; left: 16px; background: rgba(0,0,0,0.7); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600;">
                    📸 Main Hotel View
                </div>
            </div>
        '''

  # Build the complete gallery
  gallery_content = f'''
        <div style="margin: 15px 0; font-family: inherit; max-width: 100%;">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); color: white; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h2 style="margin: 0 0 8px 0; font-size: 1.5em; font-weight: 700;">📸 {hotel_name} - Photo Gallery</h2>
                <p style="margin: 0; opacity: 0.9; font-size: 0.9em;">Explore {len(images)} high-quality images of this property</p>
            </div>

            {hero_section}

            <!-- Image Categories -->
            {create_image_grid(room_images, "Room Images", "🛏️")}
            {create_image_grid(lobby_images, "Lobby & Common Areas", "🏨")}
            {create_image_grid(reception_images, "Reception Area", "🗝️")}
            {create_image_grid(amenity_images, "Amenities & Features", "✨")}
            {create_image_grid(other_images, "Additional Views", "📷")}

            <!-- Summary Stats -->
            <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-top: 20px; text-align: center;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 16px; font-size: 0.9em;">
                    <div><strong style="color: #4f46e5;">{len(room_images)}</strong><br><span style="color: #6b7280;">Room Photos</span></div>
                    <div><strong style="color: #4f46e5;">{len(lobby_images)}</strong><br><span style="color: #6b7280;">Lobby Views</span></div>
                    <div><strong style="color: #4f46e5;">{len(amenity_images)}</strong><br><span style="color: #6b7280;">Amenity Photos</span></div>
                    <div><strong style="color: #4f46e5;">{len(images)}</strong><br><span style="color: #6b7280;">Total Images</span></div>
                </div>
            </div>

            <!-- Back Button -->
            <div style="text-align: center; margin-top: 20px;">
                <button onclick="goBackToHotelDetails('{property_id}', '{hotel_name.replace("'", " ")}'); return false;" 
                        style="background: #6b7280; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; font-family: inherit;">
                    ← Back to Hotel Details
                </button>
            </div>
        </div>
    '''

  return gallery_content


# Additional JavaScript functions for image gallery
def get_image_gallery_javascript():
  """
  JavaScript functions for hotel image gallery interactions
  """
  return '''
        // Image modal functionality
        function openImageModal(imageUrl, title, hotelName) {
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                background: rgba(0,0,0,0.9); z-index: 10000; display: flex; 
                align-items: center; justify-content: center; cursor: pointer;
            `;

            modal.innerHTML = `
                <div style="max-width: 90%; max-height: 90%; position: relative;">
                    <img src="${imageUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain;" />
                    <div style="position: absolute; top: -40px; left: 0; color: white; font-size: 1.1em; font-weight: 600;">
                        ${title} - ${hotelName}
                    </div>
                    <div style="position: absolute; top: -40px; right: 0; color: white; font-size: 1.5em; cursor: pointer; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">
                        ✕
                    </div>
                </div>
            `;

            modal.onclick = () => modal.remove();
            document.body.appendChild(modal);
        }

        function showMoreImages(category, propertyId) {
            addMessage('user', `Show me more ${category} images`);
            sendToBackend({
                message: `Show more ${category} images`,
                view_more_images: {
                    property_id: propertyId,
                    category: category
                }
            });
        }

        function goBackToHotelDetails(propertyId, hotelName) {
            addMessage('user', `Show hotel details for ${hotelName}`);
            sendToBackend({
                message: `Show hotel details`,
                hotel_details: {
                    property_id: propertyId
                }
            });
        }
    '''
