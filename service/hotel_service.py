from typing import List, Dict, Optional
import weaviate
import os
from weaviate.auth import Auth
from weaviate.collections.classes.filters import Filter
from weaviate.collections.classes.grpc import MetadataQuery, GroupBy
from weaviate.collections.classes.types import GeoCoordinate

openai_key = os.getenv("OPENAI_APIKEY")
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
class HotelSearch:
  def __init__(self):
    headers = {
      "X-OpenAI-Api-Key": openai_key,
    }

    # Connect to the Weaviate cluster
    self.client = weaviate.connect_to_weaviate_cloud(
        cluster_url="gqubiqfprlyhx89xcwlma.c0.europe-west3.gcp.weaviate.cloud",
        auth_credentials=Auth.api_key(weaviate_api_key),
        headers=headers
    )
    self.hotel_collection = self.client.collections.get("HotelCollectionFull")

  def search_hotels(
      self,
      preference_text: str,
      coords: Optional[Dict[str, float]] = None,
      radius_km: Optional[float] = 10,
      brand: Optional[str] = None,
      chain: Optional[str] = None,
      min_rating: Optional[float] = None,
      limit: int = 10
  ) -> List[Dict]:
    filters = None
    if coords:
      # Geo filter (e.g., within a certain radius of a location)
      geo_filter = Filter.by_property("geol").within_geo_range(
          coordinate=GeoCoordinate(latitude=coords.get('latitude'), longitude=coords.get('longitude')),
          distance=radius_km * 1000)
      filters = geo_filter

    if brand:
      brand_filter = Filter.by_property("brand_name").like(brand)
      filters = brand_filter if filters is None else filters & brand_filter

    if chain:
      chain_filter = Filter.by_property("chain_name").like(chain)
      filters = chain_filter if filters is None else filters & chain_filter

    if min_rating:
      property_filter = Filter.by_property("rating").greater_than(min_rating)
      filters = property_filter if filters is None else filters & property_filter

    # Query the collection
    response = self.hotel_collection.query.near_text(
        query=preference_text,
        filters=filters,
        limit=limit,
        return_metadata=MetadataQuery(distance=True)
    )

    result = []
    if response:
      for match in response.objects:
        item = match.properties
        item["geol"] = None
        item["vector_text"] = None
        result.append(match.properties)

    return result