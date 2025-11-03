"""
Chart generation service.
"""
from typing import Dict
import logging

from models.birth_data import BirthData
from models.chart_data import ChartData
from services.astro_calculator import AstroCalculator
from services.geocoding_service import GeocodingService
from models.constants import PLANETS, FLATLIB_PLANET_MAP

logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generates birth charts using flatlib."""

    @staticmethod
    def generate_chart(birth_data: BirthData) -> ChartData:
        """Generate complete birth chart."""
        try:
            from flatlib import const
            from flatlib.chart import Chart
            from flatlib.datetime import Datetime
            from flatlib.geopos import GeoPos
        except ImportError:
            raise ImportError("flatlib is required. Install with: pip install flatlib")

        try:
            # Geocode location if not already done
            if birth_data.latitude is None or birth_data.longitude is None:
                lat, lon = GeocodingService.get_coordinates(birth_data.place)
                birth_data.latitude = lat
                birth_data.longitude = lon

            # Create flatlib objects
            birthdate = Datetime(
                birth_data.date,      # keep as YYYY/MM/DD
                birth_data.time,
                birth_data.timezone
            )


            birthplace = GeoPos(
                birth_data.latitude,
                birth_data.longitude
            )

            # Generate chart
            chart = Chart(birthdate, birthplace)

            # Extract planetary data
            planets_data: Dict[str, any] = {}

            for planet_name in PLANETS:
                flatlib_name = FLATLIB_PLANET_MAP.get(planet_name)
                if flatlib_name:
                    try:
                        planet_obj = chart.get(getattr(const, flatlib_name))
                        position = AstroCalculator.create_planetary_position(
                            planet_name,
                            planet_obj.lon,
                            birth_data.year
                        )
                        planets_data[planet_name] = position
                    except Exception as e:
                        logger.warning(f"Could not get {planet_name}: {str(e)}")

            # Extract houses (1-12)
            houses_data: Dict[int, float] = {}
            for house_num in range(1, 13):
                try:
                    house_obj = chart.getHouse(house_num)
                    sidereal = AstroCalculator.tropical_to_sidereal(
                        house_obj.lon,
                        birth_data.year
                    )
                    houses_data[house_num] = sidereal
                except Exception as e:
                    logger.warning(f"Could not get house {house_num}: {str(e)}")

            # Get ayanamsa
            ayanamsa = AstroCalculator.calculate_ayanamsa(birth_data.year)

            # Create and return ChartData
            chart_data = ChartData(
                birth_info=birth_data,
                planets=planets_data,
                houses=houses_data,
                ayanamsa=ayanamsa
            )

            logger.info(f"Successfully generated chart for {birth_data.place}")
            return chart_data

        except Exception as e:
            logger.error(f"Chart generation failed: {str(e)}")
            raise ValueError(f"Failed to generate chart: {str(e)}")
