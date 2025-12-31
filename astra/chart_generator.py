"""
Chart Generator Module
Generates Matplotlib visualizations and converts them to Base64-encoded images
for embedding in HTML reports.
"""

import base64
import io
from typing import Dict, List
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from astra.metrics_visitor import ClassMetrics


class ChartGenerator:
    """Generates various charts for the analysis report"""
    
    @staticmethod
    def figure_to_base64(fig) -> str:
        """Convert matplotlib figure to Base64-encoded string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return img_str
    
    @staticmethod
    def generate_complexity_scatter_plot(classes: List[ClassMetrics]) -> str:
        """
        Generate Complexity Scatter Plot.
        X-axis = Cyclomatic Complexity (WMC), Y-axis = Halstead Volume.
        Each dot represents a class.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x_values = []
        y_values = []
        labels = []
        
        for class_metrics in classes:
            if class_metrics.aggregated_halstead:
                volume = class_metrics.aggregated_halstead.get('V', 0)
                wmc = class_metrics.wmc
                
                if volume > 0 and wmc > 0:
                    x_values.append(wmc)
                    y_values.append(volume)
                    labels.append(class_metrics.class_name)
        
        if x_values and y_values:
            ax.scatter(x_values, y_values, alpha=0.6, s=100, c='steelblue', edgecolors='black', linewidth=1)
            
            # Add labels for top classes
            if len(x_values) <= 20:  # Only label if not too many classes
                for i, label in enumerate(labels):
                    ax.annotate(label, (x_values[i], y_values[i]), 
                              xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        ax.set_xlabel('Cyclomatic Complexity (WMC)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Halstead Volume (V)', fontsize=12, fontweight='bold')
        ax.set_title('Complexity Scatter Plot\n(Classes in Hard-to-Maintain Zone)', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        return ChartGenerator.figure_to_base64(fig)
    
    @staticmethod
    def generate_ck_radar_chart(classes: List[ClassMetrics], top_n: int = 5) -> str:
        """
        Generate CK Metrics Radar Chart (Spider Plot).
        Compares top N classes based on WMC, DIT, CBO.
        """
        # Sort classes by WMC and take top N
        sorted_classes = sorted(classes, key=lambda c: c.wmc, reverse=True)[:top_n]
        
        if not sorted_classes:
            # Return empty chart
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            return ChartGenerator.figure_to_base64(fig)
        
        # Prepare data
        metrics = ['WMC', 'DIT', 'CBO']
        num_metrics = len(metrics)
        
        # Calculate angles for radar chart
        angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Normalize values for better visualization
        max_wmc = max(c.wmc for c in sorted_classes) if sorted_classes else 1
        max_dit = max(c.dit for c in sorted_classes) if sorted_classes else 1
        max_cbo = max(c.cbo for c in sorted_classes) if sorted_classes else 1
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(sorted_classes)))
        
        for idx, class_metrics in enumerate(sorted_classes):
            # Normalize values (0-1 scale)
            values = [
                class_metrics.wmc / max_wmc if max_wmc > 0 else 0,
                class_metrics.dit / max_dit if max_dit > 0 else 0,
                class_metrics.cbo / max_cbo if max_cbo > 0 else 0
            ]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=class_metrics.class_name, color=colors[idx])
            ax.fill(angles, values, alpha=0.25, color=colors[idx])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=11, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.set_title('CK Metrics Radar Chart\n(Top Classes Comparison)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)
        
        return ChartGenerator.figure_to_base64(fig)
    
    @staticmethod
    def generate_mi_distribution_bar(classes: List[ClassMetrics]) -> str:
        """
        Generate Maintainability Index Distribution Bar Chart.
        Shows how many classes are Green (>85), Yellow (65-85), Red (<65).
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        green_count = sum(1 for c in classes if c.maintainability_index > 85)
        yellow_count = sum(1 for c in classes if 65 <= c.maintainability_index <= 85)
        red_count = sum(1 for c in classes if c.maintainability_index < 65)
        
        categories = ['Green\n(>85)', 'Yellow\n(65-85)', 'Red\n(<65)']
        counts = [green_count, yellow_count, red_count]
        colors = ['#2ecc71', '#f39c12', '#e74c3c']
        
        bars = ax.bar(categories, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Number of Classes', fontsize=12, fontweight='bold')
        ax.set_title('Maintainability Index Distribution', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        return ChartGenerator.figure_to_base64(fig)
    
    @staticmethod
    def generate_all_charts(classes: List[ClassMetrics]) -> Dict[str, str]:
        """
        Generate all charts and return as Base64-encoded strings.
        
        Returns:
            Dictionary with chart names as keys and Base64 strings as values
        """
        return {
            'complexity_scatter': ChartGenerator.generate_complexity_scatter_plot(classes),
            'ck_radar': ChartGenerator.generate_ck_radar_chart(classes),
            'mi_distribution': ChartGenerator.generate_mi_distribution_bar(classes)
        }

