"""
Chart display view using CustomTkinter.
"""
import customtkinter as ctk
from typing import List
import logging

from utils.formatters import Formatters

logger = logging.getLogger(__name__)


class ChartDisplayView(ctk.CTkFrame):
    """View for displaying birth chart results."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create UI widgets."""
        self.title_label = ctk.CTkLabel(
            self,
            text="Birth Chart",
            font=("Helvetica", 20, "bold"),
            text_color="#FFD700"
        )

        self.info_frame = ctk.CTkFrame(self, border_width=2, border_color="#555555")
        self.info_text = ctk.CTkTextbox(
            self.info_frame,
            height=150,
            font=("Courier", 10),
            state="normal"
        )

        self.table_frame = ctk.CTkFrame(self, border_width=2, border_color="#555555")
        self.table_text = ctk.CTkTextbox(
            self.table_frame,
            height=300,
            font=("Courier", 10),
            state="normal"
        )

        self.export_button = ctk.CTkButton(
            self,
            text="Export as Text",
            command=self._export_text,
            height=40,
            font=("Helvetica", 12, "bold"),
            fg_color="#2196F3",
            hover_color="#0b7dda"
        )

    def _layout_widgets(self):
        """Arrange widgets."""
        self.title_label.grid(
            row=0, column=0, columnspan=2,
            pady=15, padx=20, sticky="ew"
        )

        ctk.CTkLabel(
            self, text="Birth Information",
            font=("Helvetica", 12, "bold")
        ).grid(row=1, column=0, columnspan=2, pady=(15, 5), padx=20, sticky="w")

        self.info_frame.grid(
            row=2, column=0, columnspan=2,
            pady=10, padx=20, sticky="ew"
        )
        self.info_text.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            self, text="Planetary Positions",
            font=("Helvetica", 12, "bold")
        ).grid(row=3, column=0, columnspan=2, pady=(15, 5), padx=20, sticky="w")

        self.table_frame.grid(
            row=4, column=0, columnspan=2,
            pady=10, padx=20, sticky="ew"
        )
        self.table_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.export_button.grid(
            row=5, column=0, columnspan=2,
            pady=15, padx=20, sticky="ew"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def display_chart(self, chart_data):
        """Display chart data."""
        try:
            self.info_text.delete("1.0", "end")
            self.table_text.delete("1.0", "end")

            info_summary = self._format_info(chart_data)
            self.info_text.insert("1.0", info_summary)
            self.info_text.configure(state="disabled")

            table_data = self._format_table(chart_data)
            self.table_text.insert("1.0", table_data)
            self.table_text.configure(state="disabled")

            logger.info("Chart displayed successfully")

        except Exception as e:
            logger.error(f"Error displaying chart: {str(e)}")
            self.info_text.delete("1.0", "end")
            self.info_text.insert("1.0", f"Error: {str(e)}")

    def _format_info(self, chart_data) -> str:
        """Format birth information."""
        birth = chart_data.birth_info

        info = f"""Birth Information:
───────────────────────────────────────
Date:       {Formatters.format_date_display(birth.date)}
Time:       {Formatters.format_time_12hour(birth.time)}
Place:      {birth.place}
Timezone:   {birth.timezone}

Coordinates:
Latitude:   {birth.latitude:.6f}°
Longitude:  {birth.longitude:.6f}°

Ayanamsa:   {chart_data.ayanamsa:.6f}°
"""
        return info

    def _format_table(self, chart_data) -> str:
        """Format planetary data as table."""
        table_data = chart_data.to_table_data()

        output = "Planetary Positions:\n"
        output += "───────────────────────────────────────────────────────────\n"

        output += f"{'Planet':<15} {'Sign':<12} {'Longitude':<12} {'Nakshatra':<15} {'P'}\n"
        output += "───────────────────────────────────────────────────────────\n"

        for row in table_data[1:]:
            output += f"{row[0]:<15} {row[1]:<12} {row[2]:<12} {row[3]:<15} {row[4]}\n"

        return output

    def _export_text(self):
        """Export chart as text file."""
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                content = self.info_text.get("1.0", "end") + "\n" + self.table_text.get("1.0", "end")
                with open(file_path, 'w') as f:
                    f.write(content)
                logger.info(f"Chart exported to {file_path}")
            except Exception as e:
                logger.error(f"Export failed: {str(e)}")
