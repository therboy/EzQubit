from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QSplitter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from gui.gate_info_data import GATE_INFO
import numpy as np

class GateInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the window background color (light gray)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f5f5f5"))
        self.setPalette(palette)

        # Main layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Create a splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Left side: Gate selection and controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Gate selection list
        self.gate_list = QListWidget()

        # Set style for the gate list to enhance readability (light background and blue text)
        self.gate_list.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                color: #2B5D81;
                font-size: 18px;
                padding: 5px;
                border: 1px solid #e0e0e0;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #6FA6D6;
                color: white;
            }
        """)

        for gate in GATE_INFO.keys():
            self.gate_list.addItem(gate)

        left_layout.addWidget(self.gate_list)

        # Add buttons for interaction
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")

        # Style buttons to make them more prominent
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #6FA6D6;
                color: white;
                font-size: 16px;
                padding: 8px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #50799B;
            }
        """)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #6FA6D6;
                color: white;
                font-size: 16px;
                padding: 8px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #50799B;
            }
        """)

        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        left_layout.addLayout(button_layout)

        splitter.addWidget(left_widget)

        # Right side: Web view for displaying gate information
        self.info_display = QWebEngineView()

        # Add right widget to splitter
        splitter.addWidget(self.info_display)

        # Set initial sizes for splitter sections
        splitter.setSizes([200, 600])

        # Connect the selection change to display_info
        self.gate_list.currentItemChanged.connect(self.display_info)
        self.prev_button.clicked.connect(self.show_previous_gate)
        self.next_button.clicked.connect(self.show_next_gate)

    def show_previous_gate(self):
        """Show the previous gate in the list."""
        current_row = self.gate_list.currentRow()
        if current_row > 0:
            self.gate_list.setCurrentRow(current_row - 1)

    def show_next_gate(self):
        """Show the next gate in the list."""
        current_row = self.gate_list.currentRow()
        if current_row < self.gate_list.count() - 1:
            self.gate_list.setCurrentRow(current_row + 1)

    def display_info(self, current, previous):
        """Display information about the selected gate."""
        if current:
            gate = current.text()
            info = GATE_INFO.get(gate, {})
            description = info.get('description', '')
            matrix_latex = info.get('matrix', '')
            examples = info.get('examples', [])

            # Enhanced HTML styling for display
            html = f"""
            <html>
            <head>
                <script type="text/javascript">
                    MathJax = {{
                        tex: {{
                            inlineMath: [['$', '$'], ['\\(', '\\)']],
                            displayMath: [['$$', '$$'], ['\\[', '\\]']]
                        }},
                        svg: {{fontCache: 'global'}}
                    }};
                </script>
                <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
                <style>
                    body {{
                        font-family: 'Segoe UI', Arial, sans-serif;
                        background-color: #FAFAFA;
                        color: #333333;
                        font-size: 18px;
                        line-height: 1.6;
                    }}
                    h2 {{
                        color: #2B5D81;
                        font-size: 28px;
                        border-bottom: 2px solid #2B5D81;
                        padding-bottom: 10px;
                    }}
                    h3 {{
                        color: #4682B4;
                        font-size: 24px;
                        margin-top: 20px;
                    }}
                    ol {{
                        font-size: 18px;
                        color: #444444;
                    }}
                    .matrix {{
                        background-color: #EDF5FA;
                        padding: 10px;
                        border-radius: 8px;
                        border: 1px solid #6FA6D6;
                    }}
                </style>
            </head>
            <body>
                <h2>{gate} Gate</h2>
                <p>{description}</p>
                <h3>Matrix Representation:</h3>
                <div class="matrix">$$ {matrix_latex} $$</div>
                <h3>Examples:</h3>
                <ol>
            """
            for ex in examples:
                html += f"<li>$$ {ex} $$</li>"
            html += """
                </ol>
            </body>
            </html>
            """
            self.info_display.setHtml(html)
