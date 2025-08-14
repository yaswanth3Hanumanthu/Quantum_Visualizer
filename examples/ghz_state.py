"""
GHZ State Example Circuit
Creates the three-qubit entangled state (|000⟩ + |111⟩)/√2
"""

from qiskit import QuantumCircuit, Aer, execute
from qiskit.quantum_info import Statevector
import numpy as np

def create_ghz_state_circuit():
    """
    Create a GHZ state circuit.
    
    Returns:
        QuantumCircuit: The GHZ state circuit
    """
    # Create a quantum circuit with 3 qubits and 3 classical bits
    qc = QuantumCircuit(3, 3)
    
    # Apply Hadamard gate to the first qubit
    qc.h(0)
    
    # Apply CNOT gates to create entanglement
    qc.cx(0, 1)  # CNOT with control qubit 0 and target qubit 1
    qc.cx(1, 2)  # CNOT with control qubit 1 and target qubit 2
    
    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    return qc

def simulate_ghz_state():
    """
    Simulate the GHZ state circuit and show results.
    
    Returns:
        dict: Simulation results
    """
    # Create the circuit
    qc = create_ghz_state_circuit()
    
    # Simulate the circuit
    backend = Aer.get_backend('aer_simulator')
    job = execute(qc, backend, shots=1000)
    result = job.result()
    
    # Get the counts
    counts = result.get_counts(qc)
    
    # Get the statevector (before measurement)
    qc_no_measure = QuantumCircuit(3)
    qc_no_measure.h(0)
    qc_no_measure.cx(0, 1)
    qc_no_measure.cx(1, 2)
    
    statevector_job = execute(qc_no_measure, backend, shots=1)
    statevector_result = statevector_job.result()
    statevector = statevector_result.get_statevector()
    
    return {
        'circuit': qc,
        'counts': counts,
        'statevector': statevector,
        'expected_state': '(|000⟩ + |111⟩)/√2'
    }

def analyze_ghz_state():
    """
    Analyze the GHZ state properties.
    """
    results = simulate_ghz_state()
    
    print("GHZ State Circuit Analysis")
    print("=" * 40)
    print(f"Expected state: {results['expected_state']}")
    print(f"State vector: {results['statevector']}")
    print(f"Measurement counts: {results['counts']}")
    
    # Calculate entanglement properties
    statevector = results['statevector']
    rho = np.outer(statevector, statevector.conj())
    
    # Check that only |000⟩ and |111⟩ components are non-zero
    print("\nState vector components:")
    for i, amplitude in enumerate(statevector):
        binary = format(i, '03b')
        if abs(amplitude) > 1e-10:
            print(f"|{binary}⟩: {amplitude:.6f}")
    
    # Calculate reduced density matrices for each qubit
    print("\nReduced density matrices:")
    
    for qubit in range(3):
        # Calculate partial trace over other qubits
        if qubit == 0:
            # Trace over qubits 1 and 2
            rho_reduced = np.array([
                [rho[0, 0] + rho[1, 1] + rho[2, 2] + rho[3, 3], 
                 rho[0, 4] + rho[1, 5] + rho[2, 6] + rho[3, 7]],
                [rho[4, 0] + rho[5, 1] + rho[6, 2] + rho[7, 3], 
                 rho[4, 4] + rho[5, 5] + rho[6, 6] + rho[7, 7]]
            ])
        elif qubit == 1:
            # Trace over qubits 0 and 2
            rho_reduced = np.array([
                [rho[0, 0] + rho[2, 2] + rho[4, 4] + rho[6, 6], 
                 rho[0, 1] + rho[2, 3] + rho[4, 5] + rho[6, 7]],
                [rho[1, 0] + rho[3, 2] + rho[5, 4] + rho[7, 6], 
                 rho[1, 1] + rho[3, 3] + rho[5, 5] + rho[7, 7]]
            ])
        else:  # qubit == 2
            # Trace over qubits 0 and 1
            rho_reduced = np.array([
                [rho[0, 0] + rho[1, 1] + rho[4, 4] + rho[5, 5], 
                 rho[0, 2] + rho[1, 3] + rho[4, 6] + rho[5, 7]],
                [rho[2, 0] + rho[3, 1] + rho[6, 4] + rho[7, 5], 
                 rho[2, 2] + rho[3, 3] + rho[6, 6] + rho[7, 7]]
            ])
        
        # Calculate purity
        purity = np.real(np.trace(rho_reduced @ rho_reduced))
        print(f"Qubit {qubit} reduced density matrix:")
        print(rho_reduced)
        print(f"Purity: {purity:.4f}")
        print()

def create_generalized_ghz(n_qubits):
    """
    Create a generalized GHZ state with n qubits.
    
    Args:
        n_qubits: Number of qubits
        
    Returns:
        QuantumCircuit: The generalized GHZ state circuit
    """
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Apply Hadamard to first qubit
    qc.h(0)
    
    # Apply CNOT gates in a chain
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    
    # Measure all qubits
    qc.measure(range(n_qubits), range(n_qubits))
    
    return qc

if __name__ == "__main__":
    analyze_ghz_state()
    
    print("\n" + "="*50)
    print("Generalized GHZ State (4 qubits)")
    print("="*50)
    
    # Create and simulate 4-qubit GHZ state
    qc_4 = create_generalized_ghz(4)
    backend = Aer.get_backend('aer_simulator')
    job = execute(qc_4, backend, shots=1000)
    result = job.result()
    counts_4 = result.get_counts(qc_4)
    
    print(f"4-qubit GHZ state measurement counts: {counts_4}")
    print("Expected: Only |0000⟩ and |1111⟩ should have non-zero counts")
