"""
Metrics Visitor Module - Pass 2
Core visitor that traverses the AST to calculate all software metrics:
- Halstead Metrics (per method, aggregated per class)
- Cyclomatic Complexity
- Maintainability Index
- CK Metrics (WMC, DIT, NOC, CBO)
- Logical LOC
"""

import re
from typing import Dict, List, Set, Optional
from collections import defaultdict
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

# Import generated ANTLR files
try:
    from grammar.Java20Lexer import Java20Lexer
    from grammar.Java20Parser import Java20Parser
    from grammar.Java20ParserVisitor import Java20ParserVisitor
except ImportError:
    import sys
    sys.path.append('grammar')
    from Java20Lexer import Java20Lexer  # pyright: ignore[reportMissingImports]
    from Java20Parser import Java20Parser  # pyright: ignore[reportMissingImports]
    from Java20ParserVisitor import Java20ParserVisitor  # pyright: ignore[reportMissingImports]

from astra.calculator import HalsteadCalculator, ComplexityCalculator, MaintainabilityCalculator, CKCalculator


class SyntaxErrorListener(ErrorListener):
    """Custom error listener"""
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        pass


class MethodMetrics:
    """Stores metrics for a single method"""
    def __init__(self, method_name: str, class_name: str):
        self.method_name = method_name
        self.class_name = class_name
        self.operators: List[str] = []
        self.operands: List[str] = []
        self.cyclomatic_complexity = 1  # Base complexity
        self.loc = 0
        self.start_line = 0 
        self.end_line = 0
        self.halstead: Optional[Dict] = None
    
    def calculate_halstead(self):
        """Calculate Halstead metrics for this method"""
        n1 = len(set(self.operators))
        n2 = len(set(self.operands))
        N1 = len(self.operators)
        N2 = len(self.operands)
        self.halstead = HalsteadCalculator.calculate(n1, n2, N1, N2)


class ClassMetrics:
    """Stores metrics for a single class"""
    def __init__(self, class_name: str, file_path: str):
        self.class_name = class_name
        self.file_path = file_path
        self.methods: Dict[str, MethodMetrics] = {}
        self.loc = 0
        self.external_types: Set[str] = set()
        self.wmc = 0
        self.dit = 0
        self.noc = 0
        self.cbo = 0
        self.maintainability_index = 0.0
        self.aggregated_halstead: Optional[Dict] = None
    
    def add_method(self, method: MethodMetrics):
        """Add a method to this class"""
        self.methods[method.method_name] = method
    
    def calculate_class_metrics(self, inheritance_graph):
        """Calculate aggregated class-level metrics"""
        # Aggregate Halstead metrics
        all_operators = []
        all_operands = []
        method_complexities = []
        
        for method in self.methods.values():
            all_operators.extend(method.operators)
            all_operands.extend(method.operands)
            method_complexities.append(method.cyclomatic_complexity)
            self.loc += method.loc
        
        # Calculate aggregated Halstead
        if all_operators or all_operands:
            n1 = len(set(all_operators))
            n2 = len(set(all_operands))
            N1 = len(all_operators)
            N2 = len(all_operands)
            self.aggregated_halstead = HalsteadCalculator.calculate(n1, n2, N1, N2)
        
        # Calculate WMC
        self.wmc = CKCalculator.calculate_wmc(method_complexities)
        
        # Calculate CBO
        self.cbo = CKCalculator.calculate_cbo(self.external_types)
        
        # DIT and NOC are calculated from inheritance graph (external)
        
        # Calculate MI
        volume = self.aggregated_halstead.get('V', 0.0) if self.aggregated_halstead else 0.0
        avg_cc = sum(method_complexities) / len(method_complexities) if method_complexities else 1
        self.maintainability_index = MaintainabilityCalculator.calculate(volume, int(avg_cc), self.loc)


class MetricsVisitor(Java20ParserVisitor):
    """
    Visitor that traverses the AST to calculate all metrics.
    This is the core of Pass 2 analysis.
    """
    
    # Java keywords that are operators
    KEYWORD_OPERATORS = {
        'if', 'else', 'while', 'for', 'do', 'switch', 'case', 'catch', 'try', 'finally',
        'return', 'break', 'continue', 'throw', 'new', 'instanceof', 'assert',
        'synchronized', 'yield'
    }
    
    # Separators that are operators
    SEPARATOR_OPERATORS = {';', '{', '}', '(', ')', '[', ']', ',', '.', ':'}
    
    # Arithmetic/Logic operators
    OPERATOR_TOKENS = {
        '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
        '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '>>>',
        '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '>>>=',
        '++', '--', '?', '::'
    }
    
    def __init__(self, inheritance_graph: Dict[str, Optional[str]], class_files: Dict[str, str]):
        super().__init__()
        self.inheritance_graph = inheritance_graph
        self.class_files = class_files
        self.classes: Dict[str, ClassMetrics] = {}
        self.current_class: Optional[ClassMetrics] = None
        self.current_method: Optional[MethodMetrics] = None
        self.current_file_path = ""
    
    def visitCompilationUnit(self, ctx):
        """Entry point for visiting a compilation unit"""
        if hasattr(ctx, 'ordinaryCompilationUnit'):
            unit = ctx.ordinaryCompilationUnit()
            if unit and hasattr(unit, 'topLevelClassOrInterfaceDeclaration'):
                declarations = unit.topLevelClassOrInterfaceDeclaration()
                if declarations:
                    for decl in declarations:
                        if decl and hasattr(decl, 'classDeclaration'):
                            class_decl = decl.classDeclaration()
                            if class_decl:
                                self.visit(class_decl)
        return None
    
    def visitNormalClassDeclaration(self, ctx):
        """Visit a class declaration"""
        if hasattr(ctx, 'typeIdentifier'):
            tid = ctx.typeIdentifier()
            if tid:
                class_name = tid.getText()
                self.current_class = ClassMetrics(class_name, self.current_file_path)
                self.classes[class_name] = self.current_class
                
                # Visit class body
                if hasattr(ctx, 'classBody'):
                    body = ctx.classBody()
                    if body:
                        self.visit(body)
                
                self.current_class = None
        return None
    
    def visitClassBody(self, ctx):
        """Visit class body to find methods and fields"""
        if hasattr(ctx, 'classBodyDeclaration'):
            declarations = ctx.classBodyDeclaration()
            if declarations:
                for decl in declarations:
                    if decl is not None:
                        self.visit(decl)
        return None
    
    def visitClassBodyDeclaration(self, ctx):
        """Visit class body declarations"""
        if hasattr(ctx, 'classMemberDeclaration'):
            member = ctx.classMemberDeclaration()
            if member:
                self.visit(member)
        elif hasattr(ctx, 'constructorDeclaration'):
            constructor = ctx.constructorDeclaration()
            if constructor:
                self.visit(constructor)
        elif hasattr(ctx, 'classDeclaration'):
            # Nested class
            class_decl = ctx.classDeclaration()
            if class_decl:
                self.visit(class_decl)
        return None
    
    def visitClassMemberDeclaration(self, ctx):
        """Visit class member declarations"""
        if hasattr(ctx, 'methodDeclaration'):
            method = ctx.methodDeclaration()
            if method:
                self.visit(method)
        elif hasattr(ctx, 'fieldDeclaration'):
            field = ctx.fieldDeclaration()
            if field:
                self.visit(field)
        elif hasattr(ctx, 'classDeclaration'):
            # Nested class
            class_decl = ctx.classDeclaration()
            if class_decl:
                self.visit(class_decl)
        return None
    
    def visitMethodDeclaration(self, ctx):
        """Visit a method declaration"""
        if not self.current_class:
            return None
        
        # Extract method name
        method_name = "unknown"
        if hasattr(ctx, 'methodHeader'):
            header = ctx.methodHeader()
            if header and hasattr(header, 'methodDeclarator'):
                declarator = header.methodDeclarator()
                if declarator and hasattr(declarator, 'identifier'):
                    method_name = declarator.identifier().getText()
        
        # Create method metrics
        self.current_method = MethodMetrics(method_name, self.current_class.class_name)
        
        self.current_method.start_line = ctx.start.line
        self.current_method.end_line = ctx.stop.line

        # Visit method header to collect tokens (parameters, return type, etc.)
        if hasattr(ctx, 'methodHeader'):
            header = ctx.methodHeader()
            if header:
                self.visit(header)
        
        # Visit method body to collect tokens
        if hasattr(ctx, 'methodBody'):
            body = ctx.methodBody()
            if body and hasattr(body, 'block'):
                block = body.block()
                if block:
                    self.visit(block)
        
        # Calculate method metrics
        self.current_method.calculate_halstead()
        self.current_class.add_method(self.current_method)
        self.current_method = None
        return None
    
    def visitConstructorDeclaration(self, ctx):
        """Visit a constructor declaration"""
        if not self.current_class:
            return None
        
        # Extract constructor name
        method_name = "<init>"
        if hasattr(ctx, 'constructorDeclarator'):
            declarator = ctx.constructorDeclarator()
            if declarator and hasattr(declarator, 'simpleTypeName'):
                stn = declarator.simpleTypeName()
                if stn and hasattr(stn, 'typeIdentifier'):
                    method_name = stn.typeIdentifier().getText()
        
        # Create method metrics
        self.current_method = MethodMetrics(method_name, self.current_class.class_name)
        
        self.current_method.start_line = ctx.start.line
        self.current_method.end_line = ctx.stop.line

        # Visit constructor declarator to collect tokens (parameters)
        if hasattr(ctx, 'constructorDeclarator'):
            declarator = ctx.constructorDeclarator()
            if declarator:
                self.visit(declarator)
        
        # Visit constructor body
        if hasattr(ctx, 'constructorBody'):
            body = ctx.constructorBody()
            if body and hasattr(body, 'block'):
                block = body.block()
                if block:
                    self.visit(block)
        
        # Calculate method metrics
        self.current_method.calculate_halstead()
        self.current_class.add_method(self.current_method)
        self.current_method = None
        return None
    
    def visitFieldDeclaration(self, ctx):
        """Visit field declaration to extract external types"""
        if not self.current_class:
            return None
        
        if hasattr(ctx, 'unannType'):
            unann_type = ctx.unannType()
            if unann_type:
                type_name = self._extract_type_name(unann_type)
                if type_name and not self._is_primitive_or_builtin(type_name):
                    self.current_class.external_types.add(type_name)
        return None
    
    def visitBlock(self, ctx):
        """Visit a block statement"""
        if hasattr(ctx, 'blockStatements'):
            statements = ctx.blockStatements()
            if statements:
                self.visit(statements)
        return None
    
    def visitBlockStatements(self, ctx):
        """Visit block statements"""
        if hasattr(ctx, 'blockStatement'):
            for stmt in ctx.blockStatement():
                self.visit(stmt)
        return None
    
    def visitBlockStatement(self, ctx):
        """Visit a block statement"""
        if hasattr(ctx, 'localVariableDeclarationStatement'):
            var_decl = ctx.localVariableDeclarationStatement()
            if var_decl:
                self.visit(var_decl)
        elif hasattr(ctx, 'statement'):
            stmt = ctx.statement()
            if stmt:
                self.visit(stmt)
        return None
    
    def visitStatement(self, ctx):
        """Visit a statement - this is where we count complexity"""
        if hasattr(ctx, 'ifThenStatement'):
            self._increment_complexity()
            stmt = ctx.ifThenStatement()
            if stmt:
                self.visit(stmt)
        elif hasattr(ctx, 'ifThenElseStatement'):
            self._increment_complexity()
            stmt = ctx.ifThenElseStatement()
            if stmt:
                self.visit(stmt)
        elif hasattr(ctx, 'whileStatement'):
            self._increment_complexity()
            stmt = ctx.whileStatement()
            if stmt:
                self.visit(stmt)
        elif hasattr(ctx, 'forStatement'):
            self._increment_complexity()
            stmt = ctx.forStatement()
            if stmt:
                self.visit(stmt)
        elif hasattr(ctx, 'switchStatement'):
            self._increment_complexity()
            stmt = ctx.switchStatement()
            if stmt:
                self.visit(stmt)
        elif hasattr(ctx, 'tryStatement'):
            self._increment_complexity()
            stmt = ctx.tryStatement()
            if stmt:
                self.visit(stmt)
        elif hasattr(ctx, 'statementWithoutTrailingSubstatement'):
            stmt = ctx.statementWithoutTrailingSubstatement()
            if stmt:
                self.visit(stmt)
        else:
            # Visit any other statement type
            if hasattr(ctx, 'getChildren'):
                for child in ctx.getChildren():
                    if child is not None:
                        self.visit(child)
        return None
    
    def visitSwitchStatement(self, ctx):
        """Visit switch statement - count cases"""
        if hasattr(ctx, 'switchBlock'):
            block = ctx.switchBlock()
            if block and hasattr(block, 'switchBlockStatementGroup'):
                # Count cases
                for group in block.switchBlockStatementGroup():
                    if hasattr(group, 'switchLabel'):
                        for label in group.switchLabel():
                            if label and hasattr(label, 'CASE'):
                                self._increment_complexity()
        return None
    
    def visitExpression(self, ctx):
        """Visit expressions to count operators and operands"""
        # Visit all children to collect tokens
        return self.visitChildren(ctx)
    
    def visitTerminal(self, node):
        """Visit terminal nodes (tokens) to collect operators and operands"""
        if not self.current_method:
            return None
        
        try:
            token = node.getSymbol()
            token_type = token.type
            token_text = node.getText()
            
            # Skip whitespace and comments
            try:
                if hasattr(Java20Lexer, 'WS') and token_type == Java20Lexer.WS:
                    return None
                if hasattr(Java20Lexer, 'COMMENT') and token_type == Java20Lexer.COMMENT:
                    return None
                if hasattr(Java20Lexer, 'LINE_COMMENT') and token_type == Java20Lexer.LINE_COMMENT:
                    return None
            except Exception as e:
                print(f"DEBUG ERROR in token processing: {e}") 
                pass
            
            # Get token name
            token_name = None
            if token_type >= 0 and token_type < len(Java20Lexer.symbolicNames):
                token_name = Java20Lexer.symbolicNames[token_type]
            
            # Classify as operator or operand
            if self._is_operator(token_name, token_text):
                self.current_method.operators.append(token_text)
                # Increment complexity for logical operators (&&, ||) and ternary (?)
                if token_text in ['&&', '||'] or token_name == 'QUESTION':
                    self._increment_complexity()
            elif self._is_operand(token_name, token_text):
                self.current_method.operands.append(token_text)
        except Exception:
            # Silently handle any errors in token processing
            pass
        
        return None
    
    def visitChildren(self, node):
        """Override to ensure we visit all children including terminals"""
        result = None
        if hasattr(node, 'getChildCount'):
            n = node.getChildCount()
            for i in range(n):
                if not self.shouldVisitNextChild(node, result):
                    break
                c = node.getChild(i)
                if c is not None:
                    childResult = c.accept(self)
                    result = self.aggregateResult(result, childResult)
        return result
    
    def aggregateResult(self, aggregate, nextResult):
        """Aggregate results from child visits"""
        return nextResult if nextResult is not None else aggregate
    
    def shouldVisitNextChild(self, node, currentResult):
        """Determine if we should continue visiting children"""
        return True
    
    def _is_operator(self, token_name: Optional[str], token_text: str) -> bool:
        """Determine if a token is an operator"""
        if token_text in self.SEPARATOR_OPERATORS:
            return True
        if token_text in self.OPERATOR_TOKENS:
            return True
        if token_text.lower() in self.KEYWORD_OPERATORS:
            return True
        if token_name in ['IF', 'WHILE', 'FOR', 'DO', 'SWITCH', 'CASE', 'CATCH', 'TRY', 'RETURN', 'BREAK', 'CONTINUE', 'THROW', 'NEW', 'INSTANCEOF', 'ASSERT', 'SYNCHRONIZED', 'YIELD']:
            return True
        return False
    
    def _is_operand(self, token_name: Optional[str], token_text: str) -> bool:
        """Determine if a token is an operand"""
        if token_name in ['Identifier']:
            # Check if it's not a keyword
            if token_text.lower() not in self.KEYWORD_OPERATORS:
                return True
        elif token_name in ['IntegerLiteral', 'FloatingPointLiteral', 'BooleanLiteral', 'CharacterLiteral', 'StringLiteral', 'NullLiteral']:
            return True
        return False
    
    def _increment_complexity(self):
        """Increment cyclomatic complexity"""
        if self.current_method:
            self.current_method.cyclomatic_complexity += 1
    
    def _extract_type_name(self, ctx) -> Optional[str]:
        """Extract type name from type context"""
        if hasattr(ctx, 'unannClassOrInterfaceType'):
            coit = ctx.unannClassOrInterfaceType()
            if coit and hasattr(coit, 'typeIdentifier'):
                tid = coit.typeIdentifier()
                if tid:
                    return tid.getText()
        return None
    
    def _is_primitive_or_builtin(self, type_name: str) -> bool:
        """Check if type is primitive or built-in Java type"""
        primitives = {'int', 'long', 'short', 'byte', 'char', 'float', 'double', 'boolean', 'void'}
        builtins = {'String', 'Object', 'Integer', 'Long', 'Short', 'Byte', 'Character', 'Float', 'Double', 'Boolean'}
        return type_name in primitives or type_name in builtins
    
    def analyze_file(self, file_path: str):
        """Analyze a single Java file"""
        self.current_file_path = file_path
        try:
            input_stream = FileStream(file_path, encoding='utf-8')
            lexer = Java20Lexer(input_stream)
            lexer.removeErrorListeners()
            lexer.addErrorListener(SyntaxErrorListener())
            
            stream = CommonTokenStream(lexer)
            parser = Java20Parser(stream)
            parser.removeErrorListeners()
            parser.addErrorListener(SyntaxErrorListener())
            
            tree = parser.compilationUnit()
            if tree is None:
                print(f"Warning: Could not parse {file_path} - tree is None")
                return
            
            self.visit(tree)
            
            # Calculate LOC for methods (count non-empty, non-comment lines)
            self._calculate_loc(file_path)
            
            # Finalize class metrics
            for class_metrics in self.classes.values():
                class_metrics.calculate_class_metrics(self.inheritance_graph)
                # Set DIT and NOC from inheritance graph
                if class_metrics.class_name in self.inheritance_graph:
                    # DIT calculation would be done externally
                    pass
        except Exception as e:
            import traceback
            print(f"Error analyzing {file_path}: {e}")
            traceback.print_exc()
    
    """
    def _calculate_loc(self, file_path: str):
        \"""Calculate Logical Lines of Code for each method\"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Track which lines belong to which method
            # This is a simplified approach - we use token count as a proxy
            for class_metrics in self.classes.values():
                for method in class_metrics.methods.values():
                    # Count non-empty tokens as a proxy for LOC
                    # A more accurate approach would track line numbers from AST
                    total_tokens = len(method.operators) + len(method.operands)
                    # Heuristic: roughly 5-10 tokens per line of code
                    method.loc = max(1, total_tokens // 7)
                    
                # Class LOC is sum of method LOCs
                class_metrics.loc = sum(m.loc for m in class_metrics.methods.values())
        except Exception:
            # Fallback: use token-based heuristic
            for class_metrics in self.classes.values():
                for method in class_metrics.methods.values():
                    total_tokens = len(method.operators) + len(method.operands)
                    method.loc = max(1, total_tokens // 7)
                class_metrics.loc = sum(m.loc for m in class_metrics.methods.values())
    """

    def _calculate_loc(self, file_path: str):
        """
        Calculate Logical Lines of Code (LOC) accurately using AST line numbers.
        Reads the actual source file and counts non-empty, non-comment lines
        within the start/end range of each method.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Leggiamo tutte le linee (le liste partono da 0, le linee ANTLR da 1)
                all_lines = f.readlines()
            
            for class_metrics in self.classes.values():
                class_loc = 0
                for method in class_metrics.methods.values():
                    # Assicuriamoci che i numeri di linea siano validi
                    if method.start_line > 0 and method.end_line > 0:
                        # Estraiamo lo snippet di codice del metodo
                        # Convertiamo da 1-based (ANTLR) a 0-based (Python List)
                        start_idx = method.start_line - 1
                        end_idx = method.end_line
                        
                        method_lines = all_lines[start_idx:end_idx]
                        
                        # Contiamo le linee "vere" (non vuote, non commenti single-line)
                        real_loc = 0
                        for line in method_lines:
                            stripped = line.strip()
                            # Se la linea non è vuota e non inizia con //
                            if stripped and not stripped.startswith('//'):
                                real_loc += 1
                        
                        method.loc = max(1, real_loc)
                    else:
                        # Fallback se mancano info di linea (non dovrebbe accadere)
                        method.loc = 1
                    
                    class_loc += method.loc
                    
                # Aggiorniamo le LOC totali della classe
                class_metrics.loc = class_loc

        except Exception as e:
            print(f"Error calculating precise LOC for {file_path}: {e}")
            # Fallback euristico solo in caso di disastro I/O
            for class_metrics in self.classes.values():
                for method in class_metrics.methods.values():
                    total_tokens = len(method.operators) + len(method.operands)
                    method.loc = max(1, total_tokens // 7)
                class_metrics.loc = sum(m.loc for m in class_metrics.methods.values())

    def get_results(self) -> Dict[str, ClassMetrics]:
        """Get all calculated class metrics"""
        return self.classes

