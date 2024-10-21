# main.py

"""
Main entry point for the Qiskit GUI Application.

This script initializes the application and displays the main window.
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """
    Initializes the QApplication and displays the main window.
    """
    # Create the application instance
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Execute the application's main loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
