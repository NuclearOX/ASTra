"""
Report Generator Module
Generates a professional, self-contained HTML5 dashboard with progressive disclosure.
"""

from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    """Generates HTML reports with metrics and visualizations using progressive disclosure"""
    
    @staticmethod
    def render(data: Dict, output_path: str):
        """
        Generate a comprehensive HTML report from the data dictionary.
        
        Args:
            data: Dictionary containing project_name, summary, charts, and classes
            output_path: Path where to save the HTML report
        """
        html_content = ReportGenerator._generate_html(data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    @staticmethod
    def _generate_html(data: Dict) -> str:
        """Generate the complete HTML content"""
        
        project_name = data.get('project_name', 'Java Project')
        summary = data.get('summary', {})
        charts = data.get('charts', {})
        classes = data.get('classes', [])
        
        # Sort classes by name for consistent display
        sorted_classes = sorted(classes, key=lambda c: c.get('name', ''))
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASTra - {project_name} Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
            margin-top: 10px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 12px;
            margin-bottom: 25px;
            font-size: 1.8em;
            font-weight: 600;
        }}
        
        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .kpi-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        }}
        
        .kpi-card h3 {{
            font-size: 2.5em;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        
        .kpi-card p {{
            font-size: 1em;
            opacity: 0.95;
        }}
        
        /* Charts Grid */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }}
        
        .chart-container {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        
        /* Hall of Shame */
        .hall-of-shame {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        
        .hall-of-shame h2 {{
            color: white;
            border-bottom: 3px solid rgba(255,255,255,0.3);
            margin-bottom: 20px;
        }}
        
        .critical-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .critical-table th {{
            background: rgba(0,0,0,0.1);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .critical-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        .critical-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .critical-table tr:hover {{
            background: #fff5f5;
        }}
        
        /* Accordion Details */
        .accordion-container {{
            margin-top: 30px;
        }}
        
        .class-item {{
            margin-bottom: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .class-item summary {{
            padding: 18px 20px;
            cursor: pointer;
            background: #f8f9fa;
            font-weight: 600;
            font-size: 1.1em;
            display: flex;
            justify-content: space-between;
            align-items: center;
            list-style: none;
            transition: background 0.2s;
        }}
        
        .class-item summary::-webkit-details-marker {{
            display: none;
        }}
        
        .class-item summary::after {{
            content: '▶';
            color: #667eea;
            font-size: 0.8em;
            transition: transform 0.2s;
        }}
        
        .class-item[open] summary::after {{
            transform: rotate(90deg);
        }}
        
        .class-item summary:hover {{
            background: #e9ecef;
        }}
        
        .class-summary-row {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
            gap: 15px;
            align-items: center;
            width: 100%;
        }}
        
        .class-name {{
            font-weight: 600;
            color: #333;
        }}
        
        .badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            min-width: 60px;
            text-align: center;
        }}
        
        .badge-green {{
            background: #2ecc71;
            color: white;
        }}
        
        .badge-yellow {{
            background: #f39c12;
            color: white;
        }}
        
        .badge-red {{
            background: #e74c3c;
            color: white;
        }}
        
        .class-details {{
            padding: 20px;
            background: #fafafa;
            border-top: 2px solid #e0e0e0;
        }}
        
        .methods-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .methods-table th {{
            background: #6c757d;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .methods-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 0.9em;
        }}
        
        .methods-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .methods-table tr:hover {{
            background: #f0f0f0;
        }}
        
        .metric-value {{
            font-family: 'Courier New', monospace;
            font-weight: 600;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
            margin-top: 40px;
        }}
        
        /* Halstead Metrics Section */
        .halstead-section {{
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .halstead-section h4 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.1em;
            font-weight: 600;
        }}
        
        .halstead-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .halstead-card {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        
        .halstead-card .label {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .halstead-card .value {{
            font-size: 1.3em;
            font-weight: 700;
            color: #333;
            font-family: 'Courier New', monospace;
        }}
        
        .halstead-card .description {{
            font-size: 0.75em;
            color: #999;
            margin-top: 5px;
            font-style: italic;
        }}
        
        .halstead-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            background: white;
            border-radius: 6px;
            overflow: hidden;
        }}
        
        .halstead-table th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .halstead-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 0.9em;
        }}
        
        .halstead-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .halstead-table tr:hover {{
            background: #f0f0f0;
        }}
        
        .halstead-table .metric-name {{
            font-weight: 600;
            color: #667eea;
        }}
        
        .halstead-table .metric-value {{
            font-family: 'Courier New', monospace;
            font-weight: 600;
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 ASTra - Java Static Analysis Tool</h1>
            <p>{project_name} - Comprehensive Software Metrics Analysis</p>
            <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.9;">
                Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>
        </div>
        
        <div class="content">
            {ReportGenerator._generate_dashboard(summary, charts)}
            
            {ReportGenerator._generate_hall_of_shame(sorted_classes)}
            
            {ReportGenerator._generate_accordion_details(sorted_classes)}
        </div>
        
        <div class="footer">
            <p>Generated by ASTra - Java Automated Static Analysis Tool</p>
            <p style="margin-top: 5px; font-size: 0.85em;">All metrics calculated using industry-standard formulas</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    @staticmethod
    def _generate_dashboard(summary: Dict, charts: Dict) -> str:
        """Generate Section A: Dashboard with KPI cards and charts"""
        
        total_files = summary.get('total_files', 0)
        total_loc = summary.get('total_loc', 0)
        avg_mi = summary.get('avg_mi', 0.0)
        god_classes_count = summary.get('god_classes_count', 0)
        
        scatter_b64 = charts.get('scatter_b64', '')
        radar_b64 = charts.get('radar_b64', '')
        
        charts_html = ""
        if scatter_b64 or radar_b64:
            charts_html = '<div class="charts-grid">'
            if scatter_b64:
                charts_html += f'''
                <div class="chart-container">
                    <h3 style="margin-bottom: 15px; color: #667eea;">Complexity Scatter Plot</h3>
                    <img src="data:image/png;base64,{scatter_b64}" alt="Complexity Scatter Plot">
                </div>
                '''
            if radar_b64:
                charts_html += f'''
                <div class="chart-container">
                    <h3 style="margin-bottom: 15px; color: #667eea;">CK Metrics Radar Chart</h3>
                    <img src="data:image/png;base64,{radar_b64}" alt="CK Metrics Radar Chart">
                </div>
                '''
            charts_html += '</div>'
        
        return f"""
            <div class="section">
                <h2>📊 Dashboard</h2>
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <h3>{total_files}</h3>
                        <p>Total Files</p>
                    </div>
                    <div class="kpi-card">
                        <h3>{total_loc:,}</h3>
                        <p>Lines of Code</p>
                    </div>
                    <div class="kpi-card">
                        <h3>{avg_mi:.1f}</h3>
                        <p>Avg Maintainability Index</p>
                    </div>
                    <div class="kpi-card" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);">
                        <h3>{god_classes_count}</h3>
                        <p>Critical Classes</p>
                    </div>
                </div>
                {charts_html}
            </div>
        """
    
    @staticmethod
    def _generate_hall_of_shame(classes: List[Dict]) -> str:
        """Generate Section B: Hall of Shame - Top 5 Critical Classes"""
        
        # Sort by lowest MI first, then by highest WMC
        critical_classes = sorted(
            classes,
            key=lambda c: (c.get('mi', 100), -c.get('wmc', 0))
        )[:5]
        
        if not critical_classes:
            return ""
        
        rows = ""
        for cls in critical_classes:
            name = cls.get('name', 'Unknown')
            mi = cls.get('mi', 0.0)
            wmc = cls.get('wmc', 0)
            dit = cls.get('dit', 0)
            cbo = cls.get('cbo', 0)
            effort = cls.get('halstead_effort_sum', 0.0)
            
            mi_badge = ReportGenerator._get_mi_badge(mi)
            
            rows += f"""
            <tr>
                <td><strong>{name}</strong></td>
                <td class="metric-value">{mi_badge}</td>
                <td class="metric-value">{wmc}</td>
                <td class="metric-value">{dit}</td>
                <td class="metric-value">{cbo}</td>
                <td class="metric-value">{effort:,.0f}</td>
            </tr>
            """
        
        return f"""
            <div class="section">
                <div class="hall-of-shame">
                    <h2>⚠️ Hall of Shame - Top 5 Critical Classes</h2>
                    <table class="critical-table">
                        <thead>
                            <tr>
                                <th>Class Name</th>
                                <th>MI</th>
                                <th>WMC</th>
                                <th>DIT</th>
                                <th>CBO</th>
                                <th>Halstead Effort</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows}
                        </tbody>
                    </table>
                </div>
            </div>
        """
    
    @staticmethod
    def _generate_accordion_details(classes: List[Dict]) -> str:
        """Generate Section C: Accordion with all classes and their methods"""
        
        accordion_html = ""
        
        for cls in classes:
            name = cls.get('name', 'Unknown')
            mi = cls.get('mi', 0.0)
            wmc = cls.get('wmc', 0)
            dit = cls.get('dit', 0)
            cbo = cls.get('cbo', 0)
            methods = cls.get('methods', [])
            halstead = cls.get('halstead', {})
            
            mi_badge = ReportGenerator._get_mi_badge(mi)
            
            # Generate Halstead metrics section
            halstead_html = ReportGenerator._generate_halstead_section(halstead)
            
            # Generate methods table with full Halstead metrics
            methods_html = ""
            if methods:
                methods_rows = ""
                for method in methods:
                    method_name = method.get('name', 'Unknown')
                    complexity = method.get('complexity', 0)
                    method_halstead = method.get('halstead', {})
                    
                    # Extract Halstead metrics for method
                    method_effort = method_halstead.get('E', 0.0)
                    method_volume = method_halstead.get('V', 0.0)
                    method_difficulty = method_halstead.get('D', 0.0)
                    method_time = method_halstead.get('T', 0.0)
                    method_bugs = method_halstead.get('B', 0.0)
                    
                    methods_rows += f"""
                    <tr>
                        <td><strong>{method_name}</strong></td>
                        <td class="metric-value">{complexity}</td>
                        <td class="metric-value">{method_volume:,.0f}</td>
                        <td class="metric-value">{method_difficulty:.2f}</td>
                        <td class="metric-value">{method_effort:,.0f}</td>
                        <td class="metric-value">{method_time:.2f}s</td>
                        <td class="metric-value">{method_bugs:.2f}</td>
                    </tr>
                    """
                
                methods_html = f"""
                <div class="class-details">
                    <h3 style="margin-bottom: 15px; color: #667eea; font-size: 1.1em;">Methods ({len(methods)})</h3>
                    <table class="methods-table">
                        <thead>
                            <tr>
                                <th>Method Name</th>
                                <th>CC</th>
                                <th>Volume (V)</th>
                                <th>Difficulty (D)</th>
                                <th>Effort (E)</th>
                                <th>Time (T)</th>
                                <th>Bugs (B)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {methods_rows}
                        </tbody>
                    </table>
                </div>
                """
            else:
                methods_html = """
                <div class="class-details">
                    <p style="color: #999; font-style: italic;">No methods found</p>
                </div>
                """
            
            accordion_html += f"""
            <div class="class-item">
                <details>
                    <summary>
                        <div class="class-summary-row">
                            <span class="class-name">{name}</span>
                            <span>{mi_badge}</span>
                            <span class="metric-value">WMC: {wmc}</span>
                            <span class="metric-value">DIT: {dit}</span>
                            <span class="metric-value">CBO: {cbo}</span>
                        </div>
                    </summary>
                    {halstead_html}
                    {methods_html}
                </details>
            </div>
            """
        
        return f"""
            <div class="section">
                <h2>📋 Detailed Class Analysis</h2>
                <p style="margin-bottom: 20px; color: #666;">
                    Click on any class to expand and view detailed metrics including all Halstead complexity measures.
                </p>
                <div class="accordion-container">
                    {accordion_html}
                </div>
            </div>
        """
    
    @staticmethod
    def _generate_halstead_section(halstead: Dict) -> str:
        """Generate a comprehensive Halstead metrics section"""
        
        if not halstead:
            return """
            <div class="class-details">
                <div class="halstead-section">
                    <h4>📊 Halstead Complexity Metrics</h4>
                    <p style="color: #999; font-style: italic;">No Halstead metrics available</p>
                </div>
            </div>
            """
        
        # Extract all 12 Halstead metrics
        n1 = halstead.get('n1', 0)
        n2 = halstead.get('n2', 0)
        N1 = halstead.get('N1', 0)
        N2 = halstead.get('N2', 0)
        N = halstead.get('N', 0)
        n = halstead.get('n', 0)
        V = halstead.get('V', 0.0)
        D = halstead.get('D', 0.0)
        E = halstead.get('E', 0.0)
        T = halstead.get('T', 0.0)
        L = halstead.get('L', 0.0)
        B = halstead.get('B', 0.0)
        
        # Create table with all metrics
        metrics_table = f"""
        <div class="class-details">
            <div class="halstead-section">
                <h4>📊 Halstead Complexity Metrics</h4>
                <table class="halstead-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Symbol</th>
                            <th>Value</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="metric-name">Unique Operators</td>
                            <td><strong>n₁</strong></td>
                            <td class="metric-value">{n1}</td>
                            <td>Number of distinct operators</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Unique Operands</td>
                            <td><strong>n₂</strong></td>
                            <td class="metric-value">{n2}</td>
                            <td>Number of distinct operands</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Total Operators</td>
                            <td><strong>N₁</strong></td>
                            <td class="metric-value">{N1}</td>
                            <td>Total occurrences of operators</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Total Operands</td>
                            <td><strong>N₂</strong></td>
                            <td class="metric-value">{N2}</td>
                            <td>Total occurrences of operands</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Program Length</td>
                            <td><strong>N</strong></td>
                            <td class="metric-value">{N}</td>
                            <td>Total program length (N₁ + N₂)</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Vocabulary</td>
                            <td><strong>n</strong></td>
                            <td class="metric-value">{n}</td>
                            <td>Program vocabulary (n₁ + n₂)</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Volume</td>
                            <td><strong>V</strong></td>
                            <td class="metric-value">{V:,.2f}</td>
                            <td>Program size in bits (N × log₂(n))</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Difficulty</td>
                            <td><strong>D</strong></td>
                            <td class="metric-value">{D:.2f}</td>
                            <td>Implementation difficulty ((n₁/2) × (N₂/n₂))</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Effort</td>
                            <td><strong>E</strong></td>
                            <td class="metric-value">{E:,.2f}</td>
                            <td>Mental effort required (D × V)</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Time</td>
                            <td><strong>T</strong></td>
                            <td class="metric-value">{T:.2f} s</td>
                            <td>Estimated coding time (E / 18)</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Program Level</td>
                            <td><strong>L</strong></td>
                            <td class="metric-value">{L:.4f}</td>
                            <td>Program abstraction level (1 / D)</td>
                        </tr>
                        <tr>
                            <td class="metric-name">Estimated Bugs</td>
                            <td><strong>B</strong></td>
                            <td class="metric-value">{B:.2f}</td>
                            <td>Potential defects (V / 3000)</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        return metrics_table
    
    @staticmethod
    def _get_mi_badge(mi: float) -> str:
        """
        Get HTML badge for Maintainability Index with color coding.
        
        Args:
            mi: Maintainability Index value
            
        Returns:
            HTML string with colored badge
        """
        if mi >= 85:
            color_class = "badge-green"
        elif mi >= 65:
            color_class = "badge-yellow"
        else:
            color_class = "badge-red"
        
        return f'<span class="badge {color_class}">{mi:.1f}</span>'
    
    # Legacy method for backward compatibility
    @staticmethod
    def generate_html_report(classes, charts: Dict[str, str], output_path: str):
        """
        Legacy method for backward compatibility.
        Converts ClassMetrics objects to the new data format and calls render().
        """
        from astra.metrics_visitor import ClassMetrics, MethodMetrics
        
        # Convert to new format
        data = {
            'project_name': 'Java Project',
            'summary': {
                'total_files': len(classes),
                'total_loc': sum(c.loc for c in classes),
                'avg_mi': sum(c.maintainability_index for c in classes) / len(classes) if classes else 0.0,
                'god_classes_count': sum(1 for c in classes if c.maintainability_index < 65 or c.wmc > 20)
            },
            'charts': {
                'scatter_b64': charts.get('complexity_scatter', ''),
                'radar_b64': charts.get('ck_radar', '')
            },
            'classes': []
        }
        
        for cls in classes:
            class_data = {
                'name': cls.class_name,
                'mi': cls.maintainability_index,
                'wmc': cls.wmc,
                'dit': cls.dit,
                'cbo': cls.cbo,
                'halstead_effort_sum': cls.aggregated_halstead.get('E', 0.0) if cls.aggregated_halstead else 0.0,
                'halstead': cls.aggregated_halstead if cls.aggregated_halstead else {},
                'methods': []
            }
            
            for method_name, method in cls.methods.items():
                method_data = {
                    'name': method_name,
                    'complexity': method.cyclomatic_complexity,
                    'effort': method.halstead.get('E', 0.0) if method.halstead else 0.0,
                    'halstead': method.halstead if method.halstead else {}
                }
                class_data['methods'].append(method_data)
            
            data['classes'].append(class_data)
        
        ReportGenerator.render(data, output_path)
