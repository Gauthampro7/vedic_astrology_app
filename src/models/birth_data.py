"""
Birth data model with validation.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BirthData:
    """Represents birth information for astrological calculations.

    Attributes:
        date: Birth date in YYYY/MM/DD format
        time: Birth time in HH:MM:SS format
        place: Place name (city, country)
        timezone: Timezone offset like +05:30 or -08:00
        latitude: Latitude (auto-populated from geocoding)
        longitude: Longitude (auto-populated from geocoding)
    """
    date: str
    time: str
    place: str
    timezone: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def __post_init__(self):
        """Validate data after initialization."""
        self._validate_date()
        self._validate_time()
        self._validate_timezone()

    def _validate_date(self):
        """Validate date format."""
        try:
            datetime.strptime(self.date, '%Y/%m/%d')
        except ValueError:
            raise ValueError(f"Invalid date format: {self.date}. Expected YYYY/MM/DD")

    def _validate_time(self):
        """Validate time format."""
        try:
            datetime.strptime(self.time, '%H:%M:%S')
        except ValueError:
            raise ValueError(f"Invalid time format: {self.time}. Expected HH:MM:SS")

    def _validate_timezone(self):
        """Validate timezone format."""
        import re
        pattern = r'^[+-]\d{2}:\d{2}$'
        if not re.match(pattern, self.timezone):
            raise ValueError(f"Invalid timezone format: {self.timezone}. Expected +HH:MM or -HH:MM")

    @property
    def year(self) -> int:
        """Extract year from date."""
        return int(self.date[:4])

    @property
    def coordinates(self) -> tuple:
        """Get (latitude, longitude) tuple."""
        if self.latitude is None or self.longitude is None:
            raise ValueError("Coordinates not set. Call geocoding service first.")
        return (self.latitude, self.longitude)

    def get_datetime_obj(self) -> datetime:
        """Get combined datetime object."""
        date_part = datetime.strptime(self.date, '%Y/%m/%d')
        time_part = datetime.strptime(self.time, '%H:%M:%S')
        return date_part.replace(hour=time_part.hour, minute=time_part.minute, second=time_part.second)
