# ♻️ Frontend Development Guidelines - Fialo AI

## 🎯 Overview

This document provides comprehensive guidelines for building a **simple, user-friendly frontend** for **Fialo AI**. The app is designed for **individual users** and **waste collection companies** in Africa, with emphasis on **simplicity, accessibility, and offline capability**.

## 👥 Target Users

### 1. **Individual Users** (Primary)

- **Households**: Families wanting to convert their waste to energy
- **Small Businesses**: Restaurants, shops, small enterprises
- **Farmers**: Agricultural waste management
- **Students/Educators**: Learning about waste-to-energy

### 2. **Waste Collection Companies** (Secondary)

- **Local Waste Collectors**: Small-scale waste management companies
- **Recycling Companies**: Companies looking to add energy generation
- **Municipal Services**: City waste management departments
- **NGOs**: Organizations working on waste management projects

## 🎨 Design Principles

### Core Principles for Individual Users & Companies

1. **Simplicity First**: Even if our AI is advanced, the interface must be simple
2. **Mobile-First**: Most users will access via mobile phones
3. **Low Bandwidth**: Optimize for slow internet connections
4. **Offline Capability**: Work without internet connection
5. **Local Languages**: Support for local languages (Swahili, French, etc.)
6. **Visual Communication**: Use icons and images over text when possible
7. **Large Touch Targets**: Easy to tap on mobile devices
8. **Personal Impact**: Show individual contribution to larger environmental goals
9. **Scalable Results**: Demonstrate how individual actions multiply when many people participate

### User Experience Guidelines

- **One Action Per Screen**: Don't overwhelm users with multiple options
- **Clear Progress Indicators**: Show users where they are in the process
- **Immediate Feedback**: Provide instant visual feedback for all actions
- **Error Prevention**: Guide users to avoid mistakes
- **Helpful Defaults**: Pre-fill common values to reduce input

## 🏗️ Technical Architecture

### Recommended Tech Stack

```
Frontend Framework: React Native (for mobile) or React (for web)
State Management: Redux Toolkit or Zustand
UI Library: NativeBase (React Native) or Chakra UI (React)
Charts: Victory Native (React Native) or Recharts (React)
HTTP Client: Axios
Offline Storage: AsyncStorage (React Native) or IndexedDB (React)
```

### Alternative Simple Options

```
Option 1: Progressive Web App (PWA) with React
Option 2: Flutter (cross-platform)
Option 3: Simple HTML/CSS/JavaScript (for basic implementation)
```

## 📱 Screen Design Specifications

### 1. Welcome/Onboarding Screen

```
Purpose: Introduce the app and its benefits
Elements:
- App logo: ♻️ Fialo AI
- Simple tagline: "Turn your waste into energy"
- 3-4 key benefits with icons:
  * ♻️ Reduce pollution
  * ⚡ Generate electricity
  * 💰 Save money
  * 🌍 Help the planet
- "Get Started" button
- Language selector (English, Swahili, French)
```

### 2. User Type Selection Screen

```
Purpose: Let users select their user type
Elements:
- Title: "How will you use this app?"
- 2 large, visual cards:
  * 👤 Individual User
    - "I want to convert my personal/household waste"
    - "Small scale: 1-100 kg per day"
  * 🏢 Waste Company
    - "I manage waste collection and processing"
    - "Large scale: 100+ kg per day"
- "Continue" button
```

### 3. Personal Details Screen (Individual Users)

```
Purpose: Collect basic personal information
Elements:
- User type: "Individual User" (display only)
- Location (dropdown: Country, City)
- Waste type selection (checkboxes):
  * 🍎 Food scraps
  * 🥬 Market waste
  * 🌾 Agricultural waste
  * 🐄 Animal waste
  * 🌳 Wood/biomass
- Daily waste amount (slider: 1-100 kg)
- Energy needs (slider: 1-50 kWh)
- "Calculate My Impact" button
```

### 3b. Company Details Screen (Waste Companies)

```
Purpose: Collect company information
Elements:
- User type: "Waste Company" (display only)
- Company name (text input)
- Location (dropdown: Country, City)
- Waste types handled (checkboxes with quantities):
  * 🍎 Food scraps: ___ kg/day
  * 🥬 Market waste: ___ kg/day
  * 🌾 Agricultural waste: ___ kg/day
  * 🐄 Animal waste: ___ kg/day
  * 🌳 Wood/biomass: ___ kg/day
- Current processing method (dropdown)
- "Get Optimization Plan" button
```

### 4. Personal Impact Dashboard (Individual Users)

```
Purpose: Show personal impact and results
Elements:
- Title: "Your Personal Impact"
- Key metrics cards (4 cards in 2x2 grid):
  * 🗑️ My Waste: "25 kg this week"
  * ⚡ Energy I Can Generate: "12 kWh"
  * 🌱 CO₂ I Can Avoid: "15 kg"
  * 💰 Money I Can Save: "$3.50"
- Simple chart showing weekly energy potential
- "If 100 people like me did this:" section
  * Combined impact: "2,500 kg waste, 1,200 kWh energy"
- "Get My Plan" button
- "Share My Impact" button
```

### 4b. Company Optimization Dashboard (Waste Companies)

```
Purpose: Show company optimization results
Elements:
- Title: "Your Optimization Plan"
- Key metrics cards (4 cards in 2x2 grid):
  * 🗑️ Waste Processed: "2,800 kg/day"
  * ⚡ Energy Generated: "1,200 kWh/day"
  * 🌱 CO₂ Avoided: "1,500 kg/day"
  * 💰 Revenue Potential: "$375/day"
- ROI analysis:
  * Investment needed: "$15,000"
  * Payback period: "6.7 years"
  * Annual profit: "$5,475"
- "View Detailed Plan" button
- "Download Report" button
```

### 5. Personal Recommendations Screen (Individual Users)

```
Purpose: Show personalized recommendations
Elements:
- Title: "Your Personal Action Plan"
- 3-5 recommendation cards:
  * 🏠 "Start with food scraps - easiest to process"
  * ⚡ "Consider a small biogas digester for your home"
  * 💡 "You can power 2 light bulbs for 6 hours daily"
  * 🌱 "You're helping plant 3 trees worth of CO₂ reduction"
- "Get Started Guide" button
- "Find Local Suppliers" button
- "Share My Plan" button
```

### 5b. Company Recommendations Screen (Waste Companies)

```
Purpose: Show business optimization recommendations
Elements:
- Title: "Your Business Optimization Plan"
- 3-5 recommendation cards:
  * 🏭 "Install biogas digesters for food waste processing"
  * ⚡ "Add incineration units for wood biomass"
  * 💰 "Expected ROI: 15% with 6.7-year payback"
  * 📈 "Scale to 5x current capacity for maximum profit"
- "Implementation Roadmap" button
- "Financial Analysis" button
- "Contact Suppliers" button
```

### 6. Impact Summary Screen

```
Purpose: Show environmental and economic impact
Elements:
- Personal impact (for individuals):
  * "You're helping plant 3 trees"
  * "You're taking 0.1 cars off the road"
  * "You're saving $127 per year"
- Company impact (for companies):
  * "You're helping plant 68 trees"
  * "You're taking 0.4 cars off the road"
  * "You're generating $5,475 annual profit"
- Community multiplier effect:
  * "If 100 people used this app:"
  * "300 trees planted, 1,200 kWh daily energy"
- "Share Impact" button
- "Join Community" button
```

## 🔌 API Integration

### Base API URL

```
Development: http://localhost:8000
Production: https://your-api-domain.com
```

### Key API Endpoints

#### 1. Get Communities

```javascript
GET /api/communities
Response: {
  "communities": [
    {
      "id": "community_0",
      "name": "Kibera Market Area",
      "type": "market_area",
      "population": 5000,
      "households": 1200,
      "daily_energy_demand_kwh": 800,
      "daily_waste_generation_kg": 2500,
      "energy_cost_per_kwh": 0.20,
      "waste_disposal_cost_per_kg": 0.08,
      "waste_composition": {...}
    }
  ]
}
```

#### 2. Run Simulation

```javascript
POST /api/simulate
Body: {
  "community_id": "community_0",
  "simulation_days": 7,
  "temperature_c": 25.0,
  "humidity_percent": 60.0,
  "rainfall_mm": 0.0,
  "include_noise": true
}
Response: {
  "simulation_id": "sim_20240909_234801",
  "community": {...},
  "parameters": {...},
  "results": {
    "total_waste_processed_kg": 2800.0,
    "total_energy_generated_kwh": 1200.0,
    "total_co2_avoided_kg": 1500.0,
    "total_cost_usd": 250.0,
    "avg_demand_met_percent": 85.0,
    "daily_averages": {...}
  },
  "time_series_data": {...}
}
```

#### 3. Get Optimization

```javascript
POST /api/optimize
Body: {
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
Response: {
  "optimization_id": "opt_20240909_234801",
  "best_strategy": {...},
  "impact_assessment": {...},
  "recommendations": [...],
  "risk_assessment": {...},
  "implementation_roadmap": [...]
}
```

### API Integration Example (React)

```javascript
// API service
const API_BASE = "http://localhost:8000";

export const apiService = {
  async getCommunities() {
    const response = await fetch(`${API_BASE}/api/communities`);
    return response.json();
  },

  async runSimulation(simulationData) {
    const response = await fetch(`${API_BASE}/api/simulate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(simulationData),
    });
    return response.json();
  },

  async optimizeStrategy(optimizationData) {
    const response = await fetch(`${API_BASE}/api/optimize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(optimizationData),
    });
    return response.json();
  },
};

// Usage in component
const [results, setResults] = useState(null);
const [loading, setLoading] = useState(false);

const handleSimulate = async () => {
  setLoading(true);
  try {
    const data = await apiService.runSimulation({
      community_id: selectedCommunity,
      simulation_days: 7,
      temperature_c: 25,
      humidity_percent: 60,
      rainfall_mm: 0,
      include_noise: true,
    });
    setResults(data);
  } catch (error) {
    console.error("Simulation failed:", error);
  } finally {
    setLoading(false);
  }
};
```

## 🎨 UI/UX Guidelines

### Color Scheme

```css
Primary Colors:
- Green: #2E8B57 (environmental, positive)
- Blue: #4169E1 (energy, technology)
- Orange: #FF8C00 (warning, attention)
- Red: #DC143C (danger, high impact)

Neutral Colors:
- Dark Gray: #2C3E50 (text)
- Light Gray: #ECF0F1 (background)
- White: #FFFFFF (cards, contrast)
```

### Typography

```
Primary Font: System fonts (Arial, Helvetica, sans-serif)
Sizes:
- Headers: 24px, 20px, 18px
- Body: 16px, 14px
- Small: 12px
- Minimum: 14px (for accessibility)
```

### Spacing

```
Padding: 16px, 24px, 32px
Margins: 8px, 16px, 24px, 32px
Touch targets: Minimum 44px x 44px
```

### Icons

```
Use simple, recognizable icons:
- ♻️ Recycle/Environment (Primary - Fialo AI logo)
- ⚡ Energy/Power
- 💰 Money/Economic
- 👥 Community/People
- 🗑️ Waste/Trash
- 📊 Charts/Data
- ⚙️ Settings/Configuration
```

## 📊 Data Visualization

### Simple Charts

1. **Energy Generation Over Time**

   - Line chart showing daily energy output
   - Simple, clean design
   - Highlight peak generation times

2. **Waste Composition**

   - Pie chart or horizontal bar chart
   - Color-coded by waste type
   - Show percentages

3. **Impact Metrics**
   - Large number displays
   - Progress bars for percentages
   - Comparison indicators (before/after)

### Chart Implementation Example

```javascript
// Using Recharts for React
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const EnergyChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={200}>
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="day" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="energy" stroke="#2E8B57" strokeWidth={2} />
    </LineChart>
  </ResponsiveContainer>
);
```

## 🌐 Internationalization (i18n)

### Supported Languages

1. **English** (default)
2. **Swahili** (East Africa)
3. **French** (West Africa)
4. **Portuguese** (Angola, Mozambique)

### Translation Structure

```javascript
const translations = {
  en: {
    welcome: "Welcome to Waste-to-Energy Optimizer",
    selectCommunity: "Select Your Community",
    ruralVillage: "Rural Village",
    marketArea: "Market Area",
    miniGrid: "Mini-Grid Community",
    calculate: "Calculate",
    results: "Results",
    recommendations: "Recommendations",
  },
  sw: {
    welcome: "Karibu kwenye Mfumo wa Kubadilisha Taka kuwa Nishati",
    selectCommunity: "Chagua Jamii Yako",
    ruralVillage: "Kijiji cha Vijijini",
    marketArea: "Eneo la Soko",
    miniGrid: "Jamii ya Gridi Ndogo",
    calculate: "Hesabu",
    results: "Matokeo",
    recommendations: "Mapendekezo",
  },
};
```

## 📱 Mobile Optimization

### Responsive Design

```css
/* Mobile First */
.container {
  padding: 16px;
  max-width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    max-width: 768px;
    margin: 0 auto;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1024px;
  }
}
```

### Touch Interactions

- Minimum 44px touch targets
- Swipe gestures for navigation
- Pull-to-refresh for data updates
- Haptic feedback (where available)

## 🔄 Offline Capability

### Offline Strategy

1. **Cache API responses** for basic functionality
2. **Store user inputs** locally
3. **Show cached results** when offline
4. **Sync when connection restored**

### Implementation Example

```javascript
// Offline storage
const offlineStorage = {
  async saveSimulation(data) {
    await AsyncStorage.setItem("last_simulation", JSON.stringify(data));
  },

  async getLastSimulation() {
    const data = await AsyncStorage.getItem("last_simulation");
    return data ? JSON.parse(data) : null;
  },

  async saveUserInputs(inputs) {
    await AsyncStorage.setItem("user_inputs", JSON.stringify(inputs));
  },
};

// Network status handling
const [isOnline, setIsOnline] = useState(navigator.onLine);

useEffect(() => {
  const handleOnline = () => setIsOnline(true);
  const handleOffline = () => setIsOnline(false);

  window.addEventListener("online", handleOnline);
  window.addEventListener("offline", handleOffline);

  return () => {
    window.removeEventListener("online", handleOnline);
    window.removeEventListener("offline", handleOffline);
  };
}, []);
```

## 🧪 Testing Guidelines

### Testing Strategy

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test API integration
3. **User Testing**: Test with actual community members
4. **Accessibility Tests**: Ensure screen reader compatibility
5. **Performance Tests**: Test on low-end devices

### Testing Checklist

- [ ] App works on Android 7+ and iOS 12+
- [ ] App works with 2G internet connection
- [ ] App works offline (shows cached data)
- [ ] All text is readable (minimum 14px)
- [ ] All buttons are tappable (minimum 44px)
- [ ] App works in landscape and portrait
- [ ] App works with screen readers
- [ ] App loads in under 3 seconds

## 🚀 Deployment Guidelines

### Production Considerations

1. **CDN**: Use CDN for static assets
2. **Compression**: Enable gzip compression
3. **Caching**: Set appropriate cache headers
4. **HTTPS**: Always use HTTPS in production
5. **Monitoring**: Set up error tracking and analytics

### Performance Targets

- **First Load**: < 3 seconds
- **Subsequent Loads**: < 1 second
- **Bundle Size**: < 2MB
- **API Response**: < 500ms
- **Offline Support**: Core features work offline

## 📋 Development Checklist

### Phase 1: Basic Implementation

- [ ] Set up development environment
- [ ] Create basic navigation structure
- [ ] Implement community selection screen
- [ ] Integrate with API endpoints
- [ ] Create results display screen
- [ ] Add basic error handling

### Phase 2: Enhanced Features

- [ ] Add data visualization
- [ ] Implement offline capability
- [ ] Add internationalization
- [ ] Create recommendations screen
- [ ] Add sharing functionality
- [ ] Implement user feedback

### Phase 3: Polish & Optimization

- [ ] Performance optimization
- [ ] Accessibility improvements
- [ ] User testing and feedback
- [ ] Bug fixes and refinements
- [ ] Production deployment
- [ ] Documentation completion

## 🎯 Success Metrics

### User Experience Metrics

- **Task Completion Rate**: > 90%
- **Time to Complete**: < 5 minutes
- **User Satisfaction**: > 4.5/5
- **Error Rate**: < 5%

### Technical Metrics

- **App Load Time**: < 3 seconds
- **API Response Time**: < 500ms
- **Crash Rate**: < 1%
- **Offline Functionality**: 100% of core features

## 📞 Support & Resources

### Development Resources

- **API Documentation**: Available at `/docs` endpoint
- **Sample Data**: Available in `data/sample_data.py`
- **Test Cases**: Available in `test_system.py`
- **Backend Team**: Available for API questions

### Community Resources

- **User Research**: Connect with local communities
- **Language Support**: Local translators available
- **Design Feedback**: Regular design reviews
- **Testing Support**: Access to test devices

## 🎉 Final Notes

Remember: **Simplicity is key!** Even though our AI backend is sophisticated, the frontend should feel like a simple, helpful tool that any community member can use. Focus on:

1. **Clear communication** of benefits
2. **Easy data input** with helpful defaults
3. **Visual results** that are easy to understand
4. **Actionable recommendations** that communities can implement
5. **Offline capability** for areas with poor internet

The goal is to make advanced AI accessible to everyone, regardless of their technical background or internet connectivity.

---

**♻️ Fialo AI - Built for African communities - Simple, Powerful, Accessible**
