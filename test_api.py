#!/usr/bin/env python3
"""
Test script for the AI Community Waste-to-Energy Optimizer API.
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints."""
    print("🧪 Testing ♻️ Fialo AI - Personal Waste-to-Energy Optimizer API")
    print("=" * 60)
    
    # Test health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test get communities
    print("\n2. Testing get communities...")
    try:
        response = requests.get(f"{API_BASE}/api/communities")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get communities passed")
            print(f"   Found {len(data['communities'])} communities")
            for community in data['communities']:
                print(f"   - {community['name']} ({community['type']})")
        else:
            print(f"❌ Get communities failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get communities error: {e}")
    
    # Test get waste types
    print("\n3. Testing get waste types...")
    try:
        response = requests.get(f"{API_BASE}/api/waste-types")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get waste types passed")
            print(f"   Found {len(data['waste_types'])} waste types")
            for waste_type, details in data['waste_types'].items():
                print(f"   - {details['name']}: {details['energy_content_kwh_per_kg']} kWh/kg")
        else:
            print(f"❌ Get waste types failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get waste types error: {e}")
    
    # Test get conversion systems
    print("\n4. Testing get conversion systems...")
    try:
        response = requests.get(f"{API_BASE}/api/conversion-systems")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get conversion systems passed")
            print(f"   Found {len(data['conversion_systems'])} systems")
            for system in data['conversion_systems']:
                print(f"   - {system['name']}: {system['capacity_kg_per_day']} kg/day")
        else:
            print(f"❌ Get conversion systems failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get conversion systems error: {e}")
    
    # Test simulation
    print("\n5. Testing simulation...")
    try:
        simulation_data = {
            "community_id": "community_0",
            "simulation_days": 7,
            "temperature_c": 25.0,
            "humidity_percent": 60.0,
            "rainfall_mm": 0.0,
            "include_noise": True
        }
        
        response = requests.post(
            f"{API_BASE}/api/simulate",
            headers={"Content-Type": "application/json"},
            json=simulation_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Simulation passed")
            print(f"   Simulation ID: {data['simulation_id']}")
            print(f"   Community: {data['community']['name']}")
            print(f"   Energy Generated: {data['results']['total_energy_generated_kwh']:.1f} kWh")
            print(f"   CO₂ Avoided: {data['results']['total_co2_avoided_kg']:.1f} kg")
            print(f"   Cost: ${data['results']['total_cost_usd']:.2f}")
        else:
            print(f"❌ Simulation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Simulation error: {e}")
    
    # Test optimization
    print("\n6. Testing optimization...")
    try:
        optimization_data = {
            "community_id": "community_0",
            "waste_available": {
                "food_scraps": 100,
                "market_waste": 80,
                "agricultural_biomass": 50
            },
            "optimization_goals": {
                "energy_output": 0.4,
                "cost_efficiency": 0.3,
                "emissions_reduction": 0.2,
                "social_impact": 0.1
            },
            "time_horizon_days": 30
        }
        
        response = requests.post(
            f"{API_BASE}/api/optimize",
            headers={"Content-Type": "application/json"},
            json=optimization_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Optimization passed")
            print(f"   Optimization ID: {data['optimization_id']}")
            print(f"   Best Strategy: {data['best_strategy']['name']}")
            print(f"   Expected Energy: {data['best_strategy']['expected_energy_output']:.1f} kWh")
            print(f"   Expected ROI: {data['best_strategy']['expected_roi']:.1f}%")
            print(f"   Confidence: {data['best_strategy']['confidence_score']:.1%}")
        else:
            print(f"❌ Optimization failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Optimization error: {e}")
    
    # Test energy prediction
    print("\n7. Testing energy prediction...")
    try:
        prediction_data = {
            "waste_input": {
                "food_scraps": 50,
                "market_waste": 30
            },
            "conversion_method": "biogas_digestion",
            "environmental_conditions": {
                "temperature_c": 25.0,
                "humidity_percent": 60.0
            }
        }
        
        response = requests.post(
            f"{API_BASE}/api/predict-energy",
            headers={"Content-Type": "application/json"},
            json=prediction_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Energy prediction passed")
            print(f"   Prediction ID: {data['prediction_id']}")
            print(f"   Total Energy: {data['predictions']['total_energy_kwh']:.1f} kWh")
            print(f"   Confidence: {data['predictions']['total_confidence_lower']:.1f} - {data['predictions']['total_confidence_upper']:.1f} kWh")
        else:
            print(f"❌ Energy prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Energy prediction error: {e}")
    
    print("\n🎉 API testing completed!")
    print("\n📚 API Documentation available at: http://localhost:8000/docs")
    print("🌐 Interactive API explorer at: http://localhost:8000/redoc")

def main():
    """Main test function."""
    print("🔍 Checking if API server is running...")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            test_api_endpoints()
        else:
            print("❌ API server is not responding correctly")
            print("Please start the API server with: python run_api.py")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("Please start the API server with: python run_api.py")
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")

if __name__ == "__main__":
    main()
