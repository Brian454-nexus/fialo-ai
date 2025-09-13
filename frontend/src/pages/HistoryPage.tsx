import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useWasteStore } from '../store/wasteStore';
import { formatDate, formatNumber, formatCurrency } from '../../lib/utils';
import { ArrowLeftIcon, CalendarIcon, BoltIcon, GlobeAltIcon } from '@heroicons/react/24/outline';

export const HistoryPage: React.FC = () => {
  const { entries, getTotalStats } = useWasteStore();
  const totalStats = getTotalStats();

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      <div className="px-6 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  Waste History
                </h1>
                <p className="text-gray-600">
                  Track your waste-to-energy journey over time
                </p>
              </div>
              <Button>
                <CalendarIcon className="w-4 h-4 mr-2" />
                Filter by Date
              </Button>
            </div>
          </motion.div>

          {/* Summary Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
          >
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-2xl font-bold text-primary-600 mb-1">
                  {entries.length}
                </div>
                <div className="text-sm text-gray-600">Total Entries</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-2xl font-bold text-secondary-600 mb-1">
                  {formatNumber(totalStats.totalWaste, 1)} kg
                </div>
                <div className="text-sm text-gray-600">Waste Processed</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-2xl font-bold text-accent-600 mb-1">
                  {formatNumber(totalStats.totalEnergy, 1)} kWh
                </div>
                <div className="text-sm text-gray-600">Energy Generated</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-2xl font-bold text-green-600 mb-1">
                  {formatCurrency(totalStats.totalSavings)}
                </div>
                <div className="text-sm text-gray-600">Total Savings</div>
              </CardContent>
            </Card>
          </motion.div>

          {/* History Entries */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="space-y-4"
          >
            {entries.length === 0 ? (
              <Card>
                <CardContent className="p-12 text-center">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CalendarIcon className="w-8 h-8 text-gray-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    No waste entries yet
                  </h3>
                  <p className="text-gray-600 mb-6">
                    Start tracking your waste-to-energy journey by adding your first entry.
                  </p>
                  <Button>
                    Add First Entry
                  </Button>
                </CardContent>
              </Card>
            ) : (
              entries.map((entry, index) => (
                <motion.div
                  key={entry.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card hover>
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center">
                          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center mr-3">
                            <BoltIcon className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h3 className="text-lg font-semibold text-gray-900">
                              Waste Entry
                            </h3>
                            <p className="text-sm text-gray-600">
                              {formatDate(entry.date)}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-medium text-gray-900">
                            {formatNumber(entry.totalWeight, 1)} kg
                          </div>
                          <div className="text-xs text-gray-500">Total Weight</div>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div className="text-center">
                          <div className="text-lg font-bold text-primary-600">
                            {formatNumber(entry.energyGenerated, 1)} kWh
                          </div>
                          <div className="text-xs text-gray-500">Energy Generated</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-green-600">
                            {formatNumber(entry.co2Avoided, 1)} kg
                          </div>
                          <div className="text-xs text-gray-500">CO₂ Avoided</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-accent-600">
                            {formatCurrency(entry.costSavings)}
                          </div>
                          <div className="text-xs text-gray-500">Cost Savings</div>
                        </div>
                      </div>

                      {entry.description && (
                        <div className="bg-gray-50 p-3 rounded-lg mb-4">
                          <p className="text-sm text-gray-700">
                            {entry.description}
                          </p>
                        </div>
                      )}

                      {entry.aiAnalysis && (
                        <div className="bg-primary-50 p-3 rounded-lg">
                          <h4 className="text-sm font-semibold text-primary-900 mb-2">
                            AI Analysis
                          </h4>
                          <div className="space-y-1">
                            {entry.aiAnalysis.recommendations.slice(0, 2).map((rec: string, idx: number) => (
                              <p key={idx} className="text-xs text-primary-800">
                                • {rec}
                              </p>
                            ))}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </motion.div>
              ))
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};
