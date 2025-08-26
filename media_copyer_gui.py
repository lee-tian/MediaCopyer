#!/usr/bin/env python3
"""
Media Copyer GUI - Refactored modular version with i18n support
Main entry point that imports from the new modular GUI structure
"""

from gui import MediaCopyerApp
from gui.main_window import create_app
from gui.i18n import i18n

def main():
    """Main function to run the GUI application"""
    # Create and run the application
    root, app = create_app()
    root.mainloop()

if __name__ == "__main__":
    main()
