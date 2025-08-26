#!/usr/bin/env python3
"""
Media Copyer GUI - Refactored modular version
Main entry point that imports from the new modular GUI structure
"""

from gui import MediaCopyerApp
from gui.main_window import create_app

def main():
    """Main function to run the GUI application"""
    root, app = create_app()
    root.mainloop()

if __name__ == "__main__":
    main()
