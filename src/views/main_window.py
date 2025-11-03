"""
Main application window with tabbed interface.
"""
import customtkinter as ctk
import logging

from views.input_view import BirthDataInputView
from views.chart_view import ChartDisplayView

logger = logging.getLogger(__name__)


class MainWindow(ctk.CTk):
    """Main application window with tabbed interface."""

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.title("Vedic Astrology Calculator")
        self.geometry("1000x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._create_menu()

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.input_tab = self.tabview.add("Input")
        self.chart_tab = self.tabview.add("Chart")
        self.about_tab = self.tabview.add("About")

        self.input_view = BirthDataInputView(
            self.input_tab,
            on_submit=self.controller.handle_calculate
        )
        self.input_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.chart_view = ChartDisplayView(self.chart_tab)
        self.chart_view.pack(fill="both", expand=True, padx=10, pady=10)

        self._create_about_view()

        logger.info("Application window created")

    def _create_menu(self):
        """Create application menu."""
        menubar = ctk.CTkFrame(self, height=30, fg_color="#212121")
        menubar.pack(side="top", fill="x")

        file_btn = ctk.CTkButton(
            menubar,
            text="File",
            width=60,
            height=30,
            fg_color="#212121",
            text_color="white"
        )
        file_btn.pack(side="left", padx=5, pady=2)

        help_btn = ctk.CTkButton(
            menubar,
            text="Help",
            width=60,
            height=30,
            command=lambda: self._show_help(),
            fg_color="#212121",
            text_color="white"
        )
        help_btn.pack(side="left", padx=5, pady=2)

    def _show_help(self):
        """Show help information."""
        import tkinter.messagebox as messagebox
        messagebox.showinfo(
            "Help",
            "Vedic Astrology Calculator\n\n"
            "Instructions:\n"
            "1. Enter your birth date (YYYY/MM/DD)\n"
            "2. Enter your birth time (HH:MM:SS)\n"
            "3. Enter your timezone (±HH:MM)\n"
            "4. Enter your birth place\n"
            "5. Click Calculate\n\n"
            "The application will calculate your birth chart\n"
            "using Vedic (Sidereal) Astrology with Lahiri Ayanamsa."
        )

    def _create_about_view(self):
        """Create about tab content."""
        about_frame = ctk.CTkFrame(self.about_tab)
        about_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            about_frame,
            text="Vedic Astrology Calculator",
            font=("Helvetica", 24, "bold"),
            text_color="#FFD700"
        )
        title.pack(pady=20)

        version = ctk.CTkLabel(
            about_frame,
            text="Version 2.0 (Refactored)",
            font=("Helvetica", 12),
            text_color="gray"
        )
        version.pack()

        description = ctk.CTkLabel(
            about_frame,
            text="""A modern application for calculating birth charts
based on Vedic Astrology principles.

Uses Lahiri Ayanamsa for sidereal calculations.
Powered by flatlib for astronomical calculations.""",
            font=("Helvetica", 11),
            justify="left"
        )
        description.pack(pady=20, padx=20, fill="both", expand=True)

    def display_chart(self, chart_data):
        """Display chart data."""
        self.chart_view.display_chart(chart_data)
        self.tabview.set("Chart")

    def show_error(self, error_msg: str):
        """Show error message."""
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", error_msg)
