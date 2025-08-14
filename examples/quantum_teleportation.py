"""
Quantum Teleportation Example Circuit
Demonstrates the complete quantum teleportation protocol
"""

from qiskit import QuantumCircuit, Aer, execute
from qiskit.quantum_info import Statevector
import numpy as np

def create_teleportation_circuit(initial_state='random'):
    """
    Create a quantum teleportation circuit.
    
    Args:
        initial_state: Initial state of qubit 0 ('0', '1', '+', 'random')
        
    Returns:
        QuantumCircuit: The teleportation circuit
    """
    # Create a quantum circuit with 3 qubits and 3 classical bits
    qc = QuantumCircuit(3, 3)
    
    # Prepare the initial state of qubit 0 (the qubit to be teleported)
    if initial_state == '0':
        # Leave in |0⟩ state
        pass
    elif initial_state == '1':
        qc.x(0)  # Apply X gate to get |1⟩
    elif initial_state == '+':
        qc.h(0)  # Apply H gate to get |+⟩ = (|0⟩ + |1⟩)/√2
    elif initial_state == 'random':
        # Apply a random rotation to create an arbitrary state
        qc.rx(np.pi/3, 0)  # Rotate by π/3 around X-axis
    
    # Create Bell state between qubits 1 and 2
    qc.h(1)
    qc.cx(1, 2)
    
    # Apply teleportation protocol
    qc.cx(0, 1)  # CNOT with control qubit 0 and target qubit 1
    qc.h(0)      # Hadamard on qubit 0
    
    # Measure qubits 0 and 1
    qc.measure([0, 1], [0, 1])
    
    # Apply conditional operations on qubit 2 based on measurement results
    qc.x(2).c_if(1, 1)  # Apply X if measurement of qubit 1 is 1
    qc.z(2).c_if(0, 1)  # Apply Z if measurement of qubit 0 is 1
    
    # Measure qubit 2 (the teleported qubit)
    qc.measure(2, 2)
    
    return qc

def create_teleportation_circuit_no_measurement(initial_state='random'):
    """
    Create a teleportation circuit without final measurement for state analysis.
    
    Args:
        initial_state: Initial state of qubit 0
        
    Returns:
        QuantumCircuit: The teleportation circuit without final measurement
    """
    qc = QuantumCircuit(3, 2)  # Only 2 classical bits for intermediate measurements
    
    # Prepare the initial state
    if initial_state == '0':
        pass
    elif initial_state == '1':
        qc.x(0)
    elif initial_state == '+':
        qc.h(0)
    elif initial_state == 'random':
        qc.rx(np.pi/3, 0)
    
    # Create Bell state
    qc.h(1)
    qc.cx(1, 2)
    
    # Teleportation protocol
    qc.cx(0, 1)
    qc.h(0)
    
    # Measure qubits 0 and 1
    qc.measure([0, 1], [0, 1])
    
    # Conditional operations
    qc.x(2).c_if(1, 1)
    qc.z(2).c_if(0, 1)
    
    return qc

def simulate_teleportation(initial_state='random'):
    """
    Simulate the quantum teleportation protocol.
    
    Args:
        initial_state: Initial state of qubit 0
        
    Returns:
        dict: Simulation results
    """
    # Create the circuit
    qc = create_teleportation_circuit(initial_state)
    
    # Simulate the circuit
    backend = Aer.get_backend('aer_simulator')
    job = execute(qc, backend, shots=1000)
    result = job.result()
    
    # Get the counts
    counts = result.get_counts(qc)
    
    # Get the statevector before final measurement
    qc_no_final_measure = create_teleportation_circuit_no_measurement(initial_state)
    statevector_job = execute(qc_no_final_measure, backend, shots=1)
    statevector_result = statevector_job.result()
    statevector = statevector_result.get_statevector()
    
    return {
        'circuit': qc,
        'counts': counts,
        'statevector': statevector,
        'initial_state': initial_state
    }

def analyze_teleportation():
    """
    Analyze the quantum teleportation protocol.
    """
    print("Quantum Teleportation Analysis")
    print("=" * 50)
    
    # Test different initial states
    test_states = ['0', '1', '+', 'random']
    
    for state in test_states:
        print(f"\n--- Testing Initial State: {state} ---")
        
        results = simulate_teleportation(state)
        
        print(f"Initial state: {state}")
        print(f"Measurement counts: {results['counts']}")
        
        # Analyze the teleportation success
        counts = results['counts']
        total_shots = sum(counts.values())
        
        # The teleported state should match the initial state
        # For |0⟩ and |1⟩ states, we expect mostly |0⟩ and |1⟩ respectively
        # For |+⟩ state, we expect roughly equal |0⟩ and |1⟩
        # For random state, we expect some distribution
        
        if state == '0':
            success_rate = counts.get('000', 0) / total_shots
            print(f"Success rate for |0⟩ state: {success_rate:.3f}")
        elif state == '1':
            success_rate = counts.get('001', 0) / total_shots
            print(f"Success rate for |1⟩ state: {success_rate:.3f}")
        elif state == '+':
            # For |+⟩ state, we expect roughly equal distribution
            zero_count = sum(count for outcome, count in counts.items() if outcome.endswith('0'))
            one_count = sum(count for outcome, count in counts.items() if outcome.endswith('1'))
            print(f"|0⟩ outcomes: {zero_count}, |1⟩ outcomes: {one_count}")
            print(f"Ratio: {zero_count/one_count:.3f} (should be close to 1.0)")
        
        print(f"Total shots: {total_shots}")

def demonstrate_entanglement():
    """
    Demonstrate the entanglement properties in teleportation.
    """
    print("\n" + "="*50)
    print("Entanglement Analysis")
    print("="*50)
    
    # Create Bell state between qubits 1 and 2
    qc_bell = QuantumCircuit(2)
    qc_bell.h(0)
    qc_bell.cx(0, 1)
    
    backend = Aer.get_backend('aer_simulator')
    job = execute(qc_bell, backend, shots=1)
    result = job.result()
    bell_statevector = result.get_statevector()
    
    print("Bell state between qubits 1 and 2:")
    print(f"State vector: {bell_statevector}")
    
    # Calculate reduced density matrix of qubit 1
    rho = np.outer(bell_statevector, bell_statevector.conj())
    rho_1 = np.array([
        [rho[0, 0] + rho[1, 1], rho[0, 2] + rho[1, 3]],
        [rho[2, 0] + rho[3, 1], rho[2, 2] + rho[3, 3]]
    ])
    
    purity = np.real(np.trace(rho_1 @ rho_1))
    print(f"Purity of qubit 1: {purity:.4f}")
    print("Expected: 0.5 (maximally mixed due to entanglement)")

def create_quantum_repeater_circuit():
    """
    Create a quantum repeater circuit (extended teleportation).
    
    Returns:
        QuantumCircuit: The quantum repeater circuit
    """
    # Create a 5-qubit circuit for quantum repeater
    qc = QuantumCircuit(5, 3)
    
    # Prepare initial state on qubit 0
    qc.h(0)
    
    # Create Bell states between qubits (1,2) and (3,4)
    qc.h(1)
    qc.cx(1, 2)
    qc.h(3)
    qc.cx(3, 4)
    
    # First teleportation: qubit 0 to qubit 2
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
    
    # Apply corrections to qubit 2
    qc.x(2).c_if(1, 1)
    qc.z(2).c_if(0, 1)
    
    # Second teleportation: qubit 2 to qubit 4
    qc.cx(2, 3)
    qc.h(2)
    qc.measure([2, 3], [2, 2])  # Use classical bit 2 for second measurement
    
    # Apply corrections to qubit 4
    qc.x(4).c_if(2, 1)
    qc.z(4).c_if(0, 1)  # Use first measurement result for Z correction
    
    # Measure final qubit
    qc.measure(4, 2)
    
    return qc

if __name__ == "__main__":
    analyze_teleportation()
    demonstrate_entanglement()
    
    print("\n" + "="*50)
    print("Quantum Repeater Circuit")
    print("="*50)
    
    # Create and simulate quantum repeater
    qc_repeater = create_quantum_repeater_circuit()
    backend = Aer.get_backend('aer_simulator')
    job = execute(qc_repeater, backend, shots=1000)
    result = job.result()
    counts_repeater = result.get_counts(qc_repeater)
    
    print(f"Quantum repeater measurement counts: {counts_repeater}")
    print("This demonstrates teleportation over a longer distance using entanglement swapping")
