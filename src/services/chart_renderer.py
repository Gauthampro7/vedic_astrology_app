"""
Chart Renderer Service - Supports South Indian & North Indian Chart Layouts
Draws both chart types on a Tkinter canvas with planetary positions.
This service handles all visual chart rendering.
"""

import tkinter as tk
from typing import Dict, Tuple, Optional
import math
import logging

from models.chart_data import ChartData, PlanetaryPosition
from models.constants import ZodiacSign, Nakshatra, PLANETS

logger = logging.getLogger(__name__)


class ChartRenderer:
    """Renders Vedic astrology charts in South Indian and North Indian styles."""

    # Chart configuration
    CENTER_X = 300
    CENTER_Y = 300
    OUTER_RADIUS = 280
    INNER_RADIUS = 200
    SIGN_RADIUS = 240
    PLANET_RADIUS = 150

    # Colors
    BACKGROUND_COLOR = "#1a1a1a"
    LINE_COLOR = "#FFD700"
    TEXT_COLOR = "#FFFFFF"
    SIGN_COLOR = "#4CAF50"
    PLANET_COLOR = "#FF6B6B"

    @staticmethod
    def render_south_indian(canvas: tk.Canvas, chart_data: ChartData) -> None:
        """
        Render South Indian chart (diamond-shaped, houses in order 1-12).
        Layout: Houses arranged in square with 3 houses per side.
        """
        ChartRenderer._clear_canvas(canvas)
        ChartRenderer._draw_south_indian_grid(canvas)
        ChartRenderer._draw_planets_south_indian(canvas, chart_data)

    @staticmethod
    def render_north_indian(canvas: tk.Canvas, chart_data: ChartData) -> None:
        """
        Render North Indian chart (square-shaped, houses arranged linearly).
        Layout: Houses 1-4 on top row, 8-5 on second, etc.
        """
        ChartRenderer._clear_canvas(canvas)
        ChartRenderer._draw_north_indian_grid(canvas)
        ChartRenderer._draw_planets_north_indian(canvas, chart_data)

    @staticmethod
    def _clear_canvas(canvas: tk.Canvas) -> None:
        """Clear canvas and set background."""
        canvas.delete("all")
        canvas.create_rectangle(
            0, 0, canvas.winfo_width(), canvas.winfo_height(),
            fill=ChartRenderer.BACKGROUND_COLOR, outline=ChartRenderer.BACKGROUND_COLOR
        )

    @staticmethod
    def _draw_south_indian_grid(canvas: tk.Canvas) -> None:
        """
        Draw South Indian chart grid (diamond shape).
        12 houses arranged as: 3 on top, 3 on right, 3 on bottom, 3 on left.
        """
        cx, cy = ChartRenderer.CENTER_X, ChartRenderer.CENTER_Y
        r_outer = ChartRenderer.OUTER_RADIUS
        r_inner = ChartRenderer.INNER_RADIUS

        # Calculate diamond points
        top = (cx, cy - r_outer)
        right = (cx + r_outer, cy)
        bottom = (cx, cy + r_outer)
        left = (cx - r_outer, cy)

        # Draw outer diamond
        canvas.create_polygon(
            top[0], top[1], right[0], right[1], bottom[0], bottom[1], left[0], left[1],
            outline=ChartRenderer.LINE_COLOR, fill="", width=2
        )

        # Draw inner diamond
        inner_factor = r_inner / r_outer
        inner_points = [
            (cx + (p[0] - cx) * inner_factor, cy + (p[1] - cy) * inner_factor)
            for p in [top, right, bottom, left]
        ]
        canvas.create_polygon(
            *sum(inner_points, ()), outline=ChartRenderer.LINE_COLOR, fill="", width=1
        )

        # Draw house divisions (4 triangles, subdivided into 3)
        # Top-right triangle
        canvas.create_line(top[0], top[1], right[0], right[1], fill=ChartRenderer.LINE_COLOR, width=1)
        canvas.create_line(right[0], right[1], bottom[0], bottom[1], fill=ChartRenderer.LINE_COLOR, width=1)
        canvas.create_line(bottom[0], bottom[1], left[0], left[1], fill=ChartRenderer.LINE_COLOR, width=1)
        canvas.create_line(left[0], left[1], top[0], top[1], fill=ChartRenderer.LINE_COLOR, width=1)

        # Draw subdivisions (simplified - each side divided into 3 houses)
        for i in range(1, 3):
            factor = i / 3
            # Top-right subdivision
            p1_x = top[0] + (right[0] - top[0]) * factor
            p1_y = top[1] + (right[1] - top[1]) * factor
            p2_x = cx + (right[0] - cx) * factor
            p2_y = cy + (right[1] - cy) * factor
            canvas.create_line(p1_x, p1_y, p2_x, p2_y, fill=ChartRenderer.LINE_COLOR, width=1)

            # Right-bottom subdivision
            p3_x = right[0] + (bottom[0] - right[0]) * factor
            p3_y = right[1] + (bottom[1] - right[1]) * factor
            p4_x = cx + (bottom[0] - cx) * factor
            p4_y = cy + (bottom[1] - cy) * factor
            canvas.create_line(p3_x, p3_y, p4_x, p4_y, fill=ChartRenderer.LINE_COLOR, width=1)

            # Bottom-left subdivision
            p5_x = bottom[0] + (left[0] - bottom[0]) * factor
            p5_y = bottom[1] + (left[1] - bottom[1]) * factor
            p6_x = cx + (left[0] - cx) * factor
            p6_y = cy + (left[1] - cy) * factor
            canvas.create_line(p5_x, p5_y, p6_x, p6_y, fill=ChartRenderer.LINE_COLOR, width=1)

            # Left-top subdivision
            p7_x = left[0] + (top[0] - left[0]) * factor
            p7_y = left[1] + (top[1] - left[1]) * factor
            p8_x = cx + (top[0] - cx) * factor
            p8_y = cy + (top[1] - cy) * factor
            canvas.create_line(p7_x, p7_y, p8_x, p8_y, fill=ChartRenderer.LINE_COLOR, width=1)

        # Add house numbers
        ChartRenderer._add_house_numbers_south_indian(canvas)

    @staticmethod
    def _draw_north_indian_grid(canvas: tk.Canvas) -> None:
        """
        Draw North Indian chart grid (square shape).
        Houses arranged: 1-4 on top, 8-5 on right, 12-9 on bottom, 3-12 on left.
        """
        cx, cy = ChartRenderer.CENTER_X, ChartRenderer.CENTER_Y
        size = ChartRenderer.OUTER_RADIUS

        # Draw outer square
        canvas.create_rectangle(
            cx - size, cy - size, cx + size, cy + size,
            outline=ChartRenderer.LINE_COLOR, fill="", width=2
        )

        # Draw inner square
        inner_size = ChartRenderer.INNER_RADIUS
        canvas.create_rectangle(
            cx - inner_size, cy - inner_size, cx + inner_size, cy + inner_size,
            outline=ChartRenderer.LINE_COLOR, fill="", width=1
        )

        # Draw grid lines (4x4 grid for 12 houses)
        cell_size = (size * 2) / 4
        for i in range(1, 4):
            x = cx - size + i * cell_size
            canvas.create_line(x, cy - size, x, cy + size, fill=ChartRenderer.LINE_COLOR, width=1)
            y = cy - size + i * cell_size
            canvas.create_line(cx - size, y, cx + size, y, fill=ChartRenderer.LINE_COLOR, width=1)

        # Add house numbers
        ChartRenderer._add_house_numbers_north_indian(canvas)

    @staticmethod
    def _add_house_numbers_south_indian(canvas: tk.Canvas) -> None:
        """Add house numbers to South Indian chart."""
        cx, cy = ChartRenderer.CENTER_X, ChartRenderer.CENTER_Y
        r = ChartRenderer.SIGN_RADIUS

        # House positions in South Indian (clockwise from top)
        positions = [
            (cx, cy - r),                           # 1 - top
            (cx + r * 0.707, cy - r * 0.707),      # 2
            (cx + r, cy),                           # 3 - right
            (cx + r * 0.707, cy + r * 0.707),      # 4
            (cx, cy + r),                           # 5 - bottom
            (cx - r * 0.707, cy + r * 0.707),      # 6
            (cx - r, cy),                           # 7 - left
            (cx - r * 0.707, cy - r * 0.707),      # 8
        ]

        for i, pos in enumerate(positions):
            house_num = i + 1
            canvas.create_text(
                pos[0], pos[1], text=str(house_num),
                fill=ChartRenderer.TEXT_COLOR, font=("Helvetica", 10, "bold")
            )

    @staticmethod
    def _add_house_numbers_north_indian(canvas: tk.Canvas) -> None:
        """Add house numbers to North Indian chart."""
        cx, cy = ChartRenderer.CENTER_X, ChartRenderer.CENTER_Y
        size = ChartRenderer.OUTER_RADIUS
        cell_size = (size * 2) / 4

        # House arrangement in North Indian
        house_positions = {
            1: (cx - 2.5 * cell_size, cy - 2.5 * cell_size),
            2: (cx - 1.5 * cell_size, cy - 2.5 * cell_size),
            3: (cx - 0.5 * cell_size, cy - 2.5 * cell_size),
            4: (cx + 0.5 * cell_size, cy - 2.5 * cell_size),
            5: (cx + 0.5 * cell_size, cy - 1.5 * cell_size),
            6: (cx + 0.5 * cell_size, cy - 0.5 * cell_size),
            7: (cx + 0.5 * cell_size, cy + 0.5 * cell_size),
            8: (cx + 0.5 * cell_size, cy + 1.5 * cell_size),
            9: (cx + 0.5 * cell_size, cy + 2.5 * cell_size),
            10: (cx - 0.5 * cell_size, cy + 2.5 * cell_size),
            11: (cx - 1.5 * cell_size, cy + 2.5 * cell_size),
            12: (cx - 2.5 * cell_size, cy + 2.5 * cell_size),
        }

        for house_num, pos in house_positions.items():
            canvas.create_text(
                pos[0], pos[1], text=str(house_num),
                fill=ChartRenderer.TEXT_COLOR, font=("Helvetica", 10, "bold")
            )

    @staticmethod
    def _draw_planets_south_indian(canvas: tk.Canvas, chart_data: ChartData) -> None:
        """Draw planets on South Indian chart."""
        cx, cy = ChartRenderer.CENTER_X, ChartRenderer.CENTER_Y

        # Draw each planet
        for planet_name, planet_pos in chart_data.planets.items():
            # Convert zodiac sign to angle (0 = Aries at top)
            sign_index = planet_pos.sign_index if hasattr(planet_pos, 'sign_index') else ZodiacSign[planet_pos.sign.upper()].index
            angle = (sign_index * 30 + planet_pos.degree) * (math.pi / 180)

            # Position on outer ring
            x = cx + ChartRenderer.PLANET_RADIUS * math.sin(angle)
            y = cy - ChartRenderer.PLANET_RADIUS * math.cos(angle)

            # Draw planet symbol (using abbreviation)
            symbol = planet_name[:2].upper()
            canvas.create_text(
                x, y, text=symbol,
                fill=ChartRenderer.PLANET_COLOR, font=("Helvetica", 12, "bold"),
                tags=planet_name
            )

            # Add nakshatra info
            logger.debug(f"{planet_name}: {planet_pos.nakshatra} - {planet_pos.pada}")

    @staticmethod
    def _draw_planets_north_indian(canvas: tk.Canvas, chart_data: ChartData) -> None:
        """Draw planets on North Indian chart."""
        cx, cy = ChartRenderer.CENTER_X, ChartRenderer.CENTER_Y
        size = ChartRenderer.OUTER_RADIUS
        cell_size = (size * 2) / 4

        # North Indian chart uses different positioning
        for planet_name, planet_pos in chart_data.planets.items():
            # Get house from degree (simplified)
            house = int(planet_pos.absolute_degree / 30) + 1
            if house > 12:
                house = 12

            # Position based on house (simplified)
            row = (house - 1) // 4
            col = (house - 1) % 4

            x = cx - 1.5 * cell_size + col * cell_size
            y = cy - 1.5 * cell_size + row * cell_size

            symbol = planet_name[:2].upper()
            canvas.create_text(
                x, y, text=symbol,
                fill=ChartRenderer.PLANET_COLOR, font=("Helvetica", 12, "bold"),
                tags=planet_name
            )


class ChartCanvasWidget(tk.Canvas):
    """Tkinter Canvas widget for displaying charts."""

    def __init__(self, parent, chart_type: str = "south_indian", **kwargs):
        super().__init__(
            parent,
            width=600, height=600,
            bg=ChartRenderer.BACKGROUND_COLOR,
            highlightthickness=0,
            **kwargs
        )
        self.chart_type = chart_type
        self.current_chart = None

    def display_chart(self, chart_data: ChartData):
        """Display a chart on the canvas."""
        self.current_chart = chart_data

        if self.chart_type == "south_indian":
            ChartRenderer.render_south_indian(self, chart_data)
        elif self.chart_type == "north_indian":
            ChartRenderer.render_north_indian(self, chart_data)

    def switch_chart_type(self, new_type: str):
        """Switch between chart types."""
        if new_type not in ["south_indian", "north_indian"]:
            raise ValueError("Chart type must be 'south_indian' or 'north_indian'")

        self.chart_type = new_type
        if self.current_chart:
            self.display_chart(self.current_chart)
