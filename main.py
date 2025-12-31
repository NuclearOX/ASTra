"""
ASTra - Java Static Analysis Tool
Main entry point for the analysis tool.

Usage:
    python main.py <input_directory> [--output <output_file>]
"""

import os
import sys
import argparse
from pathlib import Path

from astra.graph_builder import InheritanceGraphBuilder
from astra.metrics_visitor import MetricsVisitor
from astra.chart_generator import ChartGenerator
from astra.report_generator import ReportGenerator
from astra.constants import C, DEFAULT_OUTPUT_DIR


def main():
    """Main entry point for ASTra"""
    parser = argparse.ArgumentParser(
        description='ASTra - Java Static Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py examples/
  python main.py /path/to/java/project --output report.html
        """
    )
    
    parser.add_argument(
        'input_dir',
        type=str,
        help='Directory containing Java source files to analyze'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='astra_report.html',
        help='Output HTML report filename (default: astra_report.html). Reports are saved in the output/ directory.'
    )
    
    args = parser.parse_args()
    
    # Validate input directory
    input_path = Path(args.input_dir)
    if not input_path.exists():
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        sys.exit(1)
    
    if not input_path.is_dir():
        print(f"Error: '{args.input_dir}' is not a directory.")
        sys.exit(1)
    
    # Ensure output directory exists
    output_dir = Path(DEFAULT_OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    # Determine output file path
    # If user provided a path, use it; otherwise use just the filename in output directory
    output_path = Path(args.output)
    if output_path.is_absolute():
        # If absolute path provided, use it as-is
        final_output_path = output_path
    elif output_path.parent != Path('.'):
        # If relative path with directory provided, put it in output directory
        final_output_path = output_dir / output_path
    else:
        # If just filename provided, put it in output directory
        final_output_path = output_dir / output_path.name
    
    # Ensure the output directory exists
    final_output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"{C.HEADER}{'=' * 60}{C.END}")
    print(f"{C.HEADER}ASTra - Java Static Analysis Tool{C.END}")
    print(f"{C.HEADER}{'=' * 60}{C.END}")
    print(f"{C.BLUE}Input directory: {input_path.absolute()}{C.END}")
    print(f"{C.BLUE}Output report: {final_output_path}{C.END}")
    print()
    
    # ============================================================
    # PASS 1: Build Inheritance Graph
    # ============================================================
    print(f"{C.BLUE}Phase 1: Building inheritance graph...{C.END}")
    graph_builder = InheritanceGraphBuilder()
    graph_builder.build_graph_from_directory(str(input_path))
    
    inheritance_graph = graph_builder.get_graph()
    class_files = {name: graph_builder.get_class_file(name) 
                   for name in graph_builder.all_classes}
    
    print(f"  {C.GREEN}Found {len(inheritance_graph)} classes{C.END}")
    print(f"  {C.GREEN}Inheritance relationships: {sum(1 for p in inheritance_graph.values() if p is not None)}{C.END}")
    print()
    
    # ============================================================
    # PASS 2: Calculate Metrics
    # ============================================================
    print(f"{C.BLUE}Phase 2: Calculating metrics...{C.END}")
    metrics_visitor = MetricsVisitor(inheritance_graph, class_files)
    
    # Analyze all Java files
    java_files = list(input_path.rglob('*.java'))
    print(f"  Analyzing {len(java_files)} Java files...")
    
    for java_file in java_files:
        metrics_visitor.analyze_file(str(java_file))
    
    # Get results
    classes = list(metrics_visitor.get_results().values())
    
    # Calculate DIT and NOC for each class
    for class_metrics in classes:
        class_metrics.dit = graph_builder.calculate_dit(class_metrics.class_name)
        class_metrics.noc = graph_builder.calculate_noc(class_metrics.class_name)
    
    print(f"  {C.GREEN}Analyzed {len(classes)} classes{C.END}")
    print(f"  {C.GREEN}Total methods: {sum(len(c.methods) for c in classes)}{C.END}")
    print()
    
    # ============================================================
    # Phase 3: Generate Visualizations
    # ============================================================
    print(f"{C.BLUE}Phase 3: Generating visualizations...{C.END}")
    chart_generator = ChartGenerator()
    charts = chart_generator.generate_all_charts(classes)
    print(f"  {C.GREEN}Generated {len(charts)} charts{C.END}")
    print()
    
    # ============================================================
    # Phase 4: Generate Report
    # ============================================================
    print(f"{C.BLUE}Phase 4: Generating HTML report...{C.END}")
    report_generator = ReportGenerator()
    report_generator.generate_html_report(classes, charts, str(final_output_path))
    print(f"  {C.GREEN}Report saved to: {final_output_path}{C.END}")
    print()
    
    # ============================================================
    # Summary
    # ============================================================
    print(f"{C.HEADER}{'=' * 60}{C.END}")
    print(f"{C.HEADER}Analysis Complete!{C.END}")
    print(f"{C.HEADER}{'=' * 60}{C.END}")
    print(f"{C.BLUE}Total Classes: {len(classes)}{C.END}")
    print(f"{C.BLUE}Total Methods: {sum(len(c.methods) for c in classes)}{C.END}")
    
    if classes:
        avg_mi = sum(c.maintainability_index for c in classes) / len(classes)
        green = sum(1 for c in classes if c.maintainability_index > 85)
        yellow = sum(1 for c in classes if 65 <= c.maintainability_index <= 85)
        red = sum(1 for c in classes if c.maintainability_index < 65)
        
        print(f"{C.BLUE}Average MI: {avg_mi:.2f}{C.END}")
        print(f"{C.BLUE}Maintainability: {C.GREEN}Green={green}{C.END}, {C.WARN}Yellow={yellow}{C.END}, {C.FAIL}Red={red}{C.END}")
    
    print(f"\n{C.GREEN}Open '{final_output_path}' in your browser to view the full report.{C.END}")
    print(f"{C.HEADER}{'=' * 60}{C.END}")


if __name__ == '__main__':
    main()

