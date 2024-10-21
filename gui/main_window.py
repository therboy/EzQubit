# gui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QMessageBox, QTabWidget, QWidget, QVBoxLayout,
    QLabel
)
from PyQt5.QtCore import Qt
from gui.circuit_builder import CircuitBuilder
from gui.gate_info_tab import GateInfoTab
from gui.latex_renderer import render_latex_to_pixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
from utils.qiskit_helpers import get_full_unitary, get_state_vector, matrix_to_latex, statevector_to_latex
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qiskit GUI Builder")
        self.setGeometry(100, 100, 1400, 900)
        self.initUI()

    def initUI(self):
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

        # Gate Information Tab
        self.gate_info_tab = GateInfoTab()
        self.tabs.addTab(self.gate_info_tab, "Gate Information")

        # Connect signals
        self.circuit_builder.circuit_updated.connect(self.update_math_display)

        # Set the status bar
        self.statusBar().showMessage("Ready")

    def create_menu_bar(self):
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
        # Web view for Unitary Matrix
        self.unitary_view = QWebEngineView()
        self.math_layout.addWidget(QLabel("<h3>Unitary Matrix of the Circuit:</h3>"))
        self.math_layout.addWidget(self.unitary_view)

        # Web view for State Vector
        self.state_vector_view = QWebEngineView()
        self.math_layout.addWidget(QLabel("<h3>State Vector:</h3>"))
        self.math_layout.addWidget(self.state_vector_view)

    def update_math_display(self):
        # Fetch unitary matrix
        unitary = get_full_unitary(self.circuit_builder.circuit)
        if unitary is not None:
            unitary_latex = matrix_to_latex(unitary)
            unitary_html = f"""
            <html>
            <head>
                <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
                <script id="MathJax-script" async
                    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
                </script>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        padding: 20px;
                    }}
                    pre {{
                        background-color: #f0f0f0;
                        padding: 10px;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                $$ {unitary_latex} $$
            </body>
            </html>
            """
            self.unitary_view.setHtml(unitary_html)
        else:
            self.unitary_view.setHtml("<p>Unitary matrix not available for the current circuit.</p>")

        # Fetch state vector
        state_vector = get_state_vector(self.circuit_builder.circuit)
        if state_vector is not None:
            state_vector_latex = statevector_to_latex(state_vector)
            state_vector_html = f"""
            <html>
            <head>
                <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
                <script id="MathJax-script" async
                    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
                </script>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        padding: 20px;
                    }}
                    pre {{
                        background-color: #f0f0f0;
                        padding: 10px;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                $$ {state_vector_latex} $$
            </body>
            </html>
            """
            self.state_vector_view.setHtml(state_vector_html)
        else:
            self.state_vector_view.setHtml("<p>State vector not available for the current circuit.</p>")

    def export_latex(self):
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
                    f.write(f"\\[\n{self.circuit_builder.get_unitary_latex()}\n\\]\n\n")
                    f.write("## State Vector\n\n")
                    f.write(f"\\[\n{self.circuit_builder.get_statevector_latex()}\n\\]\n")
                    f.write("\n\\end{document}")
                QMessageBox.information(self, "Export Successful", f"LaTeX file saved to {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export LaTeX file:\n{e}")

    def new_circuit(self):
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
        QMessageBox.information(
            self, "About",
            "Qiskit GUI Builder\nVersion 2.0\nDeveloped with PyQt5 and Qiskit\n\n" +
            "This application allows users to build quantum circuits visually, " +
            "generate corresponding Qiskit code, and explore the underlying quantum mathematics."
        )

    def closeEvent(self, event):
        response = QMessageBox.question(
            self, 'Confirm Exit',
            'Are you sure you want to exit? Unsaved changes will be lost.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if response == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
