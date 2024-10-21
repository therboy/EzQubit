# gui/code_display_dialog.py

"""
Defines the CodeDisplayDialog class, which displays the generated Qiskit code.
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QApplication
from PyQt5.QtGui import QFont

class CodeDisplayDialog(QDialog):
    """
    A dialog to display and copy the generated Qiskit code.
    """

    def __init__(self, code, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generated Qiskit Code")
        self.resize(800, 600)
        self.code = code
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components.
        """
        layout = QVBoxLayout()

        # Text edit to display the code
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.code)
        self.text_edit.setReadOnly(True)
        font = QFont("Courier", 10)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)

        # Copy to Clipboard Button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_code)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)

    def copy_code(self):
        """
        Copies the code to the clipboard.
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code)
