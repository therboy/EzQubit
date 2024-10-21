# QubitLogics | Qiskit GUI Builder (v0.00)

## Overview

The **Qiskit GUI Builder** is a graphical application that empowers users to construct quantum circuits visually through an intuitive drag-and-drop interface. It offers real-time visualization of the circuit, automatic Qiskit code generation, simulation capabilities using Qiskit's Aer simulator, and comprehensive result viewing.

## Features

- **Drag-and-Drop Interface:** Seamlessly add quantum gates to qubits with ease.
- **Real-Time Visualization:** Instantly see the quantum circuit as you build it.
- **Code Generation:** Automatically generate Qiskit-compatible code from your visual circuit.
- **Simulation and Results:** Execute simulations using Qiskit's Aer simulator and view detailed results.
- **Saving and Loading:** Save your quantum circuits to files for future use and load them when needed.

## Installation

### Prerequisites

- **Python:** Version 3.7 or later
- **pip:** Python package manager

### Install Dependencies

Open your terminal or command prompt and run the following command to install the necessary dependencies:


pip install -r requirements.txt


### Clone the Repository


git clone https://github.com/therboy/QubitLogics.git
cd QubitLogics


### Run the Application


python main.py


## Usage

1. **Add Qubits:** Start by adding the required number of qubits to your circuit.
2. **Add Gates:** Drag and drop quantum gates from the toolbar onto the qubits.
3. **Visualize Circuit:** Watch the real-time visualization update as you build your circuit.
4. **Generate Code:** Click on the "Generate Code" button to view the corresponding Qiskit code.
5. **Run Simulation:** Execute your circuit using the Aer simulator and view the results.
6. **Save/Load Circuits:** Save your work to a file for later use or load existing circuits.

## Notes

- **Line Counts:** While some files like `__init__.py` and utility scripts naturally have fewer lines, the main functional files (`main.py`, `main_window.py`, `circuit_builder.py`, and `code_generator.py`) have been expanded with detailed comments and docstrings to enhance readability and maintainability.
  
- **Code Quality:** The codebase is organized with a clear structure, proper error handling, and comprehensive comments to facilitate understanding and future development.

- **Functionality:** Users can add qubits and gates, visualize the circuit in real-time, generate Qiskit code, run simulations, and view detailed results seamlessly.

- **Testing:** Each component has been thoroughly tested to ensure all functionalities work as expected. Refer to the `tests/` directory for unit tests.

- **Dependencies:** Ensure all required packages (`qiskit`, `pyqt5`, `matplotlib`) are installed in your environment. You can install them using the provided installation instructions.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Thank you for using Qiskit GUI Builder!*
