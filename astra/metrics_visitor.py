"""
Metrics Visitor Module - Pass 2 (FINAL FIX)
Core visitor that traverses the AST to calculate all software metrics.
Fixes: Precise LOC calculation based on Class range, Recursive traversal.
"""

import re
from typing import Dict, List, Set, Optional
from collections import defaultdict
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

try:
    from grammar.Java20Lexer import Java20Lexer
    from grammar.Java20Parser import Java20Parser
    from grammar.Java20ParserVisitor import Java20ParserVisitor
except ImportError:
    import sys
    sys.path.append('grammar')
    from Java20Lexer import Java20Lexer # pyright: ignore[reportMissingImports]
    from Java20Parser import Java20Parser # pyright: ignore[reportMissingImports]
    from Java20ParserVisitor import Java20ParserVisitor # pyright: ignore[reportMissingImports]

from astra.calculator import HalsteadCalculator, ComplexityCalculator, MaintainabilityCalculator, CKCalculator


class SyntaxErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        pass


class MethodMetrics:
    def __init__(self, method_name: str, class_name: str):
        self.method_name = method_name
        self.class_name = class_name
        self.operators: List[str] = []
        self.operands: List[str] = []
        self.cyclomatic_complexity = 1
        self.loc = 0
        self.start_line = 0
        self.end_line = 0
        self.halstead: Optional[Dict] = None
    
    def calculate_halstead(self):
        n1 = len(set(self.operators))
        n2 = len(set(self.operands))
        N1 = len(self.operators)
        N2 = len(self.operands)
        self.halstead = HalsteadCalculator.calculate(n1, n2, N1, N2)


class ClassMetrics:
    def __init__(self, class_name: str, file_path: str):
        self.class_name = class_name
        self.file_path = file_path
        self.methods: Dict[str, MethodMetrics] = {}
        self.loc = 0
        # Nuovi campi per LOC precisa di classe
        self.start_line = 0
        self.end_line = 0
        
        self.external_types: Set[str] = set()
        self.wmc = 0
        self.dit = 0
        self.noc = 0
        self.cbo = 0
        self.maintainability_index = 0.0
        self.aggregated_halstead: Optional[Dict] = None
    
    def add_method(self, method: MethodMetrics):
        self.methods[method.method_name] = method
    
    def calculate_class_metrics(self, inheritance_graph):
        all_operators = []
        all_operands = []
        method_complexities = []
        
        for method in self.methods.values():
            all_operators.extend(method.operators)
            all_operands.extend(method.operands)
            method_complexities.append(method.cyclomatic_complexity)
            # Nota: La LOC di classe ora viene calcolata separatamente
        
        if all_operators or all_operands:
            n1 = len(set(all_operators))
            n2 = len(set(all_operands))
            N1 = len(all_operators)
            N2 = len(all_operands)
            self.aggregated_halstead = HalsteadCalculator.calculate(n1, n2, N1, N2)
        
        self.wmc = CKCalculator.calculate_wmc(method_complexities)
        self.cbo = CKCalculator.calculate_cbo(self.external_types)
        
        volume = self.aggregated_halstead.get('V', 0.0) if self.aggregated_halstead else 0.0
        avg_cc = sum(method_complexities) / len(method_complexities) if method_complexities else 1
        
        # Usa la LOC di classe calcolata (non la somma dei metodi)
        self.maintainability_index = MaintainabilityCalculator.calculate(volume, int(avg_cc), self.loc)


class MetricsVisitor(Java20ParserVisitor):
    
    KEYWORD_OPERATORS = {
        'if', 'else', 'while', 'for', 'do', 'switch', 'case', 'catch', 'try', 'finally',
        'return', 'break', 'continue', 'throw', 'new', 'instanceof', 'assert',
        'synchronized', 'yield', 'default'
    }
    SEPARATOR_OPERATORS = {';', '{', '}', '(', ')', '[', ']', ',', '.', ':'}
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
    
    # --- VISITA ---

    def visitCompilationUnit(self, ctx):
        return self.visitChildren(ctx)
    
    def visitNormalClassDeclaration(self, ctx):
        if hasattr(ctx, 'typeIdentifier'):
            tid = ctx.typeIdentifier()
            if tid:
                class_name = tid.getText()
                self.current_class = ClassMetrics(class_name, self.current_file_path)
                
                # CATTURA LINEE CLASSE
                self.current_class.start_line = ctx.start.line
                self.current_class.end_line = ctx.stop.line
                
                self.classes[class_name] = self.current_class
                self.visitChildren(ctx)
                self.current_class = None
        return None
    
    def visitMethodDeclaration(self, ctx):
        if not self.current_class: return None
        
        method_name = "unknown"
        if hasattr(ctx, 'methodHeader'):
            header = ctx.methodHeader()
            if header and hasattr(header, 'methodDeclarator'):
                declarator = header.methodDeclarator()
                if declarator and hasattr(declarator, 'identifier'):
                    method_name = declarator.identifier().getText()
        
        self.current_method = MethodMetrics(method_name, self.current_class.class_name)
        self.current_method.start_line = ctx.start.line
        self.current_method.end_line = ctx.stop.line
        
        self.visitChildren(ctx)
        
        self.current_method.calculate_halstead()
        self.current_class.add_method(self.current_method)
        self.current_method = None
        return None
    
    def visitConstructorDeclaration(self, ctx):
        if not self.current_class: return None
        method_name = "<init>"
        if hasattr(ctx, 'constructorDeclarator'):
            stn = ctx.constructorDeclarator().simpleTypeName()
            if stn: method_name = stn.getText()
            
        self.current_method = MethodMetrics(method_name, self.current_class.class_name)
        self.current_method.start_line = ctx.start.line
        self.current_method.end_line = ctx.stop.line
        
        self.visitChildren(ctx)
        
        self.current_method.calculate_halstead()
        self.current_class.add_method(self.current_method)
        self.current_method = None
        return None

    # --- CBO ---
    def visitFieldDeclaration(self, ctx):
        if self.current_class and hasattr(ctx, 'unannType'):
            self._check_type(ctx.unannType())
        return self.visitChildren(ctx)
    
    def visitLocalVariableDeclaration(self, ctx):
        if self.current_class and hasattr(ctx, 'localVariableType'):
            lvt = ctx.localVariableType()
            if hasattr(lvt, 'unannType'):
                self._check_type(lvt.unannType())
        return self.visitChildren(ctx)

    def _check_type(self, type_ctx):
        type_name = self._extract_type_name(type_ctx)
        if type_name and not self._is_primitive_or_builtin(type_name):
            if self.current_class:
                self.current_class.external_types.add(type_name)

    # --- COMPLEXITY ---
    def visitStatement(self, ctx):
        # Incrementa se è un nodo di controllo
        if hasattr(ctx, 'ifThenStatement') and ctx.ifThenStatement(): self._increment_complexity()
        elif hasattr(ctx, 'ifThenElseStatement') and ctx.ifThenElseStatement(): self._increment_complexity()
        elif hasattr(ctx, 'whileStatement') and ctx.whileStatement(): self._increment_complexity()
        elif hasattr(ctx, 'forStatement') and ctx.forStatement(): self._increment_complexity()
        elif hasattr(ctx, 'doStatement') and ctx.doStatement(): self._increment_complexity()
        elif hasattr(ctx, 'switchStatement') and ctx.switchStatement(): self._increment_complexity()
        elif hasattr(ctx, 'tryStatement') and ctx.tryStatement():
             try_stmt = ctx.tryStatement()
             if hasattr(try_stmt, 'catches') and try_stmt.catches():
                 for _ in try_stmt.catches().catchClause(): self._increment_complexity()
        
        return self.visitChildren(ctx)

    def visitSwitchLabel(self, ctx):
        if hasattr(ctx, 'CASE') and ctx.CASE(): self._increment_complexity()
        return self.visitChildren(ctx)

    # --- HALSTEAD ---
    def visitTerminal(self, node):
        if not self.current_method: return None
        try:
            token = node.getSymbol()
            if token.type == -1: return None # EOF
            
            # Skip hidden
            if hasattr(Java20Lexer, 'WS') and token.type == Java20Lexer.WS: return None
            if hasattr(Java20Lexer, 'COMMENT') and token.type == Java20Lexer.COMMENT: return None
            if hasattr(Java20Lexer, 'LINE_COMMENT') and token.type == Java20Lexer.LINE_COMMENT: return None

            token_text = node.getText()
            token_name = Java20Lexer.symbolicNames[token.type]
            
            if token_text in ['&&', '||', '?']: self._increment_complexity()

            if self._is_operator(token_name, token_text):
                self.current_method.operators.append(token_text)
            elif self._is_operand(token_name, token_text):
                self.current_method.operands.append(token_text)
        except: pass
        return None

    # --- HELPERS ---
    def _increment_complexity(self):
        if self.current_method: self.current_method.cyclomatic_complexity += 1

#    def _extract_type_name(self, ctx):
#        try:
#            if hasattr(ctx, 'unannClassOrInterfaceType'):
#                coit = ctx.unannClassOrInterfaceType()
#                if hasattr(coit, 'typeIdentifier'): return coit.typeIdentifier().getText()
#                return coit.getText().split('<')[0].split('.')[-1]
#        except: return None
#        return None

    def _extract_type_name(self, ctx):
        """
        Estrae il nome del tipo in modo robusto, gestendo Generics e Array.
        Esempio: 'java.util.ArrayList<String>[]' -> 'ArrayList'
        """
        if not ctx:
            return None
            
        try:
            # Approccio testuale diretto: prendiamo tutto il testo del tipo
            full_text = ctx.getText()
            
            # 1. Rimuoviamo array brackets []
            clean_text = full_text.replace('[', '').replace(']', '')
            
            # 2. Rimuoviamo la parte generica <...>
            if '<' in clean_text:
                clean_text = clean_text.split('<')[0]
            
            # 3. Prendiamo solo l'ultima parte del package (java.util.List -> List)
            if '.' in clean_text:
                clean_text = clean_text.split('.')[-1]
                
            return clean_text
            
        except Exception:
            return None

    def _is_operator(self, token_name, text):
        return (text in self.OPERATOR_TOKENS or text in self.SEPARATOR_OPERATORS or text in self.KEYWORD_OPERATORS)

    def _is_operand(self, token_name, text):
        if token_name == 'Identifier': return text not in self.KEYWORD_OPERATORS
        return token_name in ['IntegerLiteral', 'FloatingPointLiteral', 'BooleanLiteral', 'CharacterLiteral', 'StringLiteral', 'NullLiteral']

    def _is_primitive_or_builtin(self, type_name):
        return type_name in {'int','long','short','byte','char','float','double','boolean','void','String','Object','List','ArrayList','Map','HashMap','Set','HashSet','Date','File','Scanner','System','Math'}

    def analyze_file(self, file_path: str):
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
            
            self.visit(tree)
            self._calculate_loc(file_path) # Calcola LOC reali
            
            for class_metrics in self.classes.values():
                # Ricalcola metriche classe solo per le classi di QUESTO file
                if class_metrics.file_path == file_path:
                    class_metrics.calculate_class_metrics(self.inheritance_graph)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def _calculate_loc(self, file_path: str):
        """Calcolo LOC Reali basato sui limiti della CLASSE, non sui metodi."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            
            for cm in self.classes.values():
                if cm.file_path == file_path and cm.start_line > 0 and cm.end_line > 0:
                    # Estrai le righe della CLASSE intera
                    class_lines = all_lines[cm.start_line-1 : cm.end_line]
                    # Conta righe non vuote e non commenti
                    real_loc = sum(1 for line in class_lines if line.strip() and not line.strip().startswith('//') and not line.strip().startswith('/*') and not line.strip().startswith('*'))
                    cm.loc = max(1, real_loc)
                    
                    # Calcola anche LOC per i metodi per riferimento
                    for m in cm.methods.values():
                        if m.start_line > 0 and m.end_line > 0:
                            m_lines = all_lines[m.start_line-1 : m.end_line]
                            m.loc = sum(1 for l in m_lines if l.strip() and not l.strip().startswith('//'))
        except:
            pass

    def get_results(self):
        return self.classes