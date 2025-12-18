"""
Main Entry Point for Halstead Metrics Analyzer
Command-line interface for the modular analyzer
"""

import sys
import os
import webbrowser
from pathlib import Path
from halstead import (
    Analyzer, LanguageDetector, ChartGenerator, HtmlReporter,
    process_file, process_directory, print_summary, C
)
from halstead.constants import HAS_MATPLOTLIB, DEFAULT_OUTPUT_DIR


def print_detailed_results(res):
    """Print detailed analysis results to console"""
    b = res['base']
    h = res['halstead']
    q = res['quality']
    
    print(f"\n{C.BLUE}--- Base Counts ---{C.END}")
    print(f"Unique Operators (n1): {b['n1']} | Unique Operands (n2): {b['n2']}")
    print(f"Total Operators (N1): {b['N1']} | Total Operands (N2): {b['N2']}")
    
    print(f"\n{C.BLUE}--- Halstead Metrics ---{C.END}")
    print(f"Volume (V):           {h['V']:.2f}")
    print(f"Difficulty (D):       {h['D']:.2f}")
    print(f"Program Level (L):    {h['L']:.4f}")
    print(f"Effort (E):           {h['E']:.2f}")
    print(f"Time (T):             {h['T']:.2f} s")
    print(f"Estimated Bugs (B):   {h['B']:.2f}")
    
    print(f"\n{C.BLUE}--- Quality Metrics ---{C.END}")
    print(f"Maintainability Index: {q['mi']:.2f} / 100")
    print(f"Cyclomatic Complexity: {q['cc']}")
    print(f"Logical LOC:           {q['loc']}")


def main():
    """Main entry point"""
    print(f"{C.HEADER}{'='*70}{C.END}")
    print(f"{C.HEADER}  Module Complexity Analyzer - Halstead Metrics{C.END}")
    print(f"{C.HEADER}  Supports: C (.c, .h) and Java (.java){C.END}")
    print(f"{C.HEADER}{'='*70}{C.END}\n")
    
    # Get target from command line or user input
    target = ""
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(f"{C.BLUE}Enter file or directory path to analyze: {C.END}").strip().strip('"').strip("'")
    
    if not target:
        print(f"{C.FAIL}Error: No input provided.{C.END}")
        sys.exit(1)
    
    if not os.path.exists(target):
        print(f"{C.FAIL}Error: '{target}' does not exist.{C.END}")
        sys.exit(1)
    
    output_base_dir = DEFAULT_OUTPUT_DIR
    results = []
    
    try:
        if os.path.isfile(target):
            print(f"\n{C.BLUE}Analyzing single file: {target}{C.END}")
            result = process_file(target, output_base_dir)
            if result:
                results.append(result)
                res, report_path = result
                
                # Print detailed output
                print_detailed_results(res)
                
                if HAS_MATPLOTLIB:
                    print(f"\n{C.GREEN}Chart generated successfully{C.END}")
                else:
                    print(f"\n{C.WARN}Matplotlib not found. Charts disabled.{C.END}")
                
                print(f"\n{C.GREEN}Report generated: {report_path}{C.END}")
                
                # Try to open report in browser
                try:
                    webbrowser.open(report_path)
                except:
                    pass
        elif os.path.isdir(target):
            print(f"\n{C.BLUE}Analyzing directory: {target}{C.END}")
            results = process_directory(target, output_base_dir)
            print_summary(results)
            
            if results:
                print(f"\n{C.GREEN}All reports saved in: {output_base_dir}/{C.END}")
                # Try to open the first report
                try:
                    webbrowser.open(results[0][1])
                except:
                    pass
        else:
            print(f"{C.FAIL}Error: '{target}' is neither a file nor a directory.{C.END}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{C.WARN}Analysis interrupted by user.{C.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{C.FAIL}Critical error: {e}{C.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
