"""
Advanced optimization engine for waste-to-energy conversion strategies.
Uses genetic algorithms and linear programming for optimal resource allocation.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import random

from models.waste_types import WasteType, WASTE_TYPES, ConversionMethod
from models.community import Community
from models.conversion_system import ConversionSystem, ConversionPlan


@dataclass
class OptimizationConstraints:
    """Constraints for the optimization problem."""
    max_processing_capacity_kg_per_hour: float
    min_energy_output_kwh: float
    max_operational_cost_usd: float
    max_processing_time_hours: float
    system_availability: Dict[str, bool]  # system_name -> available


@dataclass
class OptimizationResult:
    """Result of the optimization process."""
    optimal_schedule: Dict[datetime, Dict[str, float]]  # timestamp -> waste_type -> amount
    optimal_systems: List[ConversionSystem]
    total_energy_output: float
    total_cost: float
    emissions_avoided: Dict[str, float]
    efficiency_score: float
    convergence_iterations: int


class GeneticOptimizer:
    """Genetic algorithm optimizer for waste-to-energy conversion scheduling."""
    
    def __init__(self, population_size: int = 50, generations: int = 100):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8
        self.elite_size = 5
    
    def optimize(
        self,
        waste_available: Dict[str, float],
        available_systems: List[ConversionSystem],
        energy_demand: List[Dict[str, float]],
        constraints: OptimizationConstraints
    ) -> OptimizationResult:
        """
        Optimize waste-to-energy conversion using genetic algorithm.
        
        Args:
            waste_available: Available waste by type (kg)
            available_systems: Available conversion systems
            energy_demand: Energy demand over time
            constraints: Optimization constraints
        
        Returns:
            Optimal conversion strategy
        """
        # Initialize population
        population = self._initialize_population(
            waste_available, available_systems, len(energy_demand)
        )
        
        best_solution = None
        best_fitness = float('-inf')
        
        for generation in range(self.generations):
            # Evaluate fitness
            fitness_scores = []
            for individual in population:
                fitness = self._evaluate_fitness(
                    individual, waste_available, available_systems, 
                    energy_demand, constraints
                )
                fitness_scores.append(fitness)
                
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_solution = individual
            
            # Selection and reproduction
            population = self._evolve_population(population, fitness_scores)
        
        # Convert best solution to result format
        return self._solution_to_result(
            best_solution, waste_available, available_systems, energy_demand
        )
    
    def _initialize_population(
        self, 
        waste_available: Dict[str, float], 
        systems: List[ConversionSystem], 
        time_horizon: int
    ) -> List[Dict]:
        """Initialize random population of solutions."""
        population = []
        
        for _ in range(self.population_size):
            individual = {
                'schedule': {},
                'system_assignments': []
            }
            
            # Random schedule
            for hour in range(time_horizon):
                hourly_schedule = {}
                for waste_type, total_amount in waste_available.items():
                    # Randomly distribute waste across time
                    hourly_amount = random.uniform(0, total_amount / time_horizon * 2)
                    hourly_schedule[waste_type] = hourly_amount
                individual['schedule'][hour] = hourly_schedule
            
            # Random system assignments
            for system in systems:
                if random.random() < 0.7:  # 70% chance of using each system
                    individual['system_assignments'].append(system.name)
            
            population.append(individual)
        
        return population
    
    def _evaluate_fitness(
        self,
        individual: Dict,
        waste_available: Dict[str, float],
        systems: List[ConversionSystem],
        energy_demand: List[Dict[str, float]],
        constraints: OptimizationConstraints
    ) -> float:
        """Evaluate fitness of an individual solution."""
        try:
            # Calculate energy output
            total_energy = 0.0
            total_cost = 0.0
            
            for hour, hourly_schedule in individual['schedule'].items():
                for waste_type_name, amount in hourly_schedule.items():
                    waste_type = WASTE_TYPES.get(waste_type_name)
                    if not waste_type or amount <= 0:
                        continue
                    
                    # Find best system for this waste type
                    best_system = None
                    best_efficiency = 0.0
                    
                    for system in systems:
                        if system.name in individual['system_assignments']:
                            efficiency = waste_type.conversion_efficiency.get(system.system_type, 0.0)
                            if efficiency > best_efficiency:
                                best_efficiency = efficiency
                                best_system = system
                    
                    if best_system:
                        energy_output = amount * waste_type.energy_content_kwh_per_kg * best_efficiency
                        total_energy += energy_output
                        total_cost += best_system.operational_cost_per_day / 24
            
            # Calculate demand satisfaction
            total_demand = sum(hour['predicted_demand_kwh'] for hour in energy_demand)
            demand_satisfaction = min(1.0, total_energy / total_demand) if total_demand > 0 else 0.0
            
            # Calculate cost efficiency
            cost_efficiency = 1.0 / (1.0 + total_cost / 1000)  # Normalize cost
            
            # Check constraints
            constraint_penalty = 0.0
            if total_energy < constraints.min_energy_output_kwh:
                constraint_penalty += 0.5
            if total_cost > constraints.max_operational_cost_usd:
                constraint_penalty += 0.5
            
            # Fitness function
            fitness = (
                demand_satisfaction * 0.4 +
                cost_efficiency * 0.3 +
                (total_energy / 1000) * 0.2 +  # Energy output bonus
                0.1 * (1.0 - constraint_penalty)  # Constraint satisfaction
            )
            
            return fitness
            
        except Exception:
            return 0.0  # Invalid solution
    
    def _evolve_population(
        self, 
        population: List[Dict], 
        fitness_scores: List[float]
    ) -> List[Dict]:
        """Evolve population through selection, crossover, and mutation."""
        # Sort by fitness
        sorted_population = sorted(
            zip(population, fitness_scores), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        new_population = []
        
        # Elitism: keep best individuals
        for i in range(self.elite_size):
            new_population.append(sorted_population[i][0])
        
        # Generate offspring
        while len(new_population) < self.population_size:
            # Selection
            parent1 = self._tournament_selection(population, fitness_scores)
            parent2 = self._tournament_selection(population, fitness_scores)
            
            # Crossover
            if random.random() < self.crossover_rate:
                child1, child2 = self._crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            
            # Mutation
            child1 = self._mutate(child1)
            child2 = self._mutate(child2)
            
            new_population.extend([child1, child2])
        
        return new_population[:self.population_size]
    
    def _tournament_selection(
        self, 
        population: List[Dict], 
        fitness_scores: List[float], 
        tournament_size: int = 3
    ) -> Dict:
        """Tournament selection for parent selection."""
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_index = tournament_indices[np.argmax(tournament_fitness)]
        return population[winner_index]
    
    def _crossover(self, parent1: Dict, parent2: Dict) -> Tuple[Dict, Dict]:
        """Crossover operation between two parents."""
        child1 = {
            'schedule': {},
            'system_assignments': []
        }
        child2 = {
            'schedule': {},
            'system_assignments': []
        }
        
        # Crossover schedule
        for hour in parent1['schedule']:
            if random.random() < 0.5:
                child1['schedule'][hour] = parent1['schedule'][hour].copy()
                child2['schedule'][hour] = parent2['schedule'][hour].copy()
            else:
                child1['schedule'][hour] = parent2['schedule'][hour].copy()
                child2['schedule'][hour] = parent1['schedule'][hour].copy()
        
        # Crossover system assignments
        if random.random() < 0.5:
            child1['system_assignments'] = parent1['system_assignments'].copy()
            child2['system_assignments'] = parent2['system_assignments'].copy()
        else:
            child1['system_assignments'] = parent2['system_assignments'].copy()
            child2['system_assignments'] = parent1['system_assignments'].copy()
        
        return child1, child2
    
    def _mutate(self, individual: Dict) -> Dict:
        """Mutation operation on an individual."""
        mutated = {
            'schedule': individual['schedule'].copy(),
            'system_assignments': individual['system_assignments'].copy()
        }
        
        # Mutate schedule
        for hour in mutated['schedule']:
            if random.random() < self.mutation_rate:
                for waste_type in mutated['schedule'][hour]:
                    # Randomly adjust waste amount
                    current_amount = mutated['schedule'][hour][waste_type]
                    mutation_factor = random.uniform(0.5, 1.5)
                    mutated['schedule'][hour][waste_type] = current_amount * mutation_factor
        
        # Mutate system assignments
        if random.random() < self.mutation_rate:
            if random.random() < 0.5 and mutated['system_assignments']:
                # Remove a system
                mutated['system_assignments'].pop(random.randint(0, len(mutated['system_assignments']) - 1))
            else:
                # Add a system (if not already present)
                available_systems = ['system1', 'system2', 'system3']  # Simplified
                new_system = random.choice(available_systems)
                if new_system not in mutated['system_assignments']:
                    mutated['system_assignments'].append(new_system)
        
        return mutated
    
    def _solution_to_result(
        self,
        solution: Dict,
        waste_available: Dict[str, float],
        systems: List[ConversionSystem],
        energy_demand: List[Dict[str, float]]
    ) -> OptimizationResult:
        """Convert genetic algorithm solution to OptimizationResult."""
        # Calculate total energy output and cost
        total_energy = 0.0
        total_cost = 0.0
        emissions_avoided = {'co2_kg': 0.0, 'methane_kg': 0.0}
        
        optimal_schedule = {}
        start_time = datetime.now()
        
        for hour, hourly_schedule in solution['schedule'].items():
            timestamp = start_time + timedelta(hours=hour)
            optimal_schedule[timestamp] = hourly_schedule
            
            for waste_type_name, amount in hourly_schedule.items():
                waste_type = WASTE_TYPES.get(waste_type_name)
                if not waste_type or amount <= 0:
                    continue
                
                # Find best system for this waste type
                best_system = None
                best_efficiency = 0.0
                
                for system in systems:
                    if system.name in solution['system_assignments']:
                        efficiency = waste_type.conversion_efficiency.get(system.system_type, 0.0)
                        if efficiency > best_efficiency:
                            best_efficiency = efficiency
                            best_system = system
                
                if best_system:
                    energy_output = amount * waste_type.energy_content_kwh_per_kg * best_efficiency
                    total_energy += energy_output
                    total_cost += best_system.operational_cost_per_day / 24
                    
                    # Calculate emissions avoided
                    emissions_avoided['co2_kg'] += amount * waste_type.co2_emissions_kg_per_kg
                    emissions_avoided['methane_kg'] += amount * waste_type.methane_emissions_kg_per_kg
        
        # Calculate efficiency score
        total_demand = sum(hour['predicted_demand_kwh'] for hour in energy_demand)
        efficiency_score = (total_energy / total_demand) if total_demand > 0 else 0.0
        
        # Get optimal systems
        optimal_systems = [
            system for system in systems 
            if system.name in solution['system_assignments']
        ]
        
        return OptimizationResult(
            optimal_schedule=optimal_schedule,
            optimal_systems=optimal_systems,
            total_energy_output=total_energy,
            total_cost=total_cost,
            emissions_avoided=emissions_avoided,
            efficiency_score=efficiency_score,
            convergence_iterations=self.generations
        )


class LinearProgrammingOptimizer:
    """Linear programming optimizer for simple waste-to-energy allocation problems."""
    
    def optimize(
        self,
        waste_available: Dict[str, float],
        available_systems: List[ConversionSystem],
        energy_demand: float,
        constraints: OptimizationConstraints
    ) -> OptimizationResult:
        """
        Optimize using linear programming (simplified implementation).
        
        Args:
            waste_available: Available waste by type (kg)
            available_systems: Available conversion systems
            energy_demand: Total energy demand (kWh)
            constraints: Optimization constraints
        
        Returns:
            Optimal allocation result
        """
        # Simplified linear programming solution
        # In a real implementation, you would use scipy.optimize.linprog or similar
        
        optimal_schedule = {}
        optimal_systems = []
        total_energy = 0.0
        total_cost = 0.0
        emissions_avoided = {'co2_kg': 0.0, 'methane_kg': 0.0}
        
        # Simple greedy allocation
        remaining_demand = energy_demand
        start_time = datetime.now()
        
        for waste_type_name, amount in waste_available.items():
            if remaining_demand <= 0:
                break
                
            waste_type = WASTE_TYPES.get(waste_type_name)
            if not waste_type:
                continue
            
            # Find best system for this waste type
            best_system = None
            best_efficiency = 0.0
            
            for system in available_systems:
                efficiency = waste_type.conversion_efficiency.get(system.system_type, 0.0)
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_system = system
            
            if best_system:
                # Calculate how much to process
                energy_per_kg = waste_type.energy_content_kwh_per_kg * best_efficiency
                max_processable = min(amount, remaining_demand / energy_per_kg)
                
                if max_processable > 0:
                    optimal_schedule[start_time] = {waste_type_name: max_processable}
                    optimal_systems.append(best_system)
                    
                    energy_output = max_processable * energy_per_kg
                    total_energy += energy_output
                    total_cost += best_system.operational_cost_per_day / 24
                    remaining_demand -= energy_output
                    
                    # Calculate emissions avoided
                    emissions_avoided['co2_kg'] += max_processable * waste_type.co2_emissions_kg_per_kg
                    emissions_avoided['methane_kg'] += max_processable * waste_type.methane_emissions_kg_per_kg
        
        efficiency_score = (total_energy / energy_demand) if energy_demand > 0 else 0.0
        
        return OptimizationResult(
            optimal_schedule=optimal_schedule,
            optimal_systems=optimal_systems,
            total_energy_output=total_energy,
            total_cost=total_cost,
            emissions_avoided=emissions_avoided,
            efficiency_score=efficiency_score,
            convergence_iterations=1
        )
