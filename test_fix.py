#!/usr/bin/env python3
"""
Test script to verify that the measurement issue is fixed.
"""

from quantum_core import QuantumStateAnalyzer

def test_circuit_with_measurements():
    """Test that circuits with measurements can be simulated."""
    print("Testing circuit with measurements...")
    
    # Create analyzer
    analyzer = QuantumStateAnalyzer()
    
    # Create a simple circuit with measurements
    analyzer.create_circuit(2)
    analyzer.add_gate('h', 0)
    analyzer.add_gate('cx', 0, 1)
    
    # Add measurements
    analyzer.circuit.measure(0, 0)
    analyzer.circuit.measure(1, 1)
    
    print(f"Circuit created: {analyzer.circuit}")
    print(f"Circuit has measurements: {any(inst.name == 'measure' for inst, _, _ in analyzer.circuit.data)}")
    
    # Try to simulate
    try:
        results = analyzer.simulate_circuit(shots=100)
        print("✅ Simulation successful!")
        statevector = results.get('statevector')
        if statevector is not None:
            print(f"Statevector length: {len(statevector)}")
        else:
            print("Statevector: None (not available)")
        print(f"Counts: {results.get('counts', {})}")
        print(f"Partial traces: {len(results.get('partial_traces', []))}")
        return True
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        return False

def test_circuit_without_measurements():
    """Test that circuits without measurements work normally."""
    print("\nTesting circuit without measurements...")
    
    # Create analyzer
    analyzer = QuantumStateAnalyzer()
    
    # Create a simple circuit without measurements
    analyzer.create_circuit(2)
    analyzer.add_gate('h', 0)
    analyzer.add_gate('cx', 0, 1)
    
    print(f"Circuit created: {analyzer.circuit}")
    print(f"Circuit has measurements: {any(inst.name == 'measure' for inst, _, _ in analyzer.circuit.data)}")
    
    # Try to simulate
    try:
        results = analyzer.simulate_circuit(shots=100)
        print("✅ Simulation successful!")
        statevector = results.get('statevector')
        if statevector is not None:
            print(f"Statevector length: {len(statevector)}")
        else:
            print("Statevector: None (not available)")
        print(f"Counts: {results.get('counts', {})}")
        print(f"Partial traces: {len(results.get('partial_traces', []))}")
        return True
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        return False

if __name__ == "__main__":
    print("🔬 Testing QTrace measurement fix...")
    print("=" * 50)
    
    success1 = test_circuit_with_measurements()
    success2 = test_circuit_without_measurements()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 All tests passed! The measurement issue is fixed.")
    else:
        print("❌ Some tests failed. Check the error messages above.")
