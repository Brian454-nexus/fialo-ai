"""
Strategy optimization engine for the AI Community Waste-to-Energy Optimizer.
Integrates AI predictions, simulation results, and impact calculations to provide optimal strategies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

from models.waste_types import WASTE_TYPES, ConversionMethod
from models.community import Community
from models.conversion_system import ConversionSystem, ConversionPlan
from ai_engine.prediction_engine import EnergyPredictionEngine
from ai_engine.optimization_engine import GeneticOptimizer, LinearProgrammingOptimizer, OptimizationConstraints
from simulation.waste_simulator import create_sample_waste_scenario
from simulation.energy_simulator import create_complete_energy_simulation
from utils.impact_calculator import ImpactCalculator, ComprehensiveImpact


@dataclass
class OptimizationStrategy:
    """Optimized waste-to-energy conversion strategy."""
    strategy_name: str
    description: str
    waste_allocation: Dict[str, float]  # waste_type -> amount
    system_selection: List[str]  # selected system names
    processing_schedule: Dict[datetime, Dict[str, float]]  # timestamp -> waste_type -> amount
    expected_energy_output: float
    expected_emissions_avoided: Dict[str, float]
    expected_cost: float
    expected_roi: float
    confidence_score: float
    implementation_difficulty: str  # "Low", "Medium", "High"
    time_to_implement: str  # "Immediate", "1-3 months", "3-6 months", "6+ months"


@dataclass
class OptimizationResult:
    """Result of strategy optimization."""
    best_strategy: OptimizationStrategy
    alternative_strategies: List[OptimizationStrategy]
    impact_assessment: ComprehensiveImpact
    recommendations: List[str]
    risk_assessment: Dict[str, Any]
    implementation_roadmap: List[Dict[str, Any]]


class StrategyOptimizer:
    """Main strategy optimization engine."""
    
    def __init__(self):
        self.prediction_engine = EnergyPredictionEngine()
        self.impact_calculator = ImpactCalculator()
        self.genetic_optimizer = GeneticOptimizer()
        self.linear_optimizer = LinearProgrammingOptimizer()
        
        # Load or train models
        try:
            self.prediction_engine._load_models()
        except:
            self.prediction_engine.train_models()
    
    def optimize_strategy(
        self,
        community: Community,
        available_systems: List[ConversionSystem],
        waste_available: Dict[str, float],
        optimization_goals: Dict[str, float] = None,
        constraints: Dict[str, Any] = None,
        time_horizon_days: int = 30
    ) -> OptimizationResult:
        """
        Optimize waste-to-energy conversion strategy for a community.
        
        Args:
            community: Community to optimize for
            available_systems: Available conversion systems
            waste_available: Available waste by type (kg)
            optimization_goals: Optimization goals and weights
            constraints: Optimization constraints
            time_horizon_days: Optimization time horizon
        
        Returns:
            Optimized strategy result
        """
        if optimization_goals is None:
            optimization_goals = {
                'energy_output': 0.4,
                'cost_efficiency': 0.3,
                'emissions_reduction': 0.2,
                'social_impact': 0.1
            }
        
        if constraints is None:
            constraints = {
                'max_cost_usd': 10000,
                'min_energy_output_kwh': 100,
                'max_processing_time_hours': 24,
                'system_availability': {system.name: True for system in available_systems}
            }
        
        # Generate multiple strategy options
        strategies = self._generate_strategy_options(
            community, available_systems, waste_available, constraints, time_horizon_days
        )
        
        # Evaluate strategies
        evaluated_strategies = []
        for strategy in strategies:
            evaluation = self._evaluate_strategy(
                strategy, community, available_systems, optimization_goals
            )
            evaluated_strategies.append(evaluation)
        
        # Select best strategy
        best_strategy = max(evaluated_strategies, key=lambda s: s.confidence_score)
        
        # Generate alternatives
        alternative_strategies = [
            s for s in evaluated_strategies 
            if s != best_strategy and s.confidence_score > 0.7
        ][:3]  # Top 3 alternatives
        
        # Calculate impact assessment
        impact_assessment = self._calculate_strategy_impact(
            best_strategy, community, available_systems
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            best_strategy, impact_assessment, community
        )
        
        # Risk assessment
        risk_assessment = self._assess_risks(best_strategy, community, available_systems)
        
        # Implementation roadmap
        implementation_roadmap = self._create_implementation_roadmap(
            best_strategy, community, available_systems
        )
        
        return OptimizationResult(
            best_strategy=best_strategy,
            alternative_strategies=alternative_strategies,
            impact_assessment=impact_assessment,
            recommendations=recommendations,
            risk_assessment=risk_assessment,
            implementation_roadmap=implementation_roadmap
        )
    
    def _generate_strategy_options(
        self,
        community: Community,
        available_systems: List[ConversionSystem],
        waste_available: Dict[str, float],
        constraints: Dict[str, Any],
        time_horizon_days: int
    ) -> List[OptimizationStrategy]:
        """Generate multiple strategy options using different approaches."""
        strategies = []
        
        # Strategy 1: Maximum Energy Output
        strategies.append(self._create_max_energy_strategy(
            community, available_systems, waste_available, constraints
        ))
        
        # Strategy 2: Cost-Optimized
        strategies.append(self._create_cost_optimized_strategy(
            community, available_systems, waste_available, constraints
        ))
        
        # Strategy 3: Balanced Approach
        strategies.append(self._create_balanced_strategy(
            community, available_systems, waste_available, constraints
        ))
        
        # Strategy 4: AI-Optimized
        strategies.append(self._create_ai_optimized_strategy(
            community, available_systems, waste_available, constraints, time_horizon_days
        ))
        
        # Strategy 5: Community-Specific
        strategies.append(self._create_community_specific_strategy(
            community, available_systems, waste_available, constraints
        ))
        
        return strategies
    
    def _create_max_energy_strategy(
        self,
        community: Community,
        available_systems: List[ConversionSystem],
        waste_available: Dict[str, float],
        constraints: Dict[str, Any]
    ) -> OptimizationStrategy:
        """Create strategy focused on maximum energy output."""
        
        # Select systems with highest energy efficiency
        energy_efficient_systems = sorted(
            available_systems,
            key=lambda s: s.efficiency,
            reverse=True
        )[:3]  # Top 3 most efficient systems
        
        # Allocate waste to maximize energy output
        waste_allocation = {}
        for waste_type_name, amount in waste_available.items():
            waste_type = WASTE_TYPES.get(waste_type_name)
            if waste_type:
                # Find best system for this waste type
                best_efficiency = 0
                for system in energy_efficient_systems:
                    efficiency = waste_type.conversion_efficiency.get(system.system_type, 0)
                    if efficiency > best_efficiency:
                        best_efficiency = efficiency
                
                if best_efficiency > 0:
                    waste_allocation[waste_type_name] = amount
        
        # Calculate expected outputs
        expected_energy = sum(
            amount * WASTE_TYPES[wt].energy_content_kwh_per_kg * 
            max(WASTE_TYPES[wt].conversion_efficiency.values())
            for wt, amount in waste_allocation.items()
        )
        
        expected_cost = sum(
            system.operational_cost_per_day for system in energy_efficient_systems
        )
        
        return OptimizationStrategy(
            strategy_name="Maximum Energy Output",
            description="Focus on maximizing energy generation using the most efficient systems",
            waste_allocation=waste_allocation,
            system_selection=[s.name for s in energy_efficient_systems],
            processing_schedule={},  # Simplified for now
            expected_energy_output=expected_energy,
            expected_emissions_avoided=self._calculate_emissions_avoided(waste_allocation),
            expected_cost=expected_cost,
            expected_roi=self._calculate_roi(expected_energy, expected_cost, community),
            confidence_score=0.85,
            implementation_difficulty="Medium",
            time_to_implement="1-3 months"
        )
    
    def _create_cost_optimized_strategy(
        self,
        community: Community,
        available_systems: List[ConversionSystem],
        waste_available: Dict[str, float],
        constraints: Dict[str, Any]
    ) -> OptimizationStrategy:
        """Create strategy focused on cost optimization."""
        
        # Select systems with lowest operational cost
        cost_efficient_systems = sorted(
            available_systems,
            key=lambda s: s.operational_cost_per_day
        )[:2]  # Top 2 most cost-efficient systems
        
        # Allocate waste to minimize cost while meeting minimum energy requirements
        waste_allocation = {}
        min_energy = constraints.get('min_energy_output_kwh', 100)
        current_energy = 0
        
        for waste_type_name, amount in waste_available.items():
            if current_energy >= min_energy:
                break
                
            waste_type = WASTE_TYPES.get(waste_type_name)
            if waste_type:
                # Find most cost-effective system for this waste type
                best_cost_benefit = float('inf')
                for system in cost_efficient_systems:
                    efficiency = waste_type.conversion_efficiency.get(system.system_type, 0)
                    if efficiency > 0:
                        cost_per_kwh = system.operational_cost_per_day / (
                            system.capacity_kg_per_day * waste_type.energy_content_kwh_per_kg * efficiency
                        )
                        if cost_per_kwh < best_cost_benefit:
                            best_cost_benefit = cost_per_kwh
                
                if best_cost_benefit < float('inf'):
                    waste_allocation[waste_type_name] = amount
                    current_energy += amount * waste_type.energy_content_kwh_per_kg * max(
                        waste_type.conversion_efficiency.values()
                    )
        
        expected_energy = sum(
            amount * WASTE_TYPES[wt].energy_content_kwh_per_kg * 
            max(WASTE_TYPES[wt].conversion_efficiency.values())
            for wt, amount in waste_allocation.items()
        )
        
        expected_cost = sum(
            system.operational_cost_per_day for system in cost_efficient_systems
        )
        
        return OptimizationStrategy(
            strategy_name="Cost-Optimized",
            description="Focus on minimizing operational costs while meeting energy requirements",
            waste_allocation=waste_allocation,
            system_selection=[s.name for s in cost_efficient_systems],
            processing_schedule={},
            expected_energy_output=expected_energy,
            expected_emissions_avoided=self._calculate_emissions_avoided(waste_allocation),
            expected_cost=expected_cost,
            expected_roi=self._calculate_roi(expected_energy, expected_cost, community),
            confidence_score=0.80,
            implementation_difficulty="Low",
            time_to_implement="Immediate"
        )
    
    def _create_balanced_strategy(
        self,
        community: Community,
        available_systems: List[ConversionSystem],
        waste_available: Dict[str, float],
        constraints: Dict[str, Any]
    ) -> OptimizationStrategy:
        """Create balanced strategy considering multiple factors."""
        
        # Select systems with balanced efficiency and cost
        balanced_systems = []
        for system in available_systems:
            # Calculate balance score (efficiency * cost_factor)
            cost_factor = 1.0 / (1.0 + system.operational_cost_per_day / 100)
            balance_score = system.efficiency * cost_factor
            balanced_systems.append((system, balance_score))
        
        balanced_systems.sort(key=lambda x: x[1], reverse=True)
        selected_systems = [s[0] for s in balanced_systems[:3]]
        
        # Allocate waste proportionally
        waste_allocation = {}
        for waste_type_name, amount in waste_available.items():
            waste_type = WASTE_TYPES.get(waste_type_name)
            if waste_type:
                # Use 80% of available waste for balanced approach
                waste_allocation[waste_type_name] = amount * 0.8
        
        expected_energy = sum(
            amount * WASTE_TYPES[wt].energy_content_kwh_per_kg * 
            max(WASTE_TYPES[wt].conversion_efficiency.values())
            for wt, amount in waste_allocation.items()
        )
        
        expected_cost = sum(
            system.operational_cost_per_day for system in selected_systems
        )
        
        return OptimizationStrategy(
            strategy_name="Balanced Approach",
            description="Balance energy output, cost efficiency, and environmental impact",
            waste_allocation=waste_allocation,
            system_selection=[s.name for s in selected_systems],
            processing_schedule={},
            expected_energy_output=expected_energy,
            expected_emissions_avoided=self._calculate_emissions_avoided(waste_allocation),
            expected_cost=expected_cost,
            expected_roi=self._calculate_roi(expected_energy, expected_cost, community),
            confidence_score=0.75,
            implementation_difficulty="Medium",
            time_to_implement="1-3 months"
        )
    
    def _create_ai_optimized_strategy(
        self,
        community: Community,
        available_systems: List[ConversionSystem],
        waste_available: Dict[str, float],
        constraints: Dict[str, Any],
        time_horizon_days: int
    ) -> OptimizationStrategy:
        """Create AI-optimized strategy using machine learning."""
        
        # Use AI to predict optimal allocation
        predictions = self.prediction_engine.predict_energy_potential(
            waste_available,
            ConversionMethod.BIOGAS_DIGESTION
        )
        
        # Use genetic algorithm for optimization
        optimization_constraints = OptimizationConstraints(
            max_processing_capacity_kg_per_hour=sum(available_systems, key=lambda s: s.capacity_kg_per_day).capacity_kg_per_day / 24,
            min_energy_output_kwh=constraints.get('min_energy_output_kwh', 100),
            max_operational_cost_usd=constraints.get('max_cost_usd', 10000),
            max_processing_time_hours=constraints.get('max_processing_time_hours', 24),
            system_availability=constraints.get('system_availability', {})
        )
        
        # Generate energy demand profile
        from ..models.community import generate_hourly_demand_profile
        demand_profile = generate_hourly_demand_profile(community, datetime.now())
        demand_data = [
            {'timestamp': demand.timestamp, 'predicted_demand_kwh': demand.demand_kwh}
            for demand in demand_profile
        ]
        
        # Run genetic optimization
        optimization_result = self.genetic_optimizer.optimize(
            waste_available,
            available_systems,
            demand_data,
            optimization_constraints
        )
        
        # Convert to strategy
        waste_allocation = {}
        for timestamp, hourly_waste in optimization_result.optimal_schedule.items():
            for waste_type, amount in hourly_waste.items():
                if waste_type in waste_allocation:
                    waste_allocation[waste_type] += amount
                else:
                    waste_allocation[waste_type] = amount
        
        return OptimizationStrategy(
            strategy_name="AI-Optimized",
            description="AI-powered optimization using machine learning and genetic algorithms",
            waste_allocation=waste_allocation,
            system_selection=[s.name for s in optimization_result.optimal_systems],
            processing_schedule=optimization_result.optimal_schedule,
            expected_energy_output=optimization_result.total_energy_output,
            expected_emissions_avoided=optimization_result.emissions_avoided,
            expected_cost=optimization_result.total_cost,
            expected_roi=self._calculate_roi(optimization_result.total_energy_output, optimization_result.total_cost, community),
            confidence_score=0.90,
            implementation_difficulty="High",
            time_to_implement="3-6 months"
        )
    
    def _create_community_specific_strategy(
        self,
        community: Community,
        available_systems: List[ConversionSystem],
        waste_available: Dict[str, float],
        constraints: Dict[str, Any]
    ) -> OptimizationStrategy:
        """Create strategy tailored to specific community characteristics."""
        
        # Adjust strategy based on community type
        if community.community_type.value == "rural_village":
            # Focus on simple, low-maintenance systems
            selected_systems = [s for s in available_systems if s.maintenance_interval_days >= 30]
        elif community.community_type.value == "market_area":
            # Focus on high-capacity systems
            selected_systems = sorted(available_systems, key=lambda s: s.capacity_kg_per_day, reverse=True)[:2]
        else:
            # Balanced selection
            selected_systems = available_systems[:3]
        
        # Adjust waste allocation based on community waste composition
        waste_allocation = {}
        for waste_type_name, amount in waste_available.items():
            # Use community's typical waste composition as guide
            community_percentage = community.waste_composition.get(waste_type_name, 0.2)
            allocated_amount = amount * community_percentage
            waste_allocation[waste_type_name] = allocated_amount
        
        expected_energy = sum(
            amount * WASTE_TYPES[wt].energy_content_kwh_per_kg * 
            max(WASTE_TYPES[wt].conversion_efficiency.values())
            for wt, amount in waste_allocation.items()
        )
        
        expected_cost = sum(
            system.operational_cost_per_day for system in selected_systems
        )
        
        return OptimizationStrategy(
            strategy_name="Community-Specific",
            description=f"Tailored strategy for {community.community_type.value} communities",
            waste_allocation=waste_allocation,
            system_selection=[s.name for s in selected_systems],
            processing_schedule={},
            expected_energy_output=expected_energy,
            expected_emissions_avoided=self._calculate_emissions_avoided(waste_allocation),
            expected_cost=expected_cost,
            expected_roi=self._calculate_roi(expected_energy, expected_cost, community),
            confidence_score=0.70,
            implementation_difficulty="Medium",
            time_to_implement="1-3 months"
        )
    
    def _evaluate_strategy(
        self,
        strategy: OptimizationStrategy,
        community: Community,
        available_systems: List[ConversionSystem],
        optimization_goals: Dict[str, float]
    ) -> OptimizationStrategy:
        """Evaluate and score a strategy."""
        
        # Calculate evaluation metrics
        energy_score = min(100, strategy.expected_energy_output / 1000 * 100)
        cost_score = min(100, max(0, 100 - strategy.expected_cost / 100))
        roi_score = min(100, strategy.expected_roi)
        emissions_score = min(100, strategy.expected_emissions_avoided.get('co2_kg', 0) / 100)
        
        # Calculate weighted score
        weighted_score = (
            energy_score * optimization_goals.get('energy_output', 0.4) +
            cost_score * optimization_goals.get('cost_efficiency', 0.3) +
            emissions_score * optimization_goals.get('emissions_reduction', 0.2) +
            roi_score * optimization_goals.get('social_impact', 0.1)
        )
        
        # Update confidence score
        strategy.confidence_score = weighted_score / 100
        
        return strategy
    
    def _calculate_emissions_avoided(self, waste_allocation: Dict[str, float]) -> Dict[str, float]:
        """Calculate emissions avoided from waste allocation."""
        total_co2 = 0.0
        total_methane = 0.0
        
        for waste_type_name, amount in waste_allocation.items():
            waste_type = WASTE_TYPES.get(waste_type_name)
            if waste_type:
                total_co2 += amount * waste_type.co2_emissions_kg_per_kg
                total_methane += amount * waste_type.methane_emissions_kg_per_kg
        
        return {
            'co2_kg': total_co2,
            'methane_kg': total_methane,
            'co2_equivalent_kg': total_co2 + (total_methane * 25)
        }
    
    def _calculate_roi(self, energy_output: float, cost: float, community: Community) -> float:
        """Calculate return on investment."""
        if cost <= 0:
            return 0.0
        
        energy_value = energy_output * community.energy_cost_per_kwh
        return (energy_value / cost) * 100
    
    def _calculate_strategy_impact(
        self,
        strategy: OptimizationStrategy,
        community: Community,
        available_systems: List[ConversionSystem]
    ) -> ComprehensiveImpact:
        """Calculate comprehensive impact for a strategy."""
        
        # Create mock conversion results for impact calculation
        mock_results = []
        for waste_type, amount in strategy.waste_allocation.items():
            if amount > 0:
                # Create a mock conversion result
                from ..models.conversion_system import ConversionResult
                mock_result = ConversionResult(
                    timestamp=datetime.now(),
                    waste_input_kg={waste_type: amount},
                    energy_output_kwh=amount * WASTE_TYPES[waste_type].energy_content_kwh_per_kg * 
                                     max(WASTE_TYPES[waste_type].conversion_efficiency.values()),
                    methane_output_m3=0.0,
                    co2_emissions_kg=-amount * WASTE_TYPES[waste_type].co2_emissions_kg_per_kg,
                    methane_emissions_kg=-amount * WASTE_TYPES[waste_type].methane_emissions_kg_per_kg,
                    processing_time_hours=1.0,
                    system_efficiency=0.7,
                    cost_usd=strategy.expected_cost / len(strategy.waste_allocation)
                )
                mock_results.append(mock_result)
        
        system_costs = [system.capital_cost for system in available_systems]
        
        return self.impact_calculator.calculate_comprehensive_impact(
            mock_results, community, system_costs
        )
    
    def _generate_recommendations(
        self,
        strategy: OptimizationStrategy,
        impact: ComprehensiveImpact,
        community: Community
    ) -> List[str]:
        """Generate recommendations based on strategy and impact."""
        recommendations = []
        
        # Energy recommendations
        if impact.environmental.renewable_energy_kwh < community.daily_energy_demand_kwh:
            recommendations.append(
                "Consider increasing waste collection or adding more conversion systems to meet energy demand."
            )
        
        # Cost recommendations
        if impact.economic.roi_percent < 10:
            recommendations.append(
                "Focus on reducing operational costs or increasing energy output to improve ROI."
            )
        
        # Environmental recommendations
        if impact.environmental.co2_equivalent_kg > 1000:
            recommendations.append(
                "Excellent environmental impact! Consider scaling up to serve more communities."
            )
        
        # Implementation recommendations
        if strategy.implementation_difficulty == "High":
            recommendations.append(
                "Start with pilot implementation to validate approach before full deployment."
            )
        
        # Community-specific recommendations
        if community.community_type.value == "rural_village":
            recommendations.append(
                "Focus on training community members for system operation and maintenance."
            )
        
        return recommendations
    
    def _assess_risks(
        self,
        strategy: OptimizationStrategy,
        community: Community,
        available_systems: List[ConversionSystem]
    ) -> Dict[str, Any]:
        """Assess risks associated with the strategy."""
        
        risks = {
            'technical_risks': [],
            'financial_risks': [],
            'operational_risks': [],
            'environmental_risks': [],
            'overall_risk_level': 'Low'
        }
        
        # Technical risks
        if strategy.implementation_difficulty == "High":
            risks['technical_risks'].append("Complex system implementation may face technical challenges")
        
        # Financial risks
        if strategy.expected_roi < 15:
            risks['financial_risks'].append("Low ROI may make financing difficult")
        
        # Operational risks
        if any(system.maintenance_interval_days < 30 for system in available_systems):
            risks['operational_risks'].append("Frequent maintenance requirements may affect operations")
        
        # Environmental risks
        if strategy.expected_emissions_avoided.get('co2_kg', 0) < 100:
            risks['environmental_risks'].append("Limited environmental impact may affect community support")
        
        # Overall risk assessment
        total_risks = sum(len(risk_list) for risk_list in risks.values() if isinstance(risk_list, list))
        if total_risks > 3:
            risks['overall_risk_level'] = 'High'
        elif total_risks > 1:
            risks['overall_risk_level'] = 'Medium'
        
        return risks
    
    def _create_implementation_roadmap(
        self,
        strategy: OptimizationStrategy,
        community: Community,
        available_systems: List[ConversionSystem]
    ) -> List[Dict[str, Any]]:
        """Create implementation roadmap for the strategy."""
        
        roadmap = []
        
        # Phase 1: Planning and Preparation
        roadmap.append({
            'phase': 'Planning and Preparation',
            'duration': '1-2 months',
            'activities': [
                'Conduct detailed feasibility study',
                'Secure funding and permits',
                'Select and train technical team',
                'Prepare site for system installation'
            ],
            'milestones': ['Feasibility study completed', 'Funding secured', 'Team trained']
        })
        
        # Phase 2: System Installation
        roadmap.append({
            'phase': 'System Installation',
            'duration': '2-4 months',
            'activities': [
                'Install conversion systems',
                'Connect to energy distribution network',
                'Install monitoring and control systems',
                'Conduct system testing'
            ],
            'milestones': ['Systems installed', 'Network connected', 'Testing completed']
        })
        
        # Phase 3: Commissioning and Training
        roadmap.append({
            'phase': 'Commissioning and Training',
            'duration': '1 month',
            'activities': [
                'Commission all systems',
                'Train community operators',
                'Develop operational procedures',
                'Begin pilot operations'
            ],
            'milestones': ['Systems commissioned', 'Operators trained', 'Pilot operations started']
        })
        
        # Phase 4: Full Operation
        roadmap.append({
            'phase': 'Full Operation',
            'duration': 'Ongoing',
            'activities': [
                'Monitor system performance',
                'Optimize operations based on data',
                'Expand system if successful',
                'Share lessons learned with other communities'
            ],
            'milestones': ['Full operation achieved', 'Performance optimized', 'Expansion planned']
        })
        
        return roadmap


def create_optimization_report(
    optimization_result: OptimizationResult,
    community: Community
) -> str:
    """Create a comprehensive optimization report."""
    
    report = f"""
# 🎯 Waste-to-Energy Optimization Report for {community.name}

## 📋 Executive Summary
**Recommended Strategy:** {optimization_result.best_strategy.strategy_name}
**Confidence Score:** {optimization_result.best_strategy.confidence_score:.1%}
**Expected ROI:** {optimization_result.best_strategy.expected_roi:.1f}%
**Implementation Difficulty:** {optimization_result.best_strategy.implementation_difficulty}

## 🎯 Recommended Strategy
**{optimization_result.best_strategy.strategy_name}**
{optimization_result.best_strategy.description}

### Key Metrics:
- **Expected Energy Output:** {optimization_result.best_strategy.expected_energy_output:.1f} kWh
- **Expected Cost:** ${optimization_result.best_strategy.expected_cost:.2f}
- **CO₂ Avoided:** {optimization_result.best_strategy.expected_emissions_avoided.get('co2_kg', 0):.1f} kg
- **Time to Implement:** {optimization_result.best_strategy.time_to_implement}

## 📊 Impact Assessment
**Overall Impact Score:** {optimization_result.impact_assessment.overall_score:.1f}/100 ({optimization_result.impact_assessment.impact_category})

### Environmental Impact:
- CO₂ Avoided: {optimization_result.impact_assessment.environmental.co2_avoided_kg:.1f} kg
- Trees Equivalent: {optimization_result.impact_assessment.environmental.trees_equivalent} trees
- Renewable Energy: {optimization_result.impact_assessment.environmental.renewable_energy_kwh:.1f} kWh

### Economic Impact:
- Net Savings: ${optimization_result.impact_assessment.economic.net_savings_usd:.2f}
- ROI: {optimization_result.impact_assessment.economic.roi_percent:.1f}%
- Payback Period: {optimization_result.impact_assessment.economic.payback_period_years:.1f} years

### Social Impact:
- Households Served: {optimization_result.impact_assessment.social.households_served}
- Jobs Created: {optimization_result.impact_assessment.social.jobs_created}
- Community Empowerment Score: {optimization_result.impact_assessment.social.community_empowerment_score:.1f}/100

## 🔄 Alternative Strategies
"""
    
    for i, alt_strategy in enumerate(optimization_result.alternative_strategies, 1):
        report += f"""
### Alternative {i}: {alt_strategy.strategy_name}
- **Confidence Score:** {alt_strategy.confidence_score:.1%}
- **Expected ROI:** {alt_strategy.expected_roi:.1f}%
- **Implementation Difficulty:** {alt_strategy.implementation_difficulty}
"""
    
    report += f"""
## 💡 Recommendations
"""
    for rec in optimization_result.recommendations:
        report += f"- {rec}\n"
    
    report += f"""
## ⚠️ Risk Assessment
**Overall Risk Level:** {optimization_result.risk_assessment['overall_risk_level']}

### Technical Risks:
"""
    for risk in optimization_result.risk_assessment.get('technical_risks', []):
        report += f"- {risk}\n"
    
    report += f"""
### Financial Risks:
"""
    for risk in optimization_result.risk_assessment.get('financial_risks', []):
        report += f"- {risk}\n"
    
    report += f"""
## 🗺️ Implementation Roadmap
"""
    for phase in optimization_result.implementation_roadmap:
        report += f"""
### {phase['phase']} ({phase['duration']})
**Activities:**
"""
        for activity in phase['activities']:
            report += f"- {activity}\n"
        
        report += f"""
**Milestones:**
"""
        for milestone in phase['milestones']:
            report += f"- {milestone}\n"
    
    return report
