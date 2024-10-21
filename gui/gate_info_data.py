# gui/gate_info_data.py
# This file contains the detailed information of various quantum gates.
# The dictionary GATE_INFO maps each gate to its properties such as description, matrix representation, and examples.
# For learning purposes, we've added additional gates and some comments explaining how each gate functions in quantum mechanics.

GATE_INFO = {
    'H': {
        'description': 'Hadamard Gate creates superposition.',
        'matrix': r'\frac{1}{\sqrt{2}}\begin{pmatrix}1 & 1\\1 & -1\end{pmatrix}',
        'examples': [
            r'Applying H to $|0\rangle$ results in $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$.',
            r'Applying H to $|1\rangle$ results in $\frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$.',
            r'Applying H twice returns the qubit to its original state.',
            r'H gate is used to create equal superposition, essential for many quantum algorithms.'
        ]
    },
    'X': {
        'description': 'Pauli-X Gate flips the qubit.',
        'matrix': r'\begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}',
        'examples': [
            r'$X|0\rangle = |1\rangle$',
            r'$X|1\rangle = |0\rangle$',
            r'$X$ applied twice returns the qubit to its original state.',
            r'X gate is equivalent to classical NOT gate, used for bit flips in quantum error correction.'
        ]
    },
    'Y': {
        'description': 'Pauli-Y Gate applies a Y rotation, affecting both phase and amplitude.',
        'matrix': r'\begin{pmatrix}0 & -i\\i & 0\end{pmatrix}',
        'examples': [
            r'$Y|0\rangle = i|1\rangle$',
            r'$Y|1\rangle = -i|0\rangle$',
            r'$Y$ applied twice results in $-I$.',
            r'Y gate combines bit and phase flips, useful in quantum tomography and error detection.'
        ]
    },
    'Z': {
        'description': 'Pauli-Z Gate applies a phase flip, changing the relative phase of the qubit.',
        'matrix': r'\begin{pmatrix}1 & 0\\0 & -1\end{pmatrix}',
        'examples': [
            r'$Z|0\rangle = |0\rangle$',
            r'$Z|1\rangle = -|1\rangle$',
            r'$Z$ applied twice returns the qubit to its original state.',
            r'Z gate is crucial for phase kickback in quantum phase estimation algorithms.'
        ]
    },
    'S': {
        'description': 'The S or Phase Gate applies a quarter turn in phase space.',
        'matrix': r'\begin{pmatrix}1 & 0\\0 & i\end{pmatrix}',
        'examples': [
            r'$S|0\rangle = |0\rangle$',
            r'$S|1\rangle = i|1\rangle$',
            r'$S$ applied twice is equivalent to $Z$.',
            r'S gate is used in the implementation of T gates and in quantum Fourier transform.'
        ]
    },
    'T': {
        'description': 'T Gate: Also known as the $\pi/8$ gate. It applies an eighth turn in phase space.',
        'matrix': r'\begin{pmatrix}1 & 0\\0 & \frac{1}{\sqrt{2}} + \frac{i}{\sqrt{2}}\end{pmatrix}',
        'examples': [
            r'$T|0\rangle = |0\rangle$',
            r'$T|1\rangle = \left(\frac{1}{\sqrt{2}} + \frac{i}{\sqrt{2}}\right)|1\rangle$',
            r'$T$ applied four times is equivalent to $Z$.',
            r'T gate is non-Clifford and essential for universal quantum computation.'
        ]
    },
    'RX': {
        'description': 'Rotation around X-axis by an angle $\\theta$.',
        'matrix': r'R_X(\theta) = \cos\left(\frac{\theta}{2}\right)I - i\sin\left(\frac{\theta}{2}\right)X',
        'examples': [
            r'$R_X(\pi)|0\rangle = |1\rangle$',
            r'$R_X(\pi)|1\rangle = |0\rangle$',
            r'$R_X(2\pi)|0\rangle = |0\rangle$',
            r'RX gates are used in variational quantum algorithms and quantum simulations.'
        ]
    },
    'RY': {
        'description': 'Rotation around Y-axis by an angle $\\theta$.',
        'matrix': r'R_Y(\theta) = \cos\left(\frac{\theta}{2}\right)I - i\sin\left(\frac{\theta}{2}\right)Y',
        'examples': [
            r'$R_Y(\pi)|0\rangle = i|1\rangle$',
            r'$R_Y(\pi)|1\rangle = -i|0\rangle$',
            r'$R_Y(2\pi)|0\rangle = |0\rangle$',
            r'RY gates are crucial in preparing arbitrary single-qubit states.'
        ]
    },
    'RZ': {
        'description': 'Rotation around Z-axis by an angle $\\theta$.',
        'matrix': r'R_Z(\theta) = \cos\left(\frac{\theta}{2}\right)I - i\sin\left(\frac{\theta}{2}\right)Z',
        'examples': [
            r'$R_Z(\pi)|0\rangle = e^{-i\pi/2}|0\rangle$',
            r'$R_Z(\pi)|1\rangle = e^{i\pi/2}|1\rangle$',
            r'$R_Z(2\pi)|0\rangle = |0\rangle$',
            r'RZ gates are often used in quantum phase estimation and quantum Fourier transform.'
        ]
    },
    'CX': {
        'description': 'Controlled-NOT Gate flips the second qubit only if the first is 1.',
        'matrix': r'\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix}',
        'examples': [
            r'$CX|00\rangle = |00\rangle$',
            r'$CX|01\rangle = |01\rangle$',
            r'$CX|10\rangle = |11\rangle$',
            r'CX (CNOT) is fundamental for entanglement creation and multi-qubit operations.'
        ]
    },
    'CY': {
        'description': 'Controlled-Y Gate applies Y if the first qubit is 1.',
        'matrix': r'\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & -i\\0 & 0 & i & 0\end{pmatrix}',
        'examples': [
            r'$CY|00\rangle = |00\rangle$',
            r'$CY|01\rangle = |01\rangle$',
            r'$CY|10\rangle = -i|11\rangle$',
            r'CY gates are used in certain quantum error correction codes and state preparation.'
        ]
    },
    'CZ': {
        'description': 'Controlled-Z Gate flips the phase of the second qubit if the first is 1.',
        'matrix': r'\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & -1\end{pmatrix}',
        'examples': [
            r'$CZ|00\rangle = |00\rangle$',
            r'$CZ|01\rangle = |01\rangle$',
            r'$CZ|11\rangle = -|11\rangle$',
            r'CZ gates are symmetric and often preferred in superconducting qubit architectures.'
        ]
    },
    'Swap': {
        'description': 'The Swap Gate swaps the states of two qubits.',
        'matrix': r'\begin{pmatrix}1 & 0 & 0 & 0\\0 & 0 & 1 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\end{pmatrix}',
        'examples': [
            r'$Swap|01\rangle = |10\rangle$',
            r'$Swap|10\rangle = |01\rangle$',
            r'$Swap|00\rangle = |00\rangle$',
            r'Swap gates are useful in quantum circuit optimization and quantum communication protocols.'
        ]
    },
    'CCX': {
        'description': 'Toffoli Gate (Controlled-Controlled-X) applies the X gate only when both control qubits are 1.',
        'matrix': r'8x8 matrix with X on target when both controls are 1.',
        'examples': [
            r'$CCX|110\rangle = |111\rangle$',
            r'$CCX|101\rangle = |101\rangle$',
            r'$CCX|111\rangle = |110\rangle$',
            r'CCX (Toffoli) gate is universal for classical reversible computation and quantum error correction.'
        ]
    }
}
