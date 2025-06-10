import hashlib
import datetime
import traceback
import requests
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
import os

# Configuration
DEFAULT_API_KEY = os.environ.get('EXPEDIA_API_KEY')
DEFAULT_SHARED_SECRET = os.environ.get('EXPEDIA_SHARED_SECRET')


# DTO (Data Transfer Objects)
@dataclass
class PropertyRequest:
  property_id: str

# Service layer classes
class AuthService:
  """Handles authentication and authorization for API requests"""

  def __init__(self, api_key: str, shared_secret: str):
    self.api_key = api_key
    self.shared_secret = shared_secret

  def get_authorization_header(self) -> str:
    """Generate the authorization header for the API request"""
    timestamp = str(int(datetime.datetime.now().timestamp()))
    return f"EAN apikey={self.api_key},signature={self._get_signature(timestamp)},timestamp={timestamp}"

  def _get_signature(self, timestamp: str) -> str:
    """Generate SHA512 signature for authentication"""
    sig = f"{self.api_key}{self.shared_secret}{timestamp}"
    return hashlib.sha512(sig.encode('utf-8')).hexdigest()


class StaticContentService:

  def __init__(self, auth_service: AuthService):
    self.auth_service = auth_service
    self.base_url = "https://test.ean.com/v3/properties/content"

  def query_content(
      self,
      property_id: str
  ):

    try:
      url = (
        f"{self.base_url}?property_id={property_id}&language=en-US&supply_source=expedia"
      )

      headers = {
        'Authorization': self.auth_service.get_authorization_header(),
        'Customer-Ip': '5.5.5.5',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
      }

      response = requests.get(url, headers=headers)

      if response.status_code == 200:
        data = response.json()

        return data
      else:
        return None

    except Exception as e:
      traceback.print_exc()
      return None


class ExpediaRapidClient:
  def __init__(self):
    """Client for querying Expedia Rapid API"""
    self.auth_service = AuthService("49qk7ovnoraob122ud1avng44e", "4l69b1ohn0j9n")
    self.content_service = StaticContentService(self.auth_service)

  def getStaticContent(self,  property_id: str):
    return self.content_service.query_content(property_id)

  def getStaticImages(self, property_id: str):
    return self._extract_hotel_image_data(self.getStaticContent(property_id))

  def _extract_hotel_image_data(self, json_data, max_images=50):
    """
    Extract hotel information and largest image URLs from JSON data

    Args:
        json_data: Dictionary containing hotel data
        max_images: Maximum number of images to extract (default: 50)

    Returns:
        List of dictionaries with extracted hotel and image information
    """

    def get_largest_image_url(links):
      """Get the largest image URL from links dictionary"""
      if not links or not isinstance(links, dict):
        return None

      # Define size priority (largest first)
      size_priority = ['1000px', '350px', '200px', '70px']

      for size in size_priority:
        if size in links and isinstance(links[size], dict) and 'href' in links[size]:
          return links[size]['href']

      # If none of the priority sizes found, get any available URL
      for qualifier, url_info in links.items():
        if isinstance(url_info, dict) and 'href' in url_info:
          return url_info['href']

      return None

    results = []

    # Iterate through each property in the JSON
    for property_id, property_data in json_data.items():
      hotel_info = {
        'property_id': property_data.get('property_id'),
        'hotel_name': property_data.get('name'),
        'images': []
      }

      all_images = []

      # Extract main property images
      if 'images' in property_data and isinstance(property_data['images'], list):
        for image in property_data['images']:
          largest_url = get_largest_image_url(image.get('links'))
          if largest_url:
            image_data = {
              'category': image.get('category'),
              'caption': image.get('caption'),
              'hero_image': image.get('hero_image', False),
              'url': largest_url,
              'source': 'property'
            }
            all_images.append(image_data)

      # Extract room images
      if 'rooms' in property_data:
        for room_id, room_data in property_data['rooms'].items():
          if 'images' in room_data and isinstance(room_data['images'], list):
            for image in room_data['images']:
              largest_url = get_largest_image_url(image.get('links'))
              if largest_url:
                image_data = {
                  'category': image.get('category'),
                  'caption': f"Room: {image.get('caption', '')}",
                  'hero_image': image.get('hero_image', False),
                  'room_id': room_id,
                  'room_name': room_data.get('name'),
                  'url': largest_url,
                  'source': 'room'
                }
                all_images.append(image_data)

      # Prioritize hero images and limit to max_images
      hero_images = [img for img in all_images if img['hero_image']]
      non_hero_images = [img for img in all_images if not img['hero_image']]

      # Take hero images first, then fill with non-hero images
      selected_images = hero_images[:max_images]
      remaining_slots = max_images - len(selected_images)
      if remaining_slots > 0:
        selected_images.extend(non_hero_images[:remaining_slots])

      hotel_info['images'] = selected_images
      results.append(hotel_info)

    return results


