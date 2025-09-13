# ♻️ Fialo AI - Frontend

AI-Powered Waste-to-Energy Conversion Platform Frontend

## 🚀 Features

- **AI-Powered Waste Analysis**: Advanced machine learning algorithms analyze waste composition
- **Smart Waste Detection**: Camera, voice, and text-based waste identification
- **Real-time Analytics**: Interactive dashboards with energy generation tracking
- **Personalized Recommendations**: AI-driven optimization suggestions
- **Multi-User Support**: Individual users and waste companies
- **Environmental Impact Tracking**: CO₂ reduction and sustainability metrics
- **Responsive Design**: Mobile-first design with beautiful animations

## 🛠️ Tech Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Recharts** for data visualization
- **Zustand** for state management
- **React Hook Form** for form handling
- **React Query** for API management

## 📦 Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## 🏗️ Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Basic UI components
│   ├── auth/           # Authentication components
│   ├── dashboard/      # Dashboard components
│   ├── waste/          # Waste-related components
│   └── ai/             # AI analysis components
├── pages/              # Page components
├── store/              # State management
├── services/           # API services
└── lib/                # Utility functions
```

## 🎨 Design System

- **Colors**: Primary (green), Secondary (blue), Accent (orange)
- **Typography**: Inter (body), Poppins (headings)
- **Animations**: Framer Motion with custom easing
- **Icons**: Heroicons and Lucide React

## 🔧 Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## 🌍 Environment Variables

Create a `.env` file in the root directory:

```
REACT_APP_API_URL=http://localhost:8000
```

## 📱 Mobile Support

The app is fully responsive and optimized for mobile devices with:
- Touch-friendly interfaces
- Swipe gestures
- Mobile-first design
- Progressive Web App capabilities

## 🚀 Deployment

The app can be deployed to any static hosting service:

1. Build the app: `npm run build`
2. Deploy the `build` folder to your hosting service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
