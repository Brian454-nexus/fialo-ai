# ♻️ Fialo AI - Personal Waste-to-Energy Optimizer

An AI-powered system that helps **individual users** and **waste collection companies** in Africa convert organic and municipal waste into energy efficiently, reducing emissions and boosting local energy independence.

## 🎯 Problem Statement

Many African communities generate large amounts of organic and municipal waste (food scraps, market waste, biomass, etc.). Poor waste management leads to:

- Methane emissions and pollution
- Missed energy opportunities
- Inefficient conversion methods with low energy output

## 🚀 Solution

AI-powered system that helps **individual users** and **waste collection companies** convert waste into energy efficiently with:

- **Personal Impact**: Individual waste-to-energy conversion with personal savings
- **Company Optimization**: Business-scale waste processing optimization
- **Real-time Predictions**: AI-powered energy potential forecasting
- **Scalable Impact**: Show how individual actions multiply when many people participate
- **Emissions Tracking**: Personal and company environmental impact visualization

## 🏗️ Project Structure

```
fialo-ai/
├── src/
│   ├── models/          # Data models and schemas
│   ├── ai_engine/       # AI prediction and optimization
│   ├── simulation/      # Waste-to-energy conversion simulation
│   ├── api/             # FastAPI REST endpoints
│   ├── optimization/    # Strategy optimization engine
│   └── utils/           # Utility functions
├── data/                # Sample data and datasets
├── tests/               # Unit tests
├── FRONTEND_GUIDELINES.md # Comprehensive frontend development guide
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the API server:

```bash
python run_api.py
```

3. Access the API:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔌 API Usage

### Core Endpoints

1. **Get User Types**: `GET /api/user-types`
2. **Run Personal Simulation**: `POST /api/simulate-personal`
3. **Get Waste Types**: `GET /api/waste-types`
4. **Get Conversion Systems**: `GET /api/conversion-systems`
5. **Predict Energy**: `POST /api/predict-energy`
6. **Get Impact**: `GET /api/impact/{simulation_id}`

### Legacy Endpoints (for reference)
- **Get Communities**: `GET /api/communities`
- **Run Community Simulation**: `POST /api/simulate`

### Example API Calls

#### Individual User Simulation
```bash
curl -X POST "http://localhost:8000/api/simulate-personal" \
  -H "Content-Type: application/json" \
  -d '{
    "user_type": "individual",
    "user_data": {
      "location": "Nairobi, Kenya",
      "waste_types": {
        "food_scraps": 5,
        "market_waste": 3
      },
      "daily_energy_needs_kwh": 10,
      "current_energy_cost_per_kwh": 0.20
    },
    "simulation_days": 7,
    "temperature_c": 25.0,
    "humidity_percent": 60.0,
    "rainfall_mm": 0.0,
    "include_noise": true
  }'
```

#### Waste Company Simulation
```bash
curl -X POST "http://localhost:8000/api/simulate-personal" \
  -H "Content-Type: application/json" \
  -d '{
    "user_type": "company",
    "user_data": {
      "company_name": "Green Waste Solutions",
      "location": "Lagos, Nigeria",
      "waste_types": {
        "food_scraps": 200,
        "market_waste": 150,
        "agricultural_biomass": 100
      },
      "current_processing_method": "landfill",
      "current_operational_cost_per_day": 50.0
    },
    "simulation_days": 7,
    "temperature_c": 28.0,
    "humidity_percent": 70.0,
    "rainfall_mm": 5.0,
    "include_noise": true
  }'
```

## 🎨 Frontend Development

The frontend should be built by your team members following the comprehensive guidelines in `FRONTEND_GUIDELINES.md`. Key principles:

- **Personal Focus**: Individual users and waste companies, not communities
- **Simplicity First**: Even with advanced AI, keep the interface simple
- **Mobile-First**: Optimize for mobile devices (primary access method)
- **Personal Impact**: Show individual contribution to larger environmental goals
- **Scalable Results**: Demonstrate how individual actions multiply when many people participate
- **Offline Capability**: Work without internet connection
- **Local Languages**: Support Swahili, French, Portuguese
- **Visual Communication**: Use icons and images over text

### Recommended Tech Stack
- **React Native** (mobile) or **React** (web)
- **Progressive Web App** (PWA) for offline capability
- **Simple HTML/CSS/JavaScript** for basic implementation

## 🔧 Advanced Features

- **AI-Powered Predictions**: Machine learning models for energy potential and demand forecasting
- **Genetic Algorithm Optimization**: Advanced optimization for conversion strategies
- **Multi-Community Analysis**: Compare impacts across different community types
- **Scenario Planning**: Test different waste management and energy strategies
- **Real-time Monitoring**: Track system performance and environmental impact

## 🌍 Impact

- **Climate**: Reduces methane & CO₂ emissions from waste decomposition
- **Energy**: Boosts community energy supply from renewable feedstock
- **Economy**: Turns waste into a resource, building local energy independence

## 🛠️ Features

- Real-time waste-to-energy projections
- AI-powered conversion optimization
- Emissions tracking and visualization
- Community impact metrics
- Scenario simulation capabilities
