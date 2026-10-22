from typing import List, Dict, Optional
import weaviate
import os
from weaviate.auth import Auth
from weaviate.collections.classes.filters import Filter
from weaviate.collections.classes.grpc import MetadataQuery, GroupBy
from weaviate.collections.classes.types import GeoCoordinate

openai_key = os.getenv("OPENAI_APIKEY")

weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
# The Weaviate Cloud cluster that backs hotel vector search. Overridable so that moving or
# restoring the cluster is a configuration change rather than a code change.
WEAVIATE_CLUSTER_URL = os.getenv(
    "WEAVIATE_CLUSTER_URL",
    "gqubiqfprlyhx89xcwlma.c0.europe-west3.gcp.weaviate.cloud",
)


class HotelSearch:
  """Vector hotel search over Weaviate.

  The connection is opened on first search, not in __init__. It used to be opened here, and
  that made an unreachable cluster fatal to the entire service: router.py constructs this
  object at module level, so connect_to_weaviate_cloud() ran during import, and its exception
  stopped the container ever listening on PORT. The function then failed its startup health
  check and could not be deployed at all, on any runtime.

  Connecting lazily keeps that failure inside the one tool call that needs it. router.py
  catches it and returns an error result for that call, so the rest of the assistant works.
  """

  def __init__(self):
    self._headers = {
      "X-OpenAI-Api-Key": openai_key,
    }
    self.client = None
    self.hotel_collection = None

  def _ensure_connected(self):
    """Open the Weaviate connection if it is not already open.

    Leaves hotel_collection as None when it fails, so a later call retries rather than
    caching the failure for the life of the instance.
    """
    if self.hotel_collection is not None:
      return

    self.client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_CLUSTER_URL,
        auth_credentials=Auth.api_key(weaviate_api_key),
        headers=self._headers
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
    self._ensure_connected()

    filters = None
    if coords:
      if not isinstance(coords, dict) or "latitude" not in coords or "longitude" not in coords:
          raise TypeError(
              "`coords` must be a dict with keys 'latitude' and 'longitude' – "
              f"got {coords!r}"
          )

      lat = coords["latitude"]
      lon = coords["longitude"]

      geo_filter = (
          Filter
          .by_property("geol")
          .within_geo_range(
              coordinate=GeoCoordinate(latitude=lat, longitude=lon),
              distance=int(radius_km * 1000)          # Weaviate expects metres (int)
          )
      )
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