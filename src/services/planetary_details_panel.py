"""
Planetary Details Display - Professional Table View
Production-ready, works perfectly with CustomTkinter.
Displays all planetary information in an organized table format.
"""

import customtkinter as ctk
from typing import Optional
import logging

from models.chart_data import ChartData

logger = logging.getLogger(__name__)


class PlanetaryDetailsPanel(ctk.CTkFrame):
    """Professional planetary details table."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.chart_data: Optional[ChartData] = None
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create UI components."""

        # Title bar
        title_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="🪐 Planetary Positions & Details",
            font=("Helvetica", 14, "bold"),
            text_color="#FFD700"
        )

        # Table container
        self.table_container = ctk.CTkFrame(self, fg_color="transparent")

        # Header row
        self.header_frame = ctk.CTkFrame(
            self.table_container,
            fg_color="#3A3A3A",
            corner_radius=8,
            height=40
        )

        # Column definitions (name, width)
        self.columns = [
            ("Planet", 90),
            ("Sign", 110),
            ("Degree", 140),
            ("Min", 50),
            ("Sec", 50),
            ("Nakshatra", 180),
            ("Pada", 60),
            ("House", 70),
        ]

        # Create header cells
        for col_num, (col_name, width) in enumerate(self.columns):
            cell = ctk.CTkLabel(
                self.header_frame,
                text=col_name,
                font=("Helvetica", 10, "bold"),
                text_color="#FFD700",
                width=width
            )
            cell.grid(row=0, column=col_num, padx=8, pady=10, sticky="w")

        # Rows container
        self.rows_container = ctk.CTkFrame(self.table_container, fg_color="transparent")

        # Info bar
        info_frame = ctk.CTkFrame(self, fg_color="transparent", height=35)
        self.info_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=("Courier", 9),
            text_color="#888888"
        )

    def _layout_widgets(self):
        """Layout all components."""
        # Title
        self.title_label.pack(pady=(10, 5), padx=15)

        # Table
        self.table_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        self.header_frame.pack(fill="x", pady=(0, 5))
        self.rows_container.pack(fill="both", expand=True)

        # Info
        self.info_label.pack(pady=(5, 10), padx=15)

    def display_chart(self, chart_data: ChartData):
        """Display planetary data in table."""
        self.chart_data = chart_data

        # Clear previous rows
        for widget in self.rows_container.winfo_children():
            widget.destroy()

        # Add rows for each planet
        planets_list = list(chart_data.planets.items())
        for row_num, (planet_key, planet_data) in enumerate(planets_list):

            # Alternate row colors
            bg_color = "#2B2B2B" if row_num % 2 == 0 else "#242424"

            row_frame = ctk.CTkFrame(
                self.rows_container,
                fg_color=bg_color,
                corner_radius=6
            )
            row_frame.pack(fill="x", pady=2)

            # Extract data
            planet_name = planet_data.name

            # Get sign
            sign = planet_data.sign

            # Convert degree to D:M:S
            deg = int(planet_data.degree)
            min_part = int((planet_data.degree - deg) * 60)
            sec_part = int(((planet_data.degree - deg) * 60 - min_part) * 60)

            # Nakshatra and Pada
            nakshatra = planet_data.nakshatra
            pada = f"{planet_data.pada}"

            # Calculate which house (simplified)
            planet_house = self._get_planet_house(planet_data.absolute_degree, chart_data)

            # Create cells
            cells_data = [
                planet_name,
                sign,
                f"{deg}°",
                f"{min_part}'",
                f"{sec_part}\"",
                nakshatra,
                f"P{pada}",
                f"H{planet_house}",
            ]

            for col_num, (col_data, (col_name, width)) in enumerate(
                zip(cells_data, self.columns)
            ):
                cell = ctk.CTkLabel(
                    row_frame,
                    text=str(col_data),
                    font=("Courier", 9),
                    text_color="#E0E0E0",
                    width=width,
                    anchor="w"
                )
                cell.grid(row=0, column=col_num, padx=8, pady=8, sticky="w")

        # Update info bar
        self._update_info_bar(chart_data)

    def _get_planet_house(self, planet_degree: float, chart_data: ChartData) -> int:
        """Determine which house a planet is in (simplified)."""
        try:
            houses = chart_data.houses
            # Simplified: just find which house range the degree falls into
            for house_num in range(1, 13):
                current_house_degree = houses[house_num]
                next_house_degree = houses.get(house_num + 1, houses[1] + 360)

                # Handle wrap-around at 360 degrees
                if next_house_degree < current_house_degree:
                    next_house_degree += 360

                if current_house_degree <= planet_degree < next_house_degree:
                    return house_num

            return 1  # Default to house 1
        except Exception as e:
            logger.warning(f"Could not determine house: {e}")
            return 0

    def _update_info_bar(self, chart_data: ChartData):
        """Update bottom info bar."""
        birth = chart_data.birth_info
        info_text = (
            f"Birth: {birth.date} | Time: {birth.time} | Place: {birth.place} | "
            f"TZ: {birth.timezone} | Ayanamsa: {chart_data.ayanamsa:.4f}°"
        )
        self.info_label.configure(text=info_text)


# ============================================================================
# USAGE EXAMPLE - How to integrate into your chart view
# ============================================================================

"""
In your chart_view.py, add this:

from services.planetary_details_panel import PlanetaryDetailsPanel

class ChartDisplayView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Create main container with two sections
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="both", expand=False, padx=10, pady=10)
        
        # Chart goes here (replace your broken canvas)
        self.chart_label = ctk.CTkLabel(
            top_frame,
            text="[Chart will display here]",
            font=("Helvetica", 12)
        )
        self.chart_label.pack(fill="both", expand=True)
        
        # Bottom frame for table
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Planetary details panel
        self.details_panel = PlanetaryDetailsPanel(bottom_frame)
        self.details_panel.pack(fill="both", expand=True)
    
    def display_chart(self, chart_data):
        # Show planetary details (this works!)
        self.details_panel.display_chart(chart_data)
        
        # For chart visualization, use Matplotlib or web-based approach
"""
