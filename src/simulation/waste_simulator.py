"""
Waste generation and collection simulation for the AI Community Waste-to-Energy Optimizer.
Simulates realistic waste generation patterns based on community characteristics.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import random

from models.waste_types import WasteType, WASTE_TYPES, WasteCategory
from models.community import Community, CommunityType, EnergyUsePattern


class WasteGenerationSimulator:
    """Simulates waste generation patterns for different community types."""
    
    def __init__(self):
        self.seasonal_factors = {
            'dry_season': 1.0,
            'wet_season': 0.8,
            'harvest_season': 1.3
        }
        self.daily_patterns = self._generate_daily_patterns()
    
    def simulate_waste_generation(
        self,
        community: Community,
        start_date: datetime,
        days: int = 7,
        include_noise: bool = True
    ) -> pd.DataFrame:
        """
        Simulate waste generation for a community over a specified period.
        
        Args:
            community: Community to simulate waste generation for
            start_date: Start date for simulation
            days: Number of days to simulate
            include_noise: Whether to include random variations
        
        Returns:
            DataFrame with hourly waste generation data
        """
        data = []
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            season = self._get_season(current_date)
            seasonal_factor = self.seasonal_factors.get(season, 1.0)
            
            # Get daily pattern for this community type
            daily_pattern = self.daily_patterns.get(community.community_type, self.daily_patterns[CommunityType.RURAL_VILLAGE])
            
            for hour in range(24):
                timestamp = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                
                # Base waste generation rate
                base_rate = community.daily_waste_generation_kg / 24
                
                # Apply hourly pattern
                hourly_factor = daily_pattern[hour]
                
                # Apply seasonal factor
                seasonal_adjusted_rate = base_rate * hourly_factor * seasonal_factor
                
                # Add random noise if requested
                if include_noise:
                    noise_factor = np.random.normal(1.0, 0.15)  # 15% standard deviation
                    seasonal_adjusted_rate *= noise_factor
                
                # Generate waste by type based on community composition
                hourly_waste = {}
                for waste_type_name, percentage in community.waste_composition.items():
                    waste_amount = seasonal_adjusted_rate * percentage
                    hourly_waste[waste_type_name] = max(0, waste_amount)
                
                # Add metadata
                data.append({
                    'timestamp': timestamp,
                    'total_waste_kg': sum(hourly_waste.values()),
                    'season': season,
                    'seasonal_factor': seasonal_factor,
                    'hourly_factor': hourly_factor,
                    **hourly_waste
                })
        
        return pd.DataFrame(data)
    
    def simulate_waste_collection(
        self,
        waste_data: pd.DataFrame,
        collection_schedule: List[int] = None,
        collection_efficiency: float = 0.85
    ) -> pd.DataFrame:
        """
        Simulate waste collection process.
        
        Args:
            waste_data: Waste generation data
            collection_schedule: Hours when collection occurs (default: [6, 14, 20])
            collection_efficiency: Efficiency of collection process
        
        Returns:
            DataFrame with collected waste data
        """
        if collection_schedule is None:
            collection_schedule = [6, 14, 20]  # Morning, afternoon, evening
        
        collected_data = waste_data.copy()
        
        # Initialize collection columns
        for waste_type in WASTE_TYPES.keys():
            collected_data[f'{waste_type}_collected'] = 0.0
        
        collected_data['total_collected_kg'] = 0.0
        collected_data['collection_efficiency'] = 0.0
        
        # Simulate collection at scheduled times
        for _, row in collected_data.iterrows():
            if row['timestamp'].hour in collection_schedule:
                # Calculate collection efficiency (can vary based on weather, etc.)
                efficiency = collection_efficiency * np.random.uniform(0.9, 1.1)
                
                total_collected = 0.0
                for waste_type in WASTE_TYPES.keys():
                    if waste_type in row:
                        collected_amount = row[waste_type] * efficiency
                        collected_data.loc[row.name, f'{waste_type}_collected'] = collected_amount
                        total_collected += collected_amount
                
                collected_data.loc[row.name, 'total_collected_kg'] = total_collected
                collected_data.loc[row.name, 'collection_efficiency'] = efficiency
        
        return collected_data
    
    def simulate_waste_processing_delays(
        self,
        collected_data: pd.DataFrame,
        processing_delay_hours: int = 2,
        storage_loss_percent: float = 0.05
    ) -> pd.DataFrame:
        """
        Simulate delays and losses in waste processing.
        
        Args:
            collected_data: Collected waste data
            processing_delay_hours: Average delay before processing
            storage_loss_percent: Percentage of waste lost during storage
        
        Returns:
            DataFrame with processed waste data
        """
        processed_data = collected_data.copy()
        
        # Initialize processing columns
        for waste_type in WASTE_TYPES.keys():
            processed_data[f'{waste_type}_processed'] = 0.0
        
        processed_data['total_processed_kg'] = 0.0
        processed_data['storage_loss_kg'] = 0.0
        
        # Simulate processing with delays and losses
        for i, row in processed_data.iterrows():
            # Calculate storage loss
            total_collected = row['total_collected_kg']
            storage_loss = total_collected * storage_loss_percent
            
            # Apply processing delay (simplified - in reality this would be more complex)
            if i >= processing_delay_hours:
                delay_row = processed_data.iloc[i - processing_delay_hours]
                
                total_processed = 0.0
                for waste_type in WASTE_TYPES.keys():
                    collected_amount = delay_row.get(f'{waste_type}_collected', 0)
                    processed_amount = collected_amount * (1 - storage_loss_percent)
                    processed_data.loc[i, f'{waste_type}_processed'] = processed_amount
                    total_processed += processed_amount
                
                processed_data.loc[i, 'total_processed_kg'] = total_processed
                processed_data.loc[i, 'storage_loss_kg'] = storage_loss
        
        return processed_data
    
    def _generate_daily_patterns(self) -> Dict[CommunityType, List[float]]:
        """Generate daily waste generation patterns for different community types."""
        patterns = {}
        
        # Rural village: peaks during meal times and evening
        patterns[CommunityType.RURAL_VILLAGE] = [
            0.2, 0.1, 0.1, 0.1, 0.2, 0.4, 0.8, 1.0, 0.6, 0.4, 0.3, 0.4,
            0.6, 0.8, 0.6, 0.4, 0.5, 0.8, 1.0, 0.8, 0.6, 0.4, 0.3, 0.2
        ]
        
        # Urban neighborhood: more consistent throughout the day
        patterns[CommunityType.URBAN_NEIGHBORHOOD] = [
            0.3, 0.2, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0, 0.8, 0.7, 0.6, 0.7,
            0.8, 0.9, 0.8, 0.7, 0.8, 0.9, 1.0, 0.9, 0.7, 0.5, 0.4, 0.3
        ]
        
        # Market area: peaks during market hours
        patterns[CommunityType.MARKET_AREA] = [
            0.1, 0.1, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 0.9, 0.8,
            0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1
        ]
        
        # Mini-grid: industrial pattern
        patterns[CommunityType.MINI_GRID] = [
            0.2, 0.2, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2
        ]
        
        # Small business: business hours pattern
        patterns[CommunityType.SMALL_BUSINESS] = [
            0.1, 0.1, 0.1, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.1, 0.1, 0.1
        ]
        
        return patterns
    
    def _get_season(self, date: datetime) -> str:
        """Determine season based on date (simplified for African context)."""
        month = date.month
        
        # Simplified seasonal classification for African regions
        if month in [12, 1, 2]:  # December, January, February
            return 'dry_season'
        elif month in [3, 4, 5]:  # March, April, May
            return 'wet_season'
        elif month in [6, 7, 8, 9, 10, 11]:  # June through November
            return 'harvest_season'
        else:
            return 'dry_season'


class WasteQualitySimulator:
    """Simulates waste quality variations that affect conversion efficiency."""
    
    def __init__(self):
        self.quality_factors = {
            'contamination': 0.1,  # 10% contamination reduces efficiency
            'decomposition': 0.05,  # 5% efficiency loss per day of decomposition
            'moisture_variation': 0.15,  # 15% moisture variation
            'temperature_effect': 0.2  # 20% efficiency variation due to temperature
        }
    
    def simulate_waste_quality(
        self,
        waste_data: pd.DataFrame,
        environmental_conditions: Dict[str, float] = None
    ) -> pd.DataFrame:
        """
        Simulate waste quality variations.
        
        Args:
            waste_data: Waste generation/collection data
            environmental_conditions: Environmental factors (temperature, humidity, etc.)
        
        Returns:
            DataFrame with quality-adjusted waste data
        """
        if environmental_conditions is None:
            environmental_conditions = {
                'temperature_c': 25.0,
                'humidity_percent': 60.0,
                'rainfall_mm': 0.0
            }
        
        quality_data = waste_data.copy()
        
        # Initialize quality columns
        for waste_type in WASTE_TYPES.keys():
            quality_data[f'{waste_type}_quality_factor'] = 1.0
        
        quality_data['overall_quality_factor'] = 1.0
        quality_data['contamination_level'] = 0.0
        quality_data['decomposition_level'] = 0.0
        
        # Simulate quality variations
        for i, row in quality_data.iterrows():
            # Contamination effect
            contamination = np.random.uniform(0, self.quality_factors['contamination'])
            
            # Decomposition effect (increases over time)
            decomposition = min(0.3, i * self.quality_factors['decomposition'] / 24)
            
            # Temperature effect
            temp_factor = 1.0 + (environmental_conditions['temperature_c'] - 25) * 0.01
            
            # Humidity effect
            humidity_factor = 1.0 + (environmental_conditions['humidity_percent'] - 60) * 0.005
            
            # Rainfall effect
            rainfall_factor = 1.0 - min(0.2, environmental_conditions['rainfall_mm'] * 0.01)
            
            # Calculate overall quality factor
            overall_quality = (1 - contamination) * (1 - decomposition) * temp_factor * humidity_factor * rainfall_factor
            overall_quality = max(0.1, min(1.0, overall_quality))  # Clamp between 0.1 and 1.0
            
            # Apply quality factors to each waste type
            for waste_type in WASTE_TYPES.keys():
                waste_type_obj = WASTE_TYPES.get(waste_type)
                if waste_type_obj:
                    # Different waste types have different sensitivity to quality factors
                    if waste_type_obj.category == WasteCategory.FOOD_SCRAPS:
                        type_quality = overall_quality * 0.9  # More sensitive
                    elif waste_type_obj.category == WasteCategory.WOOD_BIOMASS:
                        type_quality = overall_quality * 1.1  # Less sensitive
                    else:
                        type_quality = overall_quality
                    
                    quality_data.loc[i, f'{waste_type}_quality_factor'] = max(0.1, min(1.0, type_quality))
            
            quality_data.loc[i, 'overall_quality_factor'] = overall_quality
            quality_data.loc[i, 'contamination_level'] = contamination
            quality_data.loc[i, 'decomposition_level'] = decomposition
        
        return quality_data
    
    def apply_quality_adjustments(
        self,
        waste_data: pd.DataFrame,
        quality_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Apply quality adjustments to waste amounts."""
        adjusted_data = waste_data.copy()
        
        # Apply quality factors to waste amounts
        for waste_type in WASTE_TYPES.keys():
            if f'{waste_type}_processed' in adjusted_data.columns:
                quality_factor = quality_data[f'{waste_type}_quality_factor']
                original_amount = adjusted_data[f'{waste_type}_processed']
                adjusted_data[f'{waste_type}_processed'] = original_amount * quality_factor
        
        # Recalculate totals
        processed_columns = [col for col in adjusted_data.columns if col.endswith('_processed')]
        adjusted_data['total_processed_kg'] = adjusted_data[processed_columns].sum(axis=1)
        
        return adjusted_data


def create_sample_waste_scenario(
    community: Community,
    start_date: datetime = None,
    days: int = 7
) -> pd.DataFrame:
    """
    Create a complete waste generation and processing scenario.
    
    Args:
        community: Community to simulate
        start_date: Start date for simulation
        days: Number of days to simulate
    
    Returns:
        Complete waste processing scenario data
    """
    if start_date is None:
        start_date = datetime.now()
    
    # Initialize simulators
    waste_simulator = WasteGenerationSimulator()
    quality_simulator = WasteQualitySimulator()
    
    # Simulate waste generation
    waste_data = waste_simulator.simulate_waste_generation(community, start_date, days)
    
    # Simulate waste collection
    collected_data = waste_simulator.simulate_waste_collection(waste_data)
    
    # Simulate processing delays
    processed_data = waste_simulator.simulate_waste_processing_delays(collected_data)
    
    # Simulate waste quality
    quality_data = quality_simulator.simulate_waste_quality(processed_data)
    
    # Apply quality adjustments
    final_data = quality_simulator.apply_quality_adjustments(processed_data, quality_data)
    
    return final_data
