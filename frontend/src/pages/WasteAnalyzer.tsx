import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { AIWasteAnalyzer } from '../components/ai/AIWasteAnalyzer';
import { useUserStore } from '../store/userStore';
import { ArrowLeftIcon, SparklesIcon } from '@heroicons/react/24/outline';

export const WasteAnalyzer: React.FC = () => {
  const { profile } = useUserStore();
  const userType = profile?.userType || 'individual';

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      <div className="px-6 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <div className="flex items-center mb-6">
              <Button variant="ghost" className="mr-4">
                <ArrowLeftIcon className="w-4 h-4 mr-2" />
                Back to Dashboard
              </Button>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <SparklesIcon className="w-10 h-10 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                AI Waste Analyzer
              </h1>
              <p className="text-gray-600">
                Analyze your waste with advanced AI technology and get personalized recommendations
              </p>
            </div>
          </motion.div>

          {/* AI Analyzer Component */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <AIWasteAnalyzer
              wasteTypes={profile?.wasteTypes || {}}
              onAnalysisComplete={(analysis) => {
                console.log('Analysis complete:', analysis);
              }}
              userType={userType}
            />
          </motion.div>
        </div>
      </div>
    </div>
  );
};
