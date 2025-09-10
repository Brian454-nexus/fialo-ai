"""
Sample data for the AI Community Waste-to-Energy Optimizer.
Provides realistic data for demonstration and testing purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

# Sample waste generation data for different community types
SAMPLE_WASTE_DATA = {
    'rural_village': {
        'food_scraps': 120,  # kg/day
        'market_waste': 80,
        'agricultural_biomass': 200,
        'animal_waste': 50,
        'wood_biomass': 30
    },
    'urban_neighborhood': {
        'food_scraps': 300,
        'market_waste': 150,
        'agricultural_biomass': 50,
        'animal_waste': 20,
        'wood_biomass': 40
    },
    'market_area': {
        'food_scraps': 500,
        'market_waste': 800,
        'agricultural_biomass': 100,
        'animal_waste': 30,
        'wood_biomass': 20
    }
}

# Sample energy demand patterns
SAMPLE_ENERGY_DEMAND = {
    'rural_village': {
        'daily_demand_kwh': 120,
        'peak_demand_kwh': 25,
        'base_demand_kwh': 5
    },
    'urban_neighborhood': {
        'daily_demand_kwh': 400,
        'peak_demand_kwh': 80,
        'base_demand_kwh': 20
    },
    'market_area': {
        'daily_demand_kwh': 800,
        'peak_demand_kwh': 120,
        'base_demand_kwh': 30
    }
}

# Sample environmental conditions
SAMPLE_ENVIRONMENTAL_CONDITIONS = {
    'dry_season': {
        'temperature_c': 28,
        'humidity_percent': 45,
        'rainfall_mm': 0
    },
    'wet_season': {
        'temperature_c': 22,
        'humidity_percent': 80,
        'rainfall_mm': 15
    },
    'harvest_season': {
        'temperature_c': 25,
        'humidity_percent': 60,
        'rainfall_mm': 5
    }
}

# Sample conversion system specifications
SAMPLE_CONVERSION_SYSTEMS = [
    {
        'name': 'Biogas Digester - Small',
        'system_type': 'biogas_digestion',
        'capacity_kg_per_day': 500,
        'efficiency': 0.65,
        'operational_cost_per_day': 15.0,
        'capital_cost': 5000.0,
        'maintenance_interval_days': 30
    },
    {
        'name': 'Biogas Digester - Large',
        'system_type': 'biogas_digestion',
        'capacity_kg_per_day': 2000,
        'efficiency': 0.70,
        'operational_cost_per_day': 45.0,
        'capital_cost': 15000.0,
        'maintenance_interval_days': 30
    },
    {
        'name': 'Anaerobic Digester',
        'system_type': 'anaerobic_digestion',
        'capacity_kg_per_day': 1000,
        'efficiency': 0.75,
        'operational_cost_per_day': 30.0,
        'capital_cost': 12000.0,
        'maintenance_interval_days': 45
    },
    {
        'name': 'Incineration Unit',
        'system_type': 'incineration',
        'capacity_kg_per_day': 800,
        'efficiency': 0.60,
        'operational_cost_per_day': 25.0,
        'capital_cost': 8000.0,
        'maintenance_interval_days': 15
    }
]

# Sample community profiles
SAMPLE_COMMUNITIES = [
    {
        'name': 'Kibera Market Area',
        'community_type': 'market_area',
        'population': 5000,
        'households': 1200,
        'latitude': -1.2921,
        'longitude': 36.8219,
        'daily_energy_demand_kwh': 800,
        'daily_waste_generation_kg': 2500,
        'energy_cost_per_kwh': 0.20,
        'waste_disposal_cost_per_kg': 0.08
    },
    {
        'name': 'Rural Village - Kisumu',
        'community_type': 'rural_village',
        'population': 800,
        'households': 150,
        'latitude': -0.0917,
        'longitude': 34.7680,
        'daily_energy_demand_kwh': 120,
        'daily_waste_generation_kg': 400,
        'energy_cost_per_kwh': 0.25,
        'waste_disposal_cost_per_kg': 0.03
    },
    {
        'name': 'Mini-Grid Community - Nakuru',
        'community_type': 'mini_grid',
        'population': 2000,
        'households': 400,
        'latitude': -0.3031,
        'longitude': 36.0800,
        'daily_energy_demand_kwh': 300,
        'daily_waste_generation_kg': 800,
        'energy_cost_per_kwh': 0.18,
        'waste_disposal_cost_per_kg': 0.06
    }
]

# Sample optimization scenarios
SAMPLE_OPTIMIZATION_SCENARIOS = {
    'conservative': {
        'description': 'Conservative approach with low risk and moderate returns',
        'optimization_goals': {
            'energy_output': 0.3,
            'cost_efficiency': 0.4,
            'emissions_reduction': 0.2,
            'social_impact': 0.1
        },
        'constraints': {
            'max_cost_usd': 5000,
            'min_energy_output_kwh': 50,
            'max_processing_time_hours': 12
        }
    },
    'aggressive': {
        'description': 'Aggressive approach maximizing energy output',
        'optimization_goals': {
            'energy_output': 0.5,
            'cost_efficiency': 0.2,
            'emissions_reduction': 0.2,
            'social_impact': 0.1
        },
        'constraints': {
            'max_cost_usd': 15000,
            'min_energy_output_kwh': 200,
            'max_processing_time_hours': 24
        }
    },
    'balanced': {
        'description': 'Balanced approach considering all factors equally',
        'optimization_goals': {
            'energy_output': 0.25,
            'cost_efficiency': 0.25,
            'emissions_reduction': 0.25,
            'social_impact': 0.25
        },
        'constraints': {
            'max_cost_usd': 10000,
            'min_energy_output_kwh': 100,
            'max_processing_time_hours': 18
        }
    }
}

# Sample impact metrics
SAMPLE_IMPACT_METRICS = {
    'environmental': {
        'co2_avoided_kg': 1500,
        'methane_avoided_kg': 200,
        'trees_equivalent': 68,
        'cars_equivalent': 0.375,
        'renewable_energy_kwh': 2500
    },
    'economic': {
        'total_cost_usd': 2500,
        'energy_savings_usd': 375,
        'waste_disposal_savings_usd': 125,
        'net_savings_usd': -2000,
        'roi_percent': 15.0,
        'payback_period_years': 6.7
    },
    'social': {
        'households_served': 150,
        'energy_access_improvement_percent': 25,
        'jobs_created': 3,
        'health_benefits_score': 75,
        'community_empowerment_score': 80
    }
}

# Sample time series data for visualization
def generate_sample_time_series_data(days: int = 7) -> pd.DataFrame:
    """Generate sample time series data for visualization."""
    
    start_date = datetime.now() - timedelta(days=days)
    timestamps = [start_date + timedelta(hours=i) for i in range(days * 24)]
    
    data = []
    for i, timestamp in enumerate(timestamps):
        # Simulate daily patterns
        hour = timestamp.hour
        day_factor = 1.0 + 0.2 * np.sin(2 * np.pi * i / (24 * 7))  # Weekly cycle
        
        # Energy generation (peaks during day)
        energy_factor = 0.3 + 0.7 * max(0, np.sin(np.pi * (hour - 6) / 12))
        energy_generated = 50 * energy_factor * day_factor
        
        # Energy demand (peaks morning and evening)
        demand_factor = 0.4 + 0.6 * (0.5 + 0.5 * np.cos(2 * np.pi * (hour - 12) / 24))
        energy_demand = 80 * demand_factor * day_factor
        
        # Waste generation (varies by hour)
        waste_factor = 0.2 + 0.8 * max(0, np.sin(np.pi * (hour - 8) / 16))
        waste_generated = 100 * waste_factor * day_factor
        
        # CO₂ avoided (proportional to energy generated)
        co2_avoided = energy_generated * 0.6  # 0.6 kg CO₂ per kWh
        
        data.append({
            'timestamp': timestamp,
            'energy_generated_kwh': energy_generated,
            'energy_demand_kwh': energy_demand,
            'waste_generated_kg': waste_generated,
            'co2_avoided_kg': co2_avoided,
            'battery_charge_kwh': min(100, max(0, 50 + 20 * np.sin(2 * np.pi * i / 24))),
            'system_efficiency': 0.65 + 0.1 * np.sin(2 * np.pi * i / (24 * 3)),
            'cost_usd': 25 + 10 * np.sin(2 * np.pi * i / (24 * 2))
        })
    
    return pd.DataFrame(data)

# Sample optimization results
SAMPLE_OPTIMIZATION_RESULTS = {
    'max_energy_strategy': {
        'strategy_name': 'Maximum Energy Output',
        'expected_energy_output': 1200,
        'expected_cost': 8000,
        'expected_roi': 18.5,
        'confidence_score': 0.85,
        'implementation_difficulty': 'Medium',
        'time_to_implement': '1-3 months'
    },
    'cost_optimized_strategy': {
        'strategy_name': 'Cost-Optimized',
        'expected_energy_output': 800,
        'expected_cost': 4000,
        'expected_roi': 25.0,
        'confidence_score': 0.80,
        'implementation_difficulty': 'Low',
        'time_to_implement': 'Immediate'
    },
    'ai_optimized_strategy': {
        'strategy_name': 'AI-Optimized',
        'expected_energy_output': 1000,
        'expected_cost': 6000,
        'expected_roi': 22.0,
        'confidence_score': 0.90,
        'implementation_difficulty': 'High',
        'time_to_implement': '3-6 months'
    }
}

# Sample recommendations
SAMPLE_RECOMMENDATIONS = [
    "Consider increasing waste collection during peak generation hours (8-10 AM and 6-8 PM)",
    "Install energy storage systems to manage demand fluctuations",
    "Train community members on system operation and maintenance",
    "Explore partnerships with neighboring communities for shared resources",
    "Implement real-time monitoring for optimal system performance",
    "Consider carbon credit opportunities for additional revenue",
    "Develop contingency plans for system maintenance and downtime",
    "Establish community feedback mechanisms for continuous improvement"
]

# Sample risk assessments
SAMPLE_RISK_ASSESSMENTS = {
    'technical_risks': [
        "System efficiency may vary with seasonal temperature changes",
        "Waste composition variations could affect conversion efficiency",
        "Equipment maintenance requirements may be higher than expected"
    ],
    'financial_risks': [
        "Initial capital investment may exceed budget estimates",
        "Energy prices could fluctuate affecting ROI calculations",
        "Maintenance costs may be higher than projected"
    ],
    'operational_risks': [
        "Community acceptance and participation may be lower than expected",
        "Waste collection consistency could be affected by weather",
        "Technical expertise may be limited in rural areas"
    ],
    'environmental_risks': [
        "System emissions may be higher than predicted",
        "Waste processing could create local environmental concerns",
        "Water usage for some systems may be significant"
    ]
}

# Sample implementation roadmap
SAMPLE_IMPLEMENTATION_ROADMAP = [
    {
        'phase': 'Planning and Preparation',
        'duration': '1-2 months',
        'activities': [
            'Conduct detailed feasibility study',
            'Secure funding and permits',
            'Select and train technical team',
            'Prepare site for system installation'
        ],
        'milestones': ['Feasibility study completed', 'Funding secured', 'Team trained'],
        'cost_estimate': 5000
    },
    {
        'phase': 'System Installation',
        'duration': '2-4 months',
        'activities': [
            'Install conversion systems',
            'Connect to energy distribution network',
            'Install monitoring and control systems',
            'Conduct system testing'
        ],
        'milestones': ['Systems installed', 'Network connected', 'Testing completed'],
        'cost_estimate': 15000
    },
    {
        'phase': 'Commissioning and Training',
        'duration': '1 month',
        'activities': [
            'Commission all systems',
            'Train community operators',
            'Develop operational procedures',
            'Begin pilot operations'
        ],
        'milestones': ['Systems commissioned', 'Operators trained', 'Pilot operations started'],
        'cost_estimate': 3000
    },
    {
        'phase': 'Full Operation',
        'duration': 'Ongoing',
        'activities': [
            'Monitor system performance',
            'Optimize operations based on data',
            'Expand system if successful',
            'Share lessons learned with other communities'
        ],
        'milestones': ['Full operation achieved', 'Performance optimized', 'Expansion planned'],
        'cost_estimate': 2000
    }
]

# Export all sample data
def get_all_sample_data() -> Dict:
    """Get all sample data in a single dictionary."""
    return {
        'waste_data': SAMPLE_WASTE_DATA,
        'energy_demand': SAMPLE_ENERGY_DEMAND,
        'environmental_conditions': SAMPLE_ENVIRONMENTAL_CONDITIONS,
        'conversion_systems': SAMPLE_CONVERSION_SYSTEMS,
        'communities': SAMPLE_COMMUNITIES,
        'optimization_scenarios': SAMPLE_OPTIMIZATION_SCENARIOS,
        'impact_metrics': SAMPLE_IMPACT_METRICS,
        'optimization_results': SAMPLE_OPTIMIZATION_RESULTS,
        'recommendations': SAMPLE_RECOMMENDATIONS,
        'risk_assessments': SAMPLE_RISK_ASSESSMENTS,
        'implementation_roadmap': SAMPLE_IMPLEMENTATION_ROADMAP
    }
