"""
Graph Builder Module - Pass 1
Builds the inheritance graph by scanning all Java files to extract class hierarchies.
This is required for calculating CK metrics like DIT (Depth of Inheritance Tree) and NOC (Number of Children).
"""

import os
from typing import Dict, Set, Optional
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

# Import generated ANTLR files (will be generated from grammar)
try:
    from grammar.Java20Lexer import Java20Lexer
    from grammar.Java20Parser import Java20Parser
except ImportError:
    # Fallback if grammar files are in different location
    import sys
    sys.path.append('grammar')
    from Java20Lexer import Java20Lexer  # pyright: ignore[reportMissingImports]
    from Java20Parser import Java20Parser  # pyright: ignore[reportMissingImports]


class SyntaxErrorListener(ErrorListener):
    """Custom error listener to suppress syntax errors during graph building"""
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Silently continue - we'll handle errors in the main analysis
        pass


class InheritanceGraphBuilder:
    """
    Visitor for Pass 1: Builds inheritance graph by extracting class declarations
    and their parent relationships from all Java files.
    """
    
    def __init__(self):
        self.inheritance_graph: Dict[str, Optional[str]] = {}  # class_name -> parent_class_name
        self.class_files: Dict[str, str] = {}  # class_name -> file_path
        self.all_classes: Set[str] = set()
    
    def extract_class_name(self, ctx) -> Optional[str]:
        """Extract class name from class declaration context"""
        if hasattr(ctx, 'typeIdentifier'):
            if ctx.typeIdentifier():
                return ctx.typeIdentifier().getText()
        return None
    
    def extract_parent_class(self, ctx) -> Optional[str]:
        """Extract parent class name from classExtends context"""
        if hasattr(ctx, 'classExtends'):
            extends = ctx.classExtends()
            if extends and hasattr(extends, 'classType'):
                class_type = extends.classType()
                if class_type:
                    # Extract the type identifier from classType
                    # classType can be: typeIdentifier or packageName.typeIdentifier
                    if hasattr(class_type, 'typeIdentifier'):
                        tid = class_type.typeIdentifier()
                        if tid:
                            return tid.getText()
        return None
    
    def visit_class_declaration(self, ctx, file_path: str):
        """Recursively visit class declarations (including nested classes)"""
        if hasattr(ctx, 'normalClassDeclaration'):
            normal_class = ctx.normalClassDeclaration()
            if normal_class:
                class_name = self.extract_class_name(normal_class)
                if class_name:
                    # Handle fully qualified names if needed
                    parent_class = self.extract_parent_class(normal_class)
                    
                    # Store class information
                    self.all_classes.add(class_name)
                    self.class_files[class_name] = file_path
                    self.inheritance_graph[class_name] = parent_class
                    
                    # Visit nested classes
                    if hasattr(normal_class, 'classBody'):
                        body = normal_class.classBody()
                        if body and hasattr(body, 'classBodyDeclaration'):
                            for decl in body.classBodyDeclaration():
                                if hasattr(decl, 'classMemberDeclaration'):
                                    member = decl.classMemberDeclaration()
                                    if member and hasattr(member, 'classDeclaration'):
                                        nested = member.classDeclaration()
                                        if nested:
                                            self.visit_class_declaration(nested, file_path)
    
    def build_graph_from_file(self, file_path: str):
        """Parse a Java file and extract inheritance information"""
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
            
            # Visit all class declarations in the compilation unit
            if hasattr(tree, 'ordinaryCompilationUnit'):
                unit = tree.ordinaryCompilationUnit()
                if unit and hasattr(unit, 'topLevelClassOrInterfaceDeclaration'):
                    for decl in unit.topLevelClassOrInterfaceDeclaration():
                        if hasattr(decl, 'classDeclaration'):
                            self.visit_class_declaration(decl.classDeclaration(), file_path)
        except Exception as e:
            # Silently continue - file might have syntax errors
            print(f"Warning: Could not parse {file_path}: {e}")
    
    def build_graph_from_tree(self, tree, file_path: str):
        """
        Extracts inheritance info from a pre-built Parse Tree.
        Does NOT perform parsing.
        """
        try:
            # La logica di visita rimane la stessa, ma opera su un albero già esistente
            if hasattr(tree, 'ordinaryCompilationUnit'):
                unit = tree.ordinaryCompilationUnit()
                if unit and hasattr(unit, 'topLevelClassOrInterfaceDeclaration'):
                    for decl in unit.topLevelClassOrInterfaceDeclaration():
                        if hasattr(decl, 'classDeclaration'):
                            self.visit_class_declaration(decl.classDeclaration(), file_path)
        except Exception as e:
            print(f"Warning: Could not extract graph info from {file_path}: {e}")
    
    def build_graph_from_directory(self, directory: str):
        """Scan directory recursively for all Java files and build inheritance graph"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    self.build_graph_from_file(file_path)
    
    def calculate_dit(self, class_name: str) -> int:
        """
        Calculate Depth of Inheritance Tree (DIT) for a class.
        DIT is the distance from the class to java.lang.Object.
        """
        if class_name not in self.inheritance_graph:
            return 0
        
        depth = 0
        current = class_name
        visited = set()
        
        while current and current in self.inheritance_graph:
            if current in visited:
                # Circular reference detected
                break
            visited.add(current)
            
            parent = self.inheritance_graph[current]
            if parent is None:
                # Reached root (java.lang.Object)
                break
            
            depth += 1
            current = parent
        
        return depth
    
    def calculate_noc(self, class_name: str) -> int:
        """
        Calculate Number of Children (NOC) for a class.
        NOC is the count of direct subclasses.
        """
        count = 0
        for child, parent in self.inheritance_graph.items():
            if parent == class_name:
                count += 1
        return count
    
    def get_graph(self) -> Dict[str, Optional[str]]:
        """Get the complete inheritance graph"""
        return self.inheritance_graph.copy()
    
    def get_class_file(self, class_name: str) -> Optional[str]:
        """Get the file path where a class is defined"""
        return self.class_files.get(class_name)

