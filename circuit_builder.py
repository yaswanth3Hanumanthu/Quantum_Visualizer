"""
Circuit Builder Module for QTrace
Provides a user-friendly interface for building quantum circuits.
"""

import streamlit as st
from typing import Dict, List, Tuple, Optional
from quantum_core import QuantumStateAnalyzer

class CircuitBuilder:
    """Interactive circuit builder interface for QTrace."""
    
    def __init__(self, analyzer: QuantumStateAnalyzer):
        """
        Initialize the circuit builder.
        
        Args:
            analyzer: QuantumStateAnalyzer instance
        """
        self.analyzer = analyzer
        self.available_gates = {
            'Single Qubit': ['h', 'x', 'y', 'z', 's', 'sdg', 't', 'tdg'],
            'Rotation': ['rx', 'ry', 'rz'],
            'Two Qubit': ['cx', 'cy', 'cz', 'swap']
        }
    
    def render_circuit_builder(self) -> bool:
        """
        Render the circuit builder interface.
        
        Returns:
            True if circuit was modified, False otherwise
        """
        st.subheader("🔧 Circuit Builder")
        
        # Circuit setup
        col1, col2 = st.columns(2)
        
        with col1:
            num_qubits = st.number_input(
                "Number of Qubits",
                min_value=1,
                max_value=10,
                value=2,
                help="Select the number of qubits for your circuit"
            )
            
            if st.button("Create New Circuit", type="primary"):
                self.analyzer.create_circuit(num_qubits)
                st.success(f"Created circuit with {num_qubits} qubits!")
                return True
        
        with col2:
            if self.analyzer.circuit is not None:
                st.info(f"Current circuit: {self.analyzer.circuit.num_qubits} qubits, "
                       f"depth {self.analyzer.circuit.depth()}")
                
                if st.button("Reset Circuit"):
                    self.analyzer.reset_circuit()
                    st.success("Circuit reset!")
                    return True
        
        # Gate selection and application
        if self.analyzer.circuit is not None:
            st.markdown("---")
            self._render_gate_selector()
            
            # Show current circuit
            st.markdown("### Current Circuit")
            if self.analyzer.circuit.depth() > 0:
                circuit_info = self.analyzer.get_circuit_info()
                st.json(circuit_info)
            else:
                st.info("No gates added yet. Use the gate selector above to build your circuit.")
        
        return False
    
    def _render_gate_selector(self):
        """Render the gate selection and application interface."""
        st.markdown("#### Add Gates")
        
        # Gate type selection
        gate_type = st.selectbox(
            "Gate Type",
            list(self.available_gates.keys()),
            help="Select the type of quantum gate to add"
        )
        
        gates = self.available_gates[gate_type]
        
        # Gate selection
        gate_name = st.selectbox(
            "Select Gate",
            gates,
            help="Choose the specific gate to apply"
        )
        
        # Qubit selection
        col1, col2 = st.columns(2)
        
        with col1:
            if gate_type == "Two Qubit":
                control_qubit = st.selectbox(
                    "Control Qubit",
                    range(self.analyzer.circuit.num_qubits),
                    help="Select the control qubit"
                )
                target_qubit = st.selectbox(
                    "Target Qubit",
                    [i for i in range(self.analyzer.circuit.num_qubits) if i != control_qubit],
                    help="Select the target qubit"
                )
            else:
                qubit = st.selectbox(
                    "Target Qubit",
                    range(self.analyzer.circuit.num_qubits),
                    help="Select the qubit to apply the gate to"
                )
        
        with col2:
            # Angle input for rotation gates
            angle = None
            if gate_type == "Rotation":
                angle = st.number_input(
                    "Rotation Angle (radians)",
                    min_value=0.0,
                    max_value=2*3.14159,
                    value=3.14159/2,
                    step=0.1,
                    help="Enter the rotation angle in radians"
                )
            
            # Add gate button
            if st.button("Add Gate", type="secondary"):
                success = False
                
                if gate_type == "Two Qubit":
                    success = self.analyzer.add_gate(
                        gate_name, control_qubit, target_qubit
                    )
                else:
                    success = self.analyzer.add_gate(
                        gate_name, qubit, angle=angle
                    )
                
                if success:
                    st.success(f"Added {gate_name} gate successfully!")
                else:
                    st.error(f"Failed to add {gate_name} gate. Please check your parameters.")
    
    def render_openqasm_uploader(self) -> bool:
        """
        Render the OpenQASM file upload interface.
        
        Returns:
            True if circuit was loaded, False otherwise
        """
        st.markdown("---")
        st.subheader("📁 Load OpenQASM Circuit")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose an OpenQASM file",
            type=['qasm', 'txt'],
            help="Upload an OpenQASM circuit file"
        )
        
        if uploaded_file is not None:
            try:
                qasm_content = uploaded_file.read().decode("utf-8")
                st.text_area("OpenQASM Content", qasm_content, height=150)
                
                if st.button("Load Circuit"):
                    if self.analyzer.load_openqasm(qasm_content):
                        st.success("Circuit loaded successfully from OpenQASM!")
                        return True
                    else:
                        st.error("Failed to load circuit. Please check the OpenQASM format.")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        
        # Direct input
        st.markdown("#### Or paste OpenQASM directly:")
        qasm_text = st.text_area(
            "OpenQASM Code",
            height=200,
            placeholder="OPENQASM 2.0;\ninclude \"qelib1.inc\";\n\nqreg q[2];\nh q[0];\ncx q[0],q[1];"
        )
        
        if st.button("Load from Text"):
            if qasm_text.strip():
                if self.analyzer.load_openqasm(qasm_text):
                    st.success("Circuit loaded successfully from text!")
                    return True
                else:
                    st.error("Failed to load circuit. Please check the OpenQASM format.")
            else:
                st.warning("Please enter some OpenQASM code.")
        
        return False
    
    def render_quick_circuits(self) -> bool:
        """
        Render quick circuit templates.
        
        Returns:
            True if circuit was created, False otherwise
        """
        st.markdown("---")
        st.subheader("⚡ Quick Circuit Templates")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Bell State", help="Create a Bell state (|00⟩ + |11⟩)/√2"):
                self._create_bell_state()
                return True
        
        with col2:
            if st.button("GHZ State", help="Create a GHZ state (|000⟩ + |111⟩)/√2"):
                self._create_ghz_state()
                return True
        
        with col3:
            if st.button("Quantum Teleportation", help="Create a quantum teleportation circuit"):
                self._create_teleportation_circuit()
                return True
        
        return False
    
    def _create_bell_state(self):
        """Create a Bell state circuit."""
        self.analyzer.create_circuit(2)
        self.analyzer.add_gate('h', 0)
        self.analyzer.add_gate('cx', 0, 1)
        st.success("Bell state circuit created! (H on q[0], CNOT with q[0] control, q[1] target)")
    
    def _create_ghz_state(self):
        """Create a GHZ state circuit."""
        self.analyzer.create_circuit(3)
        self.analyzer.add_gate('h', 0)
        self.analyzer.add_gate('cx', 0, 1)
        self.analyzer.add_gate('cx', 1, 2)
        st.success("GHZ state circuit created! (H on q[0], CNOT chain)")
    
    def _create_teleportation_circuit(self):
        """Create a quantum teleportation circuit."""
        self.analyzer.create_circuit(3)
        # Create Bell state between q[1] and q[2]
        self.analyzer.add_gate('h', 1)
        self.analyzer.add_gate('cx', 1, 2)
        # Teleport q[0] to q[2]
        self.analyzer.add_gate('cx', 0, 1)
        self.analyzer.add_gate('h', 0)
        st.success("Quantum teleportation circuit created!")
    
    def render_circuit_operations(self) -> bool:
        """
        Render circuit operation controls.
        
        Returns:
            True if circuit was modified, False otherwise
        """
        if self.analyzer.circuit is None:
            return False
        
        st.markdown("---")
        st.subheader("⚙️ Circuit Operations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Add Measurement", help="Add measurement gates to all qubits"):
                for i in range(self.analyzer.circuit.num_qubits):
                    self.analyzer.circuit.measure(i, i)
                st.success("Measurement gates added!")
                return True
        
        with col2:
            if st.button("Optimize Circuit", help="Optimize the circuit using Qiskit transpiler"):
                try:
                    from qiskit import transpile
                    optimized = transpile(self.analyzer.circuit, optimization_level=2)
                    self.analyzer.circuit = optimized
                    st.success("Circuit optimized!")
                    return True
                except Exception as e:
                    st.error(f"Optimization failed: {str(e)}")
        
        with col3:
            if st.button("Clear Circuit", help="Remove all gates from the circuit"):
                self.analyzer.reset_circuit()
                st.success("Circuit cleared!")
                return True
        
        return False
    
    def get_circuit_summary(self) -> Dict:
        """
        Get a summary of the current circuit.
        
        Returns:
            Dictionary containing circuit summary information
        """
        if self.analyzer.circuit is None:
            return {}
        
        circuit_info = self.analyzer.get_circuit_info()
        
        summary = {
            'num_qubits': circuit_info.get('num_qubits', 0),
            'depth': circuit_info.get('depth', 0),
            'total_gates': sum(circuit_info.get('gate_counts', {}).values()),
            'gate_breakdown': circuit_info.get('gate_counts', {}),
            'has_measurements': any('measure' in str(inst) for inst in circuit_info.get('instructions', []))
        }
        
        return summary
