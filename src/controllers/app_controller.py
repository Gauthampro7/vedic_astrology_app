"""
Application controller.
Coordinates between Model (services) and View (UI).
"""
import logging
from typing import Dict

from models.birth_data import BirthData
from services.chart_generator import ChartGenerator
from services.geocoding_service import GeocodingService

logger = logging.getLogger(__name__)


class AppController:
    """Application controller - MVC pattern."""

    def __init__(self, view):
        """Initialize controller."""
        self.view = view
        logger.info("AppController initialized")

    def handle_calculate(self, form_data: Dict):
        """Handle chart calculation request."""
        try:
            logger.info(f"Calculate requested for {form_data['place']}")

            birth_data = BirthData(
                date=form_data['date'],
                time=form_data['time'],
                place=form_data['place'],
                timezone=form_data['timezone']
            )

            logger.info(f"Geocoding location: {form_data['place']}")
            lat, lon = GeocodingService.get_coordinates(form_data['place'])
            birth_data.latitude = lat
            birth_data.longitude = lon

            logger.info("Generating chart")
            chart_data = ChartGenerator.generate_chart(birth_data)

            logger.info("Displaying chart")
            self.view.display_chart(chart_data)

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            self.view.show_error(str(e))

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            self.view.show_error(f"An error occurred: {str(e)}")
