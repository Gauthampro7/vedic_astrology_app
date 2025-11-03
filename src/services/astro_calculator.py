"""
Astrological calculation service.
Pure functions for all astronomical calculations.
"""
from typing import Tuple, Optional
import logging
from datetime import datetime

from models.constants import (
    ZodiacSign, Nakshatra,
    AYANAMSA_BASE_YEAR, AYANAMSA_BASE_VALUE, AYANAMSA_ANNUAL_RATE,
    NAKSHATRA_DEGREES, PADA_DEGREES
)
from models.chart_data import PlanetaryPosition

logger = logging.getLogger(__name__)


class AstroCalculator:
    """Handles all astrological calculations."""

    @staticmethod
    def normalize_degree(degree: float) -> float:
        """Normalize degree to 0-360 range."""
        normalized = degree % 360
        return normalized if normalized >= 0 else normalized + 360

    @staticmethod
    def calculate_ayanamsa(year: int) -> float:
        """Calculate Lahiri Ayanamsa for given year."""
        if not (1800 <= year <= 2200):
            raise ValueError(f"Year {year} outside valid range (1800-2200)")

        year_diff = year - AYANAMSA_BASE_YEAR
        ayanamsa = AYANAMSA_BASE_VALUE + (year_diff * AYANAMSA_ANNUAL_RATE)

        logger.debug(f"Calculated ayanamsa for {year}: {ayanamsa:.6f}°")
        return ayanamsa

    @staticmethod
    def tropical_to_sidereal(degree: float, year: int) -> float:
        """Convert tropical zodiac degree to sidereal."""
        ayanamsa = AstroCalculator.calculate_ayanamsa(year)
        sidereal = degree - ayanamsa
        normalized = AstroCalculator.normalize_degree(sidereal)

        logger.debug(
            f"Converted tropical {degree:.6f}° to sidereal {normalized:.6f}° "
            f"(ayanamsa: {ayanamsa:.6f}°)"
        )

        return normalized

    @staticmethod
    def get_zodiac_sign(degree: float) -> Tuple[ZodiacSign, float]:
        """Determine zodiac sign from degree."""
        normalized = AstroCalculator.normalize_degree(degree)
        sign = ZodiacSign.from_degree(normalized)
        degree_in_sign = normalized % 30

        logger.debug(
            f"Degree {normalized:.6f}° is in {sign.name_str} at {degree_in_sign:.6f}°"
        )

        return sign, degree_in_sign

    @staticmethod
    def get_nakshatra_and_pada(degree: float) -> Tuple[Nakshatra, int]:
        """Calculate nakshatra and pada from degree."""
        normalized = AstroCalculator.normalize_degree(degree)

        # Get nakshatra
        nakshatra = Nakshatra.from_degree(normalized)

        # Calculate pada (1-4)
        degree_in_nakshatra = normalized - nakshatra.degree_start
        pada = int(degree_in_nakshatra // PADA_DEGREES) + 1
        pada = min(max(pada, 1), 4)  # Ensure pada is 1-4

        logger.debug(
            f"Degree {normalized:.6f}° is in {nakshatra.name_str}, Pada {pada}"
        )

        return nakshatra, pada

    @staticmethod
    def decimal_to_dms(decimal_degree: float) -> Tuple[int, int, int]:
        """Convert decimal degree to degrees, minutes, seconds."""
        degrees = int(decimal_degree)
        minutes_decimal = (decimal_degree - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = int((minutes_decimal - minutes) * 60)

        return (degrees, minutes, seconds)

    @staticmethod
    def create_planetary_position(
        planet_name: str,
        degree: float,
        year: int
    ) -> PlanetaryPosition:
        """Create a PlanetaryPosition object from raw degree."""
        # Convert to sidereal
        sidereal_degree = AstroCalculator.tropical_to_sidereal(degree, year)

        # Get sign and degree within sign
        sign, degree_in_sign = AstroCalculator.get_zodiac_sign(sidereal_degree)

        # Get nakshatra and pada
        nakshatra, pada = AstroCalculator.get_nakshatra_and_pada(sidereal_degree)

        return PlanetaryPosition(
            name=planet_name,
            sign=sign.name_str,
            degree=degree_in_sign,
            nakshatra=nakshatra.name_str,
            pada=pada,
            absolute_degree=sidereal_degree
        )
