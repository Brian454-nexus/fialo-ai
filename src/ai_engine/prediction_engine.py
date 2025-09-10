"""
AI-powered prediction engine for waste-to-energy optimization.
Uses machine learning models to predict energy potential and optimize conversion strategies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

from models.waste_types import WasteType, WASTE_TYPES, ConversionMethod
from models.community import Community, generate_hourly_demand_profile
from models.conversion_system import ConversionSystem, ConversionResult


class EnergyPredictionEngine:
    """AI engine for predicting energy potential from waste and optimizing conversion strategies."""
    
    def __init__(self):
        self.energy_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.demand_model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = "models/ai_models.pkl"
        
    def train_models(self, historical_data: pd.DataFrame = None):
        """Train the AI models with historical data or synthetic data."""
        if historical_data is None:
            historical_data = self._generate_synthetic_training_data()
        
        # Prepare features for energy prediction
        energy_features = [
            'waste_amount_kg', 'waste_type_encoded', 'conversion_method_encoded',
            'moisture_content', 'carbon_content', 'temperature_c', 'humidity_percent',
            'seasonal_factor', 'system_efficiency'
        ]
        
        X_energy = historical_data[energy_features]
        y_energy = historical_data['energy_output_kwh']
        
        # Train energy prediction model
        X_train, X_test, y_train, y_test = train_test_split(
            X_energy, y_energy, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.energy_model.fit(X_train_scaled, y_train)
        
        # Prepare features for demand prediction
        demand_features = [
            'hour_of_day', 'day_of_week', 'month', 'population', 'households',
            'community_type_encoded', 'temperature_c', 'seasonal_factor'
        ]
        
        X_demand = historical_data[demand_features]
        y_demand = historical_data['energy_demand_kwh']
        
        # Train demand prediction model
        X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
            X_demand, y_demand, test_size=0.2, random_state=42
        )
        
        self.demand_model.fit(X_train_d, y_train_d)
        
        self.is_trained = True
        
        # Save models
        self._save_models()
        
        return {
            'energy_model_score': self.energy_model.score(X_test_scaled, y_test),
            'demand_model_score': self.demand_model.score(X_test_d, y_test_d)
        }
    
    def predict_energy_potential(
        self, 
        waste_input: Dict[str, float],
        conversion_method: ConversionMethod,
        environmental_conditions: Dict[str, float] = None
    ) -> Dict[str, float]:
        """
        Predict energy potential from waste input using AI model.
        
        Args:
            waste_input: Waste amounts by type (kg)
            conversion_method: Conversion method to use
            environmental_conditions: Environmental factors (temperature, humidity, etc.)
        
        Returns:
            Dictionary with energy predictions and confidence intervals
        """
        if not self.is_trained:
            self.train_models()
        
        if environmental_conditions is None:
            environmental_conditions = {
                'temperature_c': 25.0,
                'humidity_percent': 60.0,
                'seasonal_factor': 1.0
            }
        
        predictions = {}
        total_energy = 0.0
        
        for waste_type_name, amount in waste_input.items():
            if amount <= 0:
                continue
                
            waste_type = WASTE_TYPES.get(waste_type_name)
            if not waste_type:
                continue
            
            # Prepare features for prediction
            features = np.array([[
                amount,  # waste_amount_kg
                self._encode_waste_type(waste_type_name),  # waste_type_encoded
                self._encode_conversion_method(conversion_method),  # conversion_method_encoded
                waste_type.moisture_content_percent,  # moisture_content
                waste_type.carbon_content_percent,  # carbon_content
                environmental_conditions['temperature_c'],  # temperature_c
                environmental_conditions['humidity_percent'],  # humidity_percent
                environmental_conditions['seasonal_factor'],  # seasonal_factor
                0.7  # system_efficiency (default)
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict energy output
            energy_prediction = self.energy_model.predict(features_scaled)[0]
            
            # Calculate confidence interval (simplified)
            confidence_interval = energy_prediction * 0.1  # ±10% confidence
            
            predictions[waste_type_name] = {
                'energy_kwh': energy_prediction,
                'confidence_lower': energy_prediction - confidence_interval,
                'confidence_upper': energy_prediction + confidence_interval,
                'waste_amount_kg': amount
            }
            
            total_energy += energy_prediction
        
        predictions['total_energy_kwh'] = total_energy
        predictions['total_confidence_lower'] = total_energy * 0.9
        predictions['total_confidence_upper'] = total_energy * 1.1
        
        return predictions
    
    def predict_energy_demand(
        self, 
        community: Community, 
        start_time: datetime, 
        hours_ahead: int = 24
    ) -> List[Dict[str, float]]:
        """
        Predict energy demand for a community over a time horizon.
        
        Args:
            community: Community to predict demand for
            start_time: Starting time for prediction
            hours_ahead: Number of hours to predict ahead
        
        Returns:
            List of hourly demand predictions
        """
        if not self.is_trained:
            self.train_models()
        
        predictions = []
        
        for hour in range(hours_ahead):
            current_time = start_time + timedelta(hours=hour)
            
            # Prepare features for demand prediction
            features = np.array([[
                current_time.hour,  # hour_of_day
                current_time.weekday(),  # day_of_week
                current_time.month,  # month
                community.population,  # population
                community.households,  # households
                self._encode_community_type(community.community_type),  # community_type_encoded
                25.0,  # temperature_c (default)
                1.0  # seasonal_factor (default)
            ]])
            
            # Predict demand
            demand_prediction = self.demand_model.predict(features)[0]
            
            # Apply community-specific scaling
            scaled_demand = demand_prediction * (community.daily_energy_demand_kwh / 100)
            
            predictions.append({
                'timestamp': current_time,
                'predicted_demand_kwh': max(0, scaled_demand),
                'confidence_lower': max(0, scaled_demand * 0.85),
                'confidence_upper': scaled_demand * 1.15
            })
        
        return predictions
    
    def optimize_conversion_schedule(
        self,
        waste_available: Dict[str, float],
        energy_demand: List[Dict[str, float]],
        available_systems: List[ConversionSystem],
        optimization_horizon_hours: int = 24
    ) -> Dict[str, any]:
        """
        Optimize waste-to-energy conversion schedule using AI.
        
        Args:
            waste_available: Available waste by type (kg)
            energy_demand: Predicted energy demand over time
            available_systems: Available conversion systems
            optimization_horizon_hours: Optimization time horizon
        
        Returns:
            Optimized conversion schedule and recommendations
        """
        # Simple optimization algorithm (can be enhanced with more sophisticated methods)
        optimization_results = {
            'recommended_schedule': {},
            'expected_energy_output': 0.0,
            'energy_demand_met_percent': 0.0,
            'cost_benefit_ratio': 0.0,
            'emissions_avoided': {'co2_kg': 0.0, 'methane_kg': 0.0},
            'recommendations': []
        }
        
        total_energy_demand = sum(hour['predicted_demand_kwh'] for hour in energy_demand)
        total_energy_potential = 0.0
        
        # Calculate total energy potential from available waste
        for waste_type_name, amount in waste_available.items():
            waste_type = WASTE_TYPES.get(waste_type_name)
            if not waste_type:
                continue
                
            # Find best conversion method for this waste type
            best_method = max(
                waste_type.conversion_efficiency.keys(),
                key=lambda x: waste_type.conversion_efficiency[x]
            )
            
            energy_potential = amount * waste_type.energy_content_kwh_per_kg * waste_type.conversion_efficiency[best_method]
            total_energy_potential += energy_potential
            
            # Calculate emissions avoided
            emissions = self._calculate_emissions_avoided(amount, waste_type)
            optimization_results['emissions_avoided']['co2_kg'] += emissions['co2_kg']
            optimization_results['emissions_avoided']['methane_kg'] += emissions['methane_kg']
        
        optimization_results['expected_energy_output'] = total_energy_potential
        optimization_results['energy_demand_met_percent'] = min(100, (total_energy_potential / total_energy_demand) * 100)
        
        # Generate recommendations
        if optimization_results['energy_demand_met_percent'] < 80:
            optimization_results['recommendations'].append(
                "Consider increasing waste collection or adding more conversion systems"
            )
        
        if optimization_results['energy_demand_met_percent'] > 120:
            optimization_results['recommendations'].append(
                "Excess energy capacity available - consider energy storage or selling to neighboring communities"
            )
        
        # Calculate cost-benefit ratio (simplified)
        total_cost = sum(system.operational_cost_per_day for system in available_systems)
        total_benefit = total_energy_potential * 0.15  # Assume $0.15/kWh value
        optimization_results['cost_benefit_ratio'] = total_benefit / total_cost if total_cost > 0 else 0
        
        return optimization_results
    
    def _generate_synthetic_training_data(self) -> pd.DataFrame:
        """Generate synthetic training data for model training."""
        np.random.seed(42)
        n_samples = 1000
        
        data = []
        
        for _ in range(n_samples):
            # Random waste type and amount
            waste_type_name = np.random.choice(list(WASTE_TYPES.keys()))
            waste_type = WASTE_TYPES[waste_type_name]
            waste_amount = np.random.uniform(10, 1000)
            
            # Random conversion method
            conversion_method = np.random.choice(list(ConversionMethod))
            
            # Random environmental conditions
            temperature = np.random.uniform(15, 35)
            humidity = np.random.uniform(30, 90)
            seasonal_factor = np.random.uniform(0.7, 1.3)
            
            # Calculate actual energy output
            efficiency = waste_type.conversion_efficiency.get(conversion_method, 0.0)
            energy_output = waste_amount * waste_type.energy_content_kwh_per_kg * efficiency
            
            # Add some noise
            energy_output += np.random.normal(0, energy_output * 0.1)
            
            # Random community characteristics
            population = np.random.randint(100, 10000)
            households = population // 4
            community_type = np.random.randint(0, 4)
            
            # Random time features
            hour = np.random.randint(0, 24)
            day_of_week = np.random.randint(0, 7)
            month = np.random.randint(1, 13)
            
            # Random energy demand
            energy_demand = np.random.uniform(50, 500)
            
            data.append({
                'waste_amount_kg': waste_amount,
                'waste_type_encoded': self._encode_waste_type(waste_type_name),
                'conversion_method_encoded': self._encode_conversion_method(conversion_method),
                'moisture_content': waste_type.moisture_content_percent,
                'carbon_content': waste_type.carbon_content_percent,
                'temperature_c': temperature,
                'humidity_percent': humidity,
                'seasonal_factor': seasonal_factor,
                'system_efficiency': efficiency,
                'energy_output_kwh': energy_output,
                'hour_of_day': hour,
                'day_of_week': day_of_week,
                'month': month,
                'population': population,
                'households': households,
                'community_type_encoded': community_type,
                'energy_demand_kwh': energy_demand
            })
        
        return pd.DataFrame(data)
    
    def _encode_waste_type(self, waste_type_name: str) -> int:
        """Encode waste type name to integer."""
        waste_types = list(WASTE_TYPES.keys())
        return waste_types.index(waste_type_name) if waste_type_name in waste_types else 0
    
    def _encode_conversion_method(self, method: ConversionMethod) -> int:
        """Encode conversion method to integer."""
        methods = list(ConversionMethod)
        return methods.index(method)
    
    def _encode_community_type(self, community_type) -> int:
        """Encode community type to integer."""
        from ..models.community import CommunityType
        types = list(CommunityType)
        return types.index(community_type)
    
    def _calculate_emissions_avoided(self, waste_amount: float, waste_type: WasteType) -> Dict[str, float]:
        """Calculate emissions avoided by converting waste."""
        return {
            'co2_kg': waste_amount * waste_type.co2_emissions_kg_per_kg,
            'methane_kg': waste_amount * waste_type.methane_emissions_kg_per_kg
        }
    
    def _save_models(self):
        """Save trained models to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'energy_model': self.energy_model,
            'demand_model': self.demand_model,
            'scaler': self.scaler
        }, self.model_path)
    
    def _load_models(self):
        """Load trained models from disk."""
        if os.path.exists(self.model_path):
            models = joblib.load(self.model_path)
            self.energy_model = models['energy_model']
            self.demand_model = models['demand_model']
            self.scaler = models['scaler']
            self.is_trained = True
