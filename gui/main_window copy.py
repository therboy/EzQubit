"""
Defines the MainWindow class, which is the primary window of the application.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QMessageBox, QApplication,
    QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from gui.circuit_builder import CircuitBuilder
import sys

class MainWindow(QMainWindow):
    """
    The main window of the Qiskit GUI Application.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qiskit GUI Builder")
        self.setGeometry(100, 100, 1400, 900)
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components.
        """
        # Create the menu bar
        self.create_menu_bar()

        # Create the central widget with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Circuit Builder Tab
        self.circuit_builder = CircuitBuilder()
        self.tabs.addTab(self.circuit_builder, "Circuit Builder")

        # Mathematical Representation Tab
        self.math_display = QWidget()
        self.math_layout = QVBoxLayout()
        self.math_display.setLayout(self.math_layout)
        self.tabs.addTab(self.math_display, "Mathematical Representation")

        # Add widgets to Mathematical Representation Tab
        self.add_math_widgets()

        # Connect signals
        self.circuit_builder.circuit_updated.connect(self.update_math_display)

        # Set the status bar
        self.statusBar().showMessage("Ready")

    def create_menu_bar(self):
        """
        Creates the menu bar with File and Help menus.
        """
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        # New action
        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Create a new circuit')
        new_action.triggered.connect(self.new_circuit)
        file_menu.addAction(new_action)

        # Open action
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open an existing circuit')
        open_action.triggered.connect(self.open_circuit)
        file_menu.addAction(open_action)

        # Save action
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save the current circuit')
        save_action.triggered.connect(self.save_circuit)
        file_menu.addAction(save_action)

        # Export LaTeX action
        export_latex_action = QAction('Export LaTeX', self)
        export_latex_action.setStatusTip('Export mathematical representations to LaTeX')
        export_latex_action.triggered.connect(self.export_latex)
        file_menu.addAction(export_latex_action)

        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu('Help')

        # About action
        about_action = QAction('About', self)
        about_action.setStatusTip('About the application')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def add_math_widgets(self):
        """
        Adds widgets to display mathematical representations.
        """
        # Label for Unitary Matrix
        self.unitary_label = QLabel("Unitary Matrix of the Circuit:")
        self.math_layout.addWidget(self.unitary_label)

        # Text edit for Unitary Matrix LaTeX
        self.unitary_text = QTextEdit()
        self.unitary_text.setReadOnly(True)
        self.unitary_text.setStyleSheet("background-color: #f0f0f0;")
        self.math_layout.addWidget(self.unitary_text)

        # Label for State Vector
        self.state_vector_label = QLabel("State Vector:")
        self.math_layout.addWidget(self.state_vector_label)

        # Text edit for State Vector LaTeX
        self.state_vector_text = QTextEdit()
        self.state_vector_text.setReadOnly(True)
        self.state_vector_text.setStyleSheet("background-color: #f0f0f0;")
        self.math_layout.addWidget(self.state_vector_text)

    def update_math_display(self):
        """
        Updates the mathematical representations based on the current circuit.
        """
        # Fetch unitary matrix
        unitary = self.circuit_builder.get_unitary_matrix()
        if unitary is not None:
            unitary_latex = self.format_matrix_to_latex(unitary)
            self.unitary_text.setPlainText(unitary_latex)
        else:
            self.unitary_text.setPlainText("Unitary matrix not available for the current circuit.")

        # Fetch state vector
        state_vector = self.circuit_builder.get_state_vector()
        if state_vector is not None:
            state_vector_latex = self.format_state_vector_to_latex(state_vector)
            self.state_vector_text.setPlainText(state_vector_latex)
        else:
            self.state_vector_text.setPlainText("State vector not available for the current circuit.")

    def format_matrix_to_latex(self, matrix):
        """
        Formats a numpy matrix into LaTeX string.

        Args:
            matrix (numpy.ndarray): The matrix to format.

        Returns:
            str: LaTeX-formatted matrix.
        """
        latex_str = "\\begin{pmatrix}\n"
        for row in matrix:
            row_str = " & ".join([f"{elem:.2f}" for elem in row])
            latex_str += f"{row_str} \\\\\n"
        latex_str += "\\end{pmatrix}"
        return latex_str

    def format_state_vector_to_latex(self, state_vector):
        """
        Formats a state vector into LaTeX string.

        Args:
            state_vector (numpy.ndarray): The state vector to format.

        Returns:
            str: LaTeX-formatted state vector.
        """
        latex_str = "\\begin{bmatrix}\n"
        for elem in state_vector:
            latex_str += f"{elem:.2f} \\\\\n"
        latex_str += "\\end{bmatrix}"
        return latex_str

    def export_latex(self):
        """
        Exports the mathematical representations to a LaTeX file.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Export LaTeX", "",
            "LaTeX Files (*.tex);;All Files (*)", options=options
        )
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write("\\documentclass{article}\n")
                    f.write("\\usepackage{amsmath}\n")
                    f.write("\\begin{document}\n\n")
                    f.write("## Unitary Matrix of the Circuit\n\n")
                    f.write(f"\\[\n{self.unitary_text.toPlainText()}\n\\]\n\n")
                    f.write("## State Vector\n\n")
                    f.write(f"\\[\n{self.state_vector_text.toPlainText()}\n\\]\n")
                    f.write("\n\\end{document}")
                QMessageBox.information(self, "Export Successful", f"LaTeX file saved to {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export LaTeX file:\n{e}")

    def new_circuit(self):
        """
        Clears the current circuit to start a new one.
        """
        response = QMessageBox.question(
            self, 'Confirm New Circuit',
            'Are you sure you want to create a new circuit? Unsaved changes will be lost.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if response == QMessageBox.Yes:
            self.circuit_builder.clear_circuit()
            self.update_math_display()
            self.statusBar().showMessage("New circuit created")

    def open_circuit(self):
        """
        Opens a saved circuit from a file.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Circuit", "",
            "QASM Files (*.qasm);;All Files (*)", options=options
        )
        if file_name:
            success = self.circuit_builder.load_circuit(file_name)
            if success:
                self.update_math_display()
                self.statusBar().showMessage(f"Circuit loaded from {file_name}")
            else:
                QMessageBox.critical(
                    self, "Error", f"Failed to load circuit from {file_name}"
                )

    def save_circuit(self):
        """
        Saves the current circuit to a file.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Circuit", "",
            "QASM Files (*.qasm);;All Files (*)", options=options
        )
        if file_name:
            success = self.circuit_builder.save_circuit(file_name)
            if success:
                self.statusBar().showMessage(f"Circuit saved to {file_name}")
            else:
                QMessageBox.critical(
                    self, "Error", f"Failed to save circuit to {file_name}"
                )

    def show_about(self):
        """
        Displays an About dialog with application information.
        """
        QMessageBox.information(
            self, "About",
            "Qiskit GUI Builder\nVersion 2.0\nDeveloped with PyQt5 and Qiskit\n\n" +
            "This application allows users to build quantum circuits visually, " +
            "generate corresponding Qiskit code, and explore the underlying quantum mathematics."
        )

    def closeEvent(self, event):
        """
        Overrides the close event to confirm exit.
        """
        response = QMessageBox.question(
            self, 'Confirm Exit',
            'Are you sure you want to exit? Unsaved changes will be lost.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if response == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
