"""
Astrological constants and enumerations.
This module centralizes all constants used throughout the application.
"""
from enum import Enum
from typing import Tuple


# Ayanamsa Constants (Lahiri system)
AYANAMSA_BASE_YEAR = 2023
AYANAMSA_BASE_VALUE = 24.18  # degrees for March 2023
AYANAMSA_ANNUAL_RATE = 0.013957142857  # degrees per year (50.26 arcsec/year)

# Nakshatra Constants
NAKSHATRA_DEGREES = 13.333333333333  # Each nakshatra spans 13°20'
PADA_DEGREES = 3.333333333333  # Each pada within nakshatra (3°20')

# Planet names in order
PLANETS = [
    'lagna', 'sun', 'moon', 'mars', 'mercury',
    'jupiter', 'venus', 'saturn', 'rahu', 'ketu'
]

# Flatlib constant mappings
FLATLIB_PLANET_MAP = {
    'lagna': 'ASC',
    'sun': 'SUN',
    'moon': 'MOON',
    'mars': 'MARS',
    'mercury': 'MERCURY',
    'jupiter': 'JUPITER',
    'venus': 'VENUS',
    'saturn': 'SATURN',
    'rahu': 'NORTH_NODE',
    'ketu': 'SOUTH_NODE'
}


class ZodiacSign(Enum):
    """Zodiac signs with their properties."""
    ARIES = (0, "Aries", "♈", "Fire", "Cardinal")
    TAURUS = (1, "Taurus", "♉", "Earth", "Fixed")
    GEMINI = (2, "Gemini", "♊", "Air", "Mutable")
    CANCER = (3, "Cancer", "♋", "Water", "Cardinal")
    LEO = (4, "Leo", "♌", "Fire", "Fixed")
    VIRGO = (5, "Virgo", "♍", "Earth", "Mutable")
    LIBRA = (6, "Libra", "♎", "Air", "Cardinal")
    SCORPIO = (7, "Scorpio", "♏", "Water", "Fixed")
    SAGITTARIUS = (8, "Sagittarius", "♐", "Fire", "Mutable")
    CAPRICORN = (9, "Capricorn", "♑", "Earth", "Cardinal")
    AQUARIUS = (10, "Aquarius", "♒", "Air", "Fixed")
    PISCES = (11, "Pisces", "♓", "Water", "Mutable")

    @property
    def index(self) -> int:
        return self.value[0]

    @property
    def name_str(self) -> str:
        return self.value[1]

    @property
    def symbol(self) -> str:
        return self.value[2]

    @property
    def element(self) -> str:
        return self.value[3]

    @property
    def modality(self) -> str:
        return self.value[4]

    @property
    def degree_range(self) -> Tuple[int, int]:
        """Get degree range for this sign."""
        start = self.index * 30
        return (start, start + 30)

    @classmethod
    def from_degree(cls, degree: float) -> 'ZodiacSign':
        """Get zodiac sign from degree."""
        normalized = degree % 360
        sign_index = int(normalized // 30)
        for sign in cls:
            if sign.index == sign_index:
                return sign
        return cls.ARIES


class Nakshatra(Enum):
    """27 Nakshatras with their properties."""
    ASHWINI = (0, "Ashwini", "→", "Ketu")
    BHARANI = (1, "Bharani", "↓", "Venus")
    KRITTIKA = (2, "Krittika", "↓", "Sun")
    ROHINI = (3, "Rohini", "↑", "Moon")
    MRIGASHIRA = (4, "Mrigashira", "→", "Mars")
    ARDRA = (5, "Ardra", "↑", "Rahu")
    PUNARVASU = (6, "Punarvasu", "→", "Jupiter")
    PUSHYA = (7, "Pushya", "↑", "Saturn")
    ASHLESHA = (8, "Ashlesha", "↓", "Mercury")
    MAGHA = (9, "Magha", "↓", "Ketu")
    PURVA_PHALGUNI = (10, "Purva Phalguni", "↓", "Venus")
    UTTARA_PHALGUNI = (11, "Uttara Phalguni", "↑", "Sun")
    HASTA = (12, "Hasta", "→", "Moon")
    CHITRA = (13, "Chitra", "→", "Mars")
    SWATI = (14, "Swati", "→", "Rahu")
    VISHAKHA = (15, "Vishakha", "↓", "Jupiter")
    ANURADHA = (16, "Anuradha", "→", "Saturn")
    JYESHTHA = (17, "Jyeshtha", "→", "Mercury")
    MULA = (18, "Mula", "↓", "Ketu")
    PURVA_ASHADHA = (19, "Purva Ashadha", "↓", "Venus")
    UTTARA_ASHADHA = (20, "Uttara Ashadha", "↑", "Sun")
    SHRAVANA = (21, "Shravana", "↑", "Moon")
    DHANISHTA = (22, "Dhanishta", "↑", "Mars")
    SHATABHISHA = (23, "Shatabhisha", "↑", "Rahu")
    PURVA_BHADRAPADA = (24, "Purva Bhadrapada", "↓", "Jupiter")
    UTTARA_BHADRAPADA = (25, "Uttara Bhadrapada", "↑", "Saturn")
    REVATI = (26, "Revati", "→", "Mercury")

    @property
    def index(self) -> int:
        return self.value[0]

    @property
    def name_str(self) -> str:
        return self.value[1]

    @property
    def direction(self) -> str:
        return self.value[2]

    @property
    def lord(self) -> str:
        return self.value[3]

    @property
    def degree_start(self) -> float:
        """Starting degree of this nakshatra."""
        return self.index * NAKSHATRA_DEGREES

    @classmethod
    def from_degree(cls, degree: float) -> 'Nakshatra':
        """Get nakshatra from degree."""
        normalized = degree % 360
        nakshatra_index = min(int(normalized // NAKSHATRA_DEGREES), 26)
        for nak in cls:
            if nak.index == nakshatra_index:
                return nak
        return cls.ASHWINI
