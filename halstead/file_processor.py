"""
File Processing Module
Handles single file and directory processing
"""

import os
from pathlib import Path
from .analyzer import Analyzer
from .language_detector import LanguageDetector
from .chart_generator import ChartGenerator
from .html_reporter import HtmlReporter
from .constants import C, DEFAULT_OUTPUT_DIR, SUPPORTED_EXTENSIONS


def process_file(filepath, output_base_dir):
    """
    Process a single file and generate analysis report.
    
    Args:
        filepath: Path to the source file
        output_base_dir: Base output directory (e.g., output)
        
    Returns:
        Tuple of (results_dict, report_path) or None if processing fails
    """
    lang = LanguageDetector.detect(filepath)
    if not lang:
        print(f"{C.WARN}Warning: Unsupported file type for {filepath}. Skipping.{C.END}")
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        analyzer = Analyzer(language=lang)
        res = analyzer.analyze(content, filepath)
        
        # Create structure: output/language/project_name/
        # Project name is derived from the filename stem
        project_name = Path(filepath).stem
        project_dir = os.path.join(output_base_dir, lang, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        # Generate chart (saved in project_dir)
        chart_file, _ = ChartGenerator.generate(res, project_dir)
        
        # Generate HTML report (saved in same project_dir, references chart by filename)
        report_path = HtmlReporter.generate(res, chart_file, project_dir)
        
        return res, report_path
        
    except Exception as e:
        print(f"{C.FAIL}Error processing {filepath}: {e}{C.END}")
        return None


def process_directory(dirpath, output_base_dir):
    """
    Process all supported files in a directory recursively.
    
    Args:
        dirpath: Path to directory
        output_base_dir: Base output directory (e.g., output)
        
    Returns:
        List of tuples (results_dict, report_path) for each processed file
    """
    results = []
    supported_extensions = []
    for exts in SUPPORTED_EXTENSIONS.values():
        supported_extensions.extend(exts)
    
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            filepath = os.path.join(root, file)
            if Path(filepath).suffix.lower() in supported_extensions:
                print(f"{C.BLUE}Processing: {filepath}{C.END}")
                result = process_file(filepath, output_base_dir)
                if result:
                    results.append(result)
    
    return results


def print_summary(results):
    """
    Print summary of all analyses.
    
    Args:
        results: List of tuples (results_dict, report_path)
    """
    if not results:
        return
    
    print(f"\n{C.HEADER}{'='*70}{C.END}")
    print(f"{C.HEADER}ANALYSIS SUMMARY{C.END}")
    print(f"{C.HEADER}{'='*70}{C.END}\n")
    
    for res, report_path in results:
        h = res['halstead']
        q = res['quality']
        filename = Path(res['file']).name
        
        print(f"{C.GREEN}File: {filename} ({res['language'].upper()}){C.END}")
        print(f"  Maintainability Index: {q['mi']:.1f}/100")
        print(f"  Volume: {h['V']:.0f} | Difficulty: {h['D']:.2f} | Effort: {h['E']:.0f}")
        print(f"  Report: {report_path}\n")

