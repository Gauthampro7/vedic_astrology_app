"""
Enhanced Chart Display View with South Indian & North Indian support.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import logging

from services.chart_renderer import ChartCanvasWidget, ChartRenderer
from services.vac_file_handler import VACFileHandler
from services.extensibility_hub import ModuleRegistry
from utils.formatters import Formatters

logger = logging.getLogger(__name__)


class ChartDisplayView(ctk.CTkFrame):
    """Enhanced chart display with multiple layout options and file handling."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.module_registry = ModuleRegistry()  # Initialize modules
        self.current_chart_data = None
        
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create all UI widgets."""
        
        # --- TITLE ---
        self.title_label = ctk.CTkLabel(
            self,
            text="📊 Birth Chart Visualization",
            font=("Helvetica", 20, "bold"),
            text_color="#FFD700"
        )

        # --- CONTROL PANEL ---
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")

        # Chart type selector
        self.chart_type_label = ctk.CTkLabel(
            self.control_frame,
            text="Chart Type:",
            font=("Helvetica", 11)
        )
        self.chart_type_var = ctk.StringVar(value="south_indian")
        self.chart_type_combo = ctk.CTkComboBox(
            self.control_frame,
            values=["South Indian", "North Indian"],
            variable=self.chart_type_var,
            state="readonly",
            width=150,
            command=self._on_chart_type_change
        )

        # File buttons
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

        # Module execution buttons
        self.modules_label = ctk.CTkLabel(
            self.control_frame,
            text="Additional Analysis:",
            font=("Helvetica", 11)
        )

        self.compatibility_button = ctk.CTkButton(
            self.control_frame,
            text="💕 Compatibility",
            command=lambda: self._execute_module("compatibility"),
            width=150,
            fg_color="#FF9800"
        )

        self.yoga_button = ctk.CTkButton(
            self.control_frame,
            text="✨ Yogas",
            command=lambda: self._execute_module("yoga"),
            width=150,
            fg_color="#9C27B0"
        )

        self.bhava_button = ctk.CTkButton(
            self.control_frame,
            text="🏠 Bhava Chart",
            command=lambda: self._execute_module("bhava"),
            width=150,
            fg_color="#00BCD4"
        )

        self.navamsa_button = ctk.CTkButton(
            self.control_frame,
            text="🔷 Navamsa",
            command=lambda: self._execute_module("navamsa"),
            width=150,
            fg_color="#E91E63"
        )

        # --- CHART CANVAS ---
        self.canvas = ChartCanvasWidget(self, chart_type="south_indian")

        # --- INFO PANEL ---
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="Birth Information",
            font=("Helvetica", 12, "bold")
        )

        self.info_text = ctk.CTkTextbox(
            self.info_frame,
            height=120,
            font=("Courier", 10),
            state="normal"
        )

        self.details_label = ctk.CTkLabel(
            self.info_frame,
            text="Planetary Details",
            font=("Helvetica", 12, "bold")
        )

        self.details_text = ctk.CTkTextbox(
            self.info_frame,
            height=150,
            font=("Courier", 10),
            state="normal"
        )

    def _layout_widgets(self):
        """Arrange widgets."""
        self.title_label.pack(pady=15)

        # Control panel
        self.control_frame.pack(fill="x", padx=20, pady=10)
        
        # Row 1: Chart type selector
        self.chart_type_label.grid(row=0, column=0, sticky="w", padx=5)
        self.chart_type_combo.grid(row=0, column=1, padx=5)
        
        # Row 2: File operations
        self.save_button.grid(row=1, column=0, padx=5, pady=5)
        self.load_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Row 3: Analysis modules
        self.modules_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=(10, 5))
        
        self.compatibility_button.grid(row=3, column=0, padx=5, pady=2)
        self.yoga_button.grid(row=3, column=1, padx=5, pady=2)
        self.bhava_button.grid(row=4, column=0, padx=5, pady=2)
        self.navamsa_button.grid(row=4, column=1, padx=5, pady=2)

        # Chart canvas
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

        # Info panels
        self.info_frame.pack(fill="x", padx=20, pady=10)
        self.info_label.pack(anchor="w")
        self.info_text.pack(fill="x", pady=5)
        self.details_label.pack(anchor="w")
        self.details_text.pack(fill="x", pady=5)

    def _on_chart_type_change(self, value):
        """Switch between chart types."""
        chart_type = "south_indian" if value == "South Indian" else "north_indian"
        self.canvas.switch_chart_type(chart_type)
        if self.current_chart_data:
            self.canvas.display_chart(self.current_chart_data)

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

    def _execute_module(self, module_id: str):
        """Execute a calculation module."""
        if not self.current_chart_data:
            messagebox.showwarning("No Chart", "Please calculate a chart first")
            return

        result = self.module_registry.execute(module_id, self.current_chart_data)
        
        if "error" in result:
            messagebox.showerror("Module Error", result["error"])
        else:
            # Show module results in info panel
            module = self.module_registry.get_module(module_id)
            report = module.get_report()
            messagebox.showinfo(f"{module.module_name}", report)

    def display_chart(self, chart_data):
        """Display chart data."""
        self.current_chart_data = chart_data

        # Update canvas
        self.canvas.display_chart(chart_data)

        # Update info text
        birth = chart_data.birth_info
        info_text = f"""Birth Information:
━━━━━━━━━━━━━━━━━━━━━━━
Date: {Formatters.format_date_display(birth.date)}
Time: {Formatters.format_time_12hour(birth.time)}
Place: {birth.place}
Timezone: {birth.timezone}
Coordinates: {birth.latitude:.4f}°, {birth.longitude:.4f}°
Ayanamsa: {chart_data.ayanamsa:.4f}°"""

        self.info_text.delete("1.0", "end")
        self.info_text.insert("1.0", info_text)
        self.info_text.configure(state="disabled")

        # Update planetary details
        details_text = "Planetary Positions:\n" + "━" * 50 + "\n"
        for planet_name, planet_pos in chart_data.planets.items():
            d, m, s = planet_pos.degree_minutes_seconds()
            details_text += f"{planet_pos.name:12} {planet_pos.sign:12} {d:2d}°{m:02d}'{s:02d}\" {planet_pos.nakshatra:15} P{planet_pos.pada}\n"

        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", details_text)
        self.details_text.configure(state="disabled")
