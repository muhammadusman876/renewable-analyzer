from geopy.geocoders import Nominatim
from typing import Optional, Tuple

def geocode_location(location: str) -> Optional[Tuple[float, float]]:
        """
        Geocode a city or postal code in Germany to (lat, lon).
        Returns None if not found.
        """
        try:
            geolocator = Nominatim(user_agent="renewable-analyzer")
            loc = geolocator.geocode(f"{location}, Germany")
            if loc:
                return (loc.latitude, loc.longitude)
            return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
