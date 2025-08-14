"""
Visualization Module for QTrace
Handles Bloch sphere plotting, circuit diagrams, and interactive visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import List, Dict, Tuple, Optional
import io
import base64
from qiskit.visualization import plot_circuit_layout
import pandas as pd

class QuantumVisualizer:
    """Handles all quantum state visualizations including Bloch spheres."""
    
    def __init__(self):
        """Initialize the quantum visualizer."""
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def create_bloch_sphere(self, density_matrix: np.ndarray, qubit_index: int, 
                           title: str = None) -> go.Figure:
        """
        Create an interactive 3D Bloch sphere for a single qubit.
        
        Args:
            density_matrix: 2x2 density matrix of the qubit
            qubit_index: Index of the qubit
            title: Title for the Bloch sphere
            
        Returns:
            Plotly figure object
        """
        # Extract Bloch coordinates
        x, y, z = self._get_bloch_coordinates(density_matrix)
        purity = self._calculate_purity(density_matrix)
        
        # Create the Bloch sphere
        fig = go.Figure()
        
        # Add the sphere surface
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        sphere_x = np.outer(np.cos(u), np.sin(v))
        sphere_y = np.outer(np.sin(u), np.sin(v))
        sphere_z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        fig.add_trace(go.Surface(
            x=sphere_x, y=sphere_y, z=sphere_z,
            opacity=0.1,
            colorscale='Blues',
            showscale=False,
            name='Bloch Sphere'
        ))
        
        # Add coordinate axes
        # X-axis (red)
        fig.add_trace(go.Scatter3d(
            x=[-1.2, 1.2], y=[0, 0], z=[0, 0],
            mode='lines',
            line=dict(color='red', width=5),
            name='X-axis',
            showlegend=False
        ))
        
        # Y-axis (green)
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[-1.2, 1.2], z=[0, 0],
            mode='lines',
            line=dict(color='green', width=5),
            name='Y-axis',
            showlegend=False
        ))
        
        # Z-axis (blue)
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[-1.2, 1.2],
            mode='lines',
            line=dict(color='blue', width=5),
            name='Z-axis',
            showlegend=False
        ))
        
        # Add the quantum state point
        state_color = 'red' if purity < 0.99 else 'green'
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers',
            marker=dict(
                size=10,
                color=state_color,
                symbol='diamond'
            ),
            name=f'Qubit {qubit_index} State',
            text=[f'Purity: {purity:.3f}<br>X: {x:.3f}<br>Y: {y:.3f}<br>Z: {z:.3f}'],
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
        
        # Add basis state labels
        fig.add_trace(go.Scatter3d(
            x=[0, 0, 0, 0], y=[0, 0, 0, 0], z=[1.1, -1.1, 0, 0],
            mode='text',
            text=['|0⟩', '|1⟩', '', ''],
            textposition='middle center',
            name='Basis States',
            showlegend=False
        ))
        
        # Update layout
        if title is None:
            title = f'Qubit {qubit_index} Bloch Sphere'
            
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis=dict(
                    title='X',
                    range=[-1.3, 1.3],
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                yaxis=dict(
                    title='Y',
                    range=[-1.3, 1.3],
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                zaxis=dict(
                    title='Z',
                    range=[-1.3, 1.3],
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                aspectmode='cube',
                bgcolor='rgba(248, 250, 252, 0.9)'
            ),
            width=500,
            height=500,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(248, 250, 252, 0.9)',
            plot_bgcolor='rgba(255, 255, 255, 0.9)'
        )
        
        return fig
    
    def create_multiqubit_bloch_spheres(self, partial_traces: List[np.ndarray], 
                                      title: str = "Multi-Qubit Bloch Spheres") -> go.Figure:
        """
        Create multiple Bloch spheres for all qubits in a subplot layout.
        
        Args:
            partial_traces: List of density matrices for each qubit
            title: Overall title for the visualization
            
        Returns:
            Plotly figure with subplots
        """
        num_qubits = len(partial_traces)
        
        # Calculate subplot layout
        cols = min(3, num_qubits)
        rows = (num_qubits + cols - 1) // cols
        
        fig = make_subplots(
            rows=rows, cols=cols,
            specs=[[{'type': 'scene'} for _ in range(cols)] for _ in range(rows)],
            subplot_titles=[f'Qubit {i}' for i in range(num_qubits)],
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )
        
        for i, density_matrix in enumerate(partial_traces):
            row = i // cols + 1
            col = i % cols + 1
            
            # Get Bloch coordinates
            x, y, z = self._get_bloch_coordinates(density_matrix)
            purity = self._calculate_purity(density_matrix)
            
            # Add sphere surface
            u = np.linspace(0, 2 * np.pi, 50)
            v = np.linspace(0, np.pi, 50)
            sphere_x = np.outer(np.cos(u), np.sin(v))
            sphere_y = np.outer(np.sin(u), np.sin(v))
            sphere_z = np.outer(np.ones(np.size(u)), np.cos(v))
            
            fig.add_trace(
                go.Surface(
                    x=sphere_x, y=sphere_y, z=sphere_z,
                    opacity=0.1,
                    colorscale='Blues',
                    showscale=False
                ),
                row=row, col=col
            )
            
            # Add coordinate axes
            fig.add_trace(
                go.Scatter3d(
                    x=[-1.1, 1.1], y=[0, 0], z=[0, 0],
                    mode='lines',
                    line=dict(color='red', width=3),
                    showlegend=False
                ),
                row=row, col=col
            )
            
            fig.add_trace(
                go.Scatter3d(
                    x=[0, 0], y=[-1.1, 1.1], z=[0, 0],
                    mode='lines',
                    line=dict(color='green', width=3),
                    showlegend=False
                ),
                row=row, col=col
            )
            
            fig.add_trace(
                go.Scatter3d(
                    x=[0, 0], y=[0, 0], z=[-1.1, 1.1],
                    mode='lines',
                    line=dict(color='blue', width=3),
                    showlegend=False
                ),
                row=row, col=col
            )
            
            # Add state point
            state_color = 'red' if purity < 0.99 else 'green'
            fig.add_trace(
                go.Scatter3d(
                    x=[x], y=[y], z=[z],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=state_color,
                        symbol='diamond'
                    ),
                    text=[f'Purity: {purity:.3f}<br>X: {x:.3f}<br>Y: {y:.3f}<br>Z: {z:.3f}'],
                    hovertemplate='<b>%{text}</b><extra></extra>'
                ),
                row=row, col=col
            )
            
            # Update subplot scene
            fig.update_scenes(
                xaxis=dict(range=[-1.2, 1.2], showgrid=True, gridcolor='lightgray'),
                yaxis=dict(range=[-1.2, 1.2], showgrid=True, gridcolor='lightgray'),
                zaxis=dict(range=[-1.2, 1.2], showgrid=True, gridcolor='lightgray'),
                aspectmode='cube',
                row=row, col=col
            )
        
        fig.update_layout(
            title=title,
            height=300 * rows,
            width=500 * min(cols, 3),
            showlegend=False,
            paper_bgcolor='rgba(248, 250, 252, 0.9)'
        )
        
        return fig
    
    def create_state_evolution_plot(self, state_history: List[Dict], 
                                   qubit_index: int = 0) -> go.Figure:
        """
        Create a plot showing how a qubit's state evolves through the circuit.
        
        Args:
            state_history: List of states at each step
            qubit_index: Index of the qubit to track
            
        Returns:
            Plotly figure showing state evolution
        """
        if not state_history:
            return go.Figure()
        
        steps = []
        x_coords = []
        y_coords = []
        z_coords = []
        purities = []
        
        for step_data in state_history:
            if qubit_index < len(step_data['partial_traces']):
                density_matrix = step_data['partial_traces'][qubit_index]
                x, y, z = self._get_bloch_coordinates(density_matrix)
                purity = self._calculate_purity(density_matrix)
                
                steps.append(step_data['step'])
                x_coords.append(x)
                y_coords.append(y)
                z_coords.append(z)
                purities.append(purity)
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=[f'Qubit {qubit_index} Bloch Coordinates', 'State Purity'],
            vertical_spacing=0.1
        )
        
        # Bloch coordinates over time
        fig.add_trace(
            go.Scatter(
                x=steps, y=x_coords,
                mode='lines+markers',
                name='X coordinate',
                line=dict(color='red', width=2),
                marker=dict(size=6)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=steps, y=y_coords,
                mode='lines+markers',
                name='Y coordinate',
                line=dict(color='green', width=2),
                marker=dict(size=6)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=steps, y=z_coords,
                mode='lines+markers',
                name='Z coordinate',
                line=dict(color='blue', width=2),
                marker=dict(size=6)
            ),
            row=1, col=1
        )
        
        # Purity over time
        fig.add_trace(
            go.Scatter(
                x=steps, y=purities,
                mode='lines+markers',
                name='Purity',
                line=dict(color='purple', width=3),
                marker=dict(size=8)
            ),
            row=2, col=1
        )

        fig.update_layout(
            title=f'Qubit {qubit_index} State Evolution',
            height=600,
            showlegend=True,
            paper_bgcolor='rgba(248, 250, 252, 0.9)',
            plot_bgcolor='rgba(255, 255, 255, 0.9)'
        )

        fig.update_xaxes(title_text="Circuit Step", row=1, col=1)
        fig.update_yaxes(title_text="Bloch Coordinate", row=1, col=1)
        fig.update_xaxes(title_text="Circuit Step", row=2, col=1)
        fig.update_yaxes(title_text="Purity", row=2, col=1)

        return fig
    
    def create_measurement_histogram(self, counts: Dict[str, int], 
                                   title: str = "Measurement Results") -> go.Figure:
        """
        Create a histogram of measurement results.
        
        Args:
            counts: Dictionary of measurement counts
            title: Title for the histogram
            
        Returns:
            Plotly figure with measurement histogram
        """
        # Sort counts by bitstring
        sorted_counts = dict(sorted(counts.items(), key=lambda x: x[0]))
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(sorted_counts.keys()),
                y=list(sorted_counts.values()),
                marker_color='lightblue',
                text=list(sorted_counts.values()),
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title="Measurement Outcome",
            yaxis_title="Count",
            height=400,
            showlegend=False,
            paper_bgcolor='rgba(248, 250, 252, 0.9)',
            plot_bgcolor='rgba(255, 255, 255, 0.9)'
        )
        
        return fig
    
    def create_circuit_diagram(self, circuit) -> str:
        """
        Create a circuit diagram and return it as a base64 encoded string.
        
        Args:
            circuit: Qiskit QuantumCircuit object
            
        Returns:
            Base64 encoded string of the circuit diagram
        """
        try:
            # Create the circuit diagram
            fig, ax = plt.subplots(figsize=(12, 6))
            circuit.draw('mpl', ax=ax)
            plt.tight_layout()
            
            # Convert to base64 string
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return img_str
        except Exception:
            return ""
    
    def create_purity_heatmap(self, partial_traces: List[np.ndarray]) -> go.Figure:
        """
        Create a heatmap showing the purity of each qubit.
        
        Args:
            partial_traces: List of density matrices for each qubit
            
        Returns:
            Plotly figure with purity heatmap
        """
        purities = [self._calculate_purity(rho) for rho in partial_traces]
        
        fig = go.Figure(data=go.Heatmap(
            z=[purities],
            x=[f'Qubit {i}' for i in range(len(purities))],
            y=['Purity'],
            colorscale='RdYlGn',
            zmin=0,
            zmax=1,
            text=[[f'{p:.3f}' for p in purities]],
            texttemplate="%{text}",
            textfont={"size": 14},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Qubit State Purity Heatmap",
            height=200,
            yaxis=dict(showticklabels=False),
            paper_bgcolor='rgba(248, 250, 252, 0.9)',
            plot_bgcolor='rgba(255, 255, 255, 0.9)'
        )
        
        return fig
    
    def _get_bloch_coordinates(self, density_matrix: np.ndarray) -> Tuple[float, float, float]:
        """Extract Bloch sphere coordinates from density matrix."""
        # Pauli matrices
        sigma_x = np.array([[0, 1], [1, 0]])
        sigma_y = np.array([[0, -1j], [1j, 0]])
        sigma_z = np.array([[1, 0], [0, -1]])
        
        x = np.real(np.trace(density_matrix @ sigma_x))
        y = np.real(np.trace(density_matrix @ sigma_y))
        z = np.real(np.trace(density_matrix @ sigma_z))
        
        return x, y, z
    
    def _calculate_purity(self, density_matrix: np.ndarray) -> float:
        """Calculate the purity of a quantum state."""
        import numpy as np
        # Convert to numpy array if not already
        if hasattr(density_matrix, 'data'):
            dm = np.asarray(density_matrix.data)
        else:
            dm = np.asarray(density_matrix)
        return np.real(np.trace(dm @ dm))
    
    def save_figure_as_png(self, fig: go.Figure) -> bytes:
        """
        Save a Plotly figure as PNG bytes.
        
        Args:
            fig: Plotly figure object
            
        Returns:
            PNG image as bytes
        """
        return fig.to_image(format="png")
    
    def save_figure_as_pdf(self, fig: go.Figure) -> bytes:
        """
        Save a Plotly figure as PDF bytes.
        
        Args:
            fig: Plotly figure object
            
        Returns:
            PDF as bytes
        """
        return fig.to_image(format="pdf")
