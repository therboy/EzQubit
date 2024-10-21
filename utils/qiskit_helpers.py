# utils/qiskit_helpers.py

"""
Provides helper functions for Qiskit operations.
"""

from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
import numpy as np
from qiskit.quantum_info import Operator, Statevector

def visualize_circuit(circuit: QuantumCircuit, filename: str = "circuit.png"):
    """
    Visualizes the quantum circuit and saves it as an image.

    Args:
        circuit (QuantumCircuit): The quantum circuit to visualize.
        filename (str): The filename to save the image.
    """
    figure = circuit.draw(output='mpl', fold=90)
    figure.savefig(filename)
    plt.close(figure)

def get_gate_matrix(circuit: QuantumCircuit, gate_label: str):
    """
    Retrieves the matrix representation of a specified gate in the circuit.

    Args:
        circuit (QuantumCircuit): The quantum circuit containing the gate.
        gate_label (str): The label of the gate (e.g., 'H', 'CX').

    Returns:
        numpy.ndarray or None: The matrix representation if found, else None.
    """
    for instr, qargs, cargs in circuit.data:
        if instr.name.upper() == gate_label.upper():
            return instr.to_matrix()
    return None

def get_full_unitary(circuit: QuantumCircuit):
    """
    Computes the full unitary matrix of the circuit.

    Args:
        circuit (QuantumCircuit): The quantum circuit.

    Returns:
        numpy.ndarray or None: The unitary matrix if computable, else None.
    """
    try:
        operator = Operator(circuit)
        return operator.data
    except:
        return None

def get_state_vector(circuit: QuantumCircuit):
    """
    Computes the state vector of the circuit assuming it starts in |0...0>.

    Args:
        circuit (QuantumCircuit): The quantum circuit.

    Returns:
        numpy.ndarray or None: The state vector if computable, else None.
    """
    try:
        state = Statevector.from_instruction(circuit)
        return state.data
    except:
        return None

def matrix_to_latex(matrix):
    """
    Converts a numpy matrix to a LaTeX bmatrix format.

    Args:
        matrix (numpy.ndarray): The matrix to convert.

    Returns:
        str: LaTeX-formatted matrix.
    """
    latex_str = "\\begin{bmatrix}\n"
    for row in matrix:
        row_str = " & ".join([f"{elem:.2f}" for elem in row])
        latex_str += f"{row_str} \\\\\n"
    latex_str += "\\end{bmatrix}"
    return latex_str

def statevector_to_latex(state_vector):
    """
    Converts a state vector to a LaTeX column vector format.

    Args:
        state_vector (numpy.ndarray): The state vector to convert.

    Returns:
        str: LaTeX-formatted state vector.
    """
    latex_str = "\\begin{bmatrix}\n"
    for elem in state_vector:
        latex_str += f"{elem:.2f} \\\\\n"
    latex_str += "\\end{bmatrix}"
    return latex_str
