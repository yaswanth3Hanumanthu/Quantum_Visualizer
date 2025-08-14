"""
Bell State Example Circuit
Creates the entangled state (|00⟩ + |11⟩)/√2
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import numpy as np

def create_bell_state_circuit():
    """
    Create a Bell state circuit.
    
    Returns:
        QuantumCircuit: The Bell state circuit
    """
    # Create a quantum circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)
    
    # Apply Hadamard gate to the first qubit
    qc.h(0)
    
    # Apply CNOT gate with control qubit 0 and target qubit 1
    qc.cx(0, 1)
    
    # Measure both qubits
    qc.measure([0, 1], [0, 1])
    
    return qc

def simulate_bell_state():
    """
    Simulate the Bell state circuit and show results.
    
    Returns:
        dict: Simulation results
    """
    # Create the circuit
    qc = create_bell_state_circuit()
    
    # Simulate the circuit
    backend = AerSimulator()
    job = backend.run(qc, shots=1000)
    result = job.result()
    
    # Get the counts
    counts = result.get_counts(qc)
    
    # Get the statevector (before measurement)
    qc_no_measure = QuantumCircuit(2)
    qc_no_measure.h(0)
    qc_no_measure.cx(0, 1)
    
    statevector_job = backend.run(qc_no_measure, shots=1)
    statevector_result = statevector_job.result()
    statevector = statevector_result.get_statevector()
    
    return {
        'circuit': qc,
        'counts': counts,
        'statevector': statevector,
        'expected_state': '(|00⟩ + |11⟩)/√2'
    }

def analyze_bell_state():
    """
    Analyze the Bell state properties.
    """
    results = simulate_bell_state()
    
    print("Bell State Circuit Analysis")
    print("=" * 40)
    print(f"Expected state: {results['expected_state']}")
    print(f"State vector: {results['statevector']}")
    print(f"Measurement counts: {results['counts']}")
    
    # Calculate entanglement
    statevector = results['statevector']
    rho = np.outer(statevector, statevector.conj())
    
    # Partial trace over qubit 1 to get reduced density matrix of qubit 0
    rho_0 = np.array([
        [rho[0, 0] + rho[1, 1], rho[0, 2] + rho[1, 3]],
        [rho[2, 0] + rho[3, 1], rho[2, 2] + rho[3, 3]]
    ])
    
    # Calculate purity of reduced state
    purity = np.real(np.trace(rho_0 @ rho_0))
    print(f"Purity of qubit 0 (should be 0.5 for maximally entangled): {purity:.4f}")
    
    if abs(purity - 0.5) < 0.01:
        print("✅ State is maximally entangled!")
    else:
        print("❌ State is not maximally entangled")

if __name__ == "__main__":
    analyze_bell_state()
