"""
Input validation utilities.
"""
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)


class Validators:
    """Input validation functions."""

    @staticmethod
    def validate_date(date_str: str, format: str = '%Y/%m/%d') -> bool:
        """Validate date format."""
        try:
            datetime.strptime(date_str.strip(), format)
            logger.debug(f"Date validation passed: {date_str}")
            return True
        except ValueError as e:
            logger.warning(f"Date validation failed for '{date_str}': {str(e)}")
            return False

    @staticmethod
    def validate_time(time_str: str, format: str = '%H:%M:%S') -> bool:
        """Validate time format."""
        try:
            datetime.strptime(time_str.strip(), format)
            logger.debug(f"Time validation passed: {time_str}")
            return True
        except ValueError as e:
            logger.warning(f"Time validation failed for '{time_str}': {str(e)}")
            return False

    @staticmethod
    def validate_timezone(tz_str: str) -> bool:
        """Validate timezone format."""
        pattern = r'^[+-]\d{2}:\d{2}$'
        if not re.match(pattern, tz_str.strip()):
            logger.warning(f"Timezone validation failed for '{tz_str}'")
            return False

        try:
            tz_str = tz_str.strip()
            sign = 1 if tz_str[0] == '+' else -1
            hours, minutes = map(int, tz_str[1:].split(':'))

            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError("Hours must be 0-23, minutes 0-59")

            logger.debug(f"Timezone validation passed: {tz_str}")
            return True

        except Exception as e:
            logger.warning(f"Timezone validation failed for '{tz_str}': {str(e)}")
            return False

    @staticmethod
    def validate_place(place_str: str) -> bool:
        """Validate place name."""
        place_str = place_str.strip()

        if len(place_str) < 2:
            logger.warning(f"Place validation failed: too short '{place_str}'")
            return False

        if len(place_str) > 100:
            logger.warning(f"Place validation failed: too long '{place_str}'")
            return False

        if not re.match(r'^[a-zA-Z0-9\s,\-]*$', place_str):
            logger.warning(f"Place validation failed: invalid characters '{place_str}'")
            return False

        logger.debug(f"Place validation passed: {place_str}")
        return True

    @staticmethod
    def validate_all(date: str, time: str, timezone: str, place: str) -> tuple:
        """Validate all inputs at once."""
        if not Validators.validate_date(date):
            return (False, "Invalid date format. Use YYYY/MM/DD")

        if not Validators.validate_time(time):
            return (False, "Invalid time format. Use HH:MM:SS")

        if not Validators.validate_timezone(timezone):
            return (False, "Invalid timezone format. Use +HH:MM or -HH:MM")

        if not Validators.validate_place(place):
            return (False, "Invalid place name. Use letters, numbers, commas, hyphens only")

        return (True, "All inputs valid")
