"""
Chart Generation Module
Creates visualization charts for metrics analysis
"""

import os
from pathlib import Path
from .constants import HAS_MATPLOTLIB


class ChartGenerator:
    """Generates visualization charts for Halstead metrics"""
    
    @staticmethod
    def generate(res, output_dir):
        """
        Generate chart and save as PNG file.
        
        Args:
            res: Analysis results dictionary
            output_dir: Directory to save chart file
            
        Returns:
            Tuple of (chart_filename, None) or (None, None) if matplotlib unavailable or generation fails
        """
        if not HAS_MATPLOTLIB:
            return None, None
        
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return None, None
        
        try:
            h = res['halstead']
            q = res['quality']
            filename_base = Path(res['file']).stem
            chart_filename = os.path.join(output_dir, f"{filename_base}_chart.png")
            
            # Configure chart
            plt.figure(figsize=(12, 6))
            plt.style.use('ggplot')
            
            # Subplot 1: Quality Metrics (Linear Scale)
            plt.subplot(1, 2, 1)
            labels_1 = ['Maintainability\n(MI)', 'Difficulty\n(D)', 'Complexity\n(CC)']
            values_1 = [q['mi'], min(h['D'], 100), min(q['cc'], 100)]
            colors_1 = ['#28a745', '#ffc107', '#dc3545']
            
            bars = plt.bar(labels_1, values_1, color=colors_1)
            plt.title('Quality Profile', fontsize=14, fontweight='bold')
            plt.ylim(0, 100)
            plt.ylabel('Score')
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                         f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
            
            # Subplot 2: Halstead Metrics (Logarithmic Scale)
            plt.subplot(1, 2, 2)
            labels_2 = ['Volume\n(V)', 'Effort\n(E)']
            values_2 = [h['V'], h['E']]
            colors_2 = ['#17a2b8', '#6610f2']
            
            bars2 = plt.bar(labels_2, values_2, color=colors_2)
            plt.title('Halstead Scale (Logarithmic)', fontsize=14, fontweight='bold')
            plt.yscale('log')
            plt.ylabel('Value (log scale)')
            
            for bar in bars2:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                         f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(chart_filename, dpi=150, bbox_inches='tight')
            plt.close()
            
            return chart_filename, None
        except Exception as e:
            # If chart generation fails, return None but don't crash
            try:
                plt.close()
            except:
                pass
            return None, None

