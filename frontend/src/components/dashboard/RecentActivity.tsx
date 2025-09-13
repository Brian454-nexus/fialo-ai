import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../ui/Card';
import { formatDateTime } from '../../lib/utils';
import { ClockIcon, BoltIcon, GlobeAltIcon } from '@heroicons/react/24/outline';

interface RecentActivityProps {
  entries: any[];
}

export const RecentActivity: React.FC<RecentActivityProps> = ({ entries }) => {
  // Mock recent activity data
  const activities = [
    {
      id: 1,
      type: 'waste_added',
      title: 'Waste Entry Added',
      description: '5.2 kg of food scraps processed',
      time: '2 hours ago',
      icon: BoltIcon,
      color: 'text-green-600',
    },
    {
      id: 2,
      type: 'energy_generated',
      title: 'Energy Generated',
      description: '12.3 kWh of clean energy produced',
      time: '4 hours ago',
      icon: BoltIcon,
      color: 'text-blue-600',
    },
    {
      id: 3,
      type: 'co2_avoided',
      title: 'CO₂ Avoided',
      description: '6.1 kg of CO₂ emissions prevented',
      time: '6 hours ago',
      icon: GlobeAltIcon,
      color: 'text-green-600',
    },
    {
      id: 4,
      type: 'ai_analysis',
      title: 'AI Analysis Complete',
      description: 'Waste composition analyzed and optimized',
      time: '1 day ago',
      icon: ClockIcon,
      color: 'text-purple-600',
    },
  ];

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold text-gray-900">
          Recent Activity
        </h3>
        <p className="text-sm text-gray-600">
          Your latest waste-to-energy activities
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity, index) => (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                activity.type === 'waste_added' ? 'bg-green-100' :
                activity.type === 'energy_generated' ? 'bg-blue-100' :
                activity.type === 'co2_avoided' ? 'bg-green-100' :
                'bg-purple-100'
              }`}>
                <activity.icon className={`w-4 h-4 ${activity.color}`} />
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium text-gray-900">
                  {activity.title}
                </h4>
                <p className="text-sm text-gray-600">
                  {activity.description}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {activity.time}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};
