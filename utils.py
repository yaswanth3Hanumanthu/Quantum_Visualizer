"""
Utility Functions for QTrace
Helper functions for data processing, export, and common operations.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import io
import base64
from datetime import datetime
import json

def format_complex_number(complex_num: complex, precision: int = 3) -> str:
    """
    Format a complex number for display.
    
    Args:
        complex_num: Complex number to format
        precision: Number of decimal places
        
    Returns:
        Formatted string representation
    """
    if abs(complex_num.imag) < 1e-10:
        return f"{complex_num.real:.{precision}f}"
    elif abs(complex_num.real) < 1e-10:
        return f"{complex_num.imag:.{precision}f}i"
    else:
        return f"{complex_num.real:.{precision}f} + {complex_num.imag:.{precision}f}i"

def format_density_matrix(density_matrix: np.ndarray, precision: int = 3) -> str:
    """
    Format a density matrix for display.
    
    Args:
        density_matrix: 2x2 density matrix
        precision: Number of decimal places
        
    Returns:
        Formatted string representation
    """
    if density_matrix.shape != (2, 2):
        return "Invalid density matrix shape"
    
    formatted = "[["
    formatted += format_complex_number(density_matrix[0, 0], precision)
    formatted += ", "
    formatted += format_complex_number(density_matrix[0, 1], precision)
    formatted += "],\n ["
    formatted += format_complex_number(density_matrix[1, 0], precision)
    formatted += ", "
    formatted += format_complex_number(density_matrix[1, 1], precision)
    formatted += "]]"
    
    return formatted

def create_download_button(data: Any, filename: str, file_type: str = "txt") -> None:
    """
    Create a download button for various data types.
    
    Args:
        data: Data to download
        filename: Name of the file
        file_type: Type of file (txt, csv, json, png, pdf, html)
    """
    if file_type == "txt":
        if isinstance(data, str):
            st.download_button(
                label=f"📝 Download {filename}.txt",
                data=data,
                file_name=f"{filename}.txt",
                mime="text/plain"
            )
        else:
            st.download_button(
                label=f"📝 Download {filename}.txt",
                data=str(data),
                file_name=f"{filename}.txt",
                mime="text/plain"
            )
    
    elif file_type == "csv":
        if isinstance(data, pd.DataFrame):
            csv = data.to_csv(index=False)
            st.download_button(
                label=f"📊 Download {filename}.csv",
                data=csv,
                file_name=f"{filename}.csv",
                mime="text/csv"
            )
            st.success(f"✅ CSV export ready: {filename}.csv")
        else:
            st.error("❌ Data must be a pandas DataFrame for CSV export")
    
    elif file_type == "json":
        if isinstance(data, dict):
            json_str = json.dumps(data, indent=2, default=str)
            st.download_button(
                label=f"📋 Download {filename}.json",
                data=json_str,
                file_name=f"{filename}.json",
                mime="application/json"
            )
            st.success(f"✅ JSON export ready: {filename}.json")
        else:
            st.error("❌ Data must be a dictionary for JSON export")
    
    elif file_type == "png":
        if hasattr(data, 'to_image'):
            try:
                png_data = data.to_image(format="png", width=1200, height=800, scale=2)
                st.download_button(
                    label=f"📊 Download {filename}.png",
                    data=png_data,
                    file_name=f"{filename}.png",
                    mime="image/png"
                )
                st.success(f"✅ PNG export ready: {filename}.png")
            except Exception as e:
                if "kaleido" in str(e).lower():
                    # Alternative: Export as HTML
                    try:
                        html_str = data.to_html(include_plotlyjs='cdn')
                        st.download_button(
                            label=f"🌐 Download {filename}.html (Alternative)",
                            data=html_str,
                            file_name=f"{filename}.html",
                            mime="text/html"
                        )
                        st.warning("⚠️ PNG export not available. Downloaded as interactive HTML instead.")
                    except Exception as html_e:
                        st.error(f"❌ Export failed: {str(html_e)}")
                else:
                    st.error(f"❌ Failed to export PNG: {str(e)}")
        else:
            st.error("❌ Data must be a Plotly figure for PNG export")
    
    elif file_type == "pdf":
        if hasattr(data, 'to_image'):
            try:
                pdf_data = data.to_image(format="pdf", width=1200, height=800)
                st.download_button(
                    label=f"📄 Download {filename}.pdf",
                    data=pdf_data,
                    file_name=f"{filename}.pdf",
                    mime="application/pdf"
                )
                st.success(f"✅ PDF export ready: {filename}.pdf")
            except Exception as e:
                if "kaleido" in str(e).lower():
                    # Alternative: Export as HTML
                    try:
                        html_str = data.to_html(include_plotlyjs='cdn')
                        st.download_button(
                            label=f"🌐 Download {filename}.html (Alternative)",
                            data=html_str,
                            file_name=f"{filename}.html",
                            mime="text/html"
                        )
                        st.warning("⚠️ PDF export not available. Downloaded as interactive HTML instead.")
                    except Exception as html_e:
                        st.error(f"❌ Export failed: {str(html_e)}")
                else:
                    st.error(f"❌ Failed to export PDF: {str(e)}")
        else:
            st.error("❌ Data must be a Plotly figure for PDF export")
    
    elif file_type == "html":
        if hasattr(data, 'to_html'):
            try:
                html_str = data.to_html(include_plotlyjs='cdn')
                st.download_button(
                    label=f"🌐 Download {filename}.html",
                    data=html_str,
                    file_name=f"{filename}.html",
                    mime="text/html"
                )
                st.success(f"✅ Interactive HTML export ready: {filename}.html")
            except Exception as e:
                st.error(f"❌ Failed to export HTML: {str(e)}")
        else:
            st.error("❌ Data must be a Plotly figure for HTML export")

def create_results_summary(simulation_results: Dict) -> pd.DataFrame:
    """
    Create a summary DataFrame from simulation results.
    
    Args:
        simulation_results: Dictionary containing simulation results
        
    Returns:
        Pandas DataFrame with summary information
    """
    if not simulation_results or 'error' in simulation_results:
        return pd.DataFrame()
    
    summary_data = []
    
    # Circuit information
    summary_data.append({
        'Metric': 'Number of Qubits',
        'Value': simulation_results.get('num_qubits', 'N/A')
    })
    
    summary_data.append({
        'Metric': 'Circuit Depth',
        'Value': simulation_results.get('circuit_depth', 'N/A')
    })
    
    # Gate counts
    gate_counts = simulation_results.get('num_gates', {})
    for gate, count in gate_counts.items():
        summary_data.append({
            'Metric': f'{gate.upper()} Gates',
            'Value': count
        })
    
    # Measurement results
    counts = simulation_results.get('counts', {})
    if counts:
        total_shots = sum(counts.values())
        most_likely = max(counts, key=counts.get)
        summary_data.append({
            'Metric': 'Total Shots',
            'Value': total_shots
        })
        summary_data.append({
            'Metric': 'Most Likely Outcome',
            'Value': most_likely
        })
        summary_data.append({
            'Metric': 'Most Likely Probability',
            'Value': f"{counts[most_likely]/total_shots:.3f}"
        })
    
    return pd.DataFrame(summary_data)

def create_qubit_analysis_table(partial_traces: List[np.ndarray]) -> pd.DataFrame:
    """
    Create a table analyzing each qubit's state.
    
    Args:
        partial_traces: List of density matrices for each qubit
        
    Returns:
        Pandas DataFrame with qubit analysis
    """
    if not partial_traces:
        return pd.DataFrame()
    
    analysis_data = []
    
    for i, density_matrix in enumerate(partial_traces):
        # Calculate purity - convert DensityMatrix to numpy array if needed
        if hasattr(density_matrix, 'data'):
            dm = np.asarray(density_matrix.data)
        else:
            dm = np.asarray(density_matrix)
        purity = np.real(np.trace(dm @ dm))
        
        # Get Bloch coordinates
        x, y, z = _get_bloch_coordinates(density_matrix)
        
        # Determine state type
        if purity > 0.99:
            state_type = "Pure"
        elif purity > 0.5:
            state_type = "Mixed"
        else:
            state_type = "Highly Mixed"
        
        analysis_data.append({
            'Qubit': i,
            'Purity': f"{purity:.4f}",
            'X Coordinate': f"{x:.4f}",
            'Y Coordinate': f"{y:.4f}",
            'Z Coordinate': f"{z:.4f}",
            'State Type': state_type
        })
    
    return pd.DataFrame(analysis_data)

def _get_bloch_coordinates(density_matrix: np.ndarray) -> tuple:
    """Helper function to extract Bloch coordinates."""
    # Convert to numpy array if it's a Qiskit DensityMatrix object
    if hasattr(density_matrix, 'data'):
        dm = np.asarray(density_matrix.data)
    else:
        dm = np.asarray(density_matrix)
        
    sigma_x = np.array([[0, 1], [1, 0]])
    sigma_y = np.array([[0, -1j], [1j, 0]])
    sigma_z = np.array([[1, 0], [0, -1]])
    
    x = np.real(np.trace(dm @ sigma_x))
    y = np.real(np.trace(dm @ sigma_y))
    z = np.real(np.trace(dm @ sigma_z))
    
    return x, y, z

def create_export_package(simulation_results: Dict, partial_traces: List[np.ndarray],
                         circuit_info: Dict, filename_prefix: str = "qtrace_export") -> Dict:
    """
    Create a comprehensive export package with all results.
    
    Args:
        simulation_results: Simulation results dictionary
        partial_traces: List of partial traces
        circuit_info: Circuit information
        filename_prefix: Prefix for exported files
        
    Returns:
        Dictionary containing export data
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    export_data = {
        'metadata': {
            'export_time': timestamp,
            'qtrace_version': '1.0.0',
            'export_type': 'comprehensive'
        },
        'circuit_info': circuit_info,
        'simulation_results': simulation_results,
        'qubit_analysis': []
    }
    
    # Add qubit analysis
    for i, density_matrix in enumerate(partial_traces):
        # Convert DensityMatrix to numpy array if needed
        if hasattr(density_matrix, 'data'):
            dm = np.asarray(density_matrix.data)
        else:
            dm = np.asarray(density_matrix)
            
        purity = np.real(np.trace(dm @ dm))
        x, y, z = _get_bloch_coordinates(density_matrix)
        
        export_data['qubit_analysis'].append({
            'qubit_index': i,
            'purity': float(purity),
            'bloch_coordinates': {
                'x': float(x),
                'y': float(y),
                'z': float(z)
            },
            'density_matrix': dm.tolist()
        })
    
    return export_data

def display_quantum_state_info(statevector: np.ndarray, title: str = "Quantum State Information") -> None:
    """
    Display detailed information about a quantum state vector.
    
    Args:
        statevector: Quantum state vector
        title: Title for the display section
    """
    st.subheader(title)
    
    if statevector is None:
        st.warning("No state vector available")
        return
    
    # Basic information
    num_qubits = int(np.log2(len(statevector)))
    st.write(f"**Number of qubits:** {num_qubits}")
    st.write(f"**State vector dimension:** {len(statevector)}")
    
    # State vector components
    st.write("**State Vector Components:**")
    
    # Show first few and last few components for large states
    if len(statevector) <= 16:
        # Show all components for small states
        for i, amplitude in enumerate(statevector):
            binary = format(i, f'0{num_qubits}b')
            st.write(f"|{binary}⟩: {format_complex_number(amplitude)}")
    else:
        # Show first 8 and last 8 components for large states
        st.write("*First 8 components:*")
        for i in range(min(8, len(statevector))):
            binary = format(i, f'0{num_qubits}b')
            st.write(f"|{binary}⟩: {format_complex_number(statevector[i])}")
        
        st.write("*Last 8 components:*")
        for i in range(max(0, len(statevector) - 8), len(statevector)):
            binary = format(i, f'0{num_qubits}b')
            st.write(f"|{binary}⟩: {format_complex_number(statevector[i])}")
    
    # State properties
    norm = np.sqrt(np.sum(np.abs(statevector)**2))
    st.write(f"**State norm:** {norm:.6f}")
    
    if abs(norm - 1.0) > 1e-10:
        st.warning("⚠️ State vector is not normalized!")

def create_progress_tracker(total_steps: int, current_step: int, title: str = "Progress") -> None:
    """
    Create a progress tracker for multi-step operations.
    
    Args:
        total_steps: Total number of steps
        current_step: Current step (0-indexed)
        title: Title for the progress section
    """
    st.subheader(title)
    
    progress = (current_step + 1) / total_steps
    st.progress(progress)
    
    st.write(f"Step {current_step + 1} of {total_steps}")
    
    # Progress bar with steps
    step_labels = [f"Step {i+1}" for i in range(total_steps)]
    current_step_label = step_labels[current_step] if current_step < len(step_labels) else "Complete"
    
    st.write(f"**Current:** {current_step_label}")
    
    if current_step > 0:
        st.write(f"**Previous:** {step_labels[current_step - 1]}")
    
    if current_step < total_steps - 1:
        st.write(f"**Next:** {step_labels[current_step + 1]}")

def validate_quantum_circuit(circuit) -> tuple[bool, str]:
    """
    Validate a quantum circuit for common issues.
    
    Args:
        circuit: Qiskit QuantumCircuit object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if circuit is None:
        return False, "No circuit provided"
    
    # Check for empty circuit
    if circuit.depth() == 0:
        return False, "Circuit has no gates"
    
    # Check for disconnected qubits
    used_qubits = set()
    for instruction, qargs, cargs in circuit.data:
        for q in qargs:
            used_qubits.add(q.index)
    
    if len(used_qubits) < circuit.num_qubits:
        return False, f"Some qubits are not used: {set(range(circuit.num_qubits)) - used_qubits}"
    
    # Check for measurement gates
    has_measurements = any(instruction.name == 'measure' for instruction, _, _ in circuit.data)
    if not has_measurements:
        return False, "Circuit has no measurement gates"
    
    return True, "Circuit is valid"
