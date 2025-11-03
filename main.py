"""
Vedic Astrology Calculator - Main Entry Point
Refactored application with MVC architecture.
"""
import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.settings import setup_logging, APP_NAME, APP_VERSION
from views.main_window import MainWindow
from controllers.app_controller import AppController

logger = logging.getLogger(__name__)


def main():
    try:
        setup_logging()
        logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
        
        # First, create controller with `None` as the view
        controller = AppController(None)
        
        # Pass controller to MainWindow
        app = MainWindow(controller)
        
        # Link view and controller AFTER window is created
        controller.view = app
        
        logger.info("Application started successfully")
        app.mainloop()
        logger.info("Application closed")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"Fatal error: {str(e)}")
        sys.exit(1)



if __name__ == "__main__":
    main()
