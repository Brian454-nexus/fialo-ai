"""
Impact calculation utilities for the AI Community Waste-to-Energy Optimizer.
Calculates environmental, economic, and social impact metrics.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from models.waste_types import WasteType, WASTE_TYPES
from models.community import Community
from models.conversion_system import ConversionResult


@dataclass
class EnvironmentalImpact:
    """Environmental impact metrics."""
    co2_avoided_kg: float
    methane_avoided_kg: float
    co2_equivalent_kg: float
    trees_equivalent: int
    cars_equivalent: float
    renewable_energy_kwh: float
    fossil_fuel_displaced_liters: float


@dataclass
class EconomicImpact:
    """Economic impact metrics."""
    total_cost_usd: float
    energy_savings_usd: float
    waste_disposal_savings_usd: float
    net_savings_usd: float
    cost_per_kwh: float
    payback_period_years: float
    roi_percent: float


@dataclass
class SocialImpact:
    """Social impact metrics."""
    households_served: int
    energy_access_improvement_percent: float
    jobs_created: int
    health_benefits_score: float
    community_empowerment_score: float


@dataclass
class ComprehensiveImpact:
    """Comprehensive impact assessment."""
    environmental: EnvironmentalImpact
    economic: EconomicImpact
    social: SocialImpact
    overall_score: float
    impact_category: str


class ImpactCalculator:
    """Calculator for comprehensive impact assessment."""
    
    def __init__(self):
        # Conversion factors
        self.co2_per_tree_kg = 22  # kg CO₂ sequestered per tree per year
        self.co2_per_car_kg = 4000  # kg CO₂ per car per year
        self.methane_gwp = 25  # Global Warming Potential of methane
        self.fossil_fuel_co2_per_liter = 2.3  # kg CO₂ per liter of fossil fuel
        self.energy_per_liter_fossil_fuel = 9.7  # kWh per liter of fossil fuel
        
        # Economic factors
        self.grid_energy_cost_per_kwh = 0.15  # USD per kWh
        self.waste_disposal_cost_per_kg = 0.05  # USD per kg
        self.health_cost_per_ton_co2 = 50  # USD health cost per ton CO₂
        
        # Social factors
        self.energy_access_improvement_per_kwh = 0.1  # % improvement per kWh
        self.jobs_per_mw = 5  # Jobs created per MW of renewable energy
        self.health_benefit_per_ton_co2 = 0.8  # Health benefit score per ton CO₂ avoided
    
    def calculate_environmental_impact(
        self,
        conversion_results: List[ConversionResult],
        time_period_days: int = 30
    ) -> EnvironmentalImpact:
        """
        Calculate environmental impact from waste-to-energy conversion.
        
        Args:
            conversion_results: List of conversion results
            time_period_days: Time period for calculation
        
        Returns:
            Environmental impact metrics
        """
        total_co2_avoided = 0.0
        total_methane_avoided = 0.0
        total_energy_generated = 0.0
        
        for result in conversion_results:
            total_co2_avoided += abs(result.co2_emissions_kg)
            total_methane_avoided += abs(result.methane_emissions_kg)
            total_energy_generated += result.energy_output_kwh
        
        # Calculate CO₂ equivalent (including methane)
        co2_equivalent = total_co2_avoided + (total_methane_avoided * self.methane_gwp)
        
        # Calculate equivalents
        trees_equivalent = int(co2_equivalent / self.co2_per_tree_kg)
        cars_equivalent = co2_equivalent / self.co2_per_car_kg
        
        # Calculate fossil fuel displacement
        fossil_fuel_displaced = total_energy_generated / self.energy_per_liter_fossil_fuel
        
        return EnvironmentalImpact(
            co2_avoided_kg=total_co2_avoided,
            methane_avoided_kg=total_methane_avoided,
            co2_equivalent_kg=co2_equivalent,
            trees_equivalent=trees_equivalent,
            cars_equivalent=cars_equivalent,
            renewable_energy_kwh=total_energy_generated,
            fossil_fuel_displaced_liters=fossil_fuel_displaced
        )
    
    def calculate_economic_impact(
        self,
        conversion_results: List[ConversionResult],
        community: Community,
        system_costs: List[float],
        time_period_days: int = 30
    ) -> EconomicImpact:
        """
        Calculate economic impact from waste-to-energy conversion.
        
        Args:
            conversion_results: List of conversion results
            community: Community being served
            system_costs: List of system capital costs
            time_period_days: Time period for calculation
        
        Returns:
            Economic impact metrics
        """
        total_cost = sum(result.cost_usd for result in conversion_results)
        total_energy = sum(result.energy_output_kwh for result in conversion_results)
        total_waste = sum(sum(result.waste_input_kg.values()) for result in conversion_results)
        
        # Calculate savings
        energy_savings = total_energy * community.energy_cost_per_kwh
        waste_disposal_savings = total_waste * community.waste_disposal_cost_per_kg
        net_savings = energy_savings + waste_disposal_savings - total_cost
        
        # Calculate cost metrics
        cost_per_kwh = total_cost / total_energy if total_energy > 0 else 0
        
        # Calculate ROI and payback period
        total_system_cost = sum(system_costs)
        annual_savings = net_savings * (365 / time_period_days)
        payback_period = total_system_cost / annual_savings if annual_savings > 0 else float('inf')
        roi_percent = (annual_savings / total_system_cost * 100) if total_system_cost > 0 else 0
        
        return EconomicImpact(
            total_cost_usd=total_cost,
            energy_savings_usd=energy_savings,
            waste_disposal_savings_usd=waste_disposal_savings,
            net_savings_usd=net_savings,
            cost_per_kwh=cost_per_kwh,
            payback_period_years=payback_period,
            roi_percent=roi_percent
        )
    
    def calculate_social_impact(
        self,
        conversion_results: List[ConversionResult],
        community: Community,
        time_period_days: int = 30
    ) -> SocialImpact:
        """
        Calculate social impact from waste-to-energy conversion.
        
        Args:
            conversion_results: List of conversion results
            community: Community being served
            time_period_days: Time period for calculation
        
        Returns:
            Social impact metrics
        """
        total_energy = sum(result.energy_output_kwh for result in conversion_results)
        total_co2_avoided = sum(abs(result.co2_emissions_kg) for result in conversion_results)
        
        # Calculate households served
        daily_energy_per_household = community.daily_energy_demand_kwh / community.households
        households_served = int(total_energy / (daily_energy_per_household * time_period_days))
        
        # Calculate energy access improvement
        energy_access_improvement = min(100, total_energy * self.energy_access_improvement_per_kwh)
        
        # Calculate jobs created
        system_capacity_mw = total_energy / (time_period_days * 24) / 1000  # Convert to MW
        jobs_created = int(system_capacity_mw * self.jobs_per_mw)
        
        # Calculate health benefits
        co2_avoided_tons = total_co2_avoided / 1000
        health_benefits = co2_avoided_tons * self.health_benefit_per_ton_co2
        
        # Calculate community empowerment score
        energy_independence = min(100, (total_energy / (community.daily_energy_demand_kwh * time_period_days)) * 100)
        community_empowerment = (energy_independence + health_benefits) / 2
        
        return SocialImpact(
            households_served=households_served,
            energy_access_improvement_percent=energy_access_improvement,
            jobs_created=jobs_created,
            health_benefits_score=health_benefits,
            community_empowerment_score=community_empowerment
        )
    
    def calculate_comprehensive_impact(
        self,
        conversion_results: List[ConversionResult],
        community: Community,
        system_costs: List[float],
        time_period_days: int = 30
    ) -> ComprehensiveImpact:
        """
        Calculate comprehensive impact assessment.
        
        Args:
            conversion_results: List of conversion results
            community: Community being served
            system_costs: List of system capital costs
            time_period_days: Time period for calculation
        
        Returns:
            Comprehensive impact assessment
        """
        # Calculate individual impact components
        environmental = self.calculate_environmental_impact(conversion_results, time_period_days)
        economic = self.calculate_economic_impact(conversion_results, community, system_costs, time_period_days)
        social = self.calculate_social_impact(conversion_results, community, time_period_days)
        
        # Calculate overall score (weighted average)
        env_score = min(100, (environmental.co2_equivalent_kg / 1000) * 10)  # Scale to 0-100
        econ_score = min(100, max(0, economic.roi_percent))  # ROI as percentage
        social_score = min(100, social.community_empowerment_score)
        
        overall_score = (env_score * 0.4 + econ_score * 0.3 + social_score * 0.3)
        
        # Determine impact category
        if overall_score >= 80:
            impact_category = "Excellent"
        elif overall_score >= 60:
            impact_category = "Good"
        elif overall_score >= 40:
            impact_category = "Moderate"
        else:
            impact_category = "Needs Improvement"
        
        return ComprehensiveImpact(
            environmental=environmental,
            economic=economic,
            social=social,
            overall_score=overall_score,
            impact_category=impact_category
        )
    
    def calculate_scenario_impact(
        self,
        base_scenario: List[ConversionResult],
        improved_scenario: List[ConversionResult],
        community: Community,
        system_costs: List[float]
    ) -> Dict[str, float]:
        """
        Calculate impact difference between two scenarios.
        
        Args:
            base_scenario: Base scenario results
            improved_scenario: Improved scenario results
            community: Community being served
            system_costs: System costs
        
        Returns:
            Dictionary with impact differences
        """
        base_impact = self.calculate_comprehensive_impact(base_scenario, community, system_costs)
        improved_impact = self.calculate_comprehensive_impact(improved_scenario, community, system_costs)
        
        return {
            'co2_improvement_kg': improved_impact.environmental.co2_avoided_kg - base_impact.environmental.co2_avoided_kg,
            'energy_improvement_kwh': improved_impact.environmental.renewable_energy_kwh - base_impact.environmental.renewable_energy_kwh,
            'cost_improvement_usd': improved_impact.economic.net_savings_usd - base_impact.economic.net_savings_usd,
            'roi_improvement_percent': improved_impact.economic.roi_percent - base_impact.economic.roi_percent,
            'overall_score_improvement': improved_impact.overall_score - base_impact.overall_score
        }
    
    def generate_impact_report(
        self,
        impact: ComprehensiveImpact,
        community: Community,
        time_period_days: int = 30
    ) -> str:
        """
        Generate a human-readable impact report.
        
        Args:
            impact: Comprehensive impact assessment
            community: Community being served
            time_period_days: Time period for calculation
        
        Returns:
            Formatted impact report
        """
        report = f"""
# 🌱 Impact Assessment Report for {community.name}

## 📊 Overall Assessment
**Impact Score:** {impact.overall_score:.1f}/100 ({impact.impact_category})
**Assessment Period:** {time_period_days} days

## 🌍 Environmental Impact
- **CO₂ Avoided:** {impact.environmental.co2_avoided_kg:.1f} kg
- **Methane Avoided:** {impact.environmental.methane_avoided_kg:.1f} kg
- **CO₂ Equivalent:** {impact.environmental.co2_equivalent_kg:.1f} kg
- **Trees Equivalent:** {impact.environmental.trees_equivalent} trees
- **Cars Equivalent:** {impact.environmental.cars_equivalent:.1f} cars
- **Renewable Energy:** {impact.environmental.renewable_energy_kwh:.1f} kWh
- **Fossil Fuel Displaced:** {impact.environmental.fossil_fuel_displaced_liters:.1f} liters

## 💰 Economic Impact
- **Total Cost:** ${impact.economic.total_cost_usd:.2f}
- **Energy Savings:** ${impact.economic.energy_savings_usd:.2f}
- **Waste Disposal Savings:** ${impact.economic.waste_disposal_savings_usd:.2f}
- **Net Savings:** ${impact.economic.net_savings_usd:.2f}
- **Cost per kWh:** ${impact.economic.cost_per_kwh:.3f}
- **Payback Period:** {impact.economic.payback_period_years:.1f} years
- **ROI:** {impact.economic.roi_percent:.1f}%

## 👥 Social Impact
- **Households Served:** {impact.social.households_served}
- **Energy Access Improvement:** {impact.social.energy_access_improvement_percent:.1f}%
- **Jobs Created:** {impact.social.jobs_created}
- **Health Benefits Score:** {impact.social.health_benefits_score:.1f}/100
- **Community Empowerment Score:** {impact.social.community_empowerment_score:.1f}/100

## 🎯 Key Achievements
- Converted waste into {impact.environmental.renewable_energy_kwh:.1f} kWh of renewable energy
- Avoided {impact.environmental.co2_equivalent_kg:.1f} kg of CO₂ equivalent emissions
- Achieved {impact.economic.roi_percent:.1f}% return on investment
- Improved energy access for {impact.social.households_served} households
- Created {impact.social.jobs_created} local jobs

## 📈 Recommendations
Based on the impact assessment, the waste-to-energy system shows {'excellent' if impact.overall_score >= 80 else 'good' if impact.overall_score >= 60 else 'moderate'} performance. 
{'Consider scaling up the system to serve more households.' if impact.overall_score >= 80 else 'Focus on improving efficiency and reducing costs.' if impact.overall_score >= 60 else 'Review system design and operational parameters.'}
        """
        
        return report


def calculate_community_wide_impact(
    communities: List[Community],
    conversion_results_by_community: Dict[str, List[ConversionResult]],
    system_costs: List[float]
) -> Dict[str, ComprehensiveImpact]:
    """
    Calculate impact for multiple communities.
    
    Args:
        communities: List of communities
        conversion_results_by_community: Conversion results by community
        system_costs: System costs
    
    Returns:
        Dictionary with impact assessments by community
    """
    calculator = ImpactCalculator()
    impacts = {}
    
    for community in communities:
        if community.name in conversion_results_by_community:
            impact = calculator.calculate_comprehensive_impact(
                conversion_results_by_community[community.name],
                community,
                system_costs
            )
            impacts[community.name] = impact
    
    return impacts


def generate_comparative_impact_analysis(
    scenario_impacts: Dict[str, ComprehensiveImpact]
) -> pd.DataFrame:
    """
    Generate comparative analysis of multiple scenarios.
    
    Args:
        scenario_impacts: Dictionary of scenario impacts
    
    Returns:
        DataFrame with comparative analysis
    """
    data = []
    
    for scenario_name, impact in scenario_impacts.items():
        data.append({
            'Scenario': scenario_name,
            'Overall Score': impact.overall_score,
            'Impact Category': impact.impact_category,
            'CO₂ Avoided (kg)': impact.environmental.co2_avoided_kg,
            'Energy Generated (kWh)': impact.environmental.renewable_energy_kwh,
            'Net Savings (USD)': impact.economic.net_savings_usd,
            'ROI (%)': impact.economic.roi_percent,
            'Households Served': impact.social.households_served,
            'Jobs Created': impact.social.jobs_created
        })
    
    return pd.DataFrame(data)
