"""
Data formatting utilities.
"""


class Formatters:
    """Data formatting functions."""

    @staticmethod
    def format_degree(degree: float) -> str:
        """Format degree as degrees, minutes, seconds."""
        degrees = int(degree)
        minutes_decimal = (degree - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = int((minutes_decimal - minutes) * 60)

        return f"{degrees}°{minutes}'{seconds}\""

    @staticmethod
    def format_planetary_data(planets_dict: dict) -> list:
        """Format planetary data for table display."""
        headers = ['Planet', 'Sign', 'Longitude', 'Nakshatra', 'Pada']
        rows = [headers]

        for planet_name, planet_pos in planets_dict.items():
            rows.append([
                planet_pos.name.capitalize(),
                planet_pos.sign,
                Formatters.format_degree(planet_pos.degree),
                planet_pos.nakshatra,
                str(planet_pos.pada)
            ])

        return rows

    @staticmethod
    def format_date_display(date_str: str) -> str:
        """Format date for display."""
        from datetime import datetime
        date_obj = datetime.strptime(date_str, '%Y/%m/%d')
        return date_obj.strftime('%A, %B %d, %Y')

    @staticmethod
    def format_time_12hour(time_str: str) -> str:
        """Convert 24-hour time to 12-hour format."""
        from datetime import datetime
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        return time_obj.strftime('%I:%M:%S %p')
