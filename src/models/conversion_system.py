"""
Conversion system models for waste-to-energy processing.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import math

from models.waste_types import WasteType, ConversionMethod, WASTE_TYPES
from models.community import Community


class SystemStatus(Enum):
    """Status of the conversion system."""
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    STARTING_UP = "starting_up"


@dataclass
class ConversionSystem:
    """Represents a waste-to-energy conversion system."""
    name: str
    system_type: ConversionMethod
    capacity_kg_per_day: float
    efficiency: float
    startup_time_hours: float
    maintenance_interval_days: int
    operational_cost_per_day: float
    capital_cost: float
    
    # Current status
    status: SystemStatus = SystemStatus.OFFLINE
    current_load_percent: float = 0.0
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize maintenance schedule."""
        if self.next_maintenance is None:
            self.next_maintenance = datetime.now() + timedelta(days=self.maintenance_interval_days)


@dataclass
class ConversionResult:
    """Result of a waste-to-energy conversion process."""
    timestamp: datetime
    waste_input_kg: Dict[str, float]  # waste_type -> amount
    energy_output_kwh: float
    methane_output_m3: float
    co2_emissions_kg: float
    methane_emissions_kg: float
    processing_time_hours: float
    system_efficiency: float
    cost_usd: float


@dataclass
class ConversionPlan:
    """Plan for converting waste to energy over a time period."""
    start_time: datetime
    end_time: datetime
    waste_schedule: Dict[datetime, Dict[str, float]]  # timestamp -> waste_type -> amount
    system_schedule: Dict[datetime, List[ConversionSystem]]  # timestamp -> active systems
    expected_energy_output: float
    expected_emissions_avoided: Dict[str, float]
    total_cost: float


def create_sample_conversion_systems() -> List[ConversionSystem]:
    """Create sample conversion systems for different waste types."""
    return [
        ConversionSystem(
            name="Biogas Digester - Small",
            system_type=ConversionMethod.BIOGAS_DIGESTION,
            capacity_kg_per_day=500,
            efficiency=0.65,
            startup_time_hours=2,
            maintenance_interval_days=30,
            operational_cost_per_day=15.0,
            capital_cost=5000.0
        ),
        
        ConversionSystem(
            name="Biogas Digester - Large",
            system_type=ConversionMethod.BIOGAS_DIGESTION,
            capacity_kg_per_day=2000,
            efficiency=0.70,
            startup_time_hours=4,
            maintenance_interval_days=30,
            operational_cost_per_day=45.0,
            capital_cost=15000.0
        ),
        
        ConversionSystem(
            name="Anaerobic Digester",
            system_type=ConversionMethod.ANAEROBIC_DIGESTION,
            capacity_kg_per_day=1000,
            efficiency=0.75,
            startup_time_hours=6,
            maintenance_interval_days=45,
            operational_cost_per_day=30.0,
            capital_cost=12000.0
        ),
        
        ConversionSystem(
            name="Incineration Unit",
            system_type=ConversionMethod.INCINERATION,
            capacity_kg_per_day=800,
            efficiency=0.60,
            startup_time_hours=1,
            maintenance_interval_days=15,
            operational_cost_per_day=25.0,
            capital_cost=8000.0
        ),
        
        ConversionSystem(
            name="Pyrolysis Reactor",
            system_type=ConversionMethod.PYROLYSIS,
            capacity_kg_per_day=300,
            efficiency=0.70,
            startup_time_hours=3,
            maintenance_interval_days=20,
            operational_cost_per_day=20.0,
            capital_cost=10000.0
        )
    ]


def optimize_conversion_strategy(
    waste_available: Dict[str, float],
    systems_available: List[ConversionSystem],
    energy_demand_kwh: float,
    time_horizon_hours: int = 24
) -> ConversionPlan:
    """
    Optimize waste-to-energy conversion strategy to meet energy demand.
    
    Args:
        waste_available: Available waste by type (kg)
        systems_available: Available conversion systems
        energy_demand_kwh: Required energy output (kWh)
        time_horizon_hours: Planning horizon in hours
    
    Returns:
        Optimized conversion plan
    """
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=time_horizon_hours)
    
    # Simple optimization: prioritize systems with highest efficiency for each waste type
    waste_schedule = {}
    system_schedule = {}
    total_energy_output = 0.0
    total_cost = 0.0
    emissions_avoided = {"co2_kg": 0.0, "methane_kg": 0.0, "co2_equivalent_kg": 0.0}
    
    # Process waste in hourly batches
    for hour in range(time_horizon_hours):
        current_time = start_time + timedelta(hours=hour)
        hourly_waste = {}
        active_systems = []
        
        # Distribute waste processing across available systems
        remaining_waste = waste_available.copy()
        
        for system in systems_available:
            if system.status != SystemStatus.OPERATIONAL:
                continue
                
            system_capacity_kg = system.capacity_kg_per_day / 24  # Hourly capacity
            processed_waste = {}
            
            # Find best waste type for this system
            best_waste_type = None
            best_efficiency = 0.0
            
            for waste_type_name, amount in remaining_waste.items():
                if amount <= 0:
                    continue
                    
                waste_type = WASTE_TYPES.get(waste_type_name)
                if not waste_type:
                    continue
                    
                efficiency = waste_type.conversion_efficiency.get(system.system_type, 0.0)
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_waste_type = waste_type_name
            
            if best_waste_type and remaining_waste[best_waste_type] > 0:
                process_amount = min(system_capacity_kg, remaining_waste[best_waste_type])
                processed_waste[best_waste_type] = process_amount
                remaining_waste[best_waste_type] -= process_amount
                
                # Calculate energy output
                waste_type = WASTE_TYPES[best_waste_type]
                energy_output = calculate_energy_potential(
                    process_amount, waste_type, system.system_type
                )
                total_energy_output += energy_output
                
                # Calculate emissions avoided
                emissions = calculate_emissions_avoided(process_amount, waste_type)
                for key, value in emissions.items():
                    emissions_avoided[key] += value
                
                # Calculate cost
                hourly_cost = system.operational_cost_per_day / 24
                total_cost += hourly_cost
                
                active_systems.append(system)
        
        waste_schedule[current_time] = hourly_waste
        system_schedule[current_time] = active_systems
    
    return ConversionPlan(
        start_time=start_time,
        end_time=end_time,
        waste_schedule=waste_schedule,
        system_schedule=system_schedule,
        expected_energy_output=total_energy_output,
        expected_emissions_avoided=emissions_avoided,
        total_cost=total_cost
    )


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


def simulate_conversion_process(
    waste_input: Dict[str, float],
    system: ConversionSystem,
    duration_hours: float = 1.0
) -> ConversionResult:
    """
    Simulate the waste-to-energy conversion process.
    
    Args:
        waste_input: Waste input by type (kg)
        system: Conversion system to use
        duration_hours: Processing duration in hours
    
    Returns:
        Conversion result with energy output and emissions
    """
    timestamp = datetime.now()
    total_energy_output = 0.0
    total_methane_output = 0.0
    total_co2_emissions = 0.0
    total_methane_emissions = 0.0
    
    for waste_type_name, amount in waste_input.items():
        waste_type = WASTE_TYPES.get(waste_type_name)
        if not waste_type:
            continue
            
        # Calculate outputs based on system efficiency
        efficiency = waste_type.conversion_efficiency.get(system.system_type, 0.0)
        
        # Energy output
        energy_output = amount * waste_type.energy_content_kwh_per_kg * efficiency
        total_energy_output += energy_output
        
        # Methane output (for biogas systems)
        if system.system_type in [ConversionMethod.BIOGAS_DIGESTION, ConversionMethod.ANAEROBIC_DIGESTION]:
            methane_output = amount * waste_type.methane_potential_m3_per_kg * efficiency
            total_methane_output += methane_output
        
        # Emissions avoided (negative emissions)
        co2_avoided = amount * waste_type.co2_emissions_kg_per_kg
        methane_avoided = amount * waste_type.methane_emissions_kg_per_kg
        
        total_co2_emissions -= co2_avoided  # Negative = avoided
        total_methane_emissions -= methane_avoided  # Negative = avoided
    
    # Calculate processing cost
    cost = system.operational_cost_per_day * (duration_hours / 24)
    
    return ConversionResult(
        timestamp=timestamp,
        waste_input_kg=waste_input,
        energy_output_kwh=total_energy_output,
        methane_output_m3=total_methane_output,
        co2_emissions_kg=total_co2_emissions,
        methane_emissions_kg=total_methane_emissions,
        processing_time_hours=duration_hours,
        system_efficiency=system.efficiency,
        cost_usd=cost
    )
