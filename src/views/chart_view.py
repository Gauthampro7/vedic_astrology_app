"""
Fixed Chart Display View - With Working Planetary Details Table
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import logging

from services.vac_file_handler import VACFileHandler
from services.extensibility_hub import ModuleRegistry
from services.planetary_details_panel import PlanetaryDetailsPanel
from utils.formatters import Formatters

logger = logging.getLogger(__name__)


class ChartDisplayView(ctk.CTkFrame):
    """Chart display with working planetary details table."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.module_registry = ModuleRegistry()
        self.current_chart_data = None
        
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create UI widgets."""
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="📊 Birth Chart",
            font=("Helvetica", 20, "bold"),
            text_color="#FFD700"
        )

        # Control buttons frame
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent", height=50)

        self.save_button = ctk.CTkButton(
            self.control_frame,
            text="💾 Save Chart (.vac)",
            command=self._save_chart,
            width=150,
            fg_color="#4CAF50"
        )

        self.load_button = ctk.CTkButton(
            self.control_frame,
            text="📂 Load Chart (.vac)",
            command=self._load_chart,
            width=150,
            fg_color="#2196F3"
        )

        # Placeholder for chart image (using Label for now)
        self.chart_placeholder = ctk.CTkFrame(
            self,
            fg_color="#2B2B2B",
            corner_radius=10,
            height=300
        )
        self.chart_label = ctk.CTkLabel(
            self.chart_placeholder,
            text="🎨 Chart visualization coming soon\n(Use Matplotlib or web-based approach)",
            font=("Helvetica", 14),
            text_color="#888888"
        )

        # IMPORTANT: Planetary details panel (THIS WORKS!)
        self.details_panel = PlanetaryDetailsPanel(self)

    def _layout_widgets(self):
        """Layout widgets."""
        self.title_label.pack(pady=15, padx=20)

        self.control_frame.pack(fill="x", padx=20, pady=10)
        self.save_button.pack(side="left", padx=5)
        self.load_button.pack(side="left", padx=5)

        # Chart placeholder
        self.chart_placeholder.pack(fill="x", padx=20, pady=10)
        self.chart_label.pack(fill="both", expand=True)

        # Planetary details (THIS IS YOUR WORKING TABLE)
        self.details_panel.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    def _save_chart(self):
        """Save chart to .vac file."""
        if not self.current_chart_data:
            messagebox.showwarning("No Chart", "Please calculate a chart first")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".vac",
            filetypes=[("Vedic Astrology Chart", "*.vac"), ("All files", "*.*")]
        )

        if filepath:
            if VACFileHandler.save_chart(self.current_chart_data, filepath):
                messagebox.showinfo("Success", f"Chart saved to {filepath}")
            else:
                messagebox.showerror("Error", "Failed to save chart")

    def _load_chart(self):
        """Load chart from .vac file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Vedic Astrology Chart", "*.vac"), ("All files", "*.*")]
        )

        if filepath:
            chart_data = VACFileHandler.load_chart(filepath)
            if chart_data:
                self.display_chart(chart_data)
                messagebox.showinfo("Success", f"Chart loaded from {filepath}")
            else:
                messagebox.showerror("Error", "Failed to load chart")

    def display_chart(self, chart_data):
        """Display chart data."""
        self.current_chart_data = chart_data

        # Display the working planetary details table
        self.details_panel.display_chart(chart_data)

        logger.info(f"Chart displayed for {chart_data.birth_info.place}")
