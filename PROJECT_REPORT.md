# Halstead Metrics Analyzer - Project Report

## Table of Contents

1. [Project Overview](#project-overview)
2. [Introduction to Halstead Metrics](#introduction-to-halstead-metrics)
3. [System Architecture](#system-architecture)
4. [Implementation Details](#implementation-details)
5. [Features and Capabilities](#features-and-capabilities)
6. [Usage Guide](#usage-guide)
7. [Output Structure](#output-structure)
8. [Example Analysis](#example-analysis)
9. [Technical Specifications](#technical-specifications)
10. [Limitations and Future Work](#limitations-and-future-work)
11. [Conclusion](#conclusion)

---

## Project Overview

### Purpose

The **Halstead Metrics Analyzer** is a static code analysis tool developed for the "Programming Paradigms and Languages" course in the Master's Degree in Computer Engineering. The tool implements Halstead Complexity Metrics to quantitatively assess code complexity, maintainability, and quality for C and Java programming languages.

### Objectives

- Implement comprehensive Halstead metrics calculation
- Support multiple programming languages (C and Java)
- Provide visual analysis through charts and graphs
- Generate professional HTML reports
- Enable batch processing of multiple files
- Create a modular, maintainable codebase

### Key Achievements

✅ Multi-language support (C and Java)  
✅ Automatic language detection  
✅ Single file and directory processing  
✅ Visual charts embedded in HTML reports  
✅ Project-specific output organization  
✅ Modular architecture for extensibility  

---

## Introduction to Halstead Metrics

### Historical Context

Halstead Complexity Metrics were introduced by Maurice H. Halstead in 1977 as part of his "Software Science" theory. These metrics provide a quantitative approach to measuring software complexity based on the number of operators and operands in a program.

### Theoretical Foundation

Halstead's theory is based on the premise that software can be measured using fundamental units:
- **Operators**: Symbols or keywords that perform operations (e.g., `+`, `if`, `while`, `return`)
- **Operands**: Variables, constants, and identifiers that operators act upon

### Base Metrics

The analysis begins by counting:

1. **n1**: Number of unique operators
2. **n2**: Number of unique operands
3. **N1**: Total occurrences of operators
4. **N2**: Total occurrences of operands

### Derived Metrics

From these base counts, the following metrics are calculated:

#### 1. Program Vocabulary (n)
```
n = n1 + n2
```
Total number of unique tokens in the program.

#### 2. Program Length (N)
```
N = N1 + N2
```
Total number of tokens (operators + operands) in the program.

#### 3. Volume (V)
```
V = N × log₂(n)
```
Represents the size of the program in "bits" of information. Higher volume indicates more complex code.

#### 4. Difficulty (D)
```
D = (n1/2) × (N2/n2)
```
Measures how difficult the program is to understand or implement. Higher difficulty suggests more complex logic.

#### 5. Effort (E)
```
E = D × V
```
Represents the mental effort required to implement the program. Measured in "elementary mental discriminations."

#### 6. Time (T)
```
T = E / 18
```
Estimated time (in seconds) required to implement the program, based on psychological studies.

#### 7. Program Level (L)
```
L = 1 / D
```
Represents the abstraction level of the program. Higher level indicates better abstraction.

#### 8. Estimated Bugs (B)
```
B = V / 3000
```
Estimated number of bugs in the program, based on empirical studies.

### Quality Metrics

In addition to Halstead metrics, the tool calculates:

#### Cyclomatic Complexity (CC)
Measures the number of independent paths through the code by counting control flow statements (if, while, for, switch, etc.). Lower values indicate simpler control flow.

#### Maintainability Index (MI)
A composite metric calculated as:
```
MI = 171 - 5.2 × ln(V) - 0.23 × CC - 16.2 × ln(LOC)
```
Scaled to 0-100, where:
- **80-100**: Excellent maintainability
- **50-79**: Good maintainability
- **0-49**: Poor maintainability (needs refactoring)

#### Logical Lines of Code (LOC)
Count of non-empty lines of code, excluding comments and blank lines.

---

## System Architecture

### Modular Design

The project follows a modular architecture, separating concerns into distinct, reusable modules:

```
halstead/
├── __init__.py          # Package initialization and public API
├── constants.py          # Configuration and constants
├── language_detector.py  # Language detection logic
├── analyzer.py           # Core metrics calculation
├── chart_generator.py    # Visualization generation
├── html_reporter.py      # HTML report creation
└── file_processor.py     # File/directory processing
```

### Component Responsibilities

#### 1. `constants.py`
- Centralized configuration management
- Terminal color codes for user interface
- Default paths and supported file extensions
- Dependency availability checks (matplotlib)

#### 2. `language_detector.py`
- Detects programming language from file extensions
- Validates file support
- Extensible for additional languages

#### 3. `analyzer.py`
- Core analysis engine
- Language-specific keyword and operator definitions
- Tokenization and parsing
- Metrics calculation
- Preprocessing (removes preprocessor directives, imports)

#### 4. `chart_generator.py`
- Creates visualization charts using matplotlib
- Generates base64-encoded images for HTML embedding
- Handles graceful degradation when matplotlib is unavailable

#### 5. `html_reporter.py`
- Generates professional HTML reports
- Embeds charts as base64 images
- Creates styled, responsive reports

#### 6. `file_processor.py`
- Handles single file processing
- Recursive directory processing
- Project-specific output organization
- Summary generation

#### 7. `Halstead_analyzer.py`
- Main entry point
- Command-line interface
- User interaction and error handling
- Orchestrates all modules

### Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Dependency Injection**: Modules accept dependencies as parameters
3. **Graceful Degradation**: Optional features fail gracefully
4. **Extensibility**: Easy to add new languages or features
5. **Testability**: Each module can be tested independently

---

## Implementation Details

### Language Support

#### C Language
- **Keywords**: 32 C keywords (auto, break, case, char, const, etc.)
- **Operators**: Standard C operators including pointer operators (`->`, `*`, `&`)
- **Preprocessing**: Preprocessor directives (`#include`, `#define`, etc.) are filtered out
- **File Extensions**: `.c`, `.h`

#### Java Language
- **Keywords**: 50 Java keywords (abstract, class, extends, implements, etc.)
- **Operators**: Java operators including `instanceof` and method reference `::`
- **Imports**: Package and import statements are filtered out
- **File Extensions**: `.java`

### Tokenization Process

The analyzer uses regular expressions to tokenize source code:

1. **String Literals**: `"(?:\\.|[^\\"])*"`
2. **Character Literals**: `'(?:\\.|[^\\\'])*'`
3. **Comments**: `//.*?$|/\*.*?\*/` (single-line and multi-line)
4. **Numbers**: Supports integers, floats, scientific notation, and hexadecimal
5. **Identifiers**: `[a-zA-Z_][a-zA-Z0-9_]*`
6. **Operators**: Language-specific operator patterns
7. **Whitespace**: Skipped during analysis

### Cyclomatic Complexity Calculation

The tool tracks control flow statements to calculate cyclomatic complexity:
- Base complexity starts at 1
- Incremented for: `if`, `else`, `while`, `for`, `case`, `catch`, `switch`, `try`, `?`, `&&`, `||`

### Output Organization

Each analysis creates a project-specific directory structure:

```
output/
└── {project_name}/
    ├── c/
    │   ├── charts/
    │   │   └── {filename}_chart.png
    │   └── reports/
    │       └── {filename}_report.html
    └── java/
        ├── charts/
        │   └── {filename}_chart.png
        └── reports/
            └── {filename}_report.html
```

This organization ensures:
- Each project has its own output directory
- Charts and reports are separated by language
- Easy to locate and manage analysis results
- No conflicts between different analysis runs

---

## Features and Capabilities

### Core Features

1. **Multi-Language Analysis**
   - Automatic language detection
   - Language-specific keyword and operator recognition
   - Appropriate preprocessing for each language

2. **Flexible Input**
   - Single file analysis
   - Recursive directory processing
   - Command-line or interactive input

3. **Comprehensive Metrics**
   - All Halstead base and derived metrics
   - Cyclomatic complexity
   - Maintainability index
   - Lines of code

4. **Visual Analysis**
   - Quality profile charts (MI, Difficulty, Complexity)
   - Halstead scale charts (Volume, Effort)
   - Embedded in HTML reports

5. **Professional Reports**
   - Styled HTML reports
   - Embedded charts (base64 encoded)
   - Detailed metrics tables
   - Color-coded maintainability scores

6. **User Experience**
   - Colored terminal output
   - Progress indicators
   - Summary reports
   - Automatic browser opening

### Advanced Features

- **Graceful Error Handling**: Continues processing even if individual files fail
- **Unicode Support**: Handles various character encodings
- **Modular Architecture**: Easy to extend and maintain
- **Project Isolation**: Each analysis has its own output directory

---

## Usage Guide

### Installation

1. **Prerequisites**
   - Python 3.6 or higher
   - pip package manager

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install matplotlib
   ```

### Basic Usage

#### Interactive Mode
```bash
python Halstead_analyzer.py
```
Then enter the file or directory path when prompted.

#### Command-Line Mode

**Single File:**
```bash
python Halstead_analyzer.py examples/example.c
python Halstead_analyzer.py examples/example.java
```

**Directory:**
```bash
python Halstead_analyzer.py examples/
```

### Programmatic Usage

The modules can be imported and used programmatically:

```python
from halstead import Analyzer, LanguageDetector, ChartGenerator, HtmlReporter

# Detect language
lang = LanguageDetector.detect('example.java')

# Analyze code
analyzer = Analyzer(language=lang)
with open('example.java', 'r') as f:
    code = f.read()
result = analyzer.analyze(code, 'example.java')

# Generate visualization
chart_file, chart_base64 = ChartGenerator.generate(result, 'output/charts')

# Generate report
report_path = HtmlReporter.generate(result, chart_base64, 'output/reports')
```

---

## Output Structure

### Directory Organization

When analyzing a file or directory, the tool creates a project-specific output structure:

**Example: Analyzing `examples/example.c`**
```
output/
└── example/
    └── c/
        ├── charts/
        │   └── example_chart.png
        └── reports/
            └── example_report.html
```

**Example: Analyzing `examples/` directory**
```
output/
└── examples/
    ├── c/
    │   ├── charts/
    │   │   ├── example_chart.png
    │   │   └── simple_chart.png
    │   └── reports/
    │       ├── example_report.html
    │       └── simple_report.html
    └── java/
        ├── charts/
        │   ├── example_chart.png
        │   └── simple_chart.png
        └── reports/
            ├── example_report.html
            └── simple_report.html
```

### HTML Report Contents

Each HTML report includes:

1. **Header Section**
   - File name and path
   - Analysis timestamp
   - Language badge

2. **Maintainability Index**
   - Large, color-coded score
   - Visual indicator (green/yellow/red)

3. **Visual Charts**
   - Quality Profile (MI, Difficulty, Complexity)
   - Halstead Scale (Volume, Effort) - logarithmic scale

4. **Halstead Overview Cards**
   - Program Level (L)
   - Volume (V)
   - Difficulty (D)
   - Effort (E)

5. **Detailed Metrics Table**
   - All base metrics (n1, n2, N1, N2)
   - All derived metrics (V, D, E, T, L, B)
   - Quality metrics (CC, LOC)
   - Descriptions for each metric

---

## Example Analysis

### Example 1: Simple C Program

**Input:** `examples/simple.c`
```c
#include <stdio.h>

int main() {
    int a = 10;
    int b = 5;
    int sum = a + b;
    printf("Sum: %d\n", sum);
    return 0;
}
```

**Typical Results:**
- **Volume (V)**: ~50-100
- **Difficulty (D)**: ~2-5
- **Effort (E)**: ~100-500
- **Maintainability Index**: 85-95 (Excellent)
- **Cyclomatic Complexity**: 1

### Example 2: Complex Java Program

**Input:** `examples/example.java`** (Student Management System)

**Typical Results:**
- **Volume (V)**: ~500-1000
- **Difficulty (D)**: ~10-20
- **Effort (E)**: ~5000-20000
- **Maintainability Index**: 60-80 (Good)
- **Cyclomatic Complexity**: 5-15

### Interpreting Results

**Low Complexity (Good):**
- Volume < 500
- Difficulty < 10
- Maintainability Index > 80
- Cyclomatic Complexity < 10

**Medium Complexity (Acceptable):**
- Volume 500-1000
- Difficulty 10-20
- Maintainability Index 50-80
- Cyclomatic Complexity 10-20

**High Complexity (Needs Refactoring):**
- Volume > 1000
- Difficulty > 20
- Maintainability Index < 50
- Cyclomatic Complexity > 20

---

## Technical Specifications

### System Requirements

- **Python Version**: 3.6 or higher
- **Operating System**: Cross-platform (Windows, Linux, macOS)
- **Dependencies**: 
  - `matplotlib` (optional, for charts)
  - Standard library only (re, math, os, pathlib, etc.)

### Performance Characteristics

- **Processing Speed**: ~100-1000 lines per second (depending on complexity)
- **Memory Usage**: Minimal (processes files sequentially)
- **Scalability**: Handles large codebases efficiently

### Supported File Formats

- **C Source Files**: `.c`, `.h`
- **Java Source Files**: `.java`
- **Text Encoding**: UTF-8 (with fallback handling)

### Error Handling

- **File Not Found**: Clear error message
- **Unsupported File Type**: Warning, skip file
- **Parse Errors**: Graceful degradation, continue processing
- **Missing Dependencies**: Charts disabled, analysis continues

---

## Limitations and Future Work

### Current Limitations

1. **Language Support**: Currently supports only C and Java
2. **Preprocessing**: C macros are removed but not expanded
3. **Context Awareness**: No semantic analysis or type checking
4. **Dependencies**: Does not analyze external library calls
5. **Multi-file Analysis**: Each file analyzed independently

### Potential Enhancements

1. **Additional Languages**
   - Python
   - C++
   - JavaScript
   - C#

2. **Advanced Features**
   - Comparison reports between files
   - Trend analysis over time
   - Custom threshold configuration
   - Export to JSON/CSV formats

3. **Integration**
   - CI/CD pipeline integration
   - IDE plugins
   - API interface (REST/GraphQL)
   - GUI application

4. **Analysis Improvements**
   - Semantic analysis
   - Type-aware metrics
   - Dependency analysis
   - Code smell detection

---

## Conclusion

### Summary

The Halstead Metrics Analyzer successfully implements a comprehensive static code analysis tool that:

- Calculates all Halstead complexity metrics accurately
- Supports multiple programming languages (C and Java)
- Provides visual analysis through embedded charts
- Generates professional HTML reports
- Organizes output in a clean, project-specific structure
- Follows modular architecture principles for maintainability

### Educational Value

This project demonstrates:

- **Software Engineering Principles**: Modular design, separation of concerns
- **Static Analysis**: Code analysis without execution
- **Software Metrics**: Quantitative code quality measurement
- **Multi-paradigm Programming**: Handling different programming paradigms
- **Python Best Practices**: Package structure, error handling, documentation

### Practical Applications

The tool can be used for:

- **Code Review**: Identify complex code sections
- **Refactoring Guidance**: Find areas needing improvement
- **Quality Assurance**: Maintain code quality standards
- **Educational Purposes**: Understand code complexity
- **Research**: Study software metrics and complexity

### Final Notes

The modular architecture makes the tool:
- **Extensible**: Easy to add new languages or features
- **Maintainable**: Clear separation of concerns
- **Testable**: Each module can be tested independently
- **Reusable**: Components can be used in other projects

---

## References

1. Halstead, M. H. (1977). *Elements of Software Science*. Elsevier North-Holland.
2. McCabe, T. J. (1976). A Complexity Measure. *IEEE Transactions on Software Engineering*, SE-2(4), 308-320.
3. Oman, P., & Hagemeister, J. (1992). Metrics for assessing a software system's maintainability. *Proceedings of the Conference on Software Maintenance*.

---

## Appendix

### Project Files

- `Halstead_analyzer.py` - Main entry point
- `halstead/` - Package directory with all modules
- `examples/` - Sample C and Java files for testing
- `requirements.txt` - Python dependencies
- `README.md` - User documentation
- `PROJECT_REPORT.md` - This comprehensive report

### Example Files

The `examples/` directory contains:
- `example.c` - Complex calculator program
- `simple.c` - Basic C example
- `example.java` - Student management system
- `simple.java` - Simple Java calculator

---

**Project Developed For**: Programming Paradigms and Languages Course  
**Master's Degree in Computer Engineering**  
**Academic Year**: 2024-2025

---

*End of Report*

