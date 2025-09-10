#!/usr/bin/env python3
"""
Test script for the AI Community Waste-to-Energy Optimizer.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from models.waste_types import WASTE_TYPES, ConversionMethod
        print("✅ Waste types imported successfully")
        print(f"   Available waste types: {list(WASTE_TYPES.keys())}")
        
        from models.community import create_sample_communities
        print("✅ Community models imported successfully")
        
        from models.conversion_system import create_sample_conversion_systems
        print("✅ Conversion system models imported successfully")
        
        from simulation.waste_simulator import WasteGenerationSimulator
        print("✅ Waste simulator imported successfully")
        
        from simulation.energy_simulator import EnergyConversionSimulator
        print("✅ Energy simulator imported successfully")
        
        from utils.impact_calculator import ImpactCalculator
        print("✅ Impact calculator imported successfully")
        
        from optimization.strategy_optimizer import StrategyOptimizer
        print("✅ Strategy optimizer imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of the system."""
    try:
        from models.waste_types import WASTE_TYPES
        from models.community import create_sample_communities
        from models.conversion_system import create_sample_conversion_systems
        
        # Test waste types
        waste_types = list(WASTE_TYPES.keys())
        print(f"✅ Found {len(waste_types)} waste types")
        
        # Test communities
        communities = create_sample_communities()
        print(f"✅ Created {len(communities)} sample communities")
        
        # Test conversion systems
        systems = create_sample_conversion_systems()
        print(f"✅ Created {len(systems)} sample conversion systems")
        
        # Test basic calculations
        from models.waste_types import calculate_energy_potential, ConversionMethod
        energy = calculate_energy_potential(100, WASTE_TYPES['food_scraps'], ConversionMethod.BIOGAS_DIGESTION)
        print(f"✅ Energy calculation test: 100kg food scraps → {energy:.1f} kWh")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing AI Community Waste-to-Energy Optimizer")
    print("=" * 50)
    
    # Test imports
    print("\n📦 Testing imports...")
    if not test_imports():
        print("❌ Import tests failed")
        return False
    
    # Test basic functionality
    print("\n🔧 Testing basic functionality...")
    if not test_basic_functionality():
        print("❌ Functionality tests failed")
        return False
    
    print("\n✅ All tests passed! System is ready to use.")
    print("\n🚀 To run the dashboard, use: python run_dashboard.py")
    
    return True

if __name__ == "__main__":
    main()
