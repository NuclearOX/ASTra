"""
Constants and configuration for ASTra
"""

# Terminal color management
class C:
    """Terminal color codes for formatted output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'

# Default output directory
DEFAULT_OUTPUT_DIR = "output"

# Matplotlib configuration
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

