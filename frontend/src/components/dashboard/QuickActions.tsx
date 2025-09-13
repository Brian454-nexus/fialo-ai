import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../ui/Card';
import { Button } from '../ui/Button';
import {
  PlusIcon,
  CameraIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  ShareIcon,
  DownloadIcon,
} from '@heroicons/react/24/outline';

interface QuickActionsProps {
  userType: 'individual' | 'company';
}

const actions = {
  individual: [
    {
      title: 'Add Waste Entry',
      description: 'Record your daily waste',
      icon: PlusIcon,
      color: 'from-primary-400 to-primary-600',
      action: 'add-waste',
    },
    {
      title: 'AI Waste Scan',
      description: 'Scan waste with AI',
      icon: CameraIcon,
      color: 'from-secondary-400 to-secondary-600',
      action: 'ai-scan',
    },
    {
      title: 'View Reports',
      description: 'See detailed analytics',
      icon: ChartBarIcon,
      color: 'from-accent-400 to-accent-600',
      action: 'reports',
    },
    {
      title: 'Share Impact',
      description: 'Share your progress',
      icon: ShareIcon,
      color: 'from-green-400 to-green-600',
      action: 'share',
    },
  ],
  company: [
    {
      title: 'Add Waste Batch',
      description: 'Record processed waste',
      icon: PlusIcon,
      color: 'from-primary-400 to-primary-600',
      action: 'add-batch',
    },
    {
      title: 'AI Analysis',
      description: 'Analyze waste composition',
      icon: CameraIcon,
      color: 'from-secondary-400 to-secondary-600',
      action: 'ai-analysis',
    },
    {
      title: 'Generate Report',
      description: 'Create detailed reports',
      icon: DownloadIcon,
      color: 'from-accent-400 to-accent-600',
      action: 'generate-report',
    },
    {
      title: 'Optimize Operations',
      description: 'AI optimization tools',
      icon: Cog6ToothIcon,
      color: 'from-purple-400 to-purple-600',
      action: 'optimize',
    },
  ],
};

export const QuickActions: React.FC<QuickActionsProps> = ({ userType }) => {
  const userActions = actions[userType];

  const handleAction = (action: string) => {
    console.log(`Action: ${action}`);
    // Handle different actions
  };

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold text-gray-900">
          Quick Actions
        </h3>
        <p className="text-sm text-gray-600">
          Common tasks and tools
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-3">
          {userActions.map((action, index) => (
            <motion.div
              key={action.title}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <Button
                variant="outline"
                onClick={() => handleAction(action.action)}
                className="w-full h-20 flex flex-col items-center justify-center p-3 hover:shadow-md transition-all duration-200"
              >
                <div className={`w-8 h-8 bg-gradient-to-br ${action.color} rounded-lg flex items-center justify-center mb-2`}>
                  <action.icon className="w-4 h-4 text-white" />
                </div>
                <span className="text-xs font-medium text-gray-900 text-center">
                  {action.title}
                </span>
                <span className="text-xs text-gray-500 text-center">
                  {action.description}
                </span>
              </Button>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};
