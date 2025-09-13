import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useUserStore } from '../store/userStore';
import { useWasteStore } from '../store/wasteStore';
import { useAuthStore } from '../store/authStore';
import { DashboardHeader } from '../components/dashboard/DashboardHeader';
import { StatsOverview } from '../components/dashboard/StatsOverview';
import { EnergyChart } from '../components/dashboard/EnergyChart';
import { WasteComposition } from '../components/dashboard/WasteComposition';
import { AIRecommendations } from '../components/dashboard/AIRecommendations';
import { RecentActivity } from '../components/dashboard/RecentActivity';
import { QuickActions } from '../components/dashboard/QuickActions';
import { ImpactVisualization } from '../components/dashboard/ImpactVisualization';
import {
  PlusIcon,
  ChartBarIcon,
  BoltIcon,
  GlobeAltIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';

export const Dashboard: React.FC = () => {
  const { user } = useAuthStore();
  const { profile } = useUserStore();
  const { entries, getTotalStats } = useWasteStore();
  const [selectedTimeRange, setSelectedTimeRange] = useState('7d');
  const [isLoading, setIsLoading] = useState(true);

  const totalStats = getTotalStats();
  const userType = profile?.userType || 'individual';

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => setIsLoading(false), 1000);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
            <SparklesIcon className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Loading your dashboard...
          </h3>
          <p className="text-gray-600">Preparing your personalized insights</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      {/* Header */}
      <DashboardHeader 
        user={user} 
        userType={userType}
        onTimeRangeChange={setSelectedTimeRange}
        selectedTimeRange={selectedTimeRange}
      />

      <div className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Welcome Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  Welcome back, {user?.name}! 👋
                </h1>
                <p className="text-gray-600">
                  {userType === 'individual' 
                    ? 'Track your waste-to-energy journey and environmental impact'
                    : 'Monitor your waste processing operations and optimization results'
                  }
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <Button variant="outline">
                  <ChartBarIcon className="w-4 h-4 mr-2" />
                  View Reports
                </Button>
                <Button>
                  <PlusIcon className="w-4 h-4 mr-2" />
                  Add Waste Entry
                </Button>
              </div>
            </div>
          </motion.div>

          {/* Stats Overview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="mb-8"
          >
            <StatsOverview 
              stats={totalStats} 
              userType={userType}
              timeRange={selectedTimeRange}
            />
          </motion.div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            {/* Left Column - Charts */}
            <div className="lg:col-span-2 space-y-8">
              {/* Energy Generation Chart */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center mr-3">
                          <BoltIcon className="w-5 h-5 text-white" />
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">
                            Energy Generation
                          </h3>
                          <p className="text-sm text-gray-600">
                            Daily energy production over time
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button size="sm" variant="outline">
                          7D
                        </Button>
                        <Button size="sm" variant="outline">
                          30D
                        </Button>
                        <Button size="sm" variant="primary">
                          90D
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <EnergyChart entries={entries} timeRange={selectedTimeRange} />
                  </CardContent>
                </Card>
              </motion.div>

              {/* Waste Composition */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <WasteComposition entries={entries} userType={userType} />
              </motion.div>

              {/* Impact Visualization */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <ImpactVisualization stats={totalStats} userType={userType} />
              </motion.div>
            </div>

            {/* Right Column - Recommendations & Activity */}
            <div className="space-y-8">
              {/* AI Recommendations */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <AIRecommendations userType={userType} />
              </motion.div>

              {/* Quick Actions */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <QuickActions userType={userType} />
              </motion.div>

              {/* Recent Activity */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <RecentActivity entries={entries.slice(0, 5)} />
              </motion.div>
            </div>
          </div>

          {/* Bottom Section - Additional Insights */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="grid grid-cols-1 md:grid-cols-2 gap-8"
          >
            {/* Environmental Impact */}
            <Card className="bg-gradient-to-br from-green-50 to-emerald-50">
              <CardContent className="p-6">
                <div className="flex items-center mb-4">
                  <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center mr-3">
                    <GlobeAltIcon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Environmental Impact
                    </h3>
                    <p className="text-sm text-gray-600">
                      Your contribution to a sustainable future
                    </p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {Math.round(totalStats.totalCo2Avoided / 22)}
                    </div>
                    <div className="text-sm text-gray-600">Trees Planted</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {(totalStats.totalCo2Avoided / 4000).toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-600">Cars Off Road</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Performance Metrics */}
            <Card className="bg-gradient-to-br from-blue-50 to-indigo-50">
              <CardContent className="p-6">
                <div className="flex items-center mb-4">
                  <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center mr-3">
                    <ChartBarIcon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Performance Metrics
                    </h3>
                    <p className="text-sm text-gray-600">
                      Your efficiency and optimization scores
                    </p>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Energy Efficiency</span>
                    <span className="text-sm font-semibold text-blue-600">92%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: '92%' }}></div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Waste Utilization</span>
                    <span className="text-sm font-semibold text-blue-600">87%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: '87%' }}></div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
};
