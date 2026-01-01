"""
Refactoring Advisor Module
Interprets metrics to provide actionable refactoring suggestions based on 
standard software engineering thresholds (Martin Fowler, Clean Code).
"""

from typing import List

# Importiamo solo per type hinting.
# Se questo causa problemi di import circolare, si può rimuovere l'hint o usare stringhe.
try:
    from astra.metrics_visitor import ClassMetrics, MethodMetrics
except ImportError:
    pass

class RefactoringAdvisor:
    """Analyzes metrics and generates refactoring recommendations"""
    
    # Thresholds based on industry standards
    THRESHOLDS = {
        'CC_MODERATE': 10,      # Method Cyclomatic Complexity
        'CC_HIGH': 20,
        'MI_CRITICAL': 65,      # Maintainability Index
        'MI_WARN': 85,
        'WMC_HIGH': 50,         # Weighted Methods per Class
        'CBO_HIGH': 10,         # Coupling Between Objects
        'DIT_HIGH': 5,          # Depth of Inheritance
        'METHOD_LOC_HIGH': 50,  # Lines of Code per method
        'CLASS_LOC_HIGH': 500   # Lines of Code per class
    }

    @staticmethod
    def get_class_advice(cls) -> List[str]:
        """
        Generate suggestions for a class.
        Accepts a ClassMetrics object.
        """
        tips = []

        # 1. Check Maintainability Index
        if cls.maintainability_index < RefactoringAdvisor.THRESHOLDS['MI_CRITICAL']:
            tips.append("⚠️ **Critical Maintainability**: This class is very hard to maintain. Consider a complete rewrite or splitting it into smaller components.")
        
        # 2. Check God Class (High WMC + High LOC)
        if cls.wmc > RefactoringAdvisor.THRESHOLDS['WMC_HIGH'] or cls.loc > RefactoringAdvisor.THRESHOLDS['CLASS_LOC_HIGH']:
            tips.append("🏗️ **God Class Detected**: This class does too much (High WMC/LOC). Apply **Extract Class** to separate responsibilities (Single Responsibility Principle).")

        # 3. Check High Coupling (CBO)
        if cls.cbo > RefactoringAdvisor.THRESHOLDS['CBO_HIGH']:
            tips.append("🔗 **High Coupling**: Depends on many external types. Consider using **Dependency Injection**, **Facade Pattern**, or **Mediator** to decouple.")

        # 4. Check Deep Inheritance (DIT)
        if cls.dit > RefactoringAdvisor.THRESHOLDS['DIT_HIGH']:
            tips.append("🌳 **Deep Inheritance**: Inheritance tree is too deep. Prefer **Composition over Inheritance** to reduce fragility.")

        return tips

    @staticmethod
    def get_method_advice(method) -> List[str]:
        """
        Generate suggestions for a method.
        Accepts a MethodMetrics object.
        """
        tips = []

        # 1. Cyclomatic Complexity
        cc = method.cyclomatic_complexity
        if cc > RefactoringAdvisor.THRESHOLDS['CC_HIGH']:
            tips.append(f"🔀 **Very High Complexity ({cc})**: Too many branches. Refactor using **Strategy Pattern** or **Polymorphism** to replace switch/if chains.")
        elif cc > RefactoringAdvisor.THRESHOLDS['CC_MODERATE']:
            tips.append(f"✂️ **High Complexity ({cc})**: Hard to test. Apply **Extract Method** to decompose complex logic.")

        # 2. Method Size (LOC)
        if method.loc > RefactoringAdvisor.THRESHOLDS['METHOD_LOC_HIGH']:
            tips.append(f"📜 **Long Method ({method.loc} lines)**: Hard to read. Group related lines and apply **Extract Method**.")

        # 3. Halstead Effort (Cognitive Load)
        if method.halstead:
            effort = method.halstead.get('E', 0)
            if effort > 60000: # High threshold for "Brain Melter"
                tips.append("🧠 **High Cognitive Load**: High Halstead Effort. Simplify logic or rename variables for clarity.")

        return tips