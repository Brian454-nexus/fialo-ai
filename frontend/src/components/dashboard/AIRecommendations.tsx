import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../ui/Card';
import { Button } from '../ui/Button';
import { SparklesIcon, LightBulbIcon, ArrowRightIcon } from '@heroicons/react/24/outline';

interface AIRecommendationsProps {
  userType: 'individual' | 'company';
}

const recommendations = {
  individual: [
    {
      id: 1,
      title: 'Optimize Food Waste Collection',
      description: 'Your food scraps have the highest energy potential. Consider a dedicated collection system.',
      impact: 'High',
      action: 'Set up food waste bin',
      icon: '🍎',
      color: 'from-orange-400 to-red-500',
    },
    {
      id: 2,
      title: 'Add Biogas Digester',
      description: 'Based on your waste composition, a small biogas digester could generate 15+ kWh daily.',
      impact: 'High',
      action: 'Learn more',
      icon: '⚡',
      color: 'from-yellow-400 to-orange-500',
    },
    {
      id: 3,
      title: 'Compost Garden Waste',
      description: 'Garden waste can be composted first, then used for energy generation.',
      impact: 'Medium',
      action: 'Start composting',
      icon: '🌱',
      color: 'from-green-400 to-emerald-500',
    },
  ],
  company: [
    {
      id: 1,
      title: 'Scale Biogas Operations',
      description: 'Your current setup can be scaled 3x to process 500+ kg daily with 40% ROI.',
      impact: 'High',
      action: 'View plan',
      icon: '🏭',
      color: 'from-blue-400 to-cyan-500',
    },
    {
      id: 2,
      title: 'Add Pyrolysis Unit',
      description: 'Wood biomass can be processed with pyrolysis for higher energy yield.',
      impact: 'High',
      action: 'Get quote',
      icon: '🔥',
      color: 'from-red-400 to-pink-500',
    },
    {
      id: 3,
      title: 'Optimize Collection Routes',
      description: 'AI can optimize your collection routes to reduce costs by 25%.',
      impact: 'Medium',
      action: 'Optimize',
      icon: '🗺️',
      color: 'from-purple-400 to-indigo-500',
    },
  ],
};

export const AIRecommendations: React.FC<AIRecommendationsProps> = ({ userType }) => {
  const userRecommendations = recommendations[userType];

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center">
          <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center mr-3">
            <SparklesIcon className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              AI Recommendations
            </h3>
            <p className="text-sm text-gray-600">
              Personalized optimization suggestions
            </p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {userRecommendations.map((rec, index) => (
            <motion.div
              key={rec.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className={`p-4 rounded-lg border-l-4 ${
                rec.impact === 'High' 
                  ? 'bg-primary-50 border-primary-500' 
                  : rec.impact === 'Medium'
                  ? 'bg-secondary-50 border-secondary-500'
                  : 'bg-accent-50 border-accent-500'
              }`}
            >
              <div className="flex items-start">
                <div className="text-2xl mr-3">{rec.icon}</div>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900 mb-1">
                    {rec.title}
                  </h4>
                  <p className="text-sm text-gray-700 mb-3">
                    {rec.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      rec.impact === 'High' 
                        ? 'bg-primary-100 text-primary-700' 
                        : rec.impact === 'Medium'
                        ? 'bg-secondary-100 text-secondary-700'
                        : 'bg-accent-100 text-accent-700'
                    }`}>
                      {rec.impact} Impact
                    </span>
                    <Button size="sm" variant="outline">
                      {rec.action}
                      <ArrowRightIcon className="w-3 h-3 ml-1" />
                    </Button>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
        
        <div className="mt-6 pt-4 border-t border-gray-100">
          <Button variant="outline" className="w-full">
            <LightBulbIcon className="w-4 h-4 mr-2" />
            View All Recommendations
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
