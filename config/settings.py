"""
Application configuration and settings.
"""
import os
import logging

# Application settings
APP_NAME = "Vedic Astrology Calculator"
APP_VERSION = "2.0"
APP_AUTHOR = "Your Name"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Create directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Logging configuration
LOG_LEVEL = logging.DEBUG
LOG_FILE = os.path.join(LOG_DIR, "vedic_astrology.log")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# UI Settings
THEME = "dark"
COLOR_THEME = "blue"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Astrology Settings
AYANAMSA_SYSTEM = "Lahiri"
CALCULATION_YEAR_OFFSET = 0

# Feature flags
ENABLE_PDF_EXPORT = True
ENABLE_IMAGE_EXPORT = True
ENABLE_SAVE_CHARTS = True


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
