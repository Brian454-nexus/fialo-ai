import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../ui/Card';
import { formatNumber } from '../../lib/utils';
import { GlobeAltIcon, TreeIcon, CarIcon } from '@heroicons/react/24/outline';

interface ImpactVisualizationProps {
  stats: {
    totalWaste: number;
    totalEnergy: number;
    totalCo2Avoided: number;
    totalSavings: number;
  };
  userType: 'individual' | 'company';
}

export const ImpactVisualization: React.FC<ImpactVisualizationProps> = ({ stats, userType }) => {
  const treesEquivalent = Math.round(stats.totalCo2Avoided / 22);
  const carsEquivalent = (stats.totalCo2Avoided / 4000).toFixed(2);
  const homesPowered = Math.round(stats.totalEnergy / 30); // Assuming 30 kWh per home per day

  const impactMetrics = [
    {
      title: 'Trees Planted',
      value: treesEquivalent,
      icon: TreeIcon,
      color: 'from-green-400 to-emerald-500',
      bgColor: 'bg-green-50',
      description: 'Equivalent to planting trees',
    },
    {
      title: 'Cars Off Road',
      value: carsEquivalent,
      icon: CarIcon,
      color: 'from-blue-400 to-cyan-500',
      bgColor: 'bg-blue-50',
      description: 'Cars equivalent emissions avoided',
    },
    {
      title: 'Homes Powered',
      value: homesPowered,
      icon: GlobeAltIcon,
      color: 'from-purple-400 to-pink-500',
      bgColor: 'bg-purple-50',
      description: 'Homes powered for a day',
    },
  ];

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold text-gray-900">
          Environmental Impact
        </h3>
        <p className="text-sm text-gray-600">
          Your contribution to a sustainable future
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Impact Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {impactMetrics.map((metric, index) => (
              <motion.div
                key={metric.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="text-center"
              >
                <div className={`w-16 h-16 bg-gradient-to-br ${metric.color} rounded-full flex items-center justify-center mx-auto mb-3`}>
                  <metric.icon className="w-8 h-8 text-white" />
                </div>
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {metric.value}
                </div>
                <div className="text-sm text-gray-600 mb-1">
                  {metric.title}
                </div>
                <div className="text-xs text-gray-500">
                  {metric.description}
                </div>
              </motion.div>
            ))}
          </div>

          {/* Visual Impact Representation */}
          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg">
            <h4 className="text-lg font-semibold text-gray-900 mb-4 text-center">
              Your Impact in Numbers
            </h4>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 mb-1">
                  {formatNumber(stats.totalCo2Avoided, 1)} kg
                </div>
                <div className="text-sm text-gray-600">CO₂ Avoided</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600 mb-1">
                  {formatNumber(stats.totalEnergy, 1)} kWh
                </div>
                <div className="text-sm text-gray-600">Clean Energy</div>
              </div>
            </div>
          </div>

          {/* Progress Ring */}
          <div className="text-center">
            <div className="relative inline-flex items-center justify-center w-24 h-24">
              <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#e5e7eb"
                  strokeWidth="8"
                  fill="none"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="url(#gradient)"
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray={`${(stats.totalCo2Avoided / 100) * 251.2} 251.2`}
                  strokeLinecap="round"
                  className="transition-all duration-1000"
                />
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#10b981" />
                    <stop offset="100%" stopColor="#3b82f6" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-lg font-bold text-gray-900">
                    {Math.round((stats.totalCo2Avoided / 100) * 100)}%
                  </div>
                  <div className="text-xs text-gray-500">Goal</div>
                </div>
              </div>
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Progress towards monthly CO₂ reduction goal
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
