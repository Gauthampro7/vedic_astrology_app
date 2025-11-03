"""
Geocoding service for location lookup.
"""
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class GeocodingService:
    """Handles location geocoding."""

    @staticmethod
    def get_coordinates(place_name: str) -> Tuple[float, float]:
        """Get coordinates from place name."""
        try:
            from geopy.geocoders import Nominatim
        except ImportError:
            raise ImportError("geopy is required. Install with: pip install geopy")

        try:
            geolocator = Nominatim(user_agent="vedic_astrology_app")
            location = geolocator.geocode(place_name, timeout=10)

            if location is None:
                raise ValueError(f"Location '{place_name}' not found")

            logger.info(
                f"Found location '{place_name}': "
                f"{location.latitude:.6f}°, {location.longitude:.6f}°"
            )

            return (location.latitude, location.longitude)

        except Exception as e:
            logger.error(f"Geocoding error for '{place_name}': {str(e)}")
            raise ValueError(f"Failed to geocode '{place_name}': {str(e)}")

    @staticmethod
    def format_coordinates(latitude: float, longitude: float) -> str:
        """Format coordinates as string."""
        lat_dir = "N" if latitude >= 0 else "S"
        lon_dir = "E" if longitude >= 0 else "W"

        lat_abs = abs(latitude)
        lon_abs = abs(longitude)

        lat_deg = int(lat_abs)
        lat_min = int((lat_abs - lat_deg) * 60)

        lon_deg = int(lon_abs)
        lon_min = int((lon_abs - lon_deg) * 60)

        return f"{lat_deg}°{lat_min}'{lat_dir} {lon_deg}°{lon_min}'{lon_dir}"
