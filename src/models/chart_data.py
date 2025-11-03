"""
Chart calculation results.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class PlanetaryPosition:
    """Position of a single planet or point."""
    name: str
    sign: str
    degree: float
    nakshatra: str
    pada: int
    absolute_degree: float

    def degree_minutes_seconds(self) -> tuple:
        """Convert decimal degree to degrees, minutes, seconds."""
        degrees = int(self.degree)
        minutes_decimal = (self.degree - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = int((minutes_decimal - minutes) * 60)
        return (degrees, minutes, seconds)

    def formatted_position(self) -> str:
        """Get formatted position string."""
        d, m, s = self.degree_minutes_seconds()
        return f"{self.sign} {d}°{m}'{s}\""


@dataclass
class ChartData:
    """Complete birth chart data."""
    birth_info: 'BirthData'
    planets: Dict[str, PlanetaryPosition]
    houses: Dict[int, float]
    ayanamsa: float

    def get_planet(self, name: str) -> Optional[PlanetaryPosition]:
        """Get planetary position by name."""
        name_lower = name.lower()
        return self.planets.get(name_lower)

    def to_table_data(self) -> List[List]:
        """Convert to table format for display."""
        headers = ['Planet', 'Sign', 'Longitude', 'Nakshatra', 'Pada']
        rows = [headers]

        for planet_name, planet_data in self.planets.items():
            d, m, s = planet_data.degree_minutes_seconds()
            longitude = f"{d}° {m}' {s}\""

            rows.append([
                planet_data.name.capitalize(),
                planet_data.sign,
                longitude,
                planet_data.nakshatra,
                str(planet_data.pada)
            ])

        return rows

    def get_houses_dict(self) -> Dict[str, float]:
        """Get houses with labels."""
        house_labels = {
            1: "1st House (Ascendant)",
            2: "2nd House",
            3: "3rd House",
            4: "4th House (IC)",
            5: "5th House",
            6: "6th House",
            7: "7th House (Descendant)",
            8: "8th House",
            9: "9th House",
            10: "10th House (Midheaven)",
            11: "11th House",
            12: "12th House"
        }
        return {house_labels.get(k, f"House {k}"): v for k, v in self.houses.items()}
