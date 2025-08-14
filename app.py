"""
QTrace - Quantum State Visualizer
Main Streamlit application for quantum circuit simulation and visualization.
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import io

# Import our custom modules
from quantum_core import QuantumStateAnalyzer
from visualization import QuantumVisualizer
from circuit_builder import CircuitBuilder
import utils

# Page configuration
st.set_page_config(
    page_title="QTrace - Quantum State Visualizer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern, clean CSS with high contrast and white background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;500&display=swap');
    
    /* Global reset and clean background */
    .main .block-container {
        background: linear-gradient(135deg, #f5f5f5 0%, #eeeeee 50%, #e8e8e8 100%);
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
        min-height: 100vh;
    }
    
    /* Enhanced header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #2563eb, #7c3aed, #dc2626);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #64748b;
        font-weight: 400;
        margin-bottom: 3rem;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Section headers */
    .sub-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1.5rem;
        font-family: 'Poppins', sans-serif;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
        display: inline-block;
    }
    
    /* Professional cards */
    .content-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .content-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #3b82f6;
        background: rgba(255, 255, 255, 0.98);
    }
    
    /* Status boxes with clear colors */
    .info-box {
        background: rgba(239, 246, 255, 0.9);
        border: 1px solid #93c5fd;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: #1e40af;
        font-weight: 500;
        backdrop-filter: blur(5px);
    }
    
    .success-box {
        background: rgba(240, 253, 244, 0.9);
        border: 1px solid #86efac;
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: #166534;
        font-weight: 500;
        backdrop-filter: blur(5px);
    }
    
    .warning-box {
        background: rgba(255, 251, 235, 0.9);
        border: 1px solid #fed7aa;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: #92400e;
        font-weight: 500;
        backdrop-filter: blur(5px);
    }
    
    /* Modern buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        background: linear-gradient(135deg, #2563eb, #5b21b6);
    }
    
    /* Sidebar clean styling */
    .stSidebar {
        background: linear-gradient(180deg, rgba(248, 250, 252, 0.95) 0%, rgba(241, 245, 249, 0.95) 100%);
        border-right: 1px solid #e2e8f0;
        backdrop-filter: blur(10px);
    }
    
    .stSidebar h2 {
        color: #1e293b !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        color: #1e293b;
        padding: 0.75rem;
        font-size: 0.95rem;
        transition: border-color 0.2s ease;
        backdrop-filter: blur(5px);
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6;
        outline: none;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        color: #1e293b;
        backdrop-filter: blur(5px);
    }
    
    /* DataFrames with clean styling */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
    }
    
    .stDataFrame table {
        background: rgba(255, 255, 255, 0.9);
        color: #1e293b;
        font-family: 'Source Code Pro', monospace;
    }
    
    .stDataFrame thead tr th {
        background: rgba(241, 245, 249, 0.95);
        color: #475569;
        font-weight: 600;
        border-bottom: 2px solid #e2e8f0;
        padding: 1rem 0.75rem;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background: rgba(248, 250, 252, 0.5);
    }
    
    .stDataFrame tbody tr:hover {
        background: rgba(224, 242, 254, 0.7);
    }
    
    /* Metrics styling */
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
    }
    
    .stMetric > div {
        color: #1e293b;
    }
    
    .stMetric label {
        color: #64748b;
        font-weight: 500;
    }
    
    /* Text styling */
    .stMarkdown, .stText, p, li, span {
        color: #374151 !important;
        font-family: 'Poppins', sans-serif;
        line-height: 1.6;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #1e293b !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    .stMarkdown strong {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    /* Code blocks */
    .stCode {
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        font-family: 'Source Code Pro', monospace;
        color: #374151;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #6366f1);
        border-radius: 6px;
    }
    
    /* Quantum badges */
    .quantum-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem 0.25rem 0.25rem 0;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        color: #1e293b;
        font-weight: 500;
    }
    
    /* Alert improvements */
    .stAlert {
        border-radius: 8px;
        border-width: 1px;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Navigation styling */
    .stSelectbox label {
        color: #1e293b !important;
        font-weight: 500;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Plotly containers */
    .js-plotly-plot {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* Clean scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Initialize session state
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = QuantumStateAnalyzer()
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = QuantumVisualizer()
    if 'circuit_builder' not in st.session_state:
        st.session_state.circuit_builder = CircuitBuilder(st.session_state.analyzer)
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = {}
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    
    # Header
    st.markdown('<h1 class="main-header">🔬 QTrace</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Quantum State Visualizer & Circuit Analysis Platform</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 style="color: #1e293b; font-family: Poppins, sans-serif; font-weight: 600;">🎛️ Navigation</h2>', unsafe_allow_html=True)
        
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Home", "🔧 Circuit Builder", "⚡ Simulation", "📊 Visualization", "📈 Step-by-Step", "💾 Export", "ℹ️ About"]
        )
        
        st.markdown("---")
        
        # Quick actions
        if st.button("🚀 Quick Demo", type="primary"):
            st.session_state.circuit_builder._create_bell_state()
            st.session_state.simulation_results = st.session_state.analyzer.simulate_circuit()
            st.rerun()
        
        if st.button("🔄 Reset All"):
            st.session_state.analyzer.reset_circuit()
            st.session_state.simulation_results = {}
            st.session_state.current_step = 0
            st.rerun()
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔧 Circuit Builder":
        show_circuit_builder_page()
    elif page == "⚡ Simulation":
        show_simulation_page()
    elif page == "📊 Visualization":
        show_visualization_page()
    elif page == "📈 Step-by-Step":
        show_step_by_step_page()
    elif page == "💾 Export":
        show_export_page()
    elif page == "ℹ️ About":
        show_about_page()

def show_home_page():
    """Display the home page with overview and quick start."""
    st.markdown('<h2 class="sub-header">Welcome to QTrace!</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("""
        **QTrace** is a powerful quantum computing visualization tool that allows you to:
        
        - 🔧 **Build quantum circuits** using an intuitive interface
        - ⚡ **Simulate quantum states** with Qiskit Aer
        - 📊 **Visualize quantum states** on interactive Bloch spheres
        - 📈 **Track state evolution** step-by-step through your circuit
        - 💾 **Export results** in multiple formats
        
        Perfect for learning quantum computing, research, and hackathon projects!
        """)
        
        # Quick start section
        st.markdown("### 🚀 Quick Start")
        
        if st.button("Create Bell State Circuit", type="primary"):
            st.session_state.circuit_builder._create_bell_state()
            st.session_state.simulation_results = st.session_state.analyzer.simulate_circuit()
            st.success("Bell state circuit created and simulated!")
            st.rerun()
        
        if st.button("Create GHZ State Circuit", type="secondary"):
            st.session_state.circuit_builder._create_ghz_state()
            st.session_state.simulation_results = st.session_state.analyzer.simulate_circuit()
            st.success("GHZ state circuit created and simulated!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Current Status")
        
        if st.session_state.analyzer.circuit is not None:
            circuit_info = st.session_state.analyzer.get_circuit_info()
            st.markdown(f"""
            <div class="info-box">
            <strong>Circuit Information:</strong><br/>
            🔹 Qubits: <span class="quantum-badge">{circuit_info.get('num_qubits', 0)}</span><br/>
            🔹 Depth: <span class="quantum-badge">{circuit_info.get('depth', 0)}</span><br/>
            🔹 Gates: <span class="quantum-badge">{sum(circuit_info.get('gate_counts', {}).values())}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ No circuit created yet</div>', unsafe_allow_html=True)
        
        if st.session_state.simulation_results:
            st.markdown('<div class="success-box">✅ Simulation completed!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">ℹ️ No simulation results yet</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent examples
    st.markdown("### 📚 Example Circuits")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("**🔗 Bell State**")
        st.markdown("Creates the entangled state (|00⟩ + |11⟩)/√2")
        if st.button("Try Bell State", key="bell_home"):
            st.session_state.circuit_builder._create_bell_state()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("**🌐 GHZ State**")
        st.markdown("Creates the three-qubit entangled state (|000⟩ + |111⟩)/√2")
        if st.button("Try GHZ State", key="ghz_home"):
            st.session_state.circuit_builder._create_ghz_state()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("**🚀 Quantum Teleportation**")
        st.markdown("Demonstrates quantum teleportation protocol")
        if st.button("Try Teleportation", key="tele_home"):
            st.session_state.circuit_builder._create_teleportation_circuit()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def show_circuit_builder_page():
    """Display the circuit builder page."""
    st.markdown('<h2 class="sub-header">🔧 Circuit Builder</h2>', unsafe_allow_html=True)
    
    # Circuit builder interface
    circuit_modified = st.session_state.circuit_builder.render_circuit_builder()
    
    if circuit_modified:
        st.rerun()
    
    # OpenQASM uploader
    st.session_state.circuit_builder.render_openqasm_uploader()
    
    # Quick circuit templates
    st.session_state.circuit_builder.render_quick_circuits()
    
    # Circuit operations
    st.session_state.circuit_builder.render_circuit_operations()
    
    # Check if circuit has measurements and show warning
    if st.session_state.analyzer.circuit is not None:
        circuit_info = st.session_state.analyzer.get_circuit_info()
        has_measurements = any('measure' in str(inst) for inst in circuit_info.get('instructions', []))
        
        if has_measurements:
            st.warning("""
            ⚠️ **Circuit contains measurement operations!**
            
            **Note**: Circuits with measurements can still be simulated for measurement counts, 
            but the statevector visualization will show the state before measurements.
            
            **Tip**: For full state analysis, consider removing measurements or using the 
            "Clear Circuit" button to start fresh.
            """)
    
    # Circuit diagram display
    if st.session_state.analyzer.circuit is not None and st.session_state.analyzer.circuit.depth() > 0:
        st.markdown("### 📐 Circuit Diagram")
        
        try:
            # Create circuit diagram
            circuit_diagram = st.session_state.visualizer.create_circuit_diagram(
                st.session_state.analyzer.circuit
            )
            
            if circuit_diagram:
                st.image(f"data:image/png;base64,{circuit_diagram}", 
                        caption="Quantum Circuit Diagram", use_column_width=True)
            else:
                st.info("Circuit diagram could not be generated")
        except Exception as e:
            st.error(f"Error generating circuit diagram: {str(e)}")

def show_simulation_page():
    """Display the simulation page."""
    st.markdown('<h2 class="sub-header">⚡ Quantum Simulation</h2>', unsafe_allow_html=True)
    
    if st.session_state.analyzer.circuit is None:
        st.warning("⚠️ Please create a circuit first in the Circuit Builder page.")
        return
    
    # Simulation controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        shots = st.number_input(
            "Number of Shots",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            help="Number of simulation runs"
        )
    
    with col2:
        if st.button("🚀 Run Simulation", type="primary"):
            with st.spinner("Running quantum simulation..."):
                st.session_state.simulation_results = st.session_state.analyzer.simulate_circuit(shots)
            st.success("Simulation completed!")
            st.rerun()
    
    with col3:
        if st.session_state.simulation_results:
            st.success("✅ Simulation Results Available")
        else:
            st.info("⏳ No simulation results yet")
    
    # Display simulation results
    if st.session_state.simulation_results:
        if 'error' in st.session_state.simulation_results:
            st.error(f"Simulation error: {st.session_state.simulation_results['error']}")
            return
        
        # Results summary
        st.markdown("### 📊 Simulation Results")
        
        summary_df = utils.create_results_summary(st.session_state.simulation_results)
        if not summary_df.empty:
            st.dataframe(summary_df, use_container_width=True)
        
        # Measurement results
        if 'counts' in st.session_state.simulation_results:
            st.markdown("### 📈 Measurement Results")
            
            counts = st.session_state.simulation_results['counts']
            histogram = st.session_state.visualizer.create_measurement_histogram(counts)
            st.plotly_chart(histogram, use_container_width=True)
            
            # Detailed counts table
            counts_df = pd.DataFrame([
                {'Outcome': outcome, 'Count': count, 'Probability': f"{count/sum(counts.values):.4f}"}
                for outcome, count in counts.items()
            ])
            st.dataframe(counts_df, use_container_width=True)
        
        # State vector information
        if 'statevector' in st.session_state.simulation_results and st.session_state.simulation_results['statevector'] is not None:
            st.markdown("### 🔬 Quantum State Information")
            utils.display_quantum_state_info(
                st.session_state.simulation_results['statevector']
            )
        elif 'has_measurements' in st.session_state.simulation_results and st.session_state.simulation_results['has_measurements']:
            st.warning("""
            ⚠️ **Statevector not available**
            
            This circuit contains measurement operations, which prevents us from accessing the full quantum state.
            However, you can still see:
            - ✅ Measurement counts and probabilities
            - ✅ Circuit statistics
            - ✅ Basic simulation results
            
            **To get full state analysis**: Remove measurements or create a new circuit without them.
            """)
        else:
            st.info("ℹ️ No statevector information available for this simulation.")

def show_visualization_page():
    """Display the visualization page."""
    st.markdown('<h2 class="sub-header">📊 Quantum State Visualization</h2>', unsafe_allow_html=True)
    
    if not st.session_state.simulation_results or 'error' in st.session_state.simulation_results:
        st.warning("⚠️ Please run a simulation first to see visualizations.")
        return
    
    # Bloch sphere visualizations
    if 'partial_traces' in st.session_state.simulation_results and st.session_state.simulation_results['partial_traces']:
        partial_traces = st.session_state.simulation_results['partial_traces']
        
        st.markdown("### 🌐 Bloch Sphere Visualizations")
        
        # Individual Bloch spheres
        st.markdown("#### Individual Qubit States")
        
        num_qubits = len(partial_traces)
        cols = min(3, num_qubits)
        rows = (num_qubits + cols - 1) // cols
        
        for i in range(num_qubits):
            with st.container():
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    bloch_sphere = st.session_state.visualizer.create_bloch_sphere(
                        partial_traces[i], i
                    )
                    st.plotly_chart(bloch_sphere, use_container_width=True)
                
                with col2:
                    # Qubit analysis
                    purity = st.session_state.analyzer.get_purity(partial_traces[i])
                    x, y, z = st.session_state.analyzer.get_bloch_coordinates(partial_traces[i])
                    
                    st.markdown(f"**Qubit {i} Analysis:**")
                    st.metric("Purity", f"{purity:.4f}")
                    st.metric("X Coordinate", f"{x:.4f}")
                    st.metric("Y Coordinate", f"{y:.4f}")
                    st.metric("Z Coordinate", f"{z:.4f}")
                    
                    if purity > 0.99:
                        st.success("Pure State")
                    elif purity > 0.5:
                        st.warning("Mixed State")
                    else:
                        st.error("Highly Mixed State")
        
        # Multi-qubit Bloch spheres
        st.markdown("#### Multi-Qubit Bloch Spheres")
        multi_bloch = st.session_state.visualizer.create_multiqubit_bloch_spheres(partial_traces)
        st.plotly_chart(multi_bloch, use_container_width=True)
        
        # Purity heatmap
        st.markdown("#### State Purity Analysis")
        purity_heatmap = st.session_state.visualizer.create_purity_heatmap(partial_traces)
        st.plotly_chart(purity_heatmap, use_container_width=True)
        
        # Qubit analysis table
        st.markdown("#### Detailed Qubit Analysis")
        analysis_df = utils.create_qubit_analysis_table(partial_traces)
        st.dataframe(analysis_df, use_container_width=True)
    else:
        st.warning("""
        ⚠️ **No Bloch sphere visualizations available**
        
        This usually happens when:
        - The circuit contains measurement operations
        - The simulation failed to produce a statevector
        - The circuit structure is incompatible
        
        **Tip**: Try creating a circuit without measurements, or use the "Clear Circuit" button to start fresh.
        """)
        
        # Show what information is available
        if 'counts' in st.session_state.simulation_results:
            st.info("✅ Measurement counts are available - you can still see the measurement results!")
        if 'has_measurements' in st.session_state.simulation_results and st.session_state.simulation_results['has_measurements']:
            st.info("ℹ️ This circuit contains measurements, which is why statevector analysis isn't available.")

def show_step_by_step_page():
    """Display the step-by-step analysis page."""
    st.markdown('<h2 class="sub-header">📈 Step-by-Step Analysis</h2>', unsafe_allow_html=True)
    
    if not st.session_state.simulation_results or 'error' in st.session_state.simulation_results:
        st.warning("⚠️ Please run a simulation first to see step-by-step analysis.")
        return
    
    # Check if state history exists and rebuild if needed
    if not st.session_state.analyzer.state_history:
        if st.session_state.analyzer.circuit is not None:
            st.info("🔄 Building state history for step-by-step analysis...")
            try:
                st.session_state.analyzer._build_state_history()
                if not st.session_state.analyzer.state_history:
                    st.warning("⚠️ Could not build state history. This may happen if the circuit contains only measurements or unsupported operations.")
                    return
            except Exception as e:
                st.error(f"❌ Error building state history: {str(e)}")
                return
        else:
            st.warning("⚠️ No circuit available. Please create and simulate a circuit first.")
            return
    
    # Step navigation
    total_steps = len(st.session_state.analyzer.state_history)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⏮️ Previous Step"):
            if st.session_state.current_step > 0:
                st.session_state.current_step -= 1
                st.rerun()
    
    with col2:
        st.markdown(f"**Step {st.session_state.current_step + 1} of {total_steps}**")
        progress = (st.session_state.current_step + 1) / total_steps
        st.progress(progress)
    
    with col3:
        if st.button("⏭️ Next Step"):
            if st.session_state.current_step < total_steps - 1:
                st.session_state.current_step += 1
                st.rerun()
    
    # Current step information
    current_step_data = st.session_state.analyzer.state_history[st.session_state.current_step]
    
    st.markdown(f"### 🔍 Step {st.session_state.current_step + 1}: {current_step_data['gate'].upper()} Gate")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Gate Applied:** {current_step_data['gate'].upper()}")
        st.markdown(f"**Target Qubits:** {current_step_data['qubits']}")
        
        # State evolution plot for first qubit
        if st.session_state.current_step > 0:
            evolution_plot = st.session_state.visualizer.create_state_evolution_plot(
                st.session_state.analyzer.state_history[:st.session_state.current_step + 1]
            )
            st.plotly_chart(evolution_plot, use_container_width=True)
    
    with col2:
        # Current state Bloch spheres
        if 'partial_traces' in current_step_data:
            partial_traces = current_step_data['partial_traces']
            
            st.markdown("**Current Qubit States:**")
            
            for i, density_matrix in enumerate(partial_traces):
                with st.expander(f"Qubit {i}"):
                    bloch_sphere = st.session_state.visualizer.create_bloch_sphere(
                        density_matrix, i, f"Qubit {i} at Step {st.session_state.current_step + 1}"
                    )
                    st.plotly_chart(bloch_sphere, use_container_width=True)
    
    # Step-by-step progress
    st.markdown("### 📊 Circuit Progress")
    
    steps_data = []
    for i, step_data in enumerate(st.session_state.analyzer.state_history):
        steps_data.append({
            'Step': i + 1,
            'Gate': step_data['gate'].upper(),
            'Qubits': str(step_data['qubits']),
            'Status': '✅' if i <= st.session_state.current_step else '⏳'
        })
    
    steps_df = pd.DataFrame(steps_data)
    st.dataframe(steps_df, use_container_width=True)

def show_export_page():
    """Display the export page."""
    st.markdown('<h2 class="sub-header">💾 Export Results</h2>', unsafe_allow_html=True)
    
    if not st.session_state.simulation_results or 'error' in st.session_state.simulation_results:
        st.warning("⚠️ Please run a simulation first to export results.")
        return
    
    # Export options
    st.markdown("### 📁 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Data Export")
        
        # Results summary
        if st.session_state.simulation_results:
            summary_df = utils.create_results_summary(st.session_state.simulation_results)
            if not summary_df.empty:
                utils.create_download_button(summary_df, "results_summary", "csv")
        
        # Qubit analysis
        if 'partial_traces' in st.session_state.simulation_results:
            analysis_df = utils.create_qubit_analysis_table(
                st.session_state.simulation_results['partial_traces']
            )
            if not analysis_df.empty:
                utils.create_download_button(analysis_df, "qubit_analysis", "csv")
        
        # Complete export package
        if st.session_state.analyzer.circuit is not None:
            export_package = utils.create_export_package(
                st.session_state.simulation_results,
                st.session_state.simulation_results.get('partial_traces', []),
                st.session_state.analyzer.get_circuit_info()
            )
            utils.create_download_button(export_package, "complete_export", "json")
    
    with col2:
        st.markdown("#### 🖼️ Visualization Export")
        
        # Information about export options
        st.info("""
        **Export Options:**
        - 🌐 **HTML**: Interactive plots (always available)
        - 📊 **PNG/PDF**: Static images (requires kaleido package)
        """)
        
        # Bloch sphere exports
        if 'partial_traces' in st.session_state.simulation_results:
            partial_traces = st.session_state.simulation_results['partial_traces']
            
            # Individual Bloch spheres
            st.markdown("**Individual Bloch Spheres:**")
            for i, density_matrix in enumerate(partial_traces):
                bloch_sphere = st.session_state.visualizer.create_bloch_sphere(density_matrix, i)
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    utils.create_download_button(bloch_sphere, f"bloch_sphere_qubit_{i}", "html")
                with col_b:
                    utils.create_download_button(bloch_sphere, f"bloch_sphere_qubit_{i}", "png")
                with col_c:
                    utils.create_download_button(bloch_sphere, f"bloch_sphere_qubit_{i}", "pdf")
            
            # Multi-qubit Bloch spheres
            st.markdown("**Multi-Qubit Visualization:**")
            multi_bloch = st.session_state.visualizer.create_multiqubit_bloch_spheres(partial_traces)
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                utils.create_download_button(multi_bloch, "multi_qubit_bloch_spheres", "html")
            with col_b:
                utils.create_download_button(multi_bloch, "multi_qubit_bloch_spheres", "png")
            with col_c:
                utils.create_download_button(multi_bloch, "multi_qubit_bloch_spheres", "pdf")
            
            # Purity heatmap
            st.markdown("**Purity Analysis:**")
            purity_heatmap = st.session_state.visualizer.create_purity_heatmap(partial_traces)
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                utils.create_download_button(purity_heatmap, "purity_heatmap", "html")
            with col_b:
                utils.create_download_button(purity_heatmap, "purity_heatmap", "png")
            with col_c:
                utils.create_download_button(purity_heatmap, "purity_heatmap", "pdf")
    
    # Export all at once
    st.markdown("### 🚀 Bulk Export")
    
    st.markdown("""
    **� Export Options Available:**
    
    **🌐 HTML Files (Always Available):**
    - Interactive 3D plots that work in any web browser
    - Can be shared, embedded, or opened offline
    - Full Plotly functionality preserved
    - Best for presentations and interactive analysis
    
    **📊 PNG/PDF Files (Requires kaleido):**
    - Static high-quality images
    - Perfect for papers and reports
    - Install with: `pip install kaleido`
    
    **💡 Tip:** HTML exports are a great alternative to static images!
    """)
    
    if st.button("📦 Export Everything", type="primary"):
        st.info("📋 All export options are available above. Use the individual download buttons to save specific files.")
        st.markdown("""
        **Quick Export Guide:**
        1. **Data Analysis**: Use CSV/JSON exports for data
        2. **Visualizations**: Use HTML exports (always work) or PNG/PDF (if kaleido installed)
        3. **Sharing**: HTML files can be opened in any web browser
        4. **Publications**: Try HTML first, then install kaleido for PNG/PDF if needed
        """)

def show_about_page():
    """Display the about page."""
    st.markdown('<h2 class="sub-header">ℹ️ About QTrace</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🔬 What is QTrace?
    
    **QTrace** is a comprehensive quantum computing visualization tool designed to help users understand 
    quantum states and their evolution through quantum circuits. It provides intuitive visualizations 
    of quantum states on Bloch spheres and offers step-by-step analysis of quantum circuit execution.
    
    ## 🚀 Key Features
    
    - **Circuit Builder**: Intuitive interface for creating quantum circuits
    - **State Simulation**: Run circuits using Qiskit Aer simulator
    - **Bloch Sphere Visualization**: Interactive 3D plots of quantum states
    - **Partial Trace Analysis**: Extract individual qubit states from multi-qubit systems
    - **Step-by-Step Evolution**: Watch quantum states evolve through your circuit
    - **Export Capabilities**: Save results in multiple formats (PNG, PDF, CSV, JSON)
    
    ## 🛠️ Technical Details
    
    - **Backend**: Qiskit for quantum circuit simulation
    - **Frontend**: Streamlit for interactive web interface
    - **Visualization**: Plotly for interactive 3D plots
    - **Analysis**: Custom algorithms for partial trace and state analysis
    
    ## 🎯 Use Cases
    
    - **Education**: Learn quantum computing concepts through visualization
    - **Research**: Analyze quantum states and circuit behavior
    - **Development**: Test and debug quantum algorithms
    - **Hackathons**: Quick prototyping and demonstration
    
    ## 🔧 Installation & Setup
    
    ```bash
    # Clone the repository
    git clone <your-repo-url>
    cd Quantum_Visualizer
    
    # Activate virtual environment
    .venv\\Scripts\\activate  # Windows
    source .venv/bin/activate  # Linux/Mac
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run the application
    streamlit run app.py
    ```
    
    ## 📚 Examples
    
    The application includes several example circuits:
    
    - **Bell State**: Demonstrates quantum entanglement
    - **GHZ State**: Multi-qubit entangled state
    - **Quantum Teleportation**: Complete teleportation protocol
    
    ## 🤝 Contributing
    
    This project is designed to be hackathon-friendly and welcomes contributions:
    
    - Add new quantum gates and algorithms
    - Improve the visualization interface
    - Add new export formats
    - Implement additional quantum features
    
    ## 📄 License
    
    MIT License - feel free to use this project for your hackathon!
    
    ## 🆘 Support
    
    If you encounter any issues or have questions:
    
    1. Check the documentation in the code
    2. Review the example circuits
    3. Ensure all dependencies are installed correctly
    4. Check that your quantum circuit is valid
    """)

if __name__ == "__main__":
    main()
