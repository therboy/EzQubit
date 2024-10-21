# gui/circuit_builder.py

"""
Defines the CircuitBuilder class, which provides the interface for building quantum circuits.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QInputDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QSplitter, QTextEdit, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.compiler import transpile
from qiskit.visualization import plot_histogram
from gui.code_generator import CodeGenerator
from gui.code_display_dialog import CodeDisplayDialog
from utils.qiskit_helpers import visualize_circuit, get_gate_matrix
import matplotlib.pyplot as plt
import os
import numpy as np
import sympy as sp
from qiskit.quantum_info import Operator, Statevector

class CircuitBuilder(QWidget):
    """
    Provides an interface for building and visualizing quantum circuits, along with their mathematical representations.
    """

    # Signal emitted when the circuit is updated
    circuit_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_circuit()
        self.history = []
        self.redo_stack = []

    def initUI(self):
        """
        Initializes the user interface components.
        """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Splitter to divide controls and visualization
        splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(splitter)

        # Left panel: Controls and Gates
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)

        # Gate selection list
        self.gate_list = QListWidget()
        gates = [
            'H', 'X', 'Y', 'Z', 'S', 'T', 'RX', 'RY', 'RZ',
            'CX', 'CY', 'CZ', 'Swap', 'CCX', 'Measure'
        ]
        for gate in gates:
            item = QListWidgetItem(gate)
            self.gate_list.addItem(item)
        left_layout.addWidget(QLabel("Available Gates:"))
        left_layout.addWidget(self.gate_list)

        # Add Qubit Button
        self.add_qubit_btn = QPushButton("Add Qubit")
        self.add_qubit_btn.clicked.connect(self.add_qubit)
        left_layout.addWidget(self.add_qubit_btn)

        # Add Gate Button
        self.add_gate_btn = QPushButton("Add Gate")
        self.add_gate_btn.clicked.connect(self.add_gate)
        left_layout.addWidget(self.add_gate_btn)

        # Undo Button
        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo_action)
        left_layout.addWidget(self.undo_btn)

        # Redo Button
        self.redo_btn = QPushButton("Redo")
        self.redo_btn.clicked.connect(self.redo_action)
        left_layout.addWidget(self.redo_btn)

        # Generate Code Button
        self.generate_code_btn = QPushButton("Generate Qiskit Code")
        self.generate_code_btn.clicked.connect(self.generate_code)
        left_layout.addWidget(self.generate_code_btn)

        # Run Simulation Button
        self.run_simulation_btn = QPushButton("Run Simulation")
        self.run_simulation_btn.clicked.connect(self.run_simulation)
        left_layout.addWidget(self.run_simulation_btn)

        # Right panel: Visualization and Mathematics
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)

        # Circuit Visualization
        self.visual_label = QLabel("Quantum Circuit Visualization:")
        self.visual_label.setFont(QFont("Arial", 14))
        right_layout.addWidget(self.visual_label)

        # Graphics View for circuit diagram
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setMinimumSize(600, 400)
        right_layout.addWidget(self.graphics_view)

        # Mathematics Display
        self.math_label = QLabel("Mathematical Representation:")
        self.math_label.setFont(QFont("Arial", 14))
        right_layout.addWidget(self.math_label)

        # Text Edit for mathematical equations
        self.math_text = QTextEdit()
        self.math_text.setReadOnly(True)
        self.math_text.setFont(QFont("Courier", 12))
        self.math_text.setMinimumHeight(200)
        right_layout.addWidget(self.math_text)

        # Simulation Results
        self.sim_results_label = QLabel("Simulation Results:")
        self.sim_results_label.setFont(QFont("Arial", 14))
        right_layout.addWidget(self.sim_results_label)

        # QLabel to display simulation histogram
        self.results_view = QLabel()
        self.results_view.setAlignment(Qt.AlignCenter)
        self.results_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(self.results_view)

        # Set initial sizes
        splitter.setSizes([300, 1100])

    def init_circuit(self):
        """
        Initializes the QuantumCircuit object.
        """
        self.qr = QuantumRegister(1, 'q')
        self.cr = ClassicalRegister(1, 'c')
        self.circuit = QuantumCircuit(self.qr, self.cr)
        self.update_visualization()

    def add_qubit(self):
        """
        Adds a new qubit to the circuit.
        """
        num_qubits = self.circuit.num_qubits
        self.circuit.add_register(QuantumRegister(1, f'q{num_qubits}'))
        self.circuit.add_register(ClassicalRegister(1, f'c{num_qubits}'))
        self.update_visualization()
        self.push_history('Add Qubit')
        QMessageBox.information(self, "Qubit Added", f"Qubit {num_qubits} added to the circuit.")

    def add_gate(self):
        """
        Adds the selected gate to the circuit.
        """
        selected_items = self.gate_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Gate Selected", "Please select a gate to add.")
            return

        gate = selected_items[0].text()
        num_qubits = self.circuit.num_qubits

        if num_qubits == 0:
            QMessageBox.warning(self, "No Qubits", "Please add qubits before adding gates.")
            return

        # Select target qubits
        target_qubits = self.get_qubits(f"Select target qubit(s) for {gate} gate")
        if target_qubits is None:
            return

        # Apply gate based on the type
        try:
            if gate in ['H', 'X', 'Y', 'Z', 'S', 'T']:
                self.apply_single_qubit_gate(gate, target_qubits)
            elif gate in ['RX', 'RY', 'RZ']:
                angle, ok = QInputDialog.getDouble(
                    self, f"{gate} Gate", f"Enter rotation angle for {gate} gate (in radians):", decimals=4
                )
                if ok:
                    self.apply_rotation_gate(gate, target_qubits, angle)
            elif gate in ['CX', 'CY', 'CZ', 'Swap', 'CCX']:
                control_qubits = self.get_qubits(f"Select control qubit(s) for {gate} gate")
                if control_qubits is None:
                    return
                self.apply_multi_qubit_gate(gate, control_qubits, target_qubits)
            elif gate == 'Measure':
                # Save the state vector before measurement
                self.circuit.save_statevector()
                self.circuit.measure_all()
            else:
                QMessageBox.warning(self, "Unknown Gate", f"The gate '{gate}' is not recognized.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add gate:\n{e}")
            return

        self.update_visualization()
        self.push_history(f"Add Gate: {gate}")
        QMessageBox.information(self, "Gate Added", f"{gate} gate added to the circuit.")

    def get_qubits(self, prompt):
        """
        Prompts the user to select qubits.

        Returns:
            list: A list of qubit indices.
        """
        num_qubits = self.circuit.num_qubits
        items = [str(i) for i in range(num_qubits)]
        selected, ok = QInputDialog.getItem(
            self, "Select Qubits", prompt, items, 0, False
        )
        if ok and selected:
            return [int(selected)]
        else:
            return None

    def apply_single_qubit_gate(self, gate, targets):
        """
        Applies a single-qubit gate to the specified targets.

        Args:
            gate (str): The single-qubit gate ('H', 'X', 'Y', 'Z', 'S', 'T').
            targets (list): List of target qubit indices.
        """
        target = targets[0]
        if gate == 'H':
            self.circuit.h(target)
        elif gate == 'X':
            self.circuit.x(target)
        elif gate == 'Y':
            self.circuit.y(target)
        elif gate == 'Z':
            self.circuit.z(target)
        elif gate == 'S':
            self.circuit.s(target)
        elif gate == 'T':
            self.circuit.t(target)

    def apply_rotation_gate(self, gate, targets, angle):
        """
        Applies a rotation gate to the specified targets.

        Args:
            gate (str): The rotation gate ('RX', 'RY', 'RZ').
            targets (list): List of target qubit indices.
            angle (float): Rotation angle in radians.
        """
        target = targets[0]
        if gate == 'RX':
            self.circuit.rx(angle, target)
        elif gate == 'RY':
            self.circuit.ry(angle, target)
        elif gate == 'RZ':
            self.circuit.rz(angle, target)

    def apply_multi_qubit_gate(self, gate, controls, targets):
        """
        Applies a multi-qubit gate to the specified controls and targets.

        Args:
            gate (str): The multi-qubit gate ('CX', 'CY', 'CZ', 'Swap', 'CCX').
            controls (list): List of control qubit indices.
            targets (list): List of target qubit indices.
        """
        control = controls[0]
        target = targets[0]
        if gate == 'CX':
            self.circuit.cx(control, target)
        elif gate == 'CY':
            self.circuit.cy(control, target)
        elif gate == 'CZ':
            self.circuit.cz(control, target)
        elif gate == 'Swap':
            self.circuit.swap(control, target)
        elif gate == 'CCX':
            # For CCX, require two control qubits
            if len(controls) < 2:
                QMessageBox.warning(self, "Insufficient Controls", "CCX gate requires two control qubits.")
                return
            second_control = controls[1]
            self.circuit.ccx(control, second_control, target)

    def update_visualization(self):
        """
        Updates the circuit visualization and mathematical representations.
        """
        # Clear the scene
        self.scene.clear()

        # Use Qiskit's MPL drawer to get the circuit image
        figure = self.circuit.draw(output='mpl', fold=90)
        image_path = "circuit_diagram.png"
        figure.savefig(image_path)
        plt.close(figure)

        # Display the image in the QGraphicsView
        pixmap = QPixmap(image_path)
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(pixmap_item)
        
        # Convert QRect to QRectF to match setSceneRect's expected type
        self.scene.setSceneRect(QRectF(pixmap.rect()))

        # Remove the temporary image file
        os.remove(image_path)

        # Update mathematical representations
        self.update_math_display()

    def update_math_display(self):
        """
        Updates the mathematical representations of the quantum circuit.
        """
        try:
            # Get the saved state vector
            backend = AerSimulator(method='statevector')
            transpiled_circuit = transpile(self.circuit, backend)
            job = backend.run(transpiled_circuit)
            result = job.result()
            # 'statevector' is saved via save_statevector()
            state_vector = result.data(0).get('statevector')

            if state_vector is None:
                raise ValueError("No statevector available for the current circuit.")

            # Convert state vector to a readable format
            state_vector_str = self.state_vector_to_string(state_vector)

            # Get the overall unitary matrix
            unitary = self.get_unitary()
            if unitary is not None:
                unitary_str = self.unitary_to_string(unitary)
            else:
                unitary_str = "Unitary matrix not available for this circuit."

            # Combine into a comprehensive mathematical display
            math_content = f"<h3>State Vector:</h3><pre>{state_vector_str}</pre>"
            math_content += f"<h3>Unitary Matrix:</h3><pre>{unitary_str}</pre>"

            self.math_text.setHtml(math_content)
            self.circuit_updated.emit()
        except Exception as e:
            self.math_text.setText(f"Error displaying mathematical representations:\n{e}")

    def state_vector_to_string(self, state_vector):
        """
        Converts the state vector to a readable string format.

        Args:
            state_vector (Statevector): The state vector of the circuit.

        Returns:
            str: Readable string representation of the state vector.
        """
        num_qubits = self.circuit.num_qubits
        basis_states = [f"|{i:0{num_qubits}b}>" for i in range(2**num_qubits)]
        state_str = ""
        for state, amplitude in zip(basis_states, state_vector):
            state_str += f"{amplitude:.2f} |{state[1:-1]}>\n"
        return state_str

    def unitary_to_string(self, unitary_matrix):
        """
        Converts the unitary matrix to a readable string format.

        Args:
            unitary_matrix (numpy.ndarray): The unitary matrix of the circuit.

        Returns:
            str: Readable string representation of the unitary matrix.
        """
        unitary_str = ""
        for row in unitary_matrix:
            row_str = "  ".join([f"{elem.real:.2f}+{elem.imag:.2f}j" for elem in row])
            unitary_str += f"{row_str}\n"
        return unitary_str

    def get_unitary(self):
        """
        Retrieves the unitary matrix of the current circuit.

        Returns:
            np.ndarray: The unitary matrix.
        """
        try:
            operator = Operator(self.circuit)
            return operator.data
        except Exception:
            return None

    def generate_code(self):
        """
        Generates and displays the Qiskit code corresponding to the circuit.
        """
        code_gen = CodeGenerator(self.circuit)
        code = code_gen.generate_code()
        dialog = CodeDisplayDialog(code, self)
        dialog.exec_()

    def run_simulation(self):
        """
        Runs the simulation of the circuit and displays the results.
        """
        try:
            # Simulate the circuit to get the state vector
            simulator = AerSimulator(method='statevector')
            transpiled_circuit = transpile(self.circuit, simulator)
            job = simulator.run(transpiled_circuit)
            result = job.result()
            state_vector = result.get_statevector()

            # Simulate measurements
            simulator_measure = AerSimulator(method='density_matrix')
            transpiled_circuit_measure = transpile(self.circuit, simulator_measure)
            job_measure = simulator_measure.run(transpiled_circuit_measure)
            result_measure = job_measure.result()
            counts = result_measure.get_counts()

            # Plot the histogram
            figure = plot_histogram(counts)
            image_path = "simulation_results.png"
            figure.savefig(image_path)
            plt.close(figure)

            # Display the image
            pixmap = QPixmap(image_path)
            self.results_view.setPixmap(pixmap)
            self.results_view.setAlignment(Qt.AlignCenter)
            self.results_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Remove the temporary image file
            os.remove(image_path)

            # Update mathematical representations with measurement probabilities
            self.update_simulation_math(counts)

            self.push_history('Run Simulation')
            QMessageBox.information(self, "Simulation Completed", "The simulation has been successfully run.")
        except Exception as e:
            QMessageBox.critical(self, "Simulation Error", f"Failed to run simulation:\n{e}")

    def update_simulation_math(self, counts):
        """
        Updates the mathematical display with simulation results.

        Args:
            counts (dict): Measurement results.
        """
        try:
            # Calculate probabilities
            total_shots = sum(counts.values())
            probabilities = {k: v / total_shots for k, v in counts.items()}

            # Convert probabilities to readable string
            probs_str = ""
            for state, prob in probabilities.items():
                probs_str += f"P({state}) = {prob:.2f}\n"

            # Update mathematical display
            math_content = self.math_text.toHtml()
            math_content += f"<h3>Measurement Probabilities:</h3><pre>{probs_str}</pre>"
            self.math_text.setHtml(math_content)
        except Exception as e:
            self.math_text.setText(f"Error updating simulation mathematics:\n{e}")

    def push_history(self, action):
        """
        Pushes an action to the history stack for undo functionality.

        Args:
            action (str): Description of the action.
        """
        self.history.append(action)
        self.redo_stack.clear()

    def undo_action(self):
        """
        Undoes the last action.
        """
        if not self.history:
            QMessageBox.information(self, "Undo", "No actions to undo.")
            return

        last_action = self.history.pop()
        self.redo_stack.append(last_action)

        # For simplicity, clear the circuit and rebuild it without the last action
        self.rebuild_circuit()
        QMessageBox.information(self, "Undo", f"Undid action: {last_action}")

    def redo_action(self):
        """
        Redoes the last undone action.
        """
        if not self.redo_stack:
            QMessageBox.information(self, "Redo", "No actions to redo.")
            return

        action = self.redo_stack.pop()
        self.history.append(action)

        # Reapply the action
        # Note: Implementing redo functionality requires tracking detailed actions
        # For simplicity, this example does not implement it fully
        QMessageBox.information(self, "Redo", f"Redid action: {action}")
        self.rebuild_circuit()

    def rebuild_circuit(self):
        """
        Rebuilds the circuit based on the current history.
        """
        self.init_circuit()
        for action in self.history:
            if action.startswith("Add Qubit"):
                self.add_qubit()
            elif action.startswith("Add Gate:"):
                gate = action.split(": ")[1]
                # Re-select the gate and add it
                index = self.gate_list.findItems(gate, Qt.MatchExactly)
                if index:
                    self.gate_list.setCurrentRow(index[0].row())
                    self.add_gate()
        self.update_visualization()

    def clear_circuit(self):
        """
        Clears the current circuit and resets it.
        """
        self.init_circuit()
        self.update_visualization()
        self.math_text.clear()
        QMessageBox.information(self, "Circuit Cleared", "The circuit has been cleared.")
