"""
Energy conversion and distribution simulation for the AI Community Waste-to-Energy Optimizer.
Simulates the conversion of waste to energy and energy distribution to meet community demand.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import random

from models.waste_types import WasteType, WASTE_TYPES, ConversionMethod
from models.community import Community, generate_hourly_demand_profile
from models.conversion_system import ConversionSystem, ConversionResult, SystemStatus


class EnergyConversionSimulator:
    """Simulates waste-to-energy conversion processes."""
    
    def __init__(self):
        self.conversion_efficiencies = {
            ConversionMethod.BIOGAS_DIGESTION: 0.65,
            ConversionMethod.ANAEROBIC_DIGESTION: 0.70,
            ConversionMethod.INCINERATION: 0.60,
            ConversionMethod.PYROLYSIS: 0.70,
            ConversionMethod.COMPOSTING: 0.20
        }
    
    def simulate_conversion_process(
        self,
        waste_input: Dict[str, float],
        system: ConversionSystem,
        duration_hours: float = 1.0,
        environmental_conditions: Dict[str, float] = None
    ) -> ConversionResult:
        """
        Simulate waste-to-energy conversion process.
        
        Args:
            waste_input: Waste input by type (kg)
            system: Conversion system to use
            duration_hours: Processing duration in hours
            environmental_conditions: Environmental factors affecting conversion
        
        Returns:
            Conversion result with energy output and emissions
        """
        if environmental_conditions is None:
            environmental_conditions = {
                'temperature_c': 25.0,
                'humidity_percent': 60.0,
                'pressure_kpa': 101.3
            }
        
        timestamp = datetime.now()
        total_energy_output = 0.0
        total_methane_output = 0.0
        total_co2_emissions = 0.0
        total_methane_emissions = 0.0
        
        # Calculate environmental efficiency factor
        env_efficiency = self._calculate_environmental_efficiency(
            environmental_conditions, system.system_type
        )
        
        for waste_type_name, amount in waste_input.items():
            if amount <= 0:
                continue
                
            waste_type = WASTE_TYPES.get(waste_type_name)
            if not waste_type:
                continue
            
            # Get base efficiency for this waste type and system
            base_efficiency = waste_type.conversion_efficiency.get(system.system_type, 0.0)
            
            # Apply system efficiency and environmental factors
            actual_efficiency = base_efficiency * system.efficiency * env_efficiency
            
            # Calculate energy output
            energy_output = amount * waste_type.energy_content_kwh_per_kg * actual_efficiency
            total_energy_output += energy_output
            
            # Calculate methane output (for biogas systems)
            if system.system_type in [ConversionMethod.BIOGAS_DIGESTION, ConversionMethod.ANAEROBIC_DIGESTION]:
                methane_output = amount * waste_type.methane_potential_m3_per_kg * actual_efficiency
                total_methane_output += methane_output
            
            # Calculate emissions avoided (negative emissions)
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
            system_efficiency=system.efficiency * env_efficiency,
            cost_usd=cost
        )
    
    def simulate_batch_conversion(
        self,
        waste_batches: List[Dict[str, float]],
        systems: List[ConversionSystem],
        time_horizon_hours: int = 24
    ) -> List[ConversionResult]:
        """
        Simulate batch conversion of multiple waste batches.
        
        Args:
            waste_batches: List of waste batches to process
            systems: Available conversion systems
            time_horizon_hours: Total time horizon for processing
        
        Returns:
            List of conversion results
        """
        results = []
        current_time = datetime.now()
        
        for i, waste_batch in enumerate(waste_batches):
            # Select best system for this batch
            best_system = self._select_best_system(waste_batch, systems)
            
            if best_system:
                # Simulate conversion
                result = self.simulate_conversion_process(
                    waste_batch, best_system, duration_hours=1.0
                )
                result.timestamp = current_time + timedelta(hours=i)
                results.append(result)
        
        return results
    
    def _calculate_environmental_efficiency(
        self,
        environmental_conditions: Dict[str, float],
        conversion_method: ConversionMethod
    ) -> float:
        """Calculate efficiency factor based on environmental conditions."""
        temperature = environmental_conditions['temperature_c']
        humidity = environmental_conditions['humidity_percent']
        pressure = environmental_conditions.get('pressure_kpa', 101.3)
        
        # Temperature effect
        if conversion_method in [ConversionMethod.BIOGAS_DIGESTION, ConversionMethod.ANAEROBIC_DIGESTION]:
            # Optimal temperature for anaerobic digestion: 35-40°C
            if 35 <= temperature <= 40:
                temp_factor = 1.0
            elif 25 <= temperature < 35:
                temp_factor = 0.8 + (temperature - 25) * 0.02
            elif 40 < temperature <= 50:
                temp_factor = 1.0 - (temperature - 40) * 0.02
            else:
                temp_factor = 0.5
        else:
            # For other methods, temperature has less effect
            temp_factor = 1.0 - abs(temperature - 25) * 0.005
        
        # Humidity effect
        if conversion_method == ConversionMethod.INCINERATION:
            # High humidity reduces incineration efficiency
            humidity_factor = 1.0 - (humidity - 50) * 0.002
        else:
            # Other methods are less affected by humidity
            humidity_factor = 1.0
        
        # Pressure effect (minimal for most systems)
        pressure_factor = 1.0 - abs(pressure - 101.3) * 0.001
        
        return max(0.1, min(1.0, temp_factor * humidity_factor * pressure_factor))
    
    def _select_best_system(
        self,
        waste_batch: Dict[str, float],
        systems: List[ConversionSystem]
    ) -> Optional[ConversionSystem]:
        """Select the best system for processing a waste batch."""
        best_system = None
        best_score = 0.0
        
        for system in systems:
            if system.status != SystemStatus.OPERATIONAL:
                continue
            
            # Calculate efficiency score for this system
            total_efficiency = 0.0
            total_waste = 0.0
            
            for waste_type_name, amount in waste_batch.items():
                waste_type = WASTE_TYPES.get(waste_type_name)
                if waste_type and amount > 0:
                    efficiency = waste_type.conversion_efficiency.get(system.system_type, 0.0)
                    total_efficiency += efficiency * amount
                    total_waste += amount
            
            if total_waste > 0:
                avg_efficiency = total_efficiency / total_waste
                # Consider system capacity and cost
                capacity_factor = min(1.0, total_waste / (system.capacity_kg_per_day / 24))
                cost_factor = 1.0 / (1.0 + system.operational_cost_per_day / 100)
                
                score = avg_efficiency * capacity_factor * cost_factor
                
                if score > best_score:
                    best_score = score
                    best_system = system
        
        return best_system


class EnergyDistributionSimulator:
    """Simulates energy distribution and grid management."""
    
    def __init__(self):
        self.grid_efficiency = 0.92  # 92% grid efficiency
        self.storage_efficiency = 0.85  # 85% storage efficiency
        self.transmission_losses = 0.08  # 8% transmission losses
    
    def simulate_energy_distribution(
        self,
        energy_generated: List[ConversionResult],
        energy_demand: List[Dict[str, float]],
        storage_capacity_kwh: float = 100.0
    ) -> pd.DataFrame:
        """
        Simulate energy distribution to meet community demand.
        
        Args:
            energy_generated: List of energy generation results
            energy_demand: List of energy demand data
            storage_capacity_kwh: Energy storage capacity
        
        Returns:
            DataFrame with energy distribution results
        """
        distribution_data = []
        current_storage = 0.0
        
        # Create time series from both generation and demand
        all_timestamps = set()
        for result in energy_generated:
            all_timestamps.add(result.timestamp)
        for demand in energy_demand:
            all_timestamps.add(demand['timestamp'])
        
        sorted_timestamps = sorted(all_timestamps)
        
        for timestamp in sorted_timestamps:
            # Find energy generation for this timestamp
            generated_energy = 0.0
            for result in energy_generated:
                if result.timestamp.hour == timestamp.hour:
                    generated_energy += result.energy_output_kwh
            
            # Find energy demand for this timestamp
            demand_energy = 0.0
            for demand in energy_demand:
                if demand['timestamp'].hour == timestamp.hour:
                    demand_energy = demand['predicted_demand_kwh']
                    break
            
            # Calculate energy balance
            net_energy = generated_energy - demand_energy
            
            # Handle energy storage
            if net_energy > 0:
                # Excess energy - store or export
                storage_input = min(net_energy, storage_capacity_kwh - current_storage)
                current_storage += storage_input * self.storage_efficiency
                exported_energy = net_energy - storage_input
            else:
                # Energy deficit - use storage or import
                storage_output = min(abs(net_energy), current_storage)
                current_storage -= storage_output
                imported_energy = abs(net_energy) - storage_output
                exported_energy = 0.0
            
            # Calculate grid efficiency
            grid_losses = (generated_energy + imported_energy) * self.transmission_losses
            delivered_energy = (generated_energy + imported_energy) * self.grid_efficiency - grid_losses
            
            distribution_data.append({
                'timestamp': timestamp,
                'generated_energy_kwh': generated_energy,
                'demand_energy_kwh': demand_energy,
                'net_energy_kwh': net_energy,
                'storage_level_kwh': current_storage,
                'exported_energy_kwh': exported_energy,
                'imported_energy_kwh': imported_energy if net_energy < 0 else 0.0,
                'grid_losses_kwh': grid_losses,
                'delivered_energy_kwh': delivered_energy,
                'demand_met_percent': min(100, (delivered_energy / demand_energy * 100)) if demand_energy > 0 else 100
            })
        
        return pd.DataFrame(distribution_data)
    
    def simulate_mini_grid_operation(
        self,
        energy_generated: List[ConversionResult],
        communities: List[Community],
        grid_capacity_kwh: float = 500.0
    ) -> Dict[str, pd.DataFrame]:
        """
        Simulate mini-grid operation serving multiple communities.
        
        Args:
            energy_generated: List of energy generation results
            communities: List of communities served by the grid
            grid_capacity_kwh: Total grid capacity
        
        Returns:
            Dictionary with distribution results for each community
        """
        results = {}
        
        for community in communities:
            # Generate demand profile for this community
            demand_profile = generate_hourly_demand_profile(community, datetime.now())
            demand_data = [
                {
                    'timestamp': demand.timestamp,
                    'predicted_demand_kwh': demand.demand_kwh
                }
                for demand in demand_profile
            ]
            
            # Simulate distribution
            distribution_result = self.simulate_energy_distribution(
                energy_generated, demand_data, storage_capacity_kwh=grid_capacity_kwh / len(communities)
            )
            
            results[community.name] = distribution_result
        
        return results


class EnergyStorageSimulator:
    """Simulates energy storage systems (batteries, etc.)."""
    
    def __init__(self):
        self.battery_efficiency = 0.90  # 90% round-trip efficiency
        self.self_discharge_rate = 0.001  # 0.1% per hour
        self.max_charge_rate = 0.2  # 20% of capacity per hour
        self.max_discharge_rate = 0.3  # 30% of capacity per hour
    
    def simulate_battery_operation(
        self,
        energy_flow: pd.DataFrame,
        battery_capacity_kwh: float = 100.0,
        initial_charge_percent: float = 50.0
    ) -> pd.DataFrame:
        """
        Simulate battery operation for energy storage.
        
        Args:
            energy_flow: DataFrame with energy flow data
            battery_capacity_kwh: Battery capacity in kWh
            initial_charge_percent: Initial charge percentage
        
        Returns:
            DataFrame with battery operation data
        """
        battery_data = energy_flow.copy()
        
        # Initialize battery columns
        battery_data['battery_charge_kwh'] = 0.0
        battery_data['battery_charge_percent'] = 0.0
        battery_data['charge_rate_kwh'] = 0.0
        battery_data['discharge_rate_kwh'] = 0.0
        battery_data['battery_efficiency'] = 0.0
        
        current_charge = battery_capacity_kwh * (initial_charge_percent / 100)
        
        for i, row in battery_data.iterrows():
            net_energy = row['net_energy_kwh']
            
            # Calculate charge/discharge rates
            if net_energy > 0:
                # Excess energy - charge battery
                max_charge = min(
                    net_energy,
                    battery_capacity_kwh * self.max_charge_rate,
                    battery_capacity_kwh - current_charge
                )
                charge_rate = max_charge * self.battery_efficiency
                discharge_rate = 0.0
            else:
                # Energy deficit - discharge battery
                max_discharge = min(
                    abs(net_energy),
                    battery_capacity_kwh * self.max_discharge_rate,
                    current_charge
                )
                discharge_rate = max_discharge
                charge_rate = 0.0
            
            # Update battery charge
            current_charge += charge_rate - discharge_rate
            
            # Apply self-discharge
            current_charge *= (1 - self.self_discharge_rate)
            
            # Clamp charge level
            current_charge = max(0, min(battery_capacity_kwh, current_charge))
            
            # Update data
            battery_data.loc[i, 'battery_charge_kwh'] = current_charge
            battery_data.loc[i, 'battery_charge_percent'] = (current_charge / battery_capacity_kwh) * 100
            battery_data.loc[i, 'charge_rate_kwh'] = charge_rate
            battery_data.loc[i, 'discharge_rate_kwh'] = discharge_rate
            battery_data.loc[i, 'battery_efficiency'] = self.battery_efficiency
        
        return battery_data


def create_complete_energy_simulation(
    waste_data: pd.DataFrame,
    systems: List[ConversionSystem],
    communities: List[Community],
    simulation_days: int = 7
) -> Dict[str, pd.DataFrame]:
    """
    Create a complete energy simulation from waste to energy distribution.
    
    Args:
        waste_data: Waste processing data
        systems: Available conversion systems
        communities: Communities to serve
        simulation_days: Number of days to simulate
    
    Returns:
        Dictionary with complete simulation results
    """
    # Initialize simulators
    conversion_simulator = EnergyConversionSimulator()
    distribution_simulator = EnergyDistributionSimulator()
    storage_simulator = EnergyStorageSimulator()
    
    # Simulate energy conversion
    conversion_results = []
    for _, row in waste_data.iterrows():
        if row['total_processed_kg'] > 0:
            waste_input = {
                waste_type: row.get(f'{waste_type}_processed', 0)
                for waste_type in WASTE_TYPES.keys()
            }
            
            # Select best system
            best_system = conversion_simulator._select_best_system(waste_input, systems)
            if best_system:
                result = conversion_simulator.simulate_conversion_process(
                    waste_input, best_system, duration_hours=1.0
                )
                result.timestamp = row['timestamp']
                conversion_results.append(result)
    
    # Simulate energy distribution for each community
    distribution_results = {}
    for community in communities:
        demand_profile = generate_hourly_demand_profile(community, datetime.now())
        demand_data = [
            {
                'timestamp': demand.timestamp,
                'predicted_demand_kwh': demand.demand_kwh
            }
            for demand in demand_profile
        ]
        
        # Simulate distribution
        distribution_result = distribution_simulator.simulate_energy_distribution(
            conversion_results, demand_data
        )
        
        # Add battery simulation
        battery_result = storage_simulator.simulate_battery_operation(distribution_result)
        
        distribution_results[community.name] = battery_result
    
    return {
        'conversion_results': pd.DataFrame([
            {
                'timestamp': result.timestamp,
                'energy_output_kwh': result.energy_output_kwh,
                'methane_output_m3': result.methane_output_m3,
                'co2_emissions_kg': result.co2_emissions_kg,
                'cost_usd': result.cost_usd
            }
            for result in conversion_results
        ]),
        'distribution_results': distribution_results
    }
