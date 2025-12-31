# ASTra - Java Static Analysis Tool
## Comprehensive Project Report

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [System Architecture](#system-architecture)
4. [Technical Implementation](#technical-implementation)
5. [Metrics Calculation](#metrics-calculation)
6. [Visualization & Reporting](#visualization--reporting)
7. [Project Structure](#project-structure)
8. [Installation & Setup](#installation--setup)
9. [Usage Guide](#usage-guide)
10. [Design Decisions](#design-decisions)
11. [Testing & Validation](#testing--validation)
12. [Future Enhancements](#future-enhancements)
13. [References](#references)

---

## Executive Summary

**ASTra** (Java Automated Static Analysis) is a comprehensive static analysis tool designed to analyze Java source code by generating and traversing Abstract Syntax Trees (ASTs) using ANTLR4. The tool calculates rigorous software metrics including Halstead Complexity Metrics, Cyclomatic Complexity, Maintainability Index, and CK (Chidamber & Kemerer) Object-Oriented Design Metrics.

The project implements a **two-pass analysis approach**:
- **Pass 1**: Builds a global inheritance graph for accurate CK metrics calculation
- **Pass 2**: Performs detailed AST traversal to calculate all metrics per method and class

The tool generates professional HTML5 dashboards with embedded visualizations, providing developers with actionable insights into code quality and maintainability.

---

## Project Overview

### Purpose

ASTra was developed to provide:
- **Comprehensive Metrics Analysis**: All 12 Halstead metrics, Cyclomatic Complexity, Maintainability Index, and CK metrics
- **Object-Oriented Analysis**: Proper handling of inheritance hierarchies, method complexity, and class coupling
- **Visual Reporting**: Interactive HTML dashboards with charts and progressive disclosure
- **Production-Ready Tool**: Modular architecture, error handling, and extensible design

### Key Features

✅ **ANTLR4-Based Parsing**: Uses official Java 20 grammar for accurate AST generation  
✅ **Two-Pass Analysis**: Separate inheritance graph building and metrics calculation  
✅ **Complete Metrics Suite**: Halstead, CC, MI, and CK metrics (WMC, DIT, NOC, CBO)  
✅ **Visual Dashboards**: HTML5 reports with embedded Base64 charts  
✅ **Progressive Disclosure**: Accordion-style interface for detailed exploration  
✅ **Self-Contained Reports**: No external dependencies, works offline  
✅ **Modular Architecture**: Clean separation of concerns, easy to extend  

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ASTra Tool                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   Pass 1     │      │   Pass 2     │                │
│  │ Graph Builder│─────▶│   Metrics    │                │
│  │              │      │   Visitor    │                │
│  └──────────────┘      └──────────────┘                │
│         │                      │                        │
│         ▼                      ▼                        │
│  ┌──────────────┐      ┌──────────────┐                │
│  │ Inheritance  │      │   Metrics    │                │
│  │    Graph     │      │  Calculator  │                │
│  └──────────────┘      └──────────────┘                │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │    Chart     │      │    Report    │                │
│  │  Generator   │─────▶│  Generator   │                │
│  └──────────────┘      └──────────────┘                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Two-Pass Analysis Flow

#### Pass 1: Inheritance Graph Building
1. **Purpose**: Extract class hierarchies for accurate DIT and NOC calculations
2. **Process**:
   - Scan all Java files in the target directory
   - Parse each file using ANTLR4
   - Extract class declarations and `extends` relationships
   - Build a global inheritance graph: `Class → Parent Class`
   - Handle nested classes and multiple inheritance levels

3. **Output**: 
   - Inheritance graph dictionary
   - Class-to-file mapping
   - All discovered classes

#### Pass 2: Metrics Calculation
1. **Purpose**: Calculate all software metrics by traversing ASTs
2. **Process**:
   - Parse each Java file into an AST
   - Visit class declarations
   - For each method:
     - Collect operators and operands from tokens
     - Calculate Cyclomatic Complexity
     - Calculate Halstead metrics
   - Aggregate metrics at class level
   - Calculate CK metrics using inheritance graph

3. **Output**:
   - Per-method metrics
   - Per-class aggregated metrics
   - Complete metrics dataset

---

## Technical Implementation

### Core Modules

#### 1. `graph_builder.py` - Pass 1 Implementation

**Purpose**: Build inheritance graph by scanning all Java files

**Key Components**:
- `InheritanceGraphBuilder` class
- Custom ANTLR visitor for class declarations
- Methods:
  - `build_graph_from_directory()`: Recursively scan directory
  - `build_graph_from_file()`: Parse single file
  - `calculate_dit()`: Calculate Depth of Inheritance Tree
  - `calculate_noc()`: Calculate Number of Children

**Technical Details**:
- Uses ANTLR4 `FileStream` for file reading
- Custom error listener to handle syntax errors gracefully
- Recursive class extraction for nested classes
- Handles fully qualified class names

#### 2. `metrics_visitor.py` - Pass 2 Implementation

**Purpose**: Core AST traversal and metrics collection

**Key Components**:
- `MetricsVisitor` class (extends `Java20ParserVisitor`)
- `ClassMetrics` class: Stores class-level metrics
- `MethodMetrics` class: Stores method-level metrics

**Visitor Pattern Implementation**:
- Overrides visitor methods for:
  - `visitCompilationUnit()`: Entry point
  - `visitNormalClassDeclaration()`: Class processing
  - `visitMethodDeclaration()`: Method processing
  - `visitConstructorDeclaration()`: Constructor processing
  - `visitStatement()`: Control flow detection for CC
  - `visitTerminal()`: Token collection for Halstead

**Token Classification**:
- **Operators**: Keywords (if, while, for, etc.), separators (;, {}, ()), arithmetic/logic operators
- **Operands**: Identifiers, literals (String, Integer, Boolean, Null), constants

**Complexity Calculation**:
- Base complexity: 1
- Increments for: if, while, for, switch, case, catch, try, &&, ||, ?

#### 3. `calculator.py` - Mathematical Formulas

**Purpose**: Centralized metric calculation logic

**Classes**:
- `HalsteadCalculator`: All 12 Halstead metrics
- `ComplexityCalculator`: Cyclomatic Complexity helpers
- `MaintainabilityCalculator`: MI calculation and categorization
- `CKCalculator`: WMC, CBO calculations

**Key Formulas**:
```python
# Halstead Metrics
V = N * log₂(n)                    # Volume
D = (n1/2) * (N2/n2)              # Difficulty
E = D * V                          # Effort
T = E / 18                         # Time
L = 1 / D                          # Program Level
B = V / 3000                       # Estimated Bugs

# Maintainability Index
MI = 171 - 5.2*ln(V) - 0.23*CC - 16.2*ln(LOC)
# Normalized to 0-100

# CK Metrics
WMC = Σ(CC of all methods)         # Weighted Methods per Class
CBO = |external_types|              # Coupling Between Objects
```

#### 4. `chart_generator.py` - Visualization

**Purpose**: Generate Matplotlib charts as Base64-encoded images

**Charts Generated**:
1. **Complexity Scatter Plot**: X-axis = WMC, Y-axis = Halstead Volume
   - Identifies "hard to maintain" zones
   - Each dot represents a class

2. **CK Radar Chart**: Compares top classes on WMC, DIT, CBO
   - Spider/radar plot visualization
   - Top N classes (default: 5)

3. **MI Distribution Bar**: Distribution of maintainability categories
   - Green (>85), Yellow (65-85), Red (<65)
   - Bar chart with counts

**Technical Details**:
- Uses `matplotlib.use('Agg')` for non-interactive backend
- Converts figures to Base64 strings for HTML embedding
- No external image files required

#### 5. `report_generator.py` - HTML Report Generation

**Purpose**: Generate professional HTML5 dashboards

**Report Structure**:

**Section A: Dashboard (Macro Level)**
- KPI Cards: Total Files, LOC, Average MI, Critical Classes
- Charts: Side-by-side display using CSS Grid

**Section B: Hall of Shame (Hotspots)**
- Top 5 Critical Classes table
- Sorted by lowest MI, then highest WMC
- Warning colors (red/orange)

**Section C: Accordion Details (Micro Level)**
- Expandable class list using HTML5 `<details>` and `<summary>`
- Summary row: Class name, MI badge, WMC, DIT, CBO
- Details body:
  - Complete Halstead metrics table (all 12 metrics)
  - Methods table with complexity and Halstead metrics

**Features**:
- Progressive disclosure design
- Self-contained (all CSS inline)
- Color-coded MI badges
- Responsive design
- No JavaScript dependencies

#### 6. `constants.py` - Configuration

**Purpose**: Centralized constants and configuration

**Contents**:
- Terminal color codes (for CLI output)
- Default output directory
- Matplotlib availability check

---

## Metrics Calculation

### Halstead Complexity Metrics (All 12 Metrics)

#### Base Counts
1. **n₁ (Unique Operators)**: Count of distinct operators
2. **n₂ (Unique Operands)**: Count of distinct operands
3. **N₁ (Total Operators)**: Total occurrences of operators
4. **N₂ (Total Operands)**: Total occurrences of operands

#### Derived Metrics
5. **N (Program Length)**: N₁ + N₂
6. **n (Vocabulary)**: n₁ + n₂
7. **V (Volume)**: N × log₂(n) - Program size in bits
8. **D (Difficulty)**: (n₁/2) × (N₂/n₂) - Implementation difficulty
9. **E (Effort)**: D × V - Mental effort required
10. **T (Time)**: E / 18 - Estimated coding time (seconds)
11. **L (Program Level)**: 1 / D - Program abstraction level
12. **B (Estimated Bugs)**: V / 3000 - Potential defects

**Calculation Level**: Per method, aggregated per class

### Cyclomatic Complexity (CC)

**Definition**: Number of independent paths through the code

**Increment Rules**:
- Base complexity: 1
- +1 for: if, while, for, do, switch, case, catch, try
- +1 for: &&, || (logical operators)
- +1 for: ? (ternary operator)

**Calculation Level**: Per method

### Maintainability Index (MI)

**Formula**: 
```
MI = 171 - 5.2×ln(V) - 0.23×CC - 16.2×ln(LOC)
```

**Normalization**: Clamped to 0-100 range

**Categories**:
- **Green**: MI > 85 (Excellent)
- **Yellow**: 65 ≤ MI ≤ 85 (Good)
- **Red**: MI < 65 (Needs Improvement)

**Calculation Level**: Per class

### CK Metrics (Object-Oriented Design)

#### WMC (Weighted Methods per Class)
- **Definition**: Sum of Cyclomatic Complexity of all methods in a class
- **Calculation**: Σ(CC of each method)
- **Interpretation**: Higher WMC = more complex class

#### DIT (Depth of Inheritance Tree)
- **Definition**: Distance from class to `java.lang.Object`
- **Calculation**: Traverse inheritance graph upward
- **Interpretation**: Higher DIT = deeper inheritance hierarchy

#### NOC (Number of Children)
- **Definition**: Count of direct subclasses
- **Calculation**: Count classes with this class as parent
- **Interpretation**: Higher NOC = more responsibility

#### CBO (Coupling Between Objects)
- **Definition**: Count of unique external types referenced
- **Calculation**: Count non-primitive, non-builtin types in fields/methods
- **Interpretation**: Higher CBO = more dependencies

**Calculation Level**: Per class

---

## Visualization & Reporting

### Chart Types

#### 1. Complexity Scatter Plot
- **X-axis**: Cyclomatic Complexity (WMC)
- **Y-axis**: Halstead Volume (V)
- **Purpose**: Identify classes in "hard to maintain" zones
- **Visualization**: Scatter plot with class labels

#### 2. CK Metrics Radar Chart
- **Metrics**: WMC, DIT, CBO
- **Classes**: Top N classes (sorted by WMC)
- **Purpose**: Compare multiple classes across dimensions
- **Visualization**: Polar/radar chart with normalized values

#### 3. MI Distribution Bar Chart
- **Categories**: Green (>85), Yellow (65-85), Red (<65)
- **Values**: Count of classes in each category
- **Purpose**: Overall project health overview
- **Visualization**: Bar chart with color coding

### HTML Report Features

#### Dashboard Section
- **KPI Cards**: Key metrics at a glance
- **Charts Grid**: Side-by-side visualizations
- **Responsive Layout**: CSS Grid for flexible display

#### Hall of Shame Section
- **Critical Classes**: Top 5 problematic classes
- **Sorting**: Lowest MI, then highest WMC
- **Visual Design**: Warning colors, prominent display

#### Accordion Details Section
- **Progressive Disclosure**: Click to expand classes
- **Class Summary**: MI badge, WMC, DIT, CBO
- **Class Details**:
  - Complete Halstead metrics table (12 metrics)
  - Methods table with complexity and Halstead metrics
- **No JavaScript**: Pure HTML5 `<details>` implementation

### Report Styling

- **Modern Design**: Gradient backgrounds, card layouts
- **Color Coding**: Green/Yellow/Red for MI categories
- **Typography**: System fonts (system-ui, Segoe UI, Roboto)
- **Self-Contained**: All CSS inline, no external dependencies
- **Print-Friendly**: Works offline, can be saved as PDF

---

## Project Structure

```
PLP_Project/
├── main.py                      # Entry point, orchestrates two-pass analysis
├── commands.txt                 # ANTLR4 generation commands
├── requirements.txt             # Python dependencies
├── README.md                    # User documentation
├── PROJECT_REPORT.md            # This comprehensive report
│
├── astra/                       # Main package
│   ├── __init__.py
│   ├── graph_builder.py         # Pass 1: Inheritance graph building
│   ├── metrics_visitor.py       # Pass 2: AST traversal and metrics
│   ├── calculator.py            # Mathematical formulas
│   ├── chart_generator.py       # Matplotlib visualizations
│   ├── report_generator.py      # HTML report generation
│   └── constants.py             # Configuration and constants
│
├── grammar/                     # ANTLR grammar files
│   ├── Java20Lexer.g4          # Java 20 lexer grammar
│   ├── Java20Parser.g4         # Java 20 parser grammar
│   ├── Java20Lexer.py          # Generated lexer (from .g4)
│   ├── Java20Parser.py         # Generated parser (from .g4)
│   └── Java20ParserVisitor.py  # Generated visitor base class
│
├── examples/                    # Example Java files for testing
│   ├── ComprehensiveExample.java    # Comprehensive test case
│   └── ComplexInheritance.java     # Deep inheritance test case
│
└── output/                     # Generated reports (created automatically)
    └── *.html                   # HTML analysis reports
```

---

## Installation & Setup

### Prerequisites

- **Python**: 3.7 or higher
- **ANTLR4 Tools**: For generating parser files (optional if already generated)
- **pip**: Python package manager

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `matplotlib>=3.5.0`: For chart generation
- `antlr4-python3-runtime>=4.13.0`: ANTLR4 runtime for Python
- `numpy>=1.21.0`: For numerical operations in charts

### Step 2: Generate ANTLR Parser Files (If Needed)

If the grammar files have been modified or parser files are missing:

```bash
# Install ANTLR4 tools (if not already installed)
pip install antlr4-tools

# Generate Python files from grammar
cd grammar
antlr4 -Dlanguage=Python3 -visitor -no-listener Java20Lexer.g4
antlr4 -Dlanguage=Python3 -visitor -no-listener Java20Parser.g4
```

**Note**: The generated files are already included in the project, so this step is typically not needed.

### Step 3: Verify Installation

```bash
python main.py examples --output test.html
```

If successful, you should see:
- Phase 1: Building inheritance graph
- Phase 2: Calculating metrics
- Phase 3: Generating visualizations
- Phase 4: Generating HTML report
- Report saved to `output/test.html`

---

## Usage Guide

### Basic Usage

```bash
python main.py <input_directory> [--output <filename>]
```

### Examples

```bash
# Analyze examples directory with default output name
python main.py examples

# Analyze examples directory with custom output name
python main.py examples --output my_report.html

# Analyze a specific project directory
python main.py /path/to/java/project --output project_analysis.html
```

### Command-Line Arguments

- **`input_directory`** (required): Directory containing Java source files
- **`--output`** (optional): Output HTML report filename (default: `astra_report.html`)

**Note**: All reports are saved in the `output/` directory automatically.

### Output

The tool generates:
1. **HTML Report**: Saved in `output/` directory
2. **Console Output**: Progress information and summary statistics

### Interpreting the Report

#### Dashboard Section
- **KPI Cards**: Quick overview of project metrics
- **Charts**: Visual representation of complexity and metrics

#### Hall of Shame
- Focus on classes with lowest MI or highest WMC
- These are candidates for refactoring

#### Detailed Analysis
- Expand classes to see:
  - **Halstead Metrics**: All 12 metrics with descriptions
  - **Methods**: Individual method complexity and Halstead metrics
- Use this for detailed code review

---

## Design Decisions

### Why Two-Pass Analysis?

**Problem**: CK metrics (DIT, NOC) require knowledge of the complete inheritance hierarchy, which may span multiple files.

**Solution**: 
- **Pass 1**: Build global inheritance graph by scanning all files
- **Pass 2**: Calculate metrics with access to complete hierarchy

**Benefits**:
- Accurate DIT calculation (can traverse to Object)
- Accurate NOC calculation (can find all children)
- Separation of concerns (graph building vs. metrics calculation)

### Why ANTLR4?

**Alternatives Considered**:
- Regex-based tokenization (simpler but inaccurate)
- Built-in AST parsers (language-specific, less flexible)

**Choice**: ANTLR4

**Reasons**:
- **Accuracy**: Official Java 20 grammar ensures correct parsing
- **AST Access**: Full syntax tree for precise metrics
- **Extensibility**: Easy to add new metrics or languages
- **Industry Standard**: Widely used, well-documented

### Why Visitor Pattern?

**Benefits**:
- **Separation of Concerns**: Parsing logic separate from analysis logic
- **Extensibility**: Easy to add new visitors for different analyses
- **Maintainability**: Clear structure, easy to understand
- **ANTLR Integration**: Native support in ANTLR4

### Why Self-Contained HTML?

**Benefits**:
- **Portability**: Report can be shared without dependencies
- **Offline Access**: Works without internet connection
- **Version Control**: No external resource versioning issues
- **Simplicity**: Single file to manage

### Why Progressive Disclosure?

**Benefits**:
- **Usability**: Users see high-level first, details on demand
- **Performance**: Large reports load faster (details hidden initially)
- **Focus**: Helps users identify critical issues first
- **No JavaScript**: Pure HTML5, works everywhere

---

## Testing & Validation

### Test Cases

#### Example Files

1. **`ComprehensiveExample.java`**:
   - Multiple inheritance levels (DIT = 0, 1, 2)
   - Various control flow structures (if, while, for, switch, try-catch)
   - Logical operators (&&, ||)
   - External type references (CBO)
   - Nested classes
   - Multiple methods with varying complexity

2. **`ComplexInheritance.java`**:
   - Deep inheritance hierarchy (DIT = 0, 1, 2, 3)
   - Multiple children (NOC testing)
   - Complex control flow
   - Abstract classes and interfaces

### Validation

#### Metrics Validation
- **Halstead Metrics**: Verified against manual calculations
- **Cyclomatic Complexity**: Verified against McCabe's method
- **MI**: Verified against standard formula
- **CK Metrics**: Verified against Chidamber & Kemerer definitions

#### Output Validation
- **Report Generation**: All sections render correctly
- **Charts**: Base64 encoding works, images display
- **Accordion**: Expand/collapse functionality works
- **Responsive Design**: Works on different screen sizes

### Known Limitations

1. **LOC Calculation**: Currently uses token-based heuristic; could be improved with line number tracking
2. **External Types**: CBO calculation may include some built-in types
3. **Nested Classes**: Fully supported but may affect class count
4. **Annotations**: Not fully analyzed (may affect token counts)

---

## Future Enhancements

### Potential Improvements

1. **Enhanced LOC Calculation**
   - Track line numbers from AST
   - More accurate logical LOC

2. **Additional Metrics**
   - LCOM (Lack of Cohesion of Methods)
   - RFC (Response for a Class)
   - Fan-in/Fan-out

3. **Comparison Features**
   - Compare metrics across versions
   - Trend analysis over time
   - Diff reports

4. **Export Formats**
   - JSON export for programmatic access
   - CSV export for spreadsheet analysis
   - PDF export for documentation

5. **CI/CD Integration**
   - Command-line flags for automation
   - Exit codes based on thresholds
   - JUnit XML output format

6. **Configuration**
   - Customizable thresholds
   - Metric selection
   - Report template customization

7. **Performance**
   - Parallel file processing
   - Caching for large projects
   - Incremental analysis

8. **Language Support**
   - Python analysis
   - C++ analysis
   - Multi-language projects

---

## References

### Academic References

1. **Halstead, M. H.** (1977). *Elements of Software Science*. Elsevier North-Holland.
   - Original work on Halstead Complexity Metrics

2. **McCabe, T. J.** (1976). A Complexity Measure. *IEEE Transactions on Software Engineering*, SE-2(4), 308-320.
   - Cyclomatic Complexity definition

3. **Chidamber, S. R., & Kemerer, C. F.** (1994). A Metrics Suite for Object Oriented Design. *IEEE Transactions on Software Engineering*, 20(6), 476-493.
   - CK Metrics suite definition

4. **Coleman, D., et al.** (1994). Using Metrics to Evaluate Software System Maintainability. *Computer*, 27(8), 44-49.
   - Maintainability Index formula

### Technical References

1. **ANTLR4 Documentation**: https://www.antlr.org/
   - Parser generator framework

2. **Java Language Specification**: https://docs.oracle.com/javase/specs/
   - Java 20 grammar reference

3. **Matplotlib Documentation**: https://matplotlib.org/
   - Visualization library

### Tools & Libraries

- **ANTLR4**: Parser generator (v4.13+)
- **Matplotlib**: Visualization library (v3.5+)
- **NumPy**: Numerical computing (v1.21+)
- **Python**: Programming language (v3.7+)

---

## Conclusion

ASTra represents a comprehensive solution for Java static analysis, combining:
- **Rigorous Metrics**: Industry-standard formulas and calculations
- **Modern Architecture**: Two-pass analysis, visitor pattern, modular design
- **Professional Reporting**: Interactive HTML5 dashboards with visualizations
- **Production Quality**: Error handling, extensibility, maintainability

The tool successfully demonstrates:
- Advanced compiler construction techniques (ANTLR4, AST traversal)
- Software engineering best practices (modularity, separation of concerns)
- Data visualization (charts, progressive disclosure)
- User experience design (intuitive interface, actionable insights)

ASTra is ready for use in software development workflows, providing developers with actionable insights into code quality and maintainability.

---

**Project Version**: 1.0.0  
**Last Updated**: 2024  
**License**: Academic/Educational Use

