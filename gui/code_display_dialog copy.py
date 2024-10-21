"""
Defines the CodeDisplayDialog class, which displays the generated Qiskit code.
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QApplication, QHBoxLayout
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
        self.setLayout(layout)

        # Text edit to display the code
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.code)
        self.text_edit.setReadOnly(True)
        font = QFont("Courier", 10)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Copy to Clipboard Button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_code)
        button_layout.addWidget(self.copy_button)

        # Save to File Button
        self.save_button = QPushButton("Save to File")
        self.save_button.clicked.connect(self.save_code)
        button_layout.addWidget(self.save_button)

        # Close Button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

    def copy_code(self):
        """
        Copies the code to the clipboard.
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code)

    def save_code(self):
        """
        Saves the code to a file.
        """
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Qiskit Code", "",
            "Python Files (*.py);;All Files (*)", options=options
        )
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write(self.code)
                QMessageBox.information(self, "Saved", f"Code saved to {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save code:\n{e}")
