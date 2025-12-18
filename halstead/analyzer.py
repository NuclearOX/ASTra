"""
Core Analysis Module
Implements Halstead Metrics calculation for C and Java code
"""

import re
import math
from datetime import datetime


class Analyzer:
    """Analyzes code and calculates Halstead Complexity Metrics"""
    
    def __init__(self, language='c'):
        """
        Initialize analyzer for a specific language.
        
        Args:
            language: Programming language ('c' or 'java')
        """
        self.language = language
        self.ops = self._get_operators()
        self.kws = self._get_keywords()
        self.flow = {'if', 'else', 'while', 'for', 'case', 'catch', 'switch', 'try', '?', '&&', '||'}

    def _get_operators(self):
        """Get operators based on language"""
        common_ops = [
            '>>=', '<<=', '!=', '%=', '&&', '&=', '*=', '++', '+=', 
            '--', '-=', '/=', '<<', '<=', '==', '>=', '>>', '^=', '|=', '||',
            '!', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';',
            '<', '=', '>', '?', '[', ']', '^', '{', '|', '}', '~'
        ]
        if self.language == 'java':
            # Java-specific operators
            common_ops.extend(['instanceof', '::'])
        return common_ops

    def _get_keywords(self):
        """Get keywords based on language"""
        if self.language == 'c':
            return {
                'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
                'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
                'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
                'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
            }
        elif self.language == 'java':
            return {
                'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
                'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
                'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
                'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package',
                'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp',
                'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient',
                'try', 'void', 'volatile', 'while'
            }
        return set()

    def _preprocess_code(self, code):
        """Remove language-specific constructs that shouldn't be analyzed"""
        if self.language == 'c':
            # Remove preprocessor directives
            code_clean = re.sub(r'^\s*#.*', '', code, flags=re.MULTILINE)
        elif self.language == 'java':
            # Remove package and import statements
            code_clean = re.sub(r'^\s*(package|import)\s+.*?;', '', code, flags=re.MULTILINE)
        else:
            code_clean = code
        return code_clean

    def _tokenize(self, code):
        """Tokenize code into operators and operands"""
        token_spec = [
            ('STR', r'"(?:\\.|[^\\"])*"'),
            ('CHR', r"'(?:\\.|[^\\\'])*'"),
            ('CMT', r'//.*?$|/\*.*?\*/'),
            ('NUM', r'\b0x[0-9a-fA-F]+|\b\d+\.?\d*[eE][-+]?\d+|\b\d+\.\d+|\b\d+'),
            ('ID',  r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('OP',  "|".join(map(re.escape, sorted(self.ops, key=len, reverse=True)))),
            ('SKP', r'[ \t\r\n]+'),
            ('ERR', r'.')
        ]
        
        regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
        
        n1_ops, n2_rands = [], []
        cyclomatic = 1
        
        for mo in re.finditer(regex, code, re.DOTALL | re.MULTILINE):
            kind = mo.lastgroup
            val = mo.group()
            
            if kind == 'SKP' or kind == 'CMT': 
                continue
            
            if kind == 'ID':
                if val in self.kws: 
                    n1_ops.append(val)
                    if val in self.flow: 
                        cyclomatic += 1
                else: 
                    n2_rands.append(val)
            elif kind == 'OP':
                n1_ops.append(val)
                if val in self.flow: 
                    cyclomatic += 1
            elif kind in ('STR', 'CHR', 'NUM'):
                n2_rands.append(val)
        
        return n1_ops, n2_rands, cyclomatic

    def _calculate_halstead_metrics(self, n1, n2, N1, N2):
        """Calculate Halstead metrics from base counts"""
        n = n1 + n2
        N = N1 + N2
        
        # Avoid division by zero
        if n2 == 0: 
            n2 = 1
        if n == 0: 
            n = 1
        
        volume = N * math.log2(n)
        difficulty = (n1 / 2.0) * (N2 / n2)
        effort = difficulty * volume
        time = effort / 18.0
        level = 1.0 / difficulty if difficulty > 0 else 0
        bugs = volume / 3000.0
        
        return {
            'n': n, 'N': N, 'V': volume, 'D': difficulty, 
            'E': effort, 'T': time, 'L': level, 'B': bugs
        }

    def _calculate_quality_metrics(self, code, cyclomatic, volume):
        """Calculate quality metrics (LOC, MI)"""
        loc = len([x for x in code.splitlines() if x.strip()])
        if loc == 0: 
            loc = 1
        
        mi = 171 - 5.2 * math.log(volume if volume > 0 else 1) - 0.23 * cyclomatic - 16.2 * math.log(loc)
        mi = max(0, min(100, mi * 100 / 171))
        
        return {'loc': loc, 'cc': cyclomatic, 'mi': mi}

    def analyze(self, code, filename):
        """
        Analyze code and return comprehensive metrics.
        
        Args:
            code: Source code as string
            filename: Path to the source file
            
        Returns:
            Dictionary containing all calculated metrics
        """
        # Preprocess code
        code_clean = self._preprocess_code(code)
        
        # Tokenize
        n1_ops, n2_rands, cyclomatic = self._tokenize(code_clean)
        
        # Calculate base counts
        n1 = len(set(n1_ops))
        n2 = len(set(n2_rands))
        N1 = len(n1_ops)
        N2 = len(n2_rands)
        
        # Calculate Halstead metrics
        halstead = self._calculate_halstead_metrics(n1, n2, N1, N2)
        
        # Calculate quality metrics
        quality = self._calculate_quality_metrics(code, cyclomatic, halstead['V'])
        
        return {
            'file': filename,
            'language': self.language,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'base': {'n1': n1, 'n2': n2, 'N1': N1, 'N2': N2},
            'halstead': halstead,
            'quality': quality
        }

