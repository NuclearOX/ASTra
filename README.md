# ASTra - Java Static Analysis Tool

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![ANTLR4](https://img.shields.io/badge/ANTLR4-4.13+-green.svg)](https://www.antlr.org/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)](LICENSE)

**ASTra** (Java Automated Static Analysis) is a comprehensive static analysis tool that analyzes Java source code by generating and traversing Abstract Syntax Trees (ASTs) using ANTLR4. The tool calculates rigorous software metrics and generates professional HTML5 dashboards with visualizations.

## 🚀 Features

- ✅ **ANTLR4-Based Parsing**: Uses official Java 20 grammar for accurate AST generation
- ✅ **Two-Pass Analysis**: Separate inheritance graph building and metrics calculation
- ✅ **Complete Metrics Suite**: 
  - **Halstead Metrics**: All 12 metrics (n₁, n₂, N₁, N₂, N, n, V, D, E, T, L, B)
  - **Cyclomatic Complexity**: Independent paths through code
  - **Maintainability Index**: Code maintainability score (0-100)
  - **CK Metrics**: WMC, DIT, NOC, CBO (Object-Oriented Design metrics)
- ✅ **Visual Dashboards**: HTML5 reports with embedded Base64 charts
- ✅ **Progressive Disclosure**: Accordion-style interface for detailed exploration
- ✅ **Self-Contained Reports**: No external dependencies, works offline
- ✅ **Modular Architecture**: Clean separation of concerns, easy to extend

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Metrics Explained](#metrics-explained)
- [Report Structure](#report-structure)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Java Runtime Environment (JRE) - required only for ANTLR generation tool

### Step 1: Clone or Download

```bash
git clone <repository-url>
cd PLP_Project
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `matplotlib>=3.5.0` - For chart generation
- `antlr4-python3-runtime>=4.13.0` - ANTLR4 runtime
- `numpy>=1.21.0` - For numerical operations

### Step 2.5: Generate Parser

Before running the tool, you must generate the Python lexer and parser from the grammar files.

```bash
# Run the commands specified in commands.txt
antlr4 -Dlanguage=Python3 -visitor -no-listener grammar/Java20Lexer.g4
antlr4 -Dlanguage=Python3 -visitor -no-listener grammar/Java20Parser.g4
```

### Step 3: Verify Installation

```bash
python main.py examples --output test.html
```

If successful, you should see analysis progress and a report generated in `output/test.html`.

## 🚀 Quick Start

```bash
# Analyze a Java project directory
python main.py examples

# With custom output filename
python main.py examples --output my_analysis.html

# Analyze any Java project
python main.py /path/to/java/project
```

All reports are automatically saved in the `output/` directory.

## 📖 Usage

### Basic Command

```bash
python main.py <input_directory> [--output <filename>]
```

### Arguments

- **`input_directory`** (required): Directory containing Java source files (`.java`)
- **`--output`** (optional): Output HTML report filename (default: `astra_report.html`)

### Examples

```bash
# Analyze examples with default output
python main.py examples

# Custom output filename
python main.py examples --output project_analysis.html

# Analyze a full project
python main.py /path/to/my/java/project --output project_report.html
```

### Output

The tool generates:
1. **Console Output**: Progress information and summary statistics
2. **HTML Report**: Saved in `output/` directory with:
   - Dashboard with KPI cards
   - Visual charts (scatter plot, radar chart, distribution)
   - Hall of Shame (top 5 critical classes)
   - Detailed class analysis with accordion interface

## 📊 Metrics Explained

### Halstead Complexity Metrics

**Base Counts**:
- **n₁**: Unique operators count
- **n₂**: Unique operands count
- **N₁**: Total operator occurrences
- **N₂**: Total operand occurrences

**Derived Metrics**:
- **N**: Program Length (N₁ + N₂)
- **n**: Vocabulary (n₁ + n₂)
- **V**: Volume (N × log₂(n)) - Program size in bits
- **D**: Difficulty ((n₁/2) × (N₂/n₂)) - Implementation difficulty
- **E**: Effort (D × V) - Mental effort required
- **T**: Time (E / 18) - Estimated coding time (seconds)
- **L**: Program Level (1 / D) - Program abstraction level
- **B**: Estimated Bugs (V / 3000) - Potential defects

### Cyclomatic Complexity (CC)

Measures the number of independent paths through code. Increments for:
- Control flow statements: `if`, `while`, `for`, `switch`, `case`, `catch`, `try`
- Logical operators: `&&`, `||`
- Ternary operator: `?`

**Interpretation**:
- 1-10: Simple
- 11-20: Moderate
- 21-50: Complex
- 50+: Very complex (needs refactoring)

### Maintainability Index (MI)

Formula: `MI = 171 - 5.2×ln(V) - 0.23×CC - 16.2×ln(LOC)`

**Categories**:
- **Green (MI > 85)**: Excellent maintainability
- **Yellow (65 ≤ MI ≤ 85)**: Good maintainability
- **Red (MI < 65)**: Needs improvement

### CK Metrics (Object-Oriented Design)

- **WMC (Weighted Methods per Class)**: Sum of Cyclomatic Complexity of all methods
- **DIT (Depth of Inheritance Tree)**: Distance from class to `java.lang.Object`
- **NOC (Number of Children)**: Count of direct subclasses
- **CBO (Coupling Between Objects)**: Count of unique external types referenced

## 📄 Report Structure

The generated HTML report contains three main sections:

### Section A: Dashboard
- **KPI Cards**: Total Files, LOC, Average MI, Critical Classes
- **Charts**: Complexity Scatter Plot and CK Metrics Radar Chart side-by-side

### Section B: Hall of Shame
- **Top 5 Critical Classes**: Classes with lowest MI or highest WMC
- Highlighted with warning colors for immediate attention

### Section C: Detailed Analysis
- **Accordion Interface**: Expandable class list
- **Class Summary**: MI badge, WMC, DIT, CBO
- **Class Details**:
  - Complete Halstead metrics table (all 12 metrics with descriptions)
  - Methods table with complexity and Halstead metrics

## 📁 Project Structure

```
PLP_Project/
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── commands.txt                 # ANTLR4 generation commands
│
├── astra/                       # Main package
│   ├── graph_builder.py         # Pass 1: Inheritance graph
│   ├── metrics_visitor.py       # Pass 2: AST traversal
│   ├── calculator.py            # Mathematical formulas
│   ├── chart_generator.py       # Visualizations
│   ├── report_generator.py      # HTML reports
│   └── constants.py             # Configuration
│
├── grammar/                     # ANTLR grammar files
│   ├── Java20Lexer.g4          # Lexer grammar
│   ├── Java20Parser.g4         # Parser grammar
│   └── [Generated Python files]
│
├── examples/                    # Example Java files
│   ├── ComprehensiveExample.java
│   └── ComplexInheritance.java
│
└── output/                     # Generated reports
    └── *.html
```

## 💡 Examples

The `examples/` directory contains comprehensive test cases:

- **`ComprehensiveExample.java`**: Demonstrates various Java constructs, inheritance, and control flow
- **`ComplexInheritance.java`**: Deep inheritance hierarchy for testing DIT and NOC

Run analysis on examples:

```bash
python main.py examples
```

## 🔬 Technical Details

### Two-Pass Analysis

**Pass 1: Inheritance Graph Building**
- Scans all Java files
- Extracts class declarations and `extends` relationships
- Builds global inheritance graph for accurate DIT/NOC calculation

**Pass 2: Metrics Calculation**
- Parses each file into AST using ANTLR4
- Traverses AST using visitor pattern
- Collects tokens (operators/operands) for Halstead metrics
- Calculates Cyclomatic Complexity from control flow
- Aggregates metrics at class level

### Architecture

- **Modular Design**: Each component has a single responsibility
- **Visitor Pattern**: Clean separation of parsing and analysis
- **Error Handling**: Graceful handling of syntax errors
- **Extensibility**: Easy to add new metrics or visualizations

## 🤝 Contributing

This is an academic project. For improvements or bug reports, please create an issue or submit a pull request.

## 📝 License

This project is developed for academic/educational purposes.

## 🙏 Acknowledgments

- **ANTLR4**: Parser generator framework
- **Java Language Specification**: Official Java grammar
- **Halstead, McCabe, Chidamber & Kemerer**: Original metric definitions

---

**Version**: 1.0.0  
**Last Updated**: 2025

