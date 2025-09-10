"""
FastAPI-based REST API for the AI Community Waste-to-Energy Optimizer.
Provides clean endpoints for frontend integration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.waste_types import WASTE_TYPES, ConversionMethod
from models.community import create_sample_communities, Community
from models.conversion_system import create_sample_conversion_systems
from simulation.waste_simulator import create_sample_waste_scenario
from simulation.energy_simulator import create_complete_energy_simulation
from utils.impact_calculator import ImpactCalculator
from optimization.strategy_optimizer import StrategyOptimizer

# Initialize FastAPI app
app = FastAPI(
    title="♻️ Fialo AI - Personal Waste-to-Energy Optimizer API",
    description="API for optimizing waste-to-energy conversion strategies for individual users and waste companies in Africa",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
impact_calculator = ImpactCalculator()
strategy_optimizer = StrategyOptimizer()

# Pydantic models for API requests/responses
class IndividualUserRequest(BaseModel):
    user_type: str = "individual"
    location: str
    waste_types: Dict[str, float]  # waste_type -> amount_kg_per_day
    daily_energy_needs_kwh: float
    current_energy_cost_per_kwh: float = 0.15

class WasteCompanyRequest(BaseModel):
    user_type: str = "company"
    company_name: str
    location: str
    waste_types: Dict[str, float]  # waste_type -> amount_kg_per_day
    current_processing_method: str
    current_operational_cost_per_day: float = 0.0

class PersonalSimulationRequest(BaseModel):
    user_type: str  # "individual" or "company"
    user_data: Dict[str, Any]  # IndividualUserRequest or WasteCompanyRequest data
    simulation_days: int = 7
    temperature_c: float = 25.0
    humidity_percent: float = 60.0
    rainfall_mm: float = 0.0
    include_noise: bool = True

class PersonalOptimizationRequest(BaseModel):
    user_type: str  # "individual" or "company"
    user_data: Dict[str, Any]  # IndividualUserRequest or WasteCompanyRequest data
    optimization_goals: Optional[Dict[str, float]] = None
    constraints: Optional[Dict[str, Any]] = None
    time_horizon_days: int = 30

class EnergyPredictionRequest(BaseModel):
    waste_input: Dict[str, float]
    conversion_method: str
    environmental_conditions: Optional[Dict[str, float]] = None

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "♻️ Fialo AI - Personal Waste-to-Energy Optimizer API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "user_types": "/api/user-types",
            "personal_simulation": "/api/simulate-personal",
            "waste_types": "/api/waste-types",
            "conversion_systems": "/api/conversion-systems",
            "prediction": "/api/predict-energy",
            "impact": "/api/impact"
        }
    }

@app.get("/api/user-types")
async def get_user_types():
    """Get available user types and their characteristics."""
    return {
        "user_types": [
            {
                "type": "individual",
                "name": "Individual User",
                "description": "Personal or household waste-to-energy conversion",
                "scale": "Small scale: 1-100 kg per day",
                "examples": ["Households", "Small businesses", "Farmers", "Students"],
                "icon": "👤"
            },
            {
                "type": "company",
                "name": "Waste Company",
                "description": "Business waste collection and processing optimization",
                "scale": "Large scale: 100+ kg per day",
                "examples": ["Waste collectors", "Recycling companies", "Municipal services", "NGOs"],
                "icon": "🏢"
            }
        ]
    }

@app.get("/api/communities")
async def get_communities():
    """Get all available communities (for reference/backward compatibility)."""
    communities = create_sample_communities()
    return {
        "communities": [
            {
                "id": f"community_{i}",
                "name": community.name,
                "type": community.community_type.value,
                "population": community.population,
                "households": community.households,
                "daily_energy_demand_kwh": community.daily_energy_demand_kwh,
                "daily_waste_generation_kg": community.daily_waste_generation_kg,
                "energy_cost_per_kwh": community.energy_cost_per_kwh,
                "waste_disposal_cost_per_kg": community.waste_disposal_cost_per_kg,
                "waste_composition": community.waste_composition
            }
            for i, community in enumerate(communities)
        ]
    }

@app.get("/api/waste-types")
async def get_waste_types():
    """Get all available waste types with their properties."""
    return {
        "waste_types": {
            name: {
                "name": waste_type.name,
                "category": waste_type.category.value,
                "energy_content_kwh_per_kg": waste_type.energy_content_kwh_per_kg,
                "methane_potential_m3_per_kg": waste_type.methane_potential_m3_per_kg,
                "moisture_content_percent": waste_type.moisture_content_percent,
                "carbon_content_percent": waste_type.carbon_content_percent,
                "conversion_efficiency": {
                    method.value: efficiency 
                    for method, efficiency in waste_type.conversion_efficiency.items()
                },
                "co2_emissions_kg_per_kg": waste_type.co2_emissions_kg_per_kg,
                "methane_emissions_kg_per_kg": waste_type.methane_emissions_kg_per_kg
            }
            for name, waste_type in WASTE_TYPES.items()
        }
    }

@app.get("/api/conversion-systems")
async def get_conversion_systems():
    """Get all available conversion systems."""
    systems = create_sample_conversion_systems()
    return {
        "conversion_systems": [
            {
                "name": system.name,
                "system_type": system.system_type.value,
                "capacity_kg_per_day": system.capacity_kg_per_day,
                "efficiency": system.efficiency,
                "operational_cost_per_day": system.operational_cost_per_day,
                "capital_cost": system.capital_cost,
                "maintenance_interval_days": system.maintenance_interval_days
            }
            for system in systems
        ]
    }

@app.post("/api/simulate-personal")
async def run_personal_simulation(request: PersonalSimulationRequest):
    """Run waste-to-energy simulation for individual users or waste companies."""
    try:
        systems = create_sample_conversion_systems()
        
        # Create a mock community based on user data
        if request.user_type == "individual":
            # For individual users, create a small-scale community
            from models.community import Community, CommunityType, EnergyUsePattern
            community = Community(
                name=f"Individual User - {request.user_data.get('location', 'Unknown')}",
                community_type=CommunityType.RURAL_VILLAGE,
                population=1,
                households=1,
                energy_use_pattern=EnergyUsePattern.RESIDENTIAL,
                daily_energy_demand_kwh=request.user_data.get('daily_energy_needs_kwh', 10),
                peak_demand_kwh=request.user_data.get('daily_energy_needs_kwh', 10) * 0.3,
                base_demand_kwh=request.user_data.get('daily_energy_needs_kwh', 10) * 0.1,
                daily_waste_generation_kg=sum(request.user_data.get('waste_types', {}).values()),
                waste_composition=request.user_data.get('waste_types', {}),
                latitude=0.0,
                longitude=0.0,
                climate_zone="tropical",
                energy_cost_per_kwh=request.user_data.get('current_energy_cost_per_kwh', 0.15)
            )
        else:  # company
            # For companies, create a larger-scale community
            from models.community import Community, CommunityType, EnergyUsePattern
            community = Community(
                name=f"Company - {request.user_data.get('company_name', 'Unknown')}",
                community_type=CommunityType.MARKET_AREA,
                population=100,
                households=20,
                energy_use_pattern=EnergyUsePattern.COMMERCIAL,
                daily_energy_demand_kwh=sum(request.user_data.get('waste_types', {}).values()) * 0.5,
                peak_demand_kwh=sum(request.user_data.get('waste_types', {}).values()) * 0.15,
                base_demand_kwh=sum(request.user_data.get('waste_types', {}).values()) * 0.05,
                daily_waste_generation_kg=sum(request.user_data.get('waste_types', {}).values()),
                waste_composition=request.user_data.get('waste_types', {}),
                latitude=0.0,
                longitude=0.0,
                climate_zone="tropical",
                energy_cost_per_kwh=0.15
            )
        
        # Run simulation
        waste_data = create_sample_waste_scenario(
            community,
            datetime.now(),
            request.simulation_days,
            request.include_noise
        )
        
        energy_results = create_complete_energy_simulation(
            waste_data,
            systems,
            [community],
            request.simulation_days
        )
        
        # Calculate key metrics
        total_waste_processed = waste_data['total_processed_kg'].sum()
        total_energy_generated = energy_results['conversion_results']['energy_output_kwh'].sum()
        total_co2_avoided = abs(energy_results['conversion_results']['co2_emissions_kg'].sum())
        total_cost = energy_results['conversion_results']['cost_usd'].sum()
        
        # Energy demand satisfaction
        distribution_data = energy_results['distribution_results'][community.name]
        avg_demand_met = distribution_data['demand_met_percent'].mean()
        
        # Calculate personal impact metrics
        if request.user_type == "individual":
            # Individual user metrics
            daily_energy = total_energy_generated / request.simulation_days
            daily_savings = daily_energy * request.user_data.get('current_energy_cost_per_kwh', 0.15)
            annual_savings = daily_savings * 365
            
            # Community multiplier effect
            community_multiplier = {
                "if_100_people": {
                    "waste_processed_kg": total_waste_processed * 100,
                    "energy_generated_kwh": total_energy_generated * 100,
                    "co2_avoided_kg": total_co2_avoided * 100,
                    "trees_equivalent": int((total_co2_avoided * 100) / 22)
                }
            }
        else:
            # Company metrics
            daily_revenue = total_energy_generated / request.simulation_days * 0.15
            annual_revenue = daily_revenue * 365
            community_multiplier = None
        
        return {
            "simulation_id": f"personal_sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_type": request.user_type,
            "user_data": request.user_data,
            "parameters": {
                "simulation_days": request.simulation_days,
                "temperature_c": request.temperature_c,
                "humidity_percent": request.humidity_percent,
                "rainfall_mm": request.rainfall_mm
            },
            "results": {
                "total_waste_processed_kg": float(total_waste_processed),
                "total_energy_generated_kwh": float(total_energy_generated),
                "total_co2_avoided_kg": float(total_co2_avoided),
                "total_cost_usd": float(total_cost),
                "avg_demand_met_percent": float(avg_demand_met),
                "daily_averages": {
                    "waste_processed_kg": float(total_waste_processed / request.simulation_days),
                    "energy_generated_kwh": float(total_energy_generated / request.simulation_days),
                    "co2_avoided_kg": float(total_co2_avoided / request.simulation_days),
                    "cost_usd": float(total_cost / request.simulation_days)
                }
            },
            "personal_impact": {
                "daily_energy_kwh": float(total_energy_generated / request.simulation_days),
                "daily_savings_usd": float(daily_savings) if request.user_type == "individual" else float(daily_revenue),
                "annual_savings_usd": float(annual_savings) if request.user_type == "individual" else float(annual_revenue),
                "trees_equivalent": int(total_co2_avoided / 22),
                "cars_equivalent": float(total_co2_avoided / 4000)
            },
            "community_multiplier": community_multiplier,
            "time_series_data": {
                "waste_data": waste_data.to_dict('records'),
                "energy_data": energy_results['conversion_results'].to_dict('records'),
                "distribution_data": distribution_data.to_dict('records')
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personal simulation failed: {str(e)}")

@app.post("/api/simulate")
async def run_simulation(request: SimulationRequest):
    """Run waste-to-energy simulation for a community."""
    try:
        communities = create_sample_communities()
        systems = create_sample_conversion_systems()
        
        # Find the requested community
        community = None
        for i, comm in enumerate(communities):
            if f"community_{i}" == request.community_id:
                community = comm
                break
        
        if not community:
            raise HTTPException(status_code=404, detail="Community not found")
        
        # Run simulation
        waste_data = create_sample_waste_scenario(
            community,
            datetime.now(),
            request.simulation_days,
            request.include_noise
        )
        
        energy_results = create_complete_energy_simulation(
            waste_data,
            systems,
            [community],
            request.simulation_days
        )
        
        # Calculate key metrics
        total_waste_processed = waste_data['total_processed_kg'].sum()
        total_energy_generated = energy_results['conversion_results']['energy_output_kwh'].sum()
        total_co2_avoided = abs(energy_results['conversion_results']['co2_emissions_kg'].sum())
        total_cost = energy_results['conversion_results']['cost_usd'].sum()
        
        # Energy demand satisfaction
        distribution_data = energy_results['distribution_results'][community.name]
        avg_demand_met = distribution_data['demand_met_percent'].mean()
        
        return {
            "simulation_id": f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "community": {
                "name": community.name,
                "type": community.community_type.value
            },
            "parameters": {
                "simulation_days": request.simulation_days,
                "temperature_c": request.temperature_c,
                "humidity_percent": request.humidity_percent,
                "rainfall_mm": request.rainfall_mm
            },
            "results": {
                "total_waste_processed_kg": float(total_waste_processed),
                "total_energy_generated_kwh": float(total_energy_generated),
                "total_co2_avoided_kg": float(total_co2_avoided),
                "total_cost_usd": float(total_cost),
                "avg_demand_met_percent": float(avg_demand_met),
                "daily_averages": {
                    "waste_processed_kg": float(total_waste_processed / request.simulation_days),
                    "energy_generated_kwh": float(total_energy_generated / request.simulation_days),
                    "co2_avoided_kg": float(total_co2_avoided / request.simulation_days),
                    "cost_usd": float(total_cost / request.simulation_days)
                }
            },
            "time_series_data": {
                "waste_data": waste_data.to_dict('records'),
                "energy_data": energy_results['conversion_results'].to_dict('records'),
                "distribution_data": distribution_data.to_dict('records')
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.post("/api/optimize")
async def optimize_strategy(request: OptimizationRequest):
    """Optimize waste-to-energy conversion strategy."""
    try:
        communities = create_sample_communities()
        systems = create_sample_conversion_systems()
        
        # Find the requested community
        community = None
        for i, comm in enumerate(communities):
            if f"community_{i}" == request.community_id:
                community = comm
                break
        
        if not community:
            raise HTTPException(status_code=404, detail="Community not found")
        
        # Run optimization
        optimization_result = strategy_optimizer.optimize_strategy(
            community=community,
            available_systems=systems,
            waste_available=request.waste_available,
            optimization_goals=request.optimization_goals,
            constraints=request.constraints,
            time_horizon_days=request.time_horizon_days
        )
        
        return {
            "optimization_id": f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "community": {
                "name": community.name,
                "type": community.community_type.value
            },
            "best_strategy": {
                "name": optimization_result.best_strategy.strategy_name,
                "description": optimization_result.best_strategy.description,
                "expected_energy_output_kwh": optimization_result.best_strategy.expected_energy_output,
                "expected_cost_usd": optimization_result.best_strategy.expected_cost,
                "expected_roi_percent": optimization_result.best_strategy.expected_roi,
                "confidence_score": optimization_result.best_strategy.confidence_score,
                "implementation_difficulty": optimization_result.best_strategy.implementation_difficulty,
                "time_to_implement": optimization_result.best_strategy.time_to_implement,
                "waste_allocation": optimization_result.best_strategy.waste_allocation,
                "system_selection": optimization_result.best_strategy.system_selection
            },
            "impact_assessment": {
                "overall_score": optimization_result.impact_assessment.overall_score,
                "impact_category": optimization_result.impact_assessment.impact_category,
                "environmental": {
                    "co2_avoided_kg": optimization_result.impact_assessment.environmental.co2_avoided_kg,
                    "methane_avoided_kg": optimization_result.impact_assessment.environmental.methane_avoided_kg,
                    "trees_equivalent": optimization_result.impact_assessment.environmental.trees_equivalent,
                    "renewable_energy_kwh": optimization_result.impact_assessment.environmental.renewable_energy_kwh
                },
                "economic": {
                    "net_savings_usd": optimization_result.impact_assessment.economic.net_savings_usd,
                    "roi_percent": optimization_result.impact_assessment.economic.roi_percent,
                    "payback_period_years": optimization_result.impact_assessment.economic.payback_period_years
                },
                "social": {
                    "households_served": optimization_result.impact_assessment.social.households_served,
                    "jobs_created": optimization_result.impact_assessment.social.jobs_created,
                    "community_empowerment_score": optimization_result.impact_assessment.social.community_empowerment_score
                }
            },
            "recommendations": optimization_result.recommendations,
            "risk_assessment": optimization_result.risk_assessment,
            "implementation_roadmap": optimization_result.implementation_roadmap
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.post("/api/predict-energy")
async def predict_energy(request: EnergyPredictionRequest):
    """Predict energy potential from waste input."""
    try:
        # Convert string to enum
        conversion_method = ConversionMethod(request.conversion_method)
        
        # Get prediction
        predictions = strategy_optimizer.prediction_engine.predict_energy_potential(
            waste_input=request.waste_input,
            conversion_method=conversion_method,
            environmental_conditions=request.environmental_conditions
        )
        
        return {
            "prediction_id": f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "waste_input": request.waste_input,
            "conversion_method": request.conversion_method,
            "predictions": predictions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/api/impact/{simulation_id}")
async def get_impact_assessment(simulation_id: str):
    """Get detailed impact assessment for a simulation."""
    # This would typically fetch from a database
    # For now, return a sample response
    return {
        "simulation_id": simulation_id,
        "impact_assessment": {
            "environmental": {
                "co2_avoided_kg": 1500.0,
                "methane_avoided_kg": 200.0,
                "trees_equivalent": 68,
                "cars_equivalent": 0.375,
                "renewable_energy_kwh": 2500.0
            },
            "economic": {
                "total_cost_usd": 2500.0,
                "energy_savings_usd": 375.0,
                "waste_disposal_savings_usd": 125.0,
                "net_savings_usd": -2000.0,
                "roi_percent": 15.0,
                "payback_period_years": 6.7
            },
            "social": {
                "households_served": 150,
                "energy_access_improvement_percent": 25.0,
                "jobs_created": 3,
                "health_benefits_score": 75.0,
                "community_empowerment_score": 80.0
            }
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
