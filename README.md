# Halstead Metrics Analyzer

## Project Overview

This project is a **Static Code Analysis Tool** developed for the "Programming Paradigms and Languages" course in the Master's Degree in Computer Engineering. The tool implements **Halstead Complexity Metrics** to analyze code complexity and maintainability for both **C** and **Java** programming languages.

## Features

- ✅ **Multi-language Support**: Analyzes both C (`.c`, `.h`) and Java (`.java`) files
- ✅ **Automatic Language Detection**: Detects programming language from file extension
- ✅ **Single File Analysis**: Analyze individual source files
- ✅ **Directory Processing**: Recursively analyze all supported files in a directory
- ✅ **Interactive Mode**: User-friendly command-line interface
- ✅ **Visual Reports**: HTML reports with embedded charts and graphs
- ✅ **Organized Output**: Results organized in subdirectories by language
- ✅ **Comprehensive Metrics**: Calculates all Halstead metrics plus quality indicators

## Halstead Metrics Explained

The tool calculates the following metrics based on Halstead's Software Science:

### Base Metrics
- **n1**: Number of unique operators
- **n2**: Number of unique operands
- **N1**: Total number of operator occurrences
- **N2**: Total number of operand occurrences

### Derived Metrics
- **n = n1 + n2**: Program vocabulary (total unique tokens)
- **N = N1 + N2**: Program length (total tokens)
- **V = N × log₂(n)**: Program volume (size in bits)
- **D = (n1/2) × (N2/n2)**: Program difficulty
- **E = D × V**: Programming effort (mental effort required)
- **T = E / 18**: Time to implement (in seconds)
- **L = 1/D**: Program level (abstraction level)
- **B = V / 3000**: Estimated number of bugs

### Quality Metrics
- **Cyclomatic Complexity (CC)**: Number of independent paths through the code
- **Maintainability Index (MI)**: Code maintainability score (0-100)
- **Logical LOC**: Lines of code (excluding empty lines)

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Required Packages

```bash
pip install matplotlib
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

The tool will work without matplotlib, but charts will be disabled.

### Project Structure

The project uses a modular architecture:

```
PLP_Project/
├── Halstead_analyzer.py  # Main entry point
├── halstead/              # Package directory
│   ├── __init__.py
│   ├── constants.py
│   ├── language_detector.py
│   ├── analyzer.py
│   ├── chart_generator.py
│   ├── html_reporter.py
│   └── file_processor.py
├── examples/              # Example source files
│   ├── example.c
│   ├── simple.c
│   ├── example.java
│   └── simple.java
├── output/                # Generated reports (created automatically)
├── requirements.txt
└── README.md
```

## Usage

### Basic Usage

Run the script and follow the interactive prompts:

```bash
python Halstead_analyzer.py
```

When prompted, enter either:
- A **file path** (e.g., `examples/example.c` or `examples/example.java`)
- A **directory path** (e.g., `examples/`) to analyze all supported files

### Command Line Usage

You can also pass the file or directory as a command-line argument:

```bash
# Analyze a single file
python Halstead_analyzer.py examples/example.c

# Analyze a directory
python Halstead_analyzer.py examples/
```

### Example Commands

```bash
# Analyze a C file
python Halstead_analyzer.py examples/example.c

# Analyze a Java file
python Halstead_analyzer.py examples/example.java

# Analyze all files in examples directory
python Halstead_analyzer.py examples/
```

## Output Structure

The tool generates organized output in the `output/` directory.

### Report Contents

Each HTML report includes:
- **Maintainability Index** with color-coded score
- **Visual Charts**: Quality profile and Halstead scale graphs (embedded as base64)
- **Halstead Overview**: Key metrics in card format
- **Detailed Metrics Table**: Complete breakdown of all calculated metrics
- **Language Badge**: Indicates the analyzed language

## Example Files

The `examples/` directory contains sample files for testing:

## How It Works

### 1. Language Detection
The tool automatically detects the programming language from the file extension:
- `.c`, `.h` → C language
- `.java` → Java language

### 2. Tokenization
The code is tokenized into:
- **Operators**: Keywords, symbols, and operators
- **Operands**: Identifiers, literals, and constants
- Comments and whitespace are ignored

### 3. Metrics Calculation
- Counts unique and total operators/operands
- Calculates Halstead metrics using the formulas
- Computes cyclomatic complexity by tracking control flow statements
- Calculates maintainability index

### 4. Visualization
- Generates charts using matplotlib (if available)
- Embeds charts as base64-encoded images in HTML reports
- Creates professional HTML reports with styling

### 5. Output Organization
- Creates language-specific subdirectories
- Separates charts and reports
- Maintains clean file structure

## Language-Specific Features

### C Language Support
- C keywords (auto, break, case, char, const, etc.)
- C operators (including pointer operators `->`, `*`, `&`)
- Preprocessor directives are filtered out
- Header files (`.h`) are supported

### Java Language Support
- Java keywords (abstract, class, extends, implements, etc.)
- Java operators (including `instanceof`, `::`)
- Package and import statements are filtered out
- Object-oriented constructs are properly recognized

## Interpreting Results

### Maintainability Index (MI)
- **80-100**: Excellent - Code is highly maintainable
- **50-79**: Good - Code is reasonably maintainable
- **0-49**: Poor - Code needs refactoring

### Volume (V)
- Lower values indicate more concise code
- Higher values suggest more complex implementations

### Difficulty (D)
- Measures how hard the code is to understand
- Lower values are better

### Effort (E)
- Mental effort required to implement the code
- Used to estimate development time

### Cyclomatic Complexity (CC)
- Measures code complexity through control flow
- Lower values (1-10) are ideal
- Higher values suggest need for refactoring

## Technical Details

### Architecture

The tool is organized into a modular package structure:

```
halstead/
├── __init__.py          # Package initialization and exports
├── constants.py          # Constants, configuration, and color codes
├── language_detector.py  # Language detection from file extensions
├── analyzer.py           # Core Halstead metrics calculation
├── chart_generator.py    # Visualization chart generation
├── html_reporter.py      # HTML report generation
└── file_processor.py     # File and directory processing logic
```

**Main Components:**

1. **`LanguageDetector`**: Detects programming language from file extension
2. **`Analyzer`**: Performs tokenization and metrics calculation
3. **`ChartGenerator`**: Creates visualization charts
4. **`HtmlReporter`**: Generates HTML reports with embedded graphics
5. **`file_processor`**: Handles single file and directory processing

**Main Entry Point:**
- **`Halstead_analyzer.py`**: Command-line interface that uses the modular components

### Token Recognition

The analyzer uses regular expressions to identify:
- String literals
- Character literals
- Comments (single-line and multi-line)
- Numbers (integers, floats, hex)
- Identifiers
- Operators
- Whitespace

### Error Handling

- Gracefully handles missing matplotlib
- Skips unsupported file types
- Provides clear error messages
- Continues processing even if individual files fail

## Limitations

1. **Preprocessing**: C preprocessor macros are removed but not expanded
2. **Context**: Does not perform semantic analysis
3. **Dependencies**: Does not analyze external library calls
4. **Multi-file**: Each file is analyzed independently

## Future Enhancements

Potential improvements:
- Support for more languages (Python, C++, etc.)
- Comparison reports between files
- Trend analysis over time
- Integration with CI/CD pipelines
- Export to JSON/CSV formats
- Custom threshold configuration

## Academic Context

This project demonstrates:
- **Static Analysis**: Code analysis without execution
- **Software Metrics**: Quantitative code quality measurement
- **Software Engineering**: Best practices in tool development
- **Multi-paradigm Support**: Handling different programming paradigms

## References

- Halstead, M. H. (1977). *Elements of Software Science*. Elsevier.
- McCabe, T. J. (1976). A Complexity Measure. *IEEE Transactions on Software Engineering*.

## License

This project is developed for academic purposes as part of the Master's Degree in Computer Engineering curriculum.

---

## Quick Start Guide

1. **Install dependencies**:
   ```bash
   pip install matplotlib
   ```

2. **Run the analyzer**:
   ```bash
   python Halstead_analyzer.py
   ```

3. **Enter a file or directory path** when prompted

4. **View the generated HTML reports** in the `output/` directory

5. **Open reports in your browser** to see visualizations and metrics

---
