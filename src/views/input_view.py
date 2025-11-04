"""
Modern Birth Data Input View - Fully CustomTkinter with ComboBoxes
Uses CustomTkinter ComboBoxes for all time fields (Hour, Minute, Second).
Professional, sleek dark-themed UI with improved contrast and refined layout.
"""

import customtkinter as ctk
from tkcalendar import DateEntry
from typing import Callable
import tkinter as tk
import tkinter.messagebox as messagebox
import logging
from datetime import datetime, timedelta

from utils.validators import Validators

logger = logging.getLogger(__name__)


class BirthDataInputView(ctk.CTkFrame):
    """Modern, sleek input form using all CustomTkinter controls."""

    def __init__(self, parent, on_submit: Callable, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_submit = on_submit
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create all UI widgets with modern styling and improved contrast."""

        # ============ TITLE SECTION ============
        self.title_label = ctk.CTkLabel(
            self,
            text="✨ Birth Chart Calculator",
            font=("Helvetica", 28, "bold"),
            text_color="#FFD700"
        )

        # ============ FORM CONTAINER ============
        self.form_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )

        # --- DATE SECTION ---
        self.date_section_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")

        self.date_label = ctk.CTkLabel(
            self.date_section_frame,
            text="📅 Date of Birth",
            font=("Helvetica", 14, "bold"),
            text_color="#FFD700"  # Better contrast - gold instead of white
        )

        # Modern DateEntry with custom colors
        self.date_entry = DateEntry(
            self.date_section_frame,
            width=35,
            background="#2B2B2B",      # Dark background
            foreground="#FFFFFF",       # Light text
            borderwidth=2,
            year=2003,                  # Changed default to 2003
            month=5,                    # May
            day=15,                     # 15th
            font=("Helvetica", 12),
            headersbackground="#1f1f1f",
            selectforeground="#FFD700",
            selectbackground="#2B2B2B"
        )

        # --- TIME SECTION ---
        self.time_section_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")

        self.time_label = ctk.CTkLabel(
            self.time_section_frame,
            text="⏰ Time of Birth",
            font=("Helvetica", 14, "bold"),
            text_color="#FFD700"  # Better contrast
        )

        # Modern time entry using ComboBoxes
        self.time_frame = ctk.CTkFrame(self.time_section_frame, fg_color="transparent")

        # Hour ComboBox (0-23)
        self.hour_label = ctk.CTkLabel(
            self.time_frame,
            text="Hour",
            font=("Helvetica", 11, "bold"),
            text_color="#E0E0E0"  # Brighter than #CCCCCC for better contrast
        )
        self.hour_combo = ctk.CTkComboBox(
            self.time_frame,
            values=[f"{i:02d}" for i in range(0, 24)],
            width=70,
            font=("Helvetica", 12),
            state="readonly",
            corner_radius=8,
            fg_color="#2B2B2B",
            button_color="#3A3A3A",  # Slightly brighter for contrast
            text_color="#FFFFFF"
        )
        self.hour_combo.set("17")  # Default: 17:55:00

        # Minute ComboBox (0-59)
        self.minute_label = ctk.CTkLabel(
            self.time_frame,
            text="Minute",
            font=("Helvetica", 11, "bold"),
            text_color="#E0E0E0"
        )
        self.minute_combo = ctk.CTkComboBox(
            self.time_frame,
            values=[f"{i:02d}" for i in range(0, 60)],
            width=70,
            font=("Helvetica", 12),
            state="readonly",
            corner_radius=8,
            fg_color="#2B2B2B",
            button_color="#3A3A3A",
            text_color="#FFFFFF"
        )
        self.minute_combo.set("55")  # Default: 17:55:00

        # Second ComboBox (0-59)
        self.second_label = ctk.CTkLabel(
            self.time_frame,
            text="Second",
            font=("Helvetica", 11, "bold"),
            text_color="#E0E0E0"
        )
        self.second_combo = ctk.CTkComboBox(
            self.time_frame,
            values=[f"{i:02d}" for i in range(0, 60)],
            width=70,
            font=("Helvetica", 12),
            state="readonly",
            corner_radius=8,
            fg_color="#2B2B2B",
            button_color="#3A3A3A",
            text_color="#FFFFFF"
        )
        self.second_combo.set("00")

        # --- TIMEZONE SECTION ---
        self.tz_section_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")

        self.timezone_label = ctk.CTkLabel(
            self.tz_section_frame,
            text="🌍 Timezone (±HH:MM)",
            font=("Helvetica", 14, "bold"),
            text_color="#FFD700"  # Better contrast
        )

        self.tz_frame = ctk.CTkFrame(self.tz_section_frame, fg_color="transparent")

        # Timezone ComboBox with common presets
        self.tz_combo = ctk.CTkComboBox(
            self.tz_frame,
            values=[
                "+05:30 (India)",
                "+05:45 (Nepal)",
                "+06:00 (Bangladesh)",
                "+07:00 (Thailand)",
                "-05:00 (EST)",
                "-08:00 (PST)",
                "+00:00 (GMT)",
                "+01:00 (CET)",
                "+05:00 (Pakistan)",
                "+09:00 (Japan)",
                "+10:00 (Sydney)",
                "Custom"
            ],
            width=280,
            font=("Helvetica", 12),
            state="readonly",
            corner_radius=8,
            fg_color="#2B2B2B",
            button_color="#3A3A3A",
            text_color="#FFFFFF",
            command=self._on_timezone_select
        )
        self.tz_combo.set("+05:30 (India)")  # Default: +05:30 (India)

        # Custom timezone entry (appears when "Custom" selected)
        self.custom_tz_entry = ctk.CTkEntry(
            self.tz_frame,
            placeholder_text="Enter timezone (e.g., +05:30)",
            width=280,
            height=38,
            font=("Helvetica", 12),
            corner_radius=8,
            border_width=2,
            fg_color="#2B2B2B",
            border_color="#3A3A3A",
            text_color="#FFFFFF",
            placeholder_text_color="#888888"
        )
        self.custom_tz_entry.grid(row=0, column=1, padx=10, sticky="ew")
        self.custom_tz_entry.grid_remove()  # Hidden by default

        # --- PLACE SECTION ---
        self.place_section_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")

        self.place_label = ctk.CTkLabel(
            self.place_section_frame,
            text="📍 Place of Birth",
            font=("Helvetica", 14, "bold"),
            text_color="#FFD700"  # Better contrast
        )

        self.place_entry = ctk.CTkEntry(
            self.place_section_frame,
            placeholder_text="e.g., Mumbai, India",
            width=400,
            height=40,
            font=("Helvetica", 12),
            corner_radius=10,
            border_width=2,
            fg_color="#2B2B2B",
            border_color="#3A3A3A",
            text_color="#FFFFFF",
            placeholder_text_color="#888888"
        )
        # Set default place
        self.place_entry.insert(0, "Thodupuzha")

        # ============ BUTTON SECTION ============
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.submit_button = ctk.CTkButton(
            self.button_frame,
            text="🔮 Calculate Birth Chart",
            command=self._handle_submit,
            height=50,
            font=("Helvetica", 14, "bold"),
            fg_color="#4CAF50",
            hover_color="#45a049",
            text_color="white",
            corner_radius=10
        )

        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear Form",
            command=self._clear_form,
            height=40,
            font=("Helvetica", 12),
            fg_color="#757575",
            hover_color="#616161",
            text_color="white",
            corner_radius=8
        )

        # ============ STATUS SECTION ============
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            text_color="gray",
            font=("Helvetica", 11)
        )

        self.progress_bar = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            height=4,
            corner_radius=2,
            fg_color="#1f1f1f",
            progress_color="#4CAF50"
        )

    def _layout_widgets(self):
        """Arrange all widgets with refined spacing and better positioning."""

        # Title
        self.title_label.pack(pady=20, padx=20)  # Reduced from 25

        # Form container
        self.form_frame.pack(fill="both", expand=True, padx=40, pady=10)  # Reduced from 15

        # --- Date Section Layout ---
        self.date_section_frame.pack(anchor="w", pady=(0, 20), fill="x")  # Reduced from 25
        self.date_label.pack(anchor="w", pady=(0, 8))  # Reduced from 10
        self.date_entry.pack(anchor="w", fill="x")

        # --- Time Section Layout ---
        self.time_section_frame.pack(anchor="w", pady=(0, 20), fill="x")  # Reduced from 25
        self.time_label.pack(anchor="w", pady=(0, 10))  # Reduced from 12
        
        self.time_frame.pack(anchor="w", fill="x")
        
        # Grid layout for time controls
        self.hour_label.grid(row=0, column=0, sticky="w", pady=(0, 4))  # Reduced from 5
        self.hour_combo.grid(row=1, column=0, sticky="ew", padx=(0, 15))  # Increased from 20

        self.minute_label.grid(row=0, column=1, sticky="w", pady=(0, 4))
        self.minute_combo.grid(row=1, column=1, sticky="ew", padx=(0, 15))

        self.second_label.grid(row=0, column=2, sticky="w", pady=(0, 4))
        self.second_combo.grid(row=1, column=2, sticky="ew")

        self.time_frame.grid_columnconfigure(0, weight=1)
        self.time_frame.grid_columnconfigure(1, weight=1)
        self.time_frame.grid_columnconfigure(2, weight=1)

        # --- Timezone Section Layout ---
        self.tz_section_frame.pack(anchor="w", pady=(0, 20), fill="x")  # Reduced from 25
        self.timezone_label.pack(anchor="w", pady=(0, 8))  # Reduced from 10
        
        self.tz_frame.pack(anchor="w", fill="x")
        self.tz_combo.grid(row=0, column=0, sticky="ew")
        self.tz_frame.grid_columnconfigure(0, weight=1)

        # --- Place Section Layout ---
        self.place_section_frame.pack(anchor="w", pady=(0, 25), fill="x")  # Reduced from 30
        self.place_label.pack(anchor="w", pady=(0, 8))  # Reduced from 10
        self.place_entry.pack(anchor="w", fill="x")

        # Button section (MOVED UP - closer to form)
        self.button_frame.pack(fill="x", padx=40, pady=(15, 10))  # Changed from (10, 15)
        self.submit_button.pack(fill="x", pady=10)  # Reduced from 12
        self.clear_button.pack(fill="x", pady=(0, 8))  # Reduced from (0, 10)

        # Status section
        self.status_label.pack(pady=8)  # Reduced from 10
        self.progress_bar.pack(fill="x", padx=40, pady=(0, 8))  # Reduced from (0, 10)

    def _on_timezone_select(self, choice):
        """Show/hide custom timezone entry based on selection."""
        if choice == "Custom":
            self.tz_combo.grid_remove()
            self.custom_tz_entry.grid()
            self.custom_tz_entry.focus()
        else:
            self.custom_tz_entry.grid_remove()
            self.tz_combo.grid()

    def _get_timezone(self) -> str:
        """Extract timezone value from combo or custom entry."""
        if self.custom_tz_entry.winfo_viewable():
            return self.custom_tz_entry.get().strip()
        else:
            selected = self.tz_combo.get()
            return selected.split()[0]  # Extract timezone part only

    def _validate_inputs(self) -> tuple:
        """Validate all form inputs before submission."""
        try:
            # Get and format date
            date_obj = self.date_entry.get_date()
            date_str = date_obj.strftime('%Y/%m/%d')

            # Get time from combo boxes
            hour = self.hour_combo.get()
            minute = self.minute_combo.get()
            second = self.second_combo.get()
            time_str = f"{hour}:{minute}:{second}"

            # Get timezone
            tz_str = self._get_timezone().strip()

            # Get place
            place_str = self.place_entry.get().strip()

            # Validate all inputs
            is_valid, error_msg = Validators.validate_all(
                date_str, time_str, tz_str, place_str
            )

            if not is_valid:
                return (False, error_msg, None)

            return (True, "", {
                'date': date_str,
                'time': time_str,
                'timezone': tz_str,
                'place': place_str
            })

        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return (False, f"Error parsing input: {str(e)}", None)

    def _handle_submit(self):
        """Handle form submission with real-time feedback."""
        is_valid, error_msg, data = self._validate_inputs()

        if not is_valid:
            messagebox.showerror("❌ Validation Error", error_msg)
            self.status_label.configure(
                text=f"✗ {error_msg}",
                text_color="red"
            )
            return

        # Start calculation
        self.status_label.configure(
            text="⏳ Calculating chart...",
            text_color="#FFD700"
        )
        self.submit_button.configure(state="disabled")
        self.progress_bar.start()

        try:
            # Call the submission handler
            self.on_submit(data)

            # Success feedback
            self.status_label.configure(
                text="✓ Chart calculated successfully! Switching to Chart view...",
                text_color="#00FF00"  # Brighter green for better contrast
            )
            logger.info(f"Chart calculated for {data['place']}")

        except Exception as e:
            # Error feedback
            error_text = str(e)
            self.status_label.configure(
                text=f"✗ Error: {error_text}",
                text_color="#FF6B6B"  # Brighter red for better contrast
            )
            messagebox.showerror("❌ Calculation Error", error_text)
            logger.error(f"Chart calculation error: {error_text}")

        finally:
            # Reset UI
            self.submit_button.configure(state="normal")
            self.progress_bar.stop()

    def _clear_form(self):
        """Clear all form fields to defaults."""
        # Reset date to 15/05/2003
        self.date_entry.set_date(datetime(2003, 5, 15).date())

        # Reset time to 17:55:00
        self.hour_combo.set("17")
        self.minute_combo.set("55")
        self.second_combo.set("00")

        # Reset timezone
        self.tz_combo.set("+05:30 (India)")
        self.custom_tz_entry.grid_remove()
        self.tz_combo.grid()

        # Reset place to Thodupuzha
        self.place_entry.delete(0, "end")
        self.place_entry.insert(0, "Thodupuzha")

        # Clear status
        self.status_label.configure(text="")

        logger.debug("Form cleared")

    def get_data(self) -> dict:
        """Get current form data."""
        is_valid, _, data = self._validate_inputs()
        return data if is_valid else {}

    def set_data(self, data: dict):
        """Pre-populate form with given data."""
        try:
            # Set date
            if 'date' in data:
                date_obj = datetime.strptime(data['date'], '%Y/%m/%d').date()
                self.date_entry.set_date(date_obj)

            # Set time
            if 'time' in data:
                time_obj = datetime.strptime(data['time'], '%H:%M:%S')
                self.hour_combo.set(f"{time_obj.hour:02d}")
                self.minute_combo.set(f"{time_obj.minute:02d}")
                self.second_combo.set(f"{time_obj.second:02d}")

            # Set timezone
            if 'timezone' in data:
                self.tz_combo.set("Custom")
                self.custom_tz_entry.grid()
                self.tz_combo.grid_remove()
                self.custom_tz_entry.delete(0, "end")
                self.custom_tz_entry.insert(0, data['timezone'])

            # Set place
            if 'place' in data:
                self.place_entry.delete(0, "end")
                self.place_entry.insert(0, data['place'])

            logger.debug("Form pre-populated with data")

        except Exception as e:
            logger.error(f"Error setting form data: {str(e)}")
