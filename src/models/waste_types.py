"""
Waste type definitions and energy conversion factors for the AI Community Waste-to-Energy Optimizer.
Based on real-world data from African communities and energy conversion literature.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class WasteCategory(Enum):
    """Categories of waste commonly found in African communities."""
    FOOD_SCRAPS = "food_scraps"
    MARKET_WASTE = "market_waste"
    AGRICULTURAL_BIOMASS = "agricultural_biomass"
    MUNICIPAL_ORGANIC = "municipal_organic"
    ANIMAL_WASTE = "animal_waste"
    WOOD_BIOMASS = "wood_biomass"


class ConversionMethod(Enum):
    """Available waste-to-energy conversion methods."""
    BIOGAS_DIGESTION = "biogas_digestion"
    ANAEROBIC_DIGESTION = "anaerobic_digestion"
    INCINERATION = "incineration"
    PYROLYSIS = "pyrolysis"
    COMPOSTING = "composting"


@dataclass
class WasteType:
    """Represents a specific type of waste with its energy conversion properties."""
    name: str
    category: WasteCategory
    energy_content_kwh_per_kg: float  # Energy content in kWh per kg
    methane_potential_m3_per_kg: float  # Methane potential in m³ per kg
    moisture_content_percent: float  # Moisture content percentage
    carbon_content_percent: float  # Carbon content percentage
    conversion_efficiency: Dict[ConversionMethod, float]  # Efficiency for each method
    seasonal_availability: Dict[str, float]  # Seasonal availability factors
    co2_emissions_kg_per_kg: float  # CO₂ emissions if left to decompose
    methane_emissions_kg_per_kg: float  # Methane emissions if left to decompose


# Waste type database with real-world data
WASTE_TYPES: Dict[str, WasteType] = {
    "food_scraps": WasteType(
        name="Food Scraps",
        category=WasteCategory.FOOD_SCRAPS,
        energy_content_kwh_per_kg=1.2,
        methane_potential_m3_per_kg=0.35,
        moisture_content_percent=70.0,
        carbon_content_percent=45.0,
        conversion_efficiency={
            ConversionMethod.BIOGAS_DIGESTION: 0.65,
            ConversionMethod.ANAEROBIC_DIGESTION: 0.70,
            ConversionMethod.INCINERATION: 0.25,
            ConversionMethod.PYROLYSIS: 0.40,
            ConversionMethod.COMPOSTING: 0.15
        },
        seasonal_availability={
            "dry_season": 0.8,
            "wet_season": 1.2,
            "harvest_season": 1.5
        },
        co2_emissions_kg_per_kg=0.8,
        methane_emissions_kg_per_kg=0.12
    ),
    
    "market_waste": WasteType(
        name="Market Waste",
        category=WasteCategory.MARKET_WASTE,
        energy_content_kwh_per_kg=1.8,
        methane_potential_m3_per_kg=0.45,
        moisture_content_percent=60.0,
        carbon_content_percent=50.0,
        conversion_efficiency={
            ConversionMethod.BIOGAS_DIGESTION: 0.70,
            ConversionMethod.ANAEROBIC_DIGESTION: 0.75,
            ConversionMethod.INCINERATION: 0.30,
            ConversionMethod.PYROLYSIS: 0.45,
            ConversionMethod.COMPOSTING: 0.20
        },
        seasonal_availability={
            "dry_season": 0.9,
            "wet_season": 1.1,
            "harvest_season": 1.3
        },
        co2_emissions_kg_per_kg=1.0,
        methane_emissions_kg_per_kg=0.15
    ),
    
    "agricultural_biomass": WasteType(
        name="Agricultural Biomass",
        category=WasteCategory.AGRICULTURAL_BIOMASS,
        energy_content_kwh_per_kg=3.5,
        methane_potential_m3_per_kg=0.25,
        moisture_content_percent=40.0,
        carbon_content_percent=55.0,
        conversion_efficiency={
            ConversionMethod.BIOGAS_DIGESTION: 0.50,
            ConversionMethod.ANAEROBIC_DIGESTION: 0.55,
            ConversionMethod.INCINERATION: 0.60,
            ConversionMethod.PYROLYSIS: 0.70,
            ConversionMethod.COMPOSTING: 0.30
        },
        seasonal_availability={
            "dry_season": 1.5,
            "wet_season": 0.7,
            "harvest_season": 2.0
        },
        co2_emissions_kg_per_kg=1.5,
        methane_emissions_kg_per_kg=0.08
    ),
    
    "animal_waste": WasteType(
        name="Animal Waste",
        category=WasteCategory.ANIMAL_WASTE,
        energy_content_kwh_per_kg=0.8,
        methane_potential_m3_per_kg=0.60,
        moisture_content_percent=80.0,
        carbon_content_percent=35.0,
        conversion_efficiency={
            ConversionMethod.BIOGAS_DIGESTION: 0.80,
            ConversionMethod.ANAEROBIC_DIGESTION: 0.85,
            ConversionMethod.INCINERATION: 0.20,
            ConversionMethod.PYROLYSIS: 0.35,
            ConversionMethod.COMPOSTING: 0.25
        },
        seasonal_availability={
            "dry_season": 1.0,
            "wet_season": 1.0,
            "harvest_season": 1.0
        },
        co2_emissions_kg_per_kg=0.6,
        methane_emissions_kg_per_kg=0.20
    ),
    
    "wood_biomass": WasteType(
        name="Wood Biomass",
        category=WasteCategory.WOOD_BIOMASS,
        energy_content_kwh_per_kg=4.2,
        methane_potential_m3_per_kg=0.15,
        moisture_content_percent=25.0,
        carbon_content_percent=60.0,
        conversion_efficiency={
            ConversionMethod.BIOGAS_DIGESTION: 0.30,
            ConversionMethod.ANAEROBIC_DIGESTION: 0.35,
            ConversionMethod.INCINERATION: 0.75,
            ConversionMethod.PYROLYSIS: 0.80,
            ConversionMethod.COMPOSTING: 0.10
        },
        seasonal_availability={
            "dry_season": 1.2,
            "wet_season": 0.8,
            "harvest_season": 1.1
        },
        co2_emissions_kg_per_kg=2.0,
        methane_emissions_kg_per_kg=0.05
    )
}


def get_waste_type(name: str) -> Optional[WasteType]:
    """Get a waste type by name."""
    return WASTE_TYPES.get(name)


def get_all_waste_types() -> List[WasteType]:
    """Get all available waste types."""
    return list(WASTE_TYPES.values())


def get_waste_types_by_category(category: WasteCategory) -> List[WasteType]:
    """Get waste types filtered by category."""
    return [wt for wt in WASTE_TYPES.values() if wt.category == category]


def calculate_energy_potential(waste_amount_kg: float, waste_type: WasteType, 
                             method: ConversionMethod) -> float:
    """Calculate energy potential from waste amount and type."""
    efficiency = waste_type.conversion_efficiency.get(method, 0.0)
    return waste_amount_kg * waste_type.energy_content_kwh_per_kg * efficiency


def calculate_emissions_avoided(waste_amount_kg: float, waste_type: WasteType) -> Dict[str, float]:
    """Calculate emissions avoided by converting waste instead of letting it decompose."""
    return {
        "co2_kg": waste_amount_kg * waste_type.co2_emissions_kg_per_kg,
        "methane_kg": waste_amount_kg * waste_type.methane_emissions_kg_per_kg,
        "co2_equivalent_kg": waste_amount_kg * (
            waste_type.co2_emissions_kg_per_kg + 
            waste_type.methane_emissions_kg_per_kg * 25  # Methane is 25x more potent than CO₂
        )
    }
