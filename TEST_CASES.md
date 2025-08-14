# QTrace Test Cases

This document contains 10 test cases to verify that QTrace is working correctly. Each test case includes the circuit setup, expected outputs, and verification steps.

## Test Case 1: Single Qubit - Hadamard Gate
**Circuit**: Single qubit with H gate
**Input**: 
- Number of qubits: 1
- Gates: H(0)
**Expected Output**:
- State vector: [0.7071, 0.7071] (approximately)
- Bloch sphere: Point on equator (x=1, y=0, z=0)
- Purity: 1.0 (pure state)
- Measurement counts: Roughly 50% |0⟩, 50% |1⟩

**Verification**: 
- Check that the Bloch sphere shows a point on the equator
- Verify purity is exactly 1.0
- Confirm measurement distribution is roughly equal

## Test Case 2: Bell State (2-Qubit Entanglement)
**Circuit**: 2 qubits with H(0) + CX(0,1)
**Input**:
- Number of qubits: 2
- Gates: H(0), CX(0,1)
**Expected Output**:
- State vector: [0.7071, 0, 0, 0.7071] (approximately)
- Qubit 0: Mixed state (purity = 0.5)
- Qubit 1: Mixed state (purity = 0.5)
- Bloch spheres: Both show mixed states (red coloring)
- Measurement counts: Only |00⟩ and |11⟩ (no |01⟩ or |10⟩)

**Verification**:
- Both qubits should show red coloring (mixed states)
- Purity should be exactly 0.5 for both qubits
- Only |00⟩ and |11⟩ outcomes should appear

## Test Case 3: GHZ State (3-Qubit Entanglement)
**Circuit**: 3 qubits with H(0) + CX(0,1) + CX(1,2)
**Input**:
- Number of qubits: 3
- Gates: H(0), CX(0,1), CX(1,2)
**Expected Output**:
- State vector: [0.7071, 0, 0, 0, 0, 0, 0, 0.7071]
- All qubits: Mixed states (purity = 0.5)
- Measurement counts: Only |000⟩ and |111⟩

**Verification**:
- All three qubits should show red coloring
- Purity should be 0.5 for all qubits
- Only |000⟩ and |111⟩ outcomes

## Test Case 4: Quantum Teleportation
**Circuit**: 3 qubits with specific teleportation protocol
**Input**:
- Number of qubits: 3
- Gates: X(0), H(1), CX(1,2), CX(0,1), H(0)
**Expected Output**:
- Initial state: |1⟩ on qubit 0
- Final state: Teleported |1⟩ on qubit 2
- Measurement pattern: Various combinations due to protocol

**Verification**:
- Check that the final state on qubit 2 matches the initial state on qubit 0
- Verify entanglement between qubits 1 and 2

## Test Case 5: Rotation Gates
**Circuit**: Single qubit with rotation gates
**Input**:
- Number of qubits: 1
- Gates: RX(π/4, 0), RY(π/3, 0)
**Expected Output**:
- State vector: Complex values depending on rotation angles
- Bloch sphere: Point not on standard axes
- Purity: 1.0 (pure state)

**Verification**:
- Bloch sphere should show a point not aligned with X, Y, or Z axes
- Purity should remain 1.0

## Test Case 6: SWAP Gate
**Circuit**: 2 qubits with SWAP operation
**Input**:
- Number of qubits: 2
- Gates: X(0), SWAP(0,1)
**Expected Output**:
- Initial: |10⟩ (qubit 0 in |1⟩, qubit 1 in |0⟩)
- Final: |01⟩ (qubits swapped)
- Both qubits: Pure states (purity = 1.0)

**Verification**:
- Check that the qubits have swapped states
- Both should show green coloring (pure states)

## Test Case 7: Phase Gates
**Circuit**: Single qubit with phase gates
**Input**:
- Number of qubits: 1
- Gates: H(0), S(0), T(0)
**Expected Output**:
- State vector: Complex values with specific phases
- Bloch sphere: Point with specific phase relationship
- Purity: 1.0

**Verification**:
- Phase relationships should be preserved
- Bloch sphere should show the correct phase

## Test Case 8: Controlled Gates
**Circuit**: 2 qubits with various controlled gates
**Input**:
- Number of qubits: 2
- Gates: X(0), CY(0,1), CZ(0,1)
**Expected Output**:
- Qubit 0: Pure state |1⟩
- Qubit 1: Mixed state due to entanglement
- Purity: Qubit 0 = 1.0, Qubit 1 < 1.0

**Verification**:
- Qubit 0 should be green (pure)
- Qubit 1 should be red (mixed)
- Check that controlled operations work correctly

## Test Case 9: OpenQASM Import
**Circuit**: Load from OpenQASM string
**Input**:
```qasm
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
```
**Expected Output**:
- Bell state circuit loaded correctly
- Same results as Test Case 2
- Circuit diagram should display properly

**Verification**:
- Circuit should load without errors
- Results should match manual Bell state creation
- Circuit diagram should be visible

## Test Case 10: Step-by-Step Evolution
**Circuit**: Any multi-gate circuit (e.g., Bell state)
**Input**:
- Use the step-by-step navigation feature
**Expected Output**:
- State history for each gate application
- Bloch sphere evolution visible
- Purity changes trackable

**Verification**:
- Each step should show the correct gate applied
- Bloch spheres should evolve step by step
- State information should be available for each step

## How to Run Tests

1. **Start QTrace**: Run `streamlit run app.py`
2. **Navigate to Circuit Builder**: Use the sidebar to go to Circuit Builder page
3. **Create Circuits**: Use the UI to build each test circuit
4. **Run Simulation**: Click "Run Simulation" button
5. **Check Results**: Verify outputs match expected results
6. **Use Quick Circuits**: Some test cases have quick circuit buttons

## Expected Behaviors

- **Pure States**: Should show green coloring on Bloch spheres
- **Mixed States**: Should show red coloring on Bloch spheres
- **Entanglement**: Should reduce individual qubit purity
- **Measurements**: Should show correct probability distributions
- **Visualizations**: All plots should render without errors
- **Export**: Download buttons should work for all data types

## Troubleshooting

If any test fails:
1. Check the browser console for JavaScript errors
2. Verify all dependencies are installed correctly
3. Ensure Qiskit version compatibility
4. Check that the circuit was created correctly
5. Verify simulation parameters (shots, etc.)

## Success Criteria

All test cases should:
- Execute without errors
- Produce correct quantum states
- Display accurate visualizations
- Allow proper navigation between features
- Support data export functionality
