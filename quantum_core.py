"""
Quantum Core Module for QTrace
Handles quantum circuit simulation, partial trace calculations, and state analysis.
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, Operator, partial_trace, DensityMatrix
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import io
import base64

class QuantumStateAnalyzer:
    """Main class for quantum state analysis and simulation."""
    
    def __init__(self, backend_name: str = 'aer_simulator'):
        """
        Initialize the quantum state analyzer.
        
        Args:
            backend_name: Name of the Qiskit backend to use
        """
        try:
            self.backend = AerSimulator(method='statevector')
        except Exception as e:
            # Fallback to default backend
            self.backend = AerSimulator(method='statevector')
        
        self.circuit = None
        self.state_history = []
        self.current_step = 0
        
    def create_circuit(self, num_qubits: int, num_classical_bits: int = 0) -> QuantumCircuit:
        """
        Create a new quantum circuit.
        
        Args:
            num_qubits: Number of qubits in the circuit
            num_classical_bits: Number of classical bits for measurement
            
        Returns:
            QuantumCircuit object
        """
        if num_classical_bits == 0:
            num_classical_bits = num_qubits
            
        self.circuit = QuantumCircuit(num_qubits, num_classical_bits)
        self.state_history = []
        self.current_step = 0
        return self.circuit
    
    def add_gate(self, gate_name: str, qubit: int, target_qubit: int = None, 
                  angle: float = None) -> bool:
        """
        Add a quantum gate to the circuit.
        
        Args:
            gate_name: Name of the gate (h, x, y, z, cx, rx, ry, rz, etc.)
            qubit: Target qubit for single-qubit gates
            target_qubit: Control qubit for two-qubit gates
            angle: Rotation angle for parameterized gates
            
        Returns:
            True if gate was added successfully, False otherwise
        """
        if self.circuit is None:
            return False
            
        try:
            if gate_name.lower() == 'h':
                self.circuit.h(qubit)
            elif gate_name.lower() == 'x':
                self.circuit.x(qubit)
            elif gate_name.lower() == 'y':
                self.circuit.y(qubit)
            elif gate_name.lower() == 'z':
                self.circuit.z(qubit)
            elif gate_name.lower() == 's':
                self.circuit.s(qubit)
            elif gate_name.lower() == 'sdg':
                self.circuit.sdg(qubit)
            elif gate_name.lower() == 't':
                self.circuit.t(qubit)
            elif gate_name.lower() == 'tdg':
                self.circuit.tdg(qubit)
            elif gate_name.lower() == 'rx' and angle is not None:
                self.circuit.rx(angle, qubit)
            elif gate_name.lower() == 'ry' and angle is not None:
                self.circuit.ry(angle, qubit)
            elif gate_name.lower() == 'rz' and angle is not None:
                self.circuit.rz(angle, qubit)
            elif gate_name.lower() == 'cx' and target_qubit is not None:
                self.circuit.cx(qubit, target_qubit)
            elif gate_name.lower() == 'cy' and target_qubit is not None:
                self.circuit.cy(qubit, target_qubit)
            elif gate_name.lower() == 'cz' and target_qubit is not None:
                self.circuit.cz(qubit, target_qubit)
            elif gate_name.lower() == 'swap' and target_qubit is not None:
                self.circuit.swap(qubit, target_qubit)
            else:
                return False
                
            return True
        except Exception:
            return False
    
    def load_openqasm(self, qasm_string: str) -> bool:
        """
        Load a circuit from OpenQASM string.
        
        Args:
            qasm_string: OpenQASM circuit description
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            self.circuit = QuantumCircuit.from_qasm_str(qasm_string)
            self.state_history = []
            self.current_step = 0
            return True
        except Exception:
            return False
    
    def simulate_circuit(self, shots: int = 1000) -> Dict:
        """
        Simulate the quantum circuit and return results.
        
        Args:
            shots: Number of simulation shots
            
        Returns:
            Dictionary containing simulation results
        """
        if self.circuit is None:
            return {}
            
        try:
            # Check if circuit has measurements
            has_measurements = any(inst.name == 'measure' for inst, _, _ in self.circuit.data)
            
            if has_measurements:
                # Create a new circuit without measurements for statevector
                circuit_no_measure = QuantumCircuit(self.circuit.num_qubits)
                
                # Copy all non-measurement gates
                non_measure_gates = []
                for instruction, qargs, cargs in self.circuit.data:
                    if instruction.name != 'measure':
                        non_measure_gates.append((instruction, qargs, cargs))
                        circuit_no_measure.append(instruction, qargs, cargs)
                
                # Only try to get statevector if we have non-measurement gates
                if non_measure_gates:
                    try:
                        # Try using Statevector class directly
                        statevector = Statevector.from_instruction(circuit_no_measure)
                    except Exception as e:
                        # Fallback to backend execution
                        try:
                            statevector_job = self.backend.run(circuit_no_measure, shots=1)
                            statevector_result = statevector_job.result()
                            statevector = statevector_result.get_statevector()
                        except Exception as e2:
                            statevector = None
                else:
                    print("Warning: Circuit only contains measurements, no gates to simulate")
                    statevector = None
            else:
                # No measurements, use original circuit
                try:
                    # Try using Statevector class directly
                    statevector = Statevector.from_instruction(self.circuit)
                except Exception as e:
                    # Fallback to backend execution
                    try:
                        statevector_job = self.backend.run(self.circuit, shots=1)
                        statevector_result = statevector_job.result()
                        statevector = statevector_result.get_statevector()
                    except Exception as e2:
                        statevector = None
            
            # Get measurement counts from original circuit
            counts = {}
            if has_measurements:
                try:
                    counts_job = self.backend.run(self.circuit, shots=shots)
                    counts_result = counts_job.result()
                    counts = counts_result.get_counts()
                except Exception as e:
                    print(f"Warning: Could not get measurement counts: {e}")
                    counts = {}
            else:
                # For circuits without measurements, we can't get counts
                counts = {}
            
            # Calculate partial traces if we have statevector
            partial_traces = []
            if statevector is not None and len(statevector) > 0:
                try:
                    # Convert Statevector to numpy array if needed
                    if hasattr(statevector, 'data'):
                        statevector_array = statevector.data
                    else:
                        statevector_array = statevector
                    partial_traces = self._calculate_partial_traces(statevector_array)
                except Exception as e:
                    print(f"Warning: Could not calculate partial traces: {e}")
                    partial_traces = []
            else:
                print(f"Warning: No valid statevector available. Statevector: {statevector}")
                partial_traces = []
            
            # Store state history for step-by-step view
            self._build_state_history()
            
            return {
                'statevector': statevector,
                'counts': counts,
                'partial_traces': partial_traces,
                'circuit_depth': self.circuit.depth(),
                'num_qubits': self.circuit.num_qubits,
                'num_gates': self.circuit.count_ops(),
                'has_measurements': has_measurements
            }
        except Exception as e:
            error_msg = f"Simulation failed: {str(e)}"
            if "No statevector" in str(e):
                error_msg += "\nThis usually happens when the circuit has measurement operations. Try removing measurements or check circuit structure."
            return {'error': error_msg}
    
    def _calculate_partial_traces(self, statevector: np.ndarray) -> List[np.ndarray]:
        """
        Calculate partial trace for each qubit to get reduced density matrices.
        
        Args:
            statevector: Full quantum state vector
            
        Returns:
            List of reduced density matrices for each qubit
        """
        num_qubits = int(np.log2(len(statevector)))
        partial_traces = []
        
        for qubit in range(num_qubits):
            # Create the full density matrix
            rho = np.outer(statevector, statevector.conj())
            
            # Calculate partial trace over all qubits except the current one
            qubits_to_trace = list(range(num_qubits))
            qubits_to_trace.remove(qubit)
            
            if qubits_to_trace:
                reduced_rho = partial_trace(rho, qubits_to_trace)
            else:
                reduced_rho = rho
                
            partial_traces.append(reduced_rho)
            
        return partial_traces
    
    def _build_state_history(self):
        """Build a history of states after each gate application."""
        if self.circuit is None:
            return
            
        self.state_history = []
        temp_circuit = QuantumCircuit(self.circuit.num_qubits)
        
        for instruction, qargs, cargs in self.circuit.data:
            # Skip measurement operations for state history
            if instruction.name == 'measure':
                continue
                
            temp_circuit.append(instruction, qargs, cargs)
            
            try:
                # Try using Statevector class directly first
                try:
                    statevector = Statevector.from_instruction(temp_circuit)
                except Exception:
                    # Fallback to backend execution
                    job = self.backend.run(temp_circuit, shots=1)
                    result = job.result()
                    statevector = result.get_statevector()
                
                # Convert Statevector to numpy array if needed
                if hasattr(statevector, 'data'):
                    statevector_array = statevector.data
                else:
                    statevector_array = statevector
                
                # Calculate partial traces for this step
                partial_traces = self._calculate_partial_traces(statevector_array)
                
                self.state_history.append({
                    'step': len(self.state_history),
                    'gate': instruction.name,
                    'qubits': [q.index for q in qargs],
                    'statevector': statevector,
                    'partial_traces': partial_traces
                })
            except Exception as e:
                print(f"Warning: Could not build state history for step {len(self.state_history)}: {e}")
                continue
    
    def get_state_at_step(self, step: int) -> Optional[Dict]:
        """
        Get the quantum state at a specific step.
        
        Args:
            step: Step number in the circuit
            
        Returns:
            State information at the specified step
        """
        if 0 <= step < len(self.state_history):
            return self.state_history[step]
        return None
    
    def get_purity(self, density_matrix: np.ndarray) -> float:
        """
        Calculate the purity of a quantum state.
        
        Args:
            density_matrix: Density matrix of the quantum state
            
        Returns:
            Purity value (1.0 for pure states, <1.0 for mixed states)
        """
        # Convert to numpy array if it's a Qiskit DensityMatrix object
        if hasattr(density_matrix, 'data'):
            dm = np.asarray(density_matrix.data)
        else:
            dm = np.asarray(density_matrix)
        return np.real(np.trace(dm @ dm))
    
    def get_bloch_coordinates(self, density_matrix: np.ndarray) -> Tuple[float, float, float]:
        """
        Extract Bloch sphere coordinates from a density matrix.
        
        Args:
            density_matrix: 2x2 density matrix
            
        Returns:
            Tuple of (x, y, z) coordinates on the Bloch sphere
        """
        # Convert to numpy array if it's a Qiskit DensityMatrix object
        if hasattr(density_matrix, 'data'):
            dm = np.asarray(density_matrix.data)
        else:
            dm = np.asarray(density_matrix)
            
        # Pauli matrices
        sigma_x = np.array([[0, 1], [1, 0]])
        sigma_y = np.array([[0, -1j], [1j, 0]])
        sigma_z = np.array([[1, 0], [0, -1]])
        
        x = np.real(np.trace(dm @ sigma_x))
        y = np.real(np.trace(dm @ sigma_y))
        z = np.real(np.trace(dm @ sigma_z))
        
        return x, y, z
    
    def get_circuit_info(self) -> Dict:
        """
        Get information about the current circuit.
        
        Returns:
            Dictionary containing circuit information
        """
        if self.circuit is None:
            return {}
            
        return {
            'num_qubits': self.circuit.num_qubits,
            'num_classical_bits': self.circuit.num_clbits,
            'depth': self.circuit.depth(),
            'gate_counts': self.circuit.count_ops(),
            'instructions': [(inst.name, [q.index for q in qargs]) 
                           for inst, qargs, cargs in self.circuit.data]
        }
    
    def reset_circuit(self):
        """Reset the circuit and clear all data."""
        self.circuit = None
        self.state_history = []
        self.current_step = 0
