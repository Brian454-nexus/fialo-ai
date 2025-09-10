"""
Community and energy demand models for the AI Community Waste-to-Energy Optimizer.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum


class CommunityType(Enum):
    """Types of communities using the system."""
    RURAL_VILLAGE = "rural_village"
    URBAN_NEIGHBORHOOD = "urban_neighborhood"
    MARKET_AREA = "market_area"
    MINI_GRID = "mini_grid"
    SMALL_BUSINESS = "small_business"


class EnergyUsePattern(Enum):
    """Energy usage patterns throughout the day."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    MIXED = "mixed"
    INDUSTRIAL = "industrial"


@dataclass
class EnergyDemand:
    """Represents energy demand at a specific time."""
    timestamp: datetime
    demand_kwh: float
    peak_demand_kwh: float
    base_demand_kwh: float


@dataclass
class Community:
    """Represents a community with its energy needs and waste generation patterns."""
    name: str
    community_type: CommunityType
    population: int
    households: int
    energy_use_pattern: EnergyUsePattern
    
    # Energy demand characteristics
    daily_energy_demand_kwh: float
    peak_demand_kwh: float
    base_demand_kwh: float
    
    # Waste generation characteristics
    daily_waste_generation_kg: float
    waste_composition: Dict[str, float]  # waste_type -> percentage
    
    # Geographic and seasonal factors
    latitude: float
    longitude: float
    climate_zone: str
    seasonal_factors: Dict[str, float] = field(default_factory=dict)
    
    # Economic factors
    energy_cost_per_kwh: float = 0.15  # USD per kWh
    waste_disposal_cost_per_kg: float = 0.05  # USD per kg
    
    def __post_init__(self):
        """Initialize default seasonal factors if not provided."""
        if not self.seasonal_factors:
            self.seasonal_factors = {
                "dry_season": 1.0,
                "wet_season": 0.8,
                "harvest_season": 1.2
            }


@dataclass
class EnergyProfile:
    """Detailed energy usage profile for a community."""
    community: Community
    hourly_demand: List[EnergyDemand]
    seasonal_variations: Dict[str, float]
    growth_rate_percent: float = 2.0  # Annual growth rate


def create_sample_communities() -> List[Community]:
    """Create sample communities for demonstration purposes."""
    return [
        Community(
            name="Kibera Market Area",
            community_type=CommunityType.MARKET_AREA,
            population=5000,
            households=1200,
            energy_use_pattern=EnergyUsePattern.MIXED,
            daily_energy_demand_kwh=800,
            peak_demand_kwh=120,
            base_demand_kwh=30,
            daily_waste_generation_kg=2500,
            waste_composition={
                "food_scraps": 0.40,
                "market_waste": 0.35,
                "agricultural_biomass": 0.15,
                "animal_waste": 0.05,
                "wood_biomass": 0.05
            },
            latitude=-1.2921,
            longitude=36.8219,
            climate_zone="tropical",
            energy_cost_per_kwh=0.20,
            waste_disposal_cost_per_kg=0.08
        ),
        
        Community(
            name="Rural Village - Kisumu",
            community_type=CommunityType.RURAL_VILLAGE,
            population=800,
            households=150,
            energy_use_pattern=EnergyUsePattern.RESIDENTIAL,
            daily_energy_demand_kwh=120,
            peak_demand_kwh=25,
            base_demand_kwh=5,
            daily_waste_generation_kg=400,
            waste_composition={
                "food_scraps": 0.30,
                "market_waste": 0.20,
                "agricultural_biomass": 0.35,
                "animal_waste": 0.10,
                "wood_biomass": 0.05
            },
            latitude=-0.0917,
            longitude=34.7680,
            climate_zone="tropical",
            energy_cost_per_kwh=0.25,
            waste_disposal_cost_per_kg=0.03
        ),
        
        Community(
            name="Mini-Grid Community - Nakuru",
            community_type=CommunityType.MINI_GRID,
            population=2000,
            households=400,
            energy_use_pattern=EnergyUsePattern.MIXED,
            daily_energy_demand_kwh=300,
            peak_demand_kwh=60,
            base_demand_kwh=15,
            daily_waste_generation_kg=800,
            waste_composition={
                "food_scraps": 0.35,
                "market_waste": 0.25,
                "agricultural_biomass": 0.25,
                "animal_waste": 0.10,
                "wood_biomass": 0.05
            },
            latitude=-0.3031,
            longitude=36.0800,
            climate_zone="tropical",
            energy_cost_per_kwh=0.18,
            waste_disposal_cost_per_kg=0.06
        )
    ]


def generate_hourly_demand_profile(community: Community, date: datetime) -> List[EnergyDemand]:
    """Generate hourly energy demand profile for a given date."""
    hourly_demand = []
    
    # Base demand pattern based on community type
    if community.energy_use_pattern == EnergyUsePattern.RESIDENTIAL:
        # Residential: low at night, peaks in morning and evening
        base_pattern = [0.3, 0.2, 0.2, 0.2, 0.3, 0.5, 0.8, 0.9, 0.7, 0.6, 0.6, 0.7,
                       0.8, 0.7, 0.6, 0.6, 0.8, 1.0, 1.0, 0.9, 0.8, 0.6, 0.4, 0.3]
    elif community.energy_use_pattern == EnergyUsePattern.COMMERCIAL:
        # Commercial: peaks during business hours
        base_pattern = [0.2, 0.2, 0.2, 0.3, 0.5, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       1.0, 1.0, 1.0, 1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2]
    else:  # MIXED
        # Mixed: combination of residential and commercial
        base_pattern = [0.3, 0.2, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0, 0.9, 0.8, 0.8, 0.9,
                       0.9, 0.8, 0.8, 0.8, 0.9, 1.0, 0.9, 0.7, 0.6, 0.5, 0.4, 0.3]
    
    for hour in range(24):
        timestamp = date.replace(hour=hour, minute=0, second=0, microsecond=0)
        base_demand = community.base_demand_kwh * base_pattern[hour]
        peak_demand = community.peak_demand_kwh * base_pattern[hour]
        total_demand = base_demand + (peak_demand - base_demand) * base_pattern[hour]
        
        hourly_demand.append(EnergyDemand(
            timestamp=timestamp,
            demand_kwh=total_demand,
            peak_demand_kwh=peak_demand,
            base_demand_kwh=base_demand
        ))
    
    return hourly_demand


def calculate_energy_savings(energy_generated_kwh: float, community: Community) -> Dict[str, float]:
    """Calculate energy cost savings from waste-to-energy conversion."""
    daily_savings = energy_generated_kwh * community.energy_cost_per_kwh
    monthly_savings = daily_savings * 30
    annual_savings = daily_savings * 365
    
    return {
        "daily_savings_usd": daily_savings,
        "monthly_savings_usd": monthly_savings,
        "annual_savings_usd": annual_savings,
        "energy_generated_kwh": energy_generated_kwh
    }
