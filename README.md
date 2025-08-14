# QTrace – Quantum State Visualizer

A powerful quantum computing visualization tool that allows you to build quantum circuits, simulate them, and visualize the quantum state evolution on interactive Bloch spheres.

## Features

- **Circuit Builder**: Create multi-qubit quantum circuits using Qiskit
- **OpenQASM Support**: Upload existing quantum circuits in OpenQASM format
- **State Simulation**: Run circuits using Qiskit Aer simulator
- **Partial Trace Analysis**: Extract reduced density matrices for individual qubits
- **Bloch Sphere Visualization**: Interactive 3D plots showing pure vs mixed states
- **Step-by-Step Evolution**: Watch quantum states evolve gate by gate
- **Export Capabilities**: Save results as PNG or PDF
- **IBM Quantum Integration**: Optional hardware execution with API key

## Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Quantum_Visualizer
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Build a Circuit**: Use the circuit builder to add gates to your qubits
2. **Simulate**: Click "Run Simulation" to execute the circuit
3. **Visualize**: View Bloch spheres for each qubit showing their quantum states
4. **Step Through**: Use the step-by-step view to see state evolution
5. **Export**: Save your results and visualizations

## Project Structure

```
Quantum_Visualizer/
├── app.py                 # Main Streamlit application
├── quantum_core.py        # Core quantum computing logic
├── visualization.py       # Bloch sphere and plotting functions
├── circuit_builder.py     # Circuit construction interface
├── utils.py              # Utility functions and helpers
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── examples/             # Example circuits and tutorials
    ├── bell_state.py
    ├── ghz_state.py
    └── quantum_teleportation.py
```

## Examples

The project includes several example circuits:
- **Bell State**: Demonstrates quantum entanglement
- **GHZ State**: Multi-qubit entangled state
- **Quantum Teleportation**: Complete teleportation protocol

## Hackathon Extensions

- **Real-time Collaboration**: Add WebSocket support for collaborative circuit building
- **Quantum Game**: Create puzzles using quantum circuits
- **Machine Learning Integration**: Use quantum states for ML applications
- **Mobile App**: Convert to React Native or Flutter
- **Cloud Deployment**: Deploy on AWS/GCP with user authentication

## Contributing

This project is designed to be hackathon-friendly. Feel free to:
- Add new quantum gates and algorithms
- Improve the visualization interface
- Add new export formats
- Implement additional quantum features

## License

MIT License - feel free to use this project for your hackathon!
