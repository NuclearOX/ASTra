"""
Calculator Module
Contains all mathematical formulas for software metrics calculations.
This module keeps the metric calculation logic clean and reusable.
"""

import math
from typing import Dict


class HalsteadCalculator:
    """Calculates Halstead Complexity Metrics"""
    
    @staticmethod
    def calculate(n1: int, n2: int, N1: int, N2: int) -> Dict[str, float]:
        """
        Calculate all Halstead metrics from base counts.
        
        Args:
            n1: Number of unique operators
            n2: Number of unique operands
            N1: Total operator occurrences
            N2: Total operand occurrences
        
        Returns:
            Dictionary containing all Halstead metrics
        """
        if n1 == 0 or n2 == 0:
            # Avoid division by zero
            return {
                'n1': n1,
                'n2': n2,
                'N1': N1,
                'N2': N2,
                'N': N1 + N2,
                'n': n1 + n2,
                'V': 0.0,
                'D': 0.0,
                'E': 0.0,
                'T': 0.0,
                'L': 0.0,
                'B': 0.0
            }
        
        # Program Length
        N = N1 + N2
        
        # Vocabulary
        n = n1 + n2
        
        # Volume: V = N * log2(n)
        V = N * math.log2(n) if n > 0 else 0.0
        
        # Difficulty: D = (n1/2) * (N2/n2)
        D = (n1 / 2.0) * (N2 / n2) if n2 > 0 else 0.0
        
        # Effort: E = D * V
        E = D * V
        
        # Time: T = E / 18
        T = E / 18.0
        
        # Program Level: L = 1 / D
        L = 1.0 / D if D > 0 else 0.0
        
        # Estimated Bugs: B = V / 3000
        B = V / 3000.0
        
        return {
            'n1': n1,
            'n2': n2,
            'N1': N1,
            'N2': N2,
            'N': N,
            'n': n,
            'V': V,
            'D': D,
            'E': E,
            'T': T,
            'L': L,
            'B': B
        }


class ComplexityCalculator:
    """Calculates Cyclomatic Complexity"""
    
    @staticmethod
    def calculate_base_complexity() -> int:
        """Base complexity is always 1"""
        return 1
    
    @staticmethod
    def increment_for_control_flow(complexity: int, increment: int = 1) -> int:
        """Increment complexity for control flow statements"""
        return complexity + increment


class MaintainabilityCalculator:
    """Calculates Maintainability Index"""
    
    @staticmethod
    def calculate(volume: float, cyclomatic_complexity: int, loc: int) -> float:
        """
        Calculate Maintainability Index (MI).
        
        Formula: MI = 171 - 5.2*ln(V) - 0.23*CC - 16.2*ln(LOC)
        Normalized to 0-100 range.
        
        Args:
            volume: Halstead Volume (V)
            cyclomatic_complexity: Cyclomatic Complexity (CC)
            loc: Logical Lines of Code (LOC)
        
        Returns:
            Maintainability Index normalized to 0-100
        """
        if loc <= 0:
            loc = 1  # Avoid log(0)
        
        if volume <= 0:
            volume = 1  # Avoid log(0)
        
        # Calculate MI using the standard formula
        mi = 171.0 - 5.2 * math.log(volume) - 0.23 * cyclomatic_complexity - 16.2 * math.log(loc)
        
        # Normalize to 0-100 range
        # MI can be negative, so we clamp it
        mi = max(0.0, min(100.0, mi))
        
        return mi
    
    @staticmethod
    def get_category(mi: float) -> str:
        """
        Categorize Maintainability Index.
        
        Returns:
            'Green' (>85), 'Yellow' (65-85), or 'Red' (<65)
        """
        if mi > 85:
            return 'Green'
        elif mi >= 65:
            return 'Yellow'
        else:
            return 'Red'


class CKCalculator:
    """Calculates CK (Chidamber & Kemerer) Object-Oriented Metrics"""
    
    @staticmethod
    def calculate_wmc(method_complexities: list) -> int:
        """
        Calculate Weighted Methods per Class (WMC).
        WMC is the sum of Cyclomatic Complexity of all methods in a class.
        
        Args:
            method_complexities: List of cyclomatic complexity values for each method
        
        Returns:
            WMC value
        """
        return sum(method_complexities)
    
    @staticmethod
    def calculate_cbo(external_types: set) -> int:
        """
        Calculate Coupling Between Objects (CBO).
        CBO is the count of unique external types referenced in fields/methods.
        
        Args:
            external_types: Set of external type names referenced
        
        Returns:
            CBO value
        """
        return len(external_types)

