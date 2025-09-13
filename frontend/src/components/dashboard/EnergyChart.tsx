import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { formatNumber } from '../../lib/utils';

interface WasteEntry {
  id: string;
  date: string;
  wasteTypes: Record<string, number>;
  totalWeight: number;
  energyGenerated: number;
  co2Avoided: number;
  costSavings: number;
  description?: string;
  imageUrl?: string;
  aiAnalysis?: {
    recommendations: string[];
    confidence: number;
    conversionMethod: string;
  };
}

interface EnergyChartProps {
  entries: WasteEntry[];
  timeRange: string;
}

export const EnergyChart: React.FC<EnergyChartProps> = ({ entries, timeRange }) => {
  // Generate mock data for demonstration
  const generateMockData = () => {
    const days = timeRange === '1d' ? 1 : timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90;
    const data = [];
    
    for (let i = 0; i < days; i++) {
      const date = new Date();
      date.setDate(date.getDate() - (days - 1 - i));
      
      // Generate realistic energy data with some variation
      const baseEnergy = 12 + Math.random() * 8; // 12-20 kWh base
      const variation = (Math.sin(i * 0.5) * 3) + (Math.random() - 0.5) * 4;
      const energy = Math.max(0, baseEnergy + variation);
      
      data.push({
        date: date.toISOString().split('T')[0],
        energy: parseFloat(energy.toFixed(1)),
        co2: parseFloat((energy * 0.5).toFixed(1)),
        savings: parseFloat((energy * 0.15).toFixed(2)),
        waste: parseFloat((energy * 0.8).toFixed(1)),
      });
    }
    
    return data;
  };

  const data = generateMockData();

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-900 mb-2">
            {new Date(label).toLocaleDateString('en-US', { 
              weekday: 'short', 
              month: 'short', 
              day: 'numeric' 
            })}
          </p>
          <div className="space-y-1">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-primary-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600">Energy: </span>
              <span className="text-sm font-semibold text-gray-900 ml-1">
                {payload[0].value} kWh
              </span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600">CO₂: </span>
              <span className="text-sm font-semibold text-gray-900 ml-1">
                {payload[1].value} kg
              </span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600">Savings: </span>
              <span className="text-sm font-semibold text-gray-900 ml-1">
                ${payload[2].value}
              </span>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <defs>
            <linearGradient id="energyGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="co2Gradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="date" 
            stroke="#6b7280"
            fontSize={12}
            tickFormatter={(value) => {
              const date = new Date(value);
              return timeRange === '1d' 
                ? date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
                : date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            }}
          />
          <YAxis 
            stroke="#6b7280"
            fontSize={12}
            tickFormatter={(value) => `${value}kWh`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="energy"
            stroke="#3b82f6"
            strokeWidth={3}
            fill="url(#energyGradient)"
            name="Energy Generated"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
