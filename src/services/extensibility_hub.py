"""
Extensibility Framework for Vedic Astrology Software
Provides plugin/module architecture for adding new features:
- Compatibility calculations
- Yoga calculations
- Bhava chart calculations
- Navamsa calculations
- And more...

This service acts as a central hub for all calculation modules.
"""

import logging
from typing import Dict, List, Callable, Optional, Any
from abc import ABC, abstractmethod

from models.chart_data import ChartData
from models.birth_data import BirthData

logger = logging.getLogger(__name__)


# ============================================================================
# ABSTRACT BASE CLASS FOR ALL MODULES
# ============================================================================

class AstrologyModule(ABC):
    """Abstract base class for all astrology calculation modules."""

    module_name: str = "Base Module"
    module_version: str = "1.0"
    description: str = "Base astrology module"

    @abstractmethod
    def calculate(self, chart_data: ChartData) -> Dict[str, Any]:
        """
        Perform calculation.
        
        Args:
            chart_data: ChartData object
            
        Returns:
            Dictionary with calculation results
        """
        pass

    @abstractmethod
    def get_report(self) -> str:
        """Get human-readable report of last calculation."""
        pass


# ============================================================================
# BUILT-IN PLACEHOLDER MODULES (Ready for you to implement)
# ============================================================================

class CompatibilityModule(AstrologyModule):
    """
    Compatibility calculations between two birth charts.
    PLACEHOLDER - Ready for your implementation
    """

    module_name = "Compatibility Analysis"
    module_version = "1.0"
    description = "Calculate compatibility between two people"

    def __init__(self):
        self.last_result = None

    def calculate(self, chart_data: ChartData, partner_chart: ChartData = None) -> Dict[str, Any]:
        """
        Calculate compatibility between two charts.
        
        YOUR CODE GOES HERE:
        - Extract planetary positions from both charts
        - Compare houses, signs, nakshatras
        - Calculate compatibility scores
        - Generate insights
        """
        logger.info("CompatibilityModule: Implement your compatibility logic here")

        # PLACEHOLDER: Return structure for your implementation
        self.last_result = {
            "status": "ready_for_implementation",
            "message": "Add your compatibility calculation code here",
            "chart1": chart_data.birth_info.place if chart_data else None,
            "chart2": partner_chart.birth_info.place if partner_chart else None,
            # Add your calculated results here
        }
        return self.last_result

    def get_report(self) -> str:
        if not self.last_result:
            return "No calculation performed yet"
        return f"Compatibility Analysis for {self.last_result['chart1']} & {self.last_result['chart2']}"


class YogaModule(AstrologyModule):
    """
    Yoga (auspicious combinations) calculations.
    PLACEHOLDER - Ready for your implementation
    """

    module_name = "Yoga Calculator"
    module_version = "1.0"
    description = "Calculate yogas and auspicious combinations"

    def __init__(self):
        self.last_result = None

    def calculate(self, chart_data: ChartData) -> Dict[str, Any]:
        """
        Calculate yogas in the chart.
        
        YOUR CODE GOES HERE:
        - Check for classical yogas (Raja Yoga, Dhana Yoga, etc.)
        - Analyze planetary conjunctions
        - Check for auspicious combinations
        - Calculate yoga strength/intensity
        """
        logger.info("YogaModule: Implement your yoga calculation logic here")

        self.last_result = {
            "status": "ready_for_implementation",
            "message": "Add your yoga calculation code here",
            "place": chart_data.birth_info.place,
            "yogas_found": [],  # Add your detected yogas here
            # Add your calculated results here
        }
        return self.last_result

    def get_report(self) -> str:
        if not self.last_result:
            return "No calculation performed yet"
        return f"Yoga Analysis for {self.last_result['place']}"


class BhavaChartModule(AstrologyModule):
    """
    Bhava (House) chart calculations.
    PLACEHOLDER - Ready for your implementation
    """

    module_name = "Bhava Chart"
    module_version = "1.0"
    description = "Calculate Bhava (house) chart and house cusps"

    def __init__(self):
        self.last_result = None

    def calculate(self, chart_data: ChartData) -> Dict[str, Any]:
        """
        Calculate Bhava chart.
        
        YOUR CODE GOES HERE:
        - Calculate exact house cusps
        - Position planets in houses
        - Calculate bhava strengths
        - Analyze house rulers
        """
        logger.info("BhavaChartModule: Implement your Bhava chart logic here")

        self.last_result = {
            "status": "ready_for_implementation",
            "message": "Add your Bhava chart calculation code here",
            "place": chart_data.birth_info.place,
            "houses": {},  # Add your house calculations here
            # Add your calculated results here
        }
        return self.last_result

    def get_report(self) -> str:
        if not self.last_result:
            return "No calculation performed yet"
        return f"Bhava Chart for {self.last_result['place']}"


class NavamsaModule(AstrologyModule):
    """
    Navamsa (D9) chart calculations.
    PLACEHOLDER - Ready for your implementation
    """

    module_name = "Navamsa Chart"
    module_version = "1.0"
    description = "Calculate Navamsa (D9) divisional chart"

    def __init__(self):
        self.last_result = None

    def calculate(self, chart_data: ChartData) -> Dict[str, Any]:
        """
        Calculate Navamsa chart.
        
        YOUR CODE GOES HERE:
        - Divide each zodiac sign into 9 parts (navamsas)
        - Calculate navamsa positions for each planet
        - Analyze navamsa placements
        - Calculate navamsa strength
        """
        logger.info("NavamsaModule: Implement your Navamsa chart logic here")

        self.last_result = {
            "status": "ready_for_implementation",
            "message": "Add your Navamsa chart calculation code here",
            "place": chart_data.birth_info.place,
            "navamsa_planets": {},  # Add your navamsa positions here
            # Add your calculated results here
        }
        return self.last_result

    def get_report(self) -> str:
        if not self.last_result:
            return "No calculation performed yet"
        return f"Navamsa Chart for {self.last_result['place']}"


# ============================================================================
# MODULE REGISTRY - Central Hub
# ============================================================================

class ModuleRegistry:
    """
    Central registry for all astrology modules.
    Manages and coordinates all calculation plugins.
    """

    def __init__(self):
        self.modules: Dict[str, AstrologyModule] = {}
        self._register_default_modules()

    def _register_default_modules(self):
        """Register built-in modules."""
        self.register("compatibility", CompatibilityModule())
        self.register("yoga", YogaModule())
        self.register("bhava", BhavaChartModule())
        self.register("navamsa", NavamsaModule())
        logger.info("Default modules registered")

    def register(self, module_id: str, module: AstrologyModule) -> None:
        """
        Register a new module.
        
        Args:
            module_id: Unique identifier for module
            module: AstrologyModule instance
        """
        self.modules[module_id] = module
        logger.info(f"Registered module: {module_id} ({module.module_name})")

    def unregister(self, module_id: str) -> bool:
        """Unregister a module."""
        if module_id in self.modules:
            del self.modules[module_id]
            logger.info(f"Unregistered module: {module_id}")
            return True
        return False

    def get_module(self, module_id: str) -> Optional[AstrologyModule]:
        """Get a module by ID."""
        return self.modules.get(module_id)

    def list_modules(self) -> Dict[str, str]:
        """List all registered modules with descriptions."""
        return {
            module_id: f"{module.module_name} v{module.module_version} - {module.description}"
            for module_id, module in self.modules.items()
        }

    def execute(self, module_id: str, chart_data: ChartData, **kwargs) -> Dict[str, Any]:
        """
        Execute a module's calculation.
        
        Args:
            module_id: ID of module to execute
            chart_data: ChartData for calculation
            **kwargs: Additional arguments for the module
            
        Returns:
            Calculation results
        """
        module = self.get_module(module_id)
        if not module:
            logger.error(f"Module not found: {module_id}")
            return {"error": f"Module '{module_id}' not found"}

        try:
            result = module.calculate(chart_data, **kwargs)
            logger.info(f"Module '{module_id}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"Module '{module_id}' execution failed: {str(e)}")
            return {"error": str(e)}

    def get_all_reports(self, executed_modules: List[str]) -> Dict[str, str]:
        """Get reports from all executed modules."""
        reports = {}
        for module_id in executed_modules:
            module = self.get_module(module_id)
            if module:
                reports[module_id] = module.get_report()
        return reports
