"""
HTML Report Generation Module
Creates professional HTML reports with embedded charts
"""

import os
from pathlib import Path


class HtmlReporter:
    """Generates HTML reports with embedded visualization charts"""
    
    @staticmethod
    def generate(res, chart_file=None, output_dir="output"):
        """
        Generate HTML report with chart reference.
        
        Args:
            res: Analysis results dictionary
            chart_file: Path to chart image file (optional)
            output_dir: Directory to save HTML report (same as chart directory)
            
        Returns:
            Path to generated HTML file
        """
        h = res['halstead']
        q = res['quality']
        b = res['base']
        
        mi_class = "good" if q['mi'] > 80 else ("warn" if q['mi'] > 50 else "bad")
        lang_display = res['language'].upper()
        
        # Chart HTML with file reference (charts are in the same directory as reports)
        chart_html = ""
        if chart_file:
            chart_filename = Path(chart_file).name
            chart_html = f'''
            <div class="chart-container">
                <h2>Visual Analysis</h2>
                <img src="{chart_filename}" alt="Metrics Chart" style="max-width:100%; border-radius:8px; border:1px solid #eee; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            </div>
            '''
        
        html = HtmlReporter._generate_html_template(res, chart_html, mi_class, lang_display, h, q, b)
        
        filename_base = Path(res['file']).stem
        out_file = os.path.join(output_dir, f"{filename_base}_report.html")
        os.makedirs(output_dir, exist_ok=True)
        
        with open(out_file, "w", encoding='utf-8') as f:
            f.write(html)
        
        return out_file
    
    @staticmethod
    def _generate_html_template(res, chart_html, mi_class, lang_display, h, q, b):
        """Generate the HTML template string"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Report: {Path(res['file']).name}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f9; color: #333; padding: 20px; margin: 0; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
                h1 {{ border-bottom: 3px solid #007bff; padding-bottom: 10px; color: #2c3e50; margin-top: 0; }}
                .meta {{ color: #7f8c8d; margin-bottom: 30px; font-size: 0.95em; }}
                .lang-badge {{ display: inline-block; background: #007bff; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; font-weight: bold; margin-left: 10px; }}
                
                .score-box {{ background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 25px; border-radius: 8px; text-align: center; margin-bottom: 30px; border: 2px solid #dee2e6; }}
                .score-val {{ font-size: 3.5em; font-weight: bold; margin: 10px 0; }}
                .good {{ color: #27ae60; }} .warn {{ color: #f39c12; }} .bad {{ color: #c0392b; }}
                
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }}
                .card {{ background: #fff; border: 1px solid #e1e4e8; padding: 15px; border-radius: 6px; text-align: center; transition: transform 0.2s, box-shadow 0.2s; }}
                .card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                .card h3 {{ margin: 0; font-size: 0.85em; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }}
                .card .val {{ font-size: 1.5em; font-weight: 600; color: #34495e; margin-top: 5px; }}
                
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; border: 1px solid #eee; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
                th {{ background-color: #f1f2f6; color: #555; font-weight: 600; }}
                tr:hover {{ background-color: #f8f9fa; }}
                
                .chart-container {{ margin-top: 30px; text-align: center; }}
                .chart-container h2 {{ color: #2c3e50; margin-bottom: 20px; }}
                .footer {{ text-align: center; margin-top: 50px; font-size: 0.8em; color: #aaa; padding-top: 20px; border-top: 1px solid #eee; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Static Analysis Report <span class="lang-badge">{lang_display}</span></h1>
                <div class="meta">
                    <strong>File:</strong> {Path(res['file']).name}<br>
                    <strong>Path:</strong> {res['file']}<br>
                    <strong>Date:</strong> {res['timestamp']}
                </div>
                
                <div class="score-box">
                    <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">MAINTAINABILITY INDEX (MI)</div>
                    <div class="score-val {mi_class}">{q['mi']:.1f}</div>
                    <small style="color: #999;">0 (Critical) - 100 (Excellent)</small>
                </div>
                
                {chart_html}

                <h2>Halstead Overview</h2>
                <div class="grid">
                    <div class="card"><h3>Program Level (L)</h3><div class="val">{h['L']:.4f}</div></div>
                    <div class="card"><h3>Volume (V)</h3><div class="val">{h['V']:.0f}</div></div>
                    <div class="card"><h3>Difficulty (D)</h3><div class="val">{h['D']:.2f}</div></div>
                    <div class="card"><h3>Effort (E)</h3><div class="val">{h['E']:.0f}</div></div>
                </div>

                <h2>Detailed Metrics Table</h2>
                <table>
                    <thead><tr><th>Metric</th><th>Value</th><th>Description</th></tr></thead>
                    <tbody>
                        <tr><td><strong>Operators (n1)</strong></td><td>{b['n1']}</td><td>Unique operators count</td></tr>
                        <tr><td><strong>Operands (n2)</strong></td><td>{b['n2']}</td><td>Unique operands count</td></tr>
                        <tr><td><strong>Total Operators (N1)</strong></td><td>{b['N1']}</td><td>Total operator occurrences</td></tr>
                        <tr><td><strong>Total Operands (N2)</strong></td><td>{b['N2']}</td><td>Total operand occurrences</td></tr>
                        <tr><td><strong>Program Length (N)</strong></td><td>{h['N']}</td><td>Total tokens (N1 + N2)</td></tr>
                        <tr><td><strong>Vocabulary (n)</strong></td><td>{h['n']}</td><td>Total unique tokens (n1 + n2)</td></tr>
                        <tr><td><strong>Volume (V)</strong></td><td>{h['V']:.2f}</td><td>Program size in bits</td></tr>
                        <tr><td><strong>Difficulty (D)</strong></td><td>{h['D']:.2f}</td><td>Implementation difficulty</td></tr>
                        <tr><td><strong>Effort (E)</strong></td><td>{h['E']:.2f}</td><td>Mental effort required</td></tr>
                        <tr><td><strong>Time (T)</strong></td><td>{h['T']:.2f} s</td><td>Estimated coding time</td></tr>
                        <tr><td><strong>Program Level (L)</strong></td><td>{h['L']:.4f}</td><td>Program abstraction level</td></tr>
                        <tr><td><strong>Est. Bugs (B)</strong></td><td>{h['B']:.2f}</td><td>Potential defects</td></tr>
                        <tr><td><strong>Cyclomatic Complexity</strong></td><td>{q['cc']}</td><td>Independent paths count</td></tr>
                        <tr><td><strong>Logical LOC</strong></td><td>{q['loc']}</td><td>Lines of code (non-empty)</td></tr>
                    </tbody>
                </table>
                
                <div class="footer">Generated by Module Complexity Analyzer | Halstead Metrics Analysis</div>
            </div>
        </body>
        </html>
        """

