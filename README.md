# Vedic Astrology Calculator

A modern, production-ready application for calculating birth charts based on Vedic Astrology principles.

## Features

✅ **Accurate Calculations**: Uses flatlib for astronomical calculations with Lahiri Ayanamsa
✅ **Modern UI**: Built with CustomTkinter for a sleek, professional interface
✅ **Data Validation**: Comprehensive input validation with helpful error messages
✅ **Clean Architecture**: MVC pattern with clear separation of concerns
✅ **Extensible**: Easy to add new features

## Quick Start

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Enter your birth date (YYYY/MM/DD format)
2. Enter your birth time (HH:MM:SS format, 24-hour)
3. Enter your timezone (±HH:MM format, e.g., +05:30 for India)
4. Enter your birth place (city/town name)
5. Click "Calculate Birth Chart"
6. View your planetary positions in the Chart tab

## Architecture

- **Models**: Data structures with validation
- **Services**: Business logic (calculations, geocoding)
- **Views**: User interface components
- **Controllers**: Coordinates between Model and View
- **Utils**: Validation and formatting utilities

## License

MIT License - See LICENSE file for details.
