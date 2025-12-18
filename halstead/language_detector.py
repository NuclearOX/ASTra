"""
Language Detection Module
Detects programming language from file extension
"""

from pathlib import Path
from .constants import SUPPORTED_EXTENSIONS


class LanguageDetector:
    """Detects programming language from file extension"""
    
    @staticmethod
    def detect(filename):
        """
        Detect programming language from file extension.
        
        Args:
            filename: Path to the file
            
        Returns:
            Language code ('c' or 'java') or None if unsupported
        """
        ext = Path(filename).suffix.lower()
        
        for lang, extensions in SUPPORTED_EXTENSIONS.items():
            if ext in extensions:
                return lang
        
        return None
    
    @staticmethod
    def is_supported(filename):
        """
        Check if file extension is supported.
        
        Args:
            filename: Path to the file
            
        Returns:
            True if supported, False otherwise
        """
        return LanguageDetector.detect(filename) is not None

