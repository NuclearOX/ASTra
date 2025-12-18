"""
Halstead Metrics Analyzer Package
Modular static analysis tool for C and Java code.
"""

from .analyzer import Analyzer
from .language_detector import LanguageDetector
from .chart_generator import ChartGenerator
from .html_reporter import HtmlReporter
from .file_processor import process_file, process_directory, print_summary
from .constants import C

__version__ = "1.0.0"
__all__ = [
    'Analyzer',
    'LanguageDetector',
    'ChartGenerator',
    'HtmlReporter',
    'process_file',
    'process_directory',
    'print_summary',
    'C'
]

