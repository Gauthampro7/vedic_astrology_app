"""
Vedic Astrology Chart File Format Handler (.vac files)
Custom simple text-based chart file format.
Allows saving and loading charts with all necessary data.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from models.birth_data import BirthData
from models.chart_data import ChartData

logger = logging.getLogger(__name__)


class VACFileHandler:
    """
    Handles .vac (Vedic Astrology Chart) file format.
    Simple text-based JSON format for easy reading/editing.
    """

    FILE_EXTENSION = ".vac"
    VERSION = "1.0"

    @staticmethod
    def save_chart(chart_data: ChartData, filepath: str) -> bool:
        """
        Save chart to .vac file.
        
        Args:
            chart_data: ChartData object to save
            filepath: Path to save file (can end with or without .vac)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure filepath has correct extension
            if not filepath.endswith(VACFileHandler.FILE_EXTENSION):
                filepath = filepath + VACFileHandler.FILE_EXTENSION

            # Create chart dictionary
            chart_dict = {
                "version": VACFileHandler.VERSION,
                "created": datetime.now().isoformat(),
                "birth_info": {
                    "date": chart_data.birth_info.date,
                    "time": chart_data.birth_info.time,
                    "place": chart_data.birth_info.place,
                    "timezone": chart_data.birth_info.timezone,
                    "latitude": chart_data.birth_info.latitude,
                    "longitude": chart_data.birth_info.longitude,
                },
                "ayanamsa": chart_data.ayanamsa,
                "planets": {},
                "houses": chart_data.houses,
            }

            # Add planetary data
            for planet_name, planet_pos in chart_data.planets.items():
                chart_dict["planets"][planet_name] = {
                    "name": planet_pos.name,
                    "sign": planet_pos.sign,
                    "degree": planet_pos.degree,
                    "nakshatra": planet_pos.nakshatra,
                    "pada": planet_pos.pada,
                    "absolute_degree": planet_pos.absolute_degree,
                }

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(chart_dict, f, indent=2, ensure_ascii=False)

            logger.info(f"Chart saved to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to save chart: {str(e)}")
            return False

    @staticmethod
    def load_chart(filepath: str) -> Optional[ChartData]:
        """
        Load chart from .vac file.
        
        Args:
            filepath: Path to .vac file
            
        Returns:
            ChartData object or None if failed
        """
        try:
            filepath = Path(filepath)

            if not filepath.exists():
                logger.error(f"File not found: {filepath}")
                return None

            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                chart_dict = json.load(f)

            # Check version
            if chart_dict.get("version") != VACFileHandler.VERSION:
                logger.warning(f"File version {chart_dict.get('version')} may not be compatible")

            # Reconstruct BirthData
            birth_info_dict = chart_dict["birth_info"]
            birth_data = BirthData(
                date=birth_info_dict["date"],
                time=birth_info_dict["time"],
                place=birth_info_dict["place"],
                timezone=birth_info_dict["timezone"],
                latitude=birth_info_dict.get("latitude"),
                longitude=birth_info_dict.get("longitude"),
            )

            # Reconstruct planets data
            from models.chart_data import PlanetaryPosition
            planets_data = {}
            for planet_name, planet_dict in chart_dict["planets"].items():
                planets_data[planet_name] = PlanetaryPosition(
                    name=planet_dict["name"],
                    sign=planet_dict["sign"],
                    degree=planet_dict["degree"],
                    nakshatra=planet_dict["nakshatra"],
                    pada=planet_dict["pada"],
                    absolute_degree=planet_dict["absolute_degree"],
                )

            # Reconstruct ChartData
            chart_data = ChartData(
                birth_info=birth_data,
                planets=planets_data,
                houses=chart_dict["houses"],
                ayanamsa=chart_dict["ayanamsa"],
            )

            logger.info(f"Chart loaded from {filepath}")
            return chart_data

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in file: {filepath}")
            return None
        except Exception as e:
            logger.error(f"Failed to load chart: {str(e)}")
            return None

    @staticmethod
    def get_chart_summary(filepath: str) -> Optional[Dict]:
        """
        Get summary info from .vac file without fully loading.
        Useful for file browser/preview.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                chart_dict = json.load(f)

            birth_info = chart_dict["birth_info"]
            return {
                "place": birth_info["place"],
                "date": birth_info["date"],
                "time": birth_info["time"],
                "created": chart_dict.get("created", "Unknown"),
                "version": chart_dict.get("version", "Unknown"),
            }

        except Exception as e:
            logger.error(f"Failed to read chart summary: {str(e)}")
            return None
