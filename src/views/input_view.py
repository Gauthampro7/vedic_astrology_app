"""
Improved birth data input view using CustomTkinter with professional date/time pickers.
Modern, clean UI for data collection with real date and time selection widgets.
"""
import customtkinter as ctk
from tkcalendar import DateEntry
from typing import Callable, Optional
import tkinter.messagebox as messagebox
import logging
from datetime import datetime, timedelta

from utils.validators import Validators

logger = logging.getLogger(__name__)


class BirthDataInputView(ctk.CTkFrame):
    """Professional input form for birth data collection."""

    def __init__(self, parent, on_submit: Callable, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_submit = on_submit
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create all UI widgets with proper organization."""
        
        # ============ TITLE SECTION ============
        self.title_label = ctk.CTkLabel(
            self,
            text="Birth Chart Calculator",
            font=("Helvetica", 28, "bold"),
            text_color="#FFD700"
        )

        # ============ FORM SECTION ============
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")

        # --- Date Section ---
        self.date_label = ctk.CTkLabel(
            self.form_frame,
            text="📅 Date of Birth",
            font=("Helvetica", 13, "bold"),
            text_color="#FFFFFF"
        )

        # Using tkcalendar DateEntry for professional date selection
        self.date_entry = DateEntry(
            self.form_frame,
            width=30,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=datetime.now().year - 30,
            month=1,
            day=15,
            font=("Helvetica", 11)
        )

        # --- Time Section (Hour) ---
        self.time_label = ctk.CTkLabel(
            self.form_frame,
            text="⏰ Time of Birth",
            font=("Helvetica", 13, "bold"),
            text_color="#FFFFFF"
        )

        # Time selection using spinboxes (Hours, Minutes, Seconds)
        self.time_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")

        # Hour
        self.hour_label = ctk.CTkLabel(
            self.time_frame,
            text="Hour:",
            font=("Helvetica", 11),
            text_color="#CCCCCC"
        )
        self.hour_spinbox = ctk.CTkSpinbox(
            self.time_frame,
            from_=0,
            to=23,
            width=70,
            font=("Helvetica", 12),
            command=self._validate_time
        )
        self.hour_spinbox.set(12)

        # Minute
        self.minute_label = ctk.CTkLabel(
            self.time_frame,
            text="Minute:",
            font=("Helvetica", 11),
            text_color="#CCCCCC"
        )
        self.minute_spinbox = ctk.CTkSpinbox(
            self.time_frame,
            from_=0,
            to=59,
            width=70,
            font=("Helvetica", 12),
            command=self._validate_time
        )
        self.minute_spinbox.set(0)

        # Second
        self.second_label = ctk.CTkLabel(
            self.time_frame,
            text="Second:",
            font=("Helvetica", 11),
            text_color="#CCCCCC"
        )
        self.second_spinbox = ctk.CTkSpinbox(
            self.time_frame,
            from_=0,
            to=59,
            width=70,
            font=("Helvetica", 12),
            command=self._validate_time
        )
        self.second_spinbox.set(0)

        # --- Timezone Section ---
        self.timezone_label = ctk.CTkLabel(
            self.form_frame,
            text="🌍 Timezone (±HH:MM)",
            font=("Helvetica", 13, "bold"),
            text_color="#FFFFFF"
        )

        # Timezone with helpful presets
        self.tz_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")

        # Dropdown for common timezones
        self.tz_dropdown = ctk.CTkComboBox(
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
                "Custom"
            ],
            width=200,
            font=("Helvetica", 11),
            command=self._on_timezone_select
        )
        self.tz_dropdown.set("+05:30 (India)")

        # Custom timezone entry (hidden by default)
        self.custom_tz_entry = ctk.CTkEntry(
            self.tz_frame,
            placeholder_text="+05:30",
            width=120,
            height=35,
            font=("Helvetica", 11),
            border_width=1
        )
        self.custom_tz_entry.grid(row=0, column=1, padx=10, sticky="ew")
        self.custom_tz_entry.grid_remove()  # Hidden by default

        # --- Place Section ---
        self.place_label = ctk.CTkLabel(
            self.form_frame,
            text="📍 Place of Birth",
            font=("Helvetica", 13, "bold"),
            text_color="#FFFFFF"
        )

        self.place_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="e.g., Mumbai, India",
            width=400,
            height=40,
            border_width=2,
            font=("Helvetica", 12)
        )

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
            text_color="white"
        )

        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear Form",
            command=self._clear_form,
            height=40,
            font=("Helvetica", 12),
            fg_color="#757575",
            hover_color="#616161",
            text_color="white"
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
            height=4
        )

    def _layout_widgets(self):
        """Arrange widgets using grid layout."""
        # Title
        self.title_label.pack(pady=25, padx=20)

        # Form Frame
        self.form_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # --- Date Section ---
        self.date_label.pack(anchor="w", pady=(20, 8))
        self.date_entry.pack(anchor="w", pady=(0, 15), fill="x")

        # --- Time Section ---
        self.time_label.pack(anchor="w", pady=(10, 8))
        self.time_frame.pack(anchor="w", pady=(0, 15), fill="x")

        self.hour_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.hour_spinbox.grid(row=0, column=1, sticky="w", padx=(0, 30))

        self.minute_label.grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.minute_spinbox.grid(row=0, column=3, sticky="w", padx=(0, 30))

        self.second_label.grid(row=0, column=4, sticky="w", padx=(0, 10))
        self.second_spinbox.grid(row=0, column=5, sticky="w")

        # --- Timezone Section ---
        self.timezone_label.pack(anchor="w", pady=(10, 8))
        self.tz_frame.pack(anchor="w", pady=(0, 15), fill="x")

        self.tz_dropdown.grid(row=0, column=0, sticky="ew")
        self.tz_frame.grid_columnconfigure(0, weight=1)

        # --- Place Section ---
        self.place_label.pack(anchor="w", pady=(10, 8))
        self.place_entry.pack(anchor="w", pady=(0, 25), fill="x")

        # Button Frame
        self.button_frame.pack(fill="x", padx=30, pady=10)

        self.submit_button.pack(fill="x", pady=10)
        self.clear_button.pack(fill="x", pady=5)

        # Status
        self.status_label.pack(pady=10)
        self.progress_bar.pack(fill="x", padx=30)

    def _validate_time(self):
        """Validate time spinbox values."""
        try:
            hour = int(self.hour_spinbox.get())
            minute = int(self.minute_spinbox.get())
            second = int(self.second_spinbox.get())

            # Clamp values
            self.hour_spinbox.set(max(0, min(23, hour)))
            self.minute_spinbox.set(max(0, min(59, minute)))
            self.second_spinbox.set(max(0, min(59, second)))
        except ValueError:
            pass

    def _on_timezone_select(self, choice):
        """Handle timezone dropdown selection."""
        if choice == "Custom":
            self.custom_tz_entry.grid()
        else:
            self.custom_tz_entry.grid_remove()

    def _get_timezone(self) -> str:
        """Get timezone value from dropdown or custom entry."""
        selected = self.tz_dropdown.get()
        if selected == "Custom":
            return self.custom_tz_entry.get().strip()
        else:
            # Extract timezone part (before the space and description)
            return selected.split()[0]

    def _validate_inputs(self) -> tuple:
        """Validate all user inputs."""
        try:
            # Get date
            date_obj = self.date_entry.get_date()
            date_str = date_obj.strftime('%Y/%m/%d')

            # Get time
            hour = int(self.hour_spinbox.get())
            minute = int(self.minute_spinbox.get())
            second = int(self.second_spinbox.get())
            time_str = f"{hour:02d}:{minute:02d}:{second:02d}"

            # Get timezone
            tz_str = self._get_timezone().strip()

            # Get place
            place_str = self.place_entry.get().strip()

            # Validate all
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
        """Handle form submission with feedback."""
        is_valid, error_msg, data = self._validate_inputs()

        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            self.status_label.configure(
                text=f"✗ {error_msg}",
                text_color="red"
            )
            return

        self.status_label.configure(text="⏳ Calculating chart...", text_color="orange")
        self.submit_button.configure(state="disabled")
        self.progress_bar.start()

        try:
            self.on_submit(data)
            self.status_label.configure(
                text="✓ Chart calculated successfully!",
                text_color="green"
            )
            logger.info(f"Chart calculated for {data['place']}")

        except Exception as e:
            error_text = str(e)
            self.status_label.configure(
                text=f"✗ Error: {error_text}",
                text_color="red"
            )
            messagebox.showerror("Calculation Error", error_text)
            logger.error(f"Chart calculation error: {error_text}")

        finally:
            self.submit_button.configure(state="normal")
            self.progress_bar.stop()

    def _clear_form(self):
        """Clear all form fields."""
        self.date_entry.set_date(datetime.now() - timedelta(days=365*30))
        self.hour_spinbox.set(12)
        self.minute_spinbox.set(0)
        self.second_spinbox.set(0)
        self.tz_dropdown.set("+05:30 (India)")
        self.custom_tz_entry.grid_remove()
        self.place_entry.delete(0, 'end')
        self.status_label.configure(text="")
        logger.debug("Form cleared")

    def get_data(self) -> dict:
        """Get current form data."""
        is_valid, _, data = self._validate_inputs()
        return data if is_valid else {}

    def set_data(self, data: dict):
        """Populate form with data."""
        if 'date' in data:
            date_obj = datetime.strptime(data['date'], '%Y/%m/%d').date()
            self.date_entry.set_date(date_obj)

        if 'time' in data:
            time_obj = datetime.strptime(data['time'], '%H:%M:%S')
            self.hour_spinbox.set(time_obj.hour)
            self.minute_spinbox.set(time_obj.minute)
            self.second_spinbox.set(time_obj.second)

        if 'timezone' in data:
            self.tz_dropdown.set("Custom")
            self.custom_tz_entry.grid()
            self.custom_tz_entry.delete(0, 'end')
            self.custom_tz_entry.insert(0, data['timezone'])

        if 'place' in data:
            self.place_entry.delete(0, 'end')
            self.place_entry.insert(0, data['place'])
