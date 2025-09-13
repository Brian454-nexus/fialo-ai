import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '../ui/Card';
import { formatNumber, formatCurrency } from '../../lib/utils';
import {
  BoltIcon,
  CurrencyDollarIcon,
  GlobeAltIcon,
  ChartBarIcon,
  TrendingUpIcon,
  TrendingDownIcon,
} from '@heroicons/react/24/outline';

interface StatsOverviewProps {
  stats: {
    totalWaste: number;
    totalEnergy: number;
    totalCo2Avoided: number;
    totalSavings: number;
  };
  userType: 'individual' | 'company';
  timeRange: string;
}

const getTimeRangeLabel = (range: string) => {
  switch (range) {
    case '1d': return 'Today';
    case '7d': return 'This Week';
    case '30d': return 'This Month';
    case '90d': return 'Last 3 Months';
    default: return 'All Time';
  }
};

export const StatsOverview: React.FC<StatsOverviewProps> = ({
  stats,
  userType,
  timeRange,
}) => {
  const timeRangeLabel = getTimeRangeLabel(timeRange);

  const statsData = [
    {
      title: userType === 'individual' ? 'Energy Generated' : 'Energy Produced',
      value: `${formatNumber(stats.totalEnergy, 1)} kWh`,
      icon: BoltIcon,
      color: 'from-yellow-400 to-orange-500',
      bgColor: 'bg-yellow-50',
      textColor: 'text-yellow-600',
      change: '+12.5%',
      trend: 'up',
      description: userType === 'individual' 
        ? 'Clean energy for your home' 
        : 'Renewable energy generated',
    },
    {
      title: userType === 'individual' ? 'Money Saved' : 'Revenue Generated',
      value: formatCurrency(stats.totalSavings),
      icon: CurrencyDollarIcon,
      color: 'from-green-400 to-emerald-500',
      bgColor: 'bg-green-50',
      textColor: 'text-green-600',
      change: '+8.2%',
      trend: 'up',
      description: userType === 'individual' 
        ? 'Reduced energy bills' 
        : 'Revenue from energy sales',
    },
    {
      title: 'CO₂ Avoided',
      value: `${formatNumber(stats.totalCo2Avoided, 1)} kg`,
      icon: GlobeAltIcon,
      color: 'from-blue-400 to-cyan-500',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-600',
      change: '+15.3%',
      trend: 'up',
      description: 'Environmental impact',
    },
    {
      title: 'Waste Processed',
      value: `${formatNumber(stats.totalWaste, 1)} kg`,
      icon: ChartBarIcon,
      color: 'from-purple-400 to-pink-500',
      bgColor: 'bg-purple-50',
      textColor: 'text-purple-600',
      change: '+6.7%',
      trend: 'up',
      description: userType === 'individual' 
        ? 'Waste converted to energy' 
        : 'Waste processed efficiently',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statsData.map((stat, index) => (
        <motion.div
          key={stat.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: index * 0.1 }}
        >
          <Card className="hover:shadow-lg transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-lg flex items-center justify-center`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex items-center space-x-1">
                  {stat.trend === 'up' ? (
                    <TrendingUpIcon className="w-4 h-4 text-green-500" />
                  ) : (
                    <TrendingDownIcon className="w-4 h-4 text-red-500" />
                  )}
                  <span className={`text-sm font-medium ${
                    stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {stat.change}
                  </span>
                </div>
              </div>

              <div className="mb-2">
                <h3 className="text-2xl font-bold text-gray-900">
                  {stat.value}
                </h3>
                <p className="text-sm text-gray-600">
                  {stat.title}
                </p>
              </div>

              <div className="flex items-center justify-between">
                <p className="text-xs text-gray-500">
                  {stat.description}
                </p>
                <span className="text-xs text-gray-400">
                  {timeRangeLabel}
                </span>
              </div>

              {/* Progress Bar */}
              <div className="mt-4">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 bg-gradient-to-r ${stat.color} rounded-full transition-all duration-1000`}
                    style={{ 
                      width: `${Math.min(100, (stats.totalEnergy / 100) * 100)}%` 
                    }}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  );
};
