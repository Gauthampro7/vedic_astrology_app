"""
Birth data input view using CustomTkinter.
Modern, clean UI for data collection.
"""
import customtkinter as ctk
from typing import Callable, Optional
import tkinter.messagebox as messagebox
import logging

from utils.validators import Validators

logger = logging.getLogger(__name__)


class BirthDataInputView(ctk.CTkFrame):
    """Modern input form for birth data collection."""

    def __init__(self, parent, on_submit: Callable, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_submit = on_submit
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create all UI widgets."""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="Birth Chart Calculator",
            font=("Helvetica", 24, "bold"),
            text_color="#FFD700"
        )

        # Date input
        self.date_label = ctk.CTkLabel(self, text="Date of Birth (YYYY/MM/DD):")
        self.date_entry = ctk.CTkEntry(
            self,
            placeholder_text="2000/01/15",
            width=250,
            height=40,
            border_width=2
        )

        # Time input
        self.time_label = ctk.CTkLabel(self, text="Time of Birth (HH:MM:SS):")
        self.time_entry = ctk.CTkEntry(
            self,
            placeholder_text="14:30:00",
            width=250,
            height=40,
            border_width=2
        )

        # Timezone
        self.tz_label = ctk.CTkLabel(self, text="Timezone (±HH:MM):")
        self.tz_entry = ctk.CTkEntry(
            self,
            placeholder_text="+05:30",
            width=250,
            height=40,
            border_width=2
        )

        # Location
        self.place_label = ctk.CTkLabel(self, text="Place of Birth:")
        self.place_entry = ctk.CTkEntry(
            self,
            placeholder_text="Mumbai, India",
            width=400,
            height=40,
            border_width=2
        )

        # Submit button
        self.submit_button = ctk.CTkButton(
            self,
            text="Calculate Birth Chart",
            command=self._handle_submit,
            height=45,
            font=("Helvetica", 14, "bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )

        # Clear button
        self.clear_button = ctk.CTkButton(
            self,
            text="Clear",
            command=self._clear_form,
            height=45,
            font=("Helvetica", 12),
            fg_color="#757575",
            hover_color="#616161"
        )

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            text_color="gray",
            font=("Helvetica", 11)
        )

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            height=5
        )

    def _layout_widgets(self):
        """Arrange widgets using grid layout."""
        self.title_label.grid(
            row=0, column=0, columnspan=2,
            pady=20, padx=20, sticky="ew"
        )

        self.date_label.grid(
            row=1, column=0, pady=15, padx=20, sticky="e"
        )
        self.date_entry.grid(
            row=1, column=1, pady=15, padx=20, sticky="ew"
        )

        self.time_label.grid(
            row=2, column=0, pady=15, padx=20, sticky="e"
        )
        self.time_entry.grid(
            row=2, column=1, pady=15, padx=20, sticky="ew"
        )

        self.tz_label.grid(
            row=3, column=0, pady=15, padx=20, sticky="e"
        )
        self.tz_entry.grid(
            row=3, column=1, pady=15, padx=20, sticky="ew"
        )

        self.place_label.grid(
            row=4, column=0, pady=15, padx=20, sticky="e"
        )
        self.place_entry.grid(
            row=4, column=1, pady=15, padx=20, sticky="ew"
        )

        self.submit_button.grid(
            row=5, column=0, columnspan=2,
            pady=20, padx=20, sticky="ew"
        )

        self.clear_button.grid(
            row=6, column=0, columnspan=2,
            pady=10, padx=20, sticky="ew"
        )

        self.status_label.grid(
            row=7, column=0, columnspan=2,
            pady=10, padx=20, sticky="ew"
        )

        self.progress_bar.grid(
            row=8, column=0, columnspan=2,
            pady=5, padx=20, sticky="ew"
        )

        self.grid_columnconfigure(1, weight=1)

    def _validate_inputs(self) -> tuple:
        """Validate all user inputs."""
        date_str = self.date_entry.get().strip()
        time_str = self.time_entry.get().strip()
        tz_str = self.tz_entry.get().strip()
        place_str = self.place_entry.get().strip()

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

        self.status_label.configure(text="Calculating...", text_color="yellow")
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
        self.date_entry.delete(0, 'end')
        self.time_entry.delete(0, 'end')
        self.tz_entry.delete(0, 'end')
        self.place_entry.delete(0, 'end')
        self.status_label.configure(text="")
        logger.debug("Form cleared")

    def get_data(self) -> dict:
        """Get current form data."""
        return {
            'date': self.date_entry.get().strip(),
            'time': self.time_entry.get().strip(),
            'timezone': self.tz_entry.get().strip(),
            'place': self.place_entry.get().strip()
        }
