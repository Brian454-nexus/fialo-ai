import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../ui/Card';
import { Button } from '../ui/Button';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import { SmartWasteDetector } from '../waste/SmartWasteDetector';
import { apiEndpoints } from '../../services/api';
import {
  SparklesIcon,
  BoltIcon,
  ChartBarIcon,
  GlobeAltIcon,
  LightBulbIcon,
  ArrowRightIcon,
  CameraIcon,
  MicrophoneIcon,
  PencilIcon,
} from '@heroicons/react/24/outline';

interface AIWasteAnalyzerProps {
  wasteTypes: Record<string, number>;
  onAnalysisComplete: (analysis: any) => void;
  userType: 'individual' | 'company';
}

const analysisSteps = [
  { id: 'analyzing', title: 'Analyzing waste composition...', icon: SparklesIcon },
  { id: 'optimizing', title: 'Optimizing conversion strategy...', icon: BoltIcon },
  { id: 'calculating', title: 'Calculating energy potential...', icon: ChartBarIcon },
  { id: 'assessing', title: 'Assessing environmental impact...', icon: GlobeAltIcon },
];

export const AIWasteAnalyzer: React.FC<AIWasteAnalyzerProps> = ({
  wasteTypes,
  onAnalysisComplete,
  userType,
}) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [analysis, setAnalysis] = useState<any>(null);
  const [showSmartDetector, setShowSmartDetector] = useState(false);
  const [wasteDescription, setWasteDescription] = useState('');

  const totalWaste = Object.values(wasteTypes).reduce((sum, weight) => sum + weight, 0);

  useEffect(() => {
    if (totalWaste > 0) {
      runAnalysis();
    }
  }, [wasteTypes]);

  const runAnalysis = async () => {
    setIsAnalyzing(true);
    setCurrentStep(0);

    try {
      // Simulate AI analysis steps
      for (let i = 0; i < analysisSteps.length; i++) {
        setCurrentStep(i);
        await new Promise(resolve => setTimeout(resolve, 1500));
      }

      // Call the actual API
      const response = await apiEndpoints.simulation.runPersonalSimulation({
        user_type: userType,
        user_data: {
          location: 'Nairobi, Kenya',
          waste_types: wasteTypes,
          daily_energy_needs_kwh: userType === 'individual' ? 10 : 50,
          current_energy_cost_per_kwh: 0.15,
        },
        simulation_days: 7,
        temperature_c: 25.0,
        humidity_percent: 60.0,
        rainfall_mm: 0.0,
        include_noise: true,
      });

      // Generate AI recommendations
      const recommendations = generateRecommendations(wasteTypes, response.data);
      
      const analysisResult = {
        energyGenerated: response.data.results.daily_averages.energy_generated_kwh,
        co2Avoided: response.data.results.daily_averages.co2_avoided_kg,
        costSavings: response.data.personal_impact.daily_savings_usd,
        recommendations,
        confidence: 0.92,
        conversionMethod: 'biogas',
        wasteComposition: wasteTypes,
        totalWaste,
        environmentalImpact: {
          treesEquivalent: Math.round(response.data.personal_impact.trees_equivalent),
          carsEquivalent: response.data.personal_impact.cars_equivalent,
        },
      };

      setAnalysis(analysisResult);
      onAnalysisComplete(analysisResult);
    } catch (error) {
      console.error('Analysis failed:', error);
      // Fallback to mock data
      const mockAnalysis = generateMockAnalysis(wasteTypes);
      setAnalysis(mockAnalysis);
      onAnalysisComplete(mockAnalysis);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const generateRecommendations = (wasteTypes: Record<string, number>, apiData: any) => {
    const recommendations = [];
    
    if (wasteTypes.food_scraps > 0) {
      recommendations.push({
        type: 'primary',
        title: 'Start with Biogas Digester',
        description: 'Food scraps are perfect for biogas production. You can generate clean cooking gas and electricity.',
        impact: 'High energy output with minimal processing',
        action: 'Consider a small home biogas digester',
      });
    }

    if (wasteTypes.agricultural_biomass > 0) {
      recommendations.push({
        type: 'secondary',
        title: 'Composting + Energy',
        description: 'Agricultural waste can be composted first, then used for energy generation.',
        impact: 'Dual benefit: soil improvement + energy',
        action: 'Set up composting system with energy recovery',
      });
    }

    if (wasteTypes.wood_biomass > 0) {
      recommendations.push({
        type: 'alternative',
        title: 'Direct Combustion',
        description: 'Wood biomass has high energy content and can be burned directly for heat.',
        impact: 'Immediate energy generation',
        action: 'Consider a wood gasifier or biomass stove',
      });
    }

    return recommendations;
  };

  const generateMockAnalysis = (wasteTypes: Record<string, number>) => {
    const totalWaste = Object.values(wasteTypes).reduce((sum, weight) => sum + weight, 0);
    const energyGenerated = totalWaste * 2.1; // Average energy per kg
    const co2Avoided = totalWaste * 0.5;
    const costSavings = energyGenerated * 0.15;

    return {
      energyGenerated,
      co2Avoided,
      costSavings,
      recommendations: generateRecommendations(wasteTypes, {}),
      confidence: 0.88,
      conversionMethod: 'biogas',
      wasteComposition: wasteTypes,
      totalWaste,
      environmentalImpact: {
        treesEquivalent: Math.round(co2Avoided / 22),
        carsEquivalent: co2Avoided / 4000,
      },
    };
  };

  const handleSmartDetection = (detectedTypes: Record<string, number>) => {
    setShowSmartDetector(false);
    // Update waste types and re-run analysis
    // This would be handled by the parent component
  };

  if (isAnalyzing) {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
            <SparklesIcon className="w-10 h-10 text-white" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            AI is analyzing your waste...
          </h3>
          <p className="text-gray-600">
            Our advanced AI is processing your waste data to provide personalized recommendations
          </p>
        </div>

        <Card>
          <CardContent className="p-8">
            <div className="space-y-6">
              {analysisSteps.map((step, index) => (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0.3 }}
                  animate={{ 
                    opacity: index <= currentStep ? 1 : 0.3,
                    scale: index === currentStep ? 1.05 : 1,
                  }}
                  transition={{ duration: 0.5 }}
                  className={`flex items-center p-4 rounded-lg ${
                    index <= currentStep 
                      ? 'bg-primary-50 border border-primary-200' 
                      : 'bg-gray-50'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center mr-4 ${
                    index < currentStep 
                      ? 'bg-primary-600 text-white' 
                      : index === currentStep
                      ? 'bg-primary-100 text-primary-600'
                      : 'bg-gray-200 text-gray-400'
                  }`}>
                    {index < currentStep ? (
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    ) : index === currentStep ? (
                      <LoadingSpinner size="sm" />
                    ) : (
                      <step.icon className="w-5 h-5" />
                    )}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">{step.title}</h4>
                    <p className="text-sm text-gray-600">
                      {index < currentStep ? 'Completed' : 
                       index === currentStep ? 'In progress...' : 'Pending'}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (analysis) {
    return (
      <div className="space-y-6">
        {/* Analysis Results Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <SparklesIcon className="w-10 h-10 text-white" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            🎉 AI Analysis Complete!
          </h3>
          <p className="text-gray-600">
            Your personalized waste-to-energy conversion strategy is ready
          </p>
        </motion.div>

        {/* Key Metrics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Card className="bg-gradient-to-r from-primary-50 to-secondary-50">
            <CardContent className="p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4 text-center">
                Your Daily Impact Potential
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-600">
                    {analysis.energyGenerated.toFixed(1)} kWh
                  </div>
                  <div className="text-sm text-gray-600">Energy Generated</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-secondary-600">
                    ${analysis.costSavings.toFixed(2)}
                  </div>
                  <div className="text-sm text-gray-600">Daily Savings</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-accent-600">
                    {analysis.co2Avoided.toFixed(1)} kg
                  </div>
                  <div className="text-sm text-gray-600">CO₂ Avoided</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {analysis.environmentalImpact.treesEquivalent}
                  </div>
                  <div className="text-sm text-gray-600">Trees Equivalent</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* AI Recommendations */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <Card>
            <CardHeader>
              <h4 className="text-lg font-semibold text-gray-900 flex items-center">
                <LightBulbIcon className="w-5 h-5 mr-2 text-yellow-500" />
                AI Recommendations
              </h4>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analysis.recommendations.map((rec: any, index: number) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.6 + index * 0.1 }}
                    className={`p-4 rounded-lg border-l-4 ${
                      rec.type === 'primary' 
                        ? 'bg-primary-50 border-primary-500' 
                        : rec.type === 'secondary'
                        ? 'bg-secondary-50 border-secondary-500'
                        : 'bg-accent-50 border-accent-500'
                    }`}
                  >
                    <h5 className="font-semibold text-gray-900 mb-2">
                      {rec.title}
                    </h5>
                    <p className="text-gray-700 mb-2">
                      {rec.description}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">
                        Impact: {rec.impact}
                      </span>
                      <Button size="sm" variant="outline">
                        Learn More
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Additional Options */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="flex flex-col sm:flex-row gap-4"
        >
          <Button
            variant="outline"
            onClick={() => setShowSmartDetector(true)}
            className="flex-1"
          >
            <CameraIcon className="w-4 h-4 mr-2" />
            Re-analyze with AI Detection
          </Button>
          <Button
            variant="outline"
            onClick={() => setWasteDescription('')}
            className="flex-1"
          >
            <PencilIcon className="w-4 h-4 mr-2" />
            Add Waste Description
          </Button>
        </motion.div>

        {/* Waste Description Input */}
        {wasteDescription !== null && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            transition={{ duration: 0.5 }}
          >
            <Card>
              <CardContent className="p-4">
                <label className="label">Describe your waste (optional)</label>
                <textarea
                  value={wasteDescription}
                  onChange={(e) => setWasteDescription(e.target.value)}
                  rows={3}
                  className="input"
                  placeholder="Tell us more about your waste: 'We have a lot of vegetable peels from cooking, some garden waste, and occasional paper products...'"
                />
                <p className="text-xs text-gray-500 mt-2">
                  This helps our AI provide more accurate recommendations
                </p>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          AI Waste Analysis
        </h3>
        <p className="text-gray-600 mb-6">
          Let our AI analyze your waste and provide personalized conversion recommendations
        </p>
      </div>

      <Card>
        <CardContent className="p-8 text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <SparklesIcon className="w-8 h-8 text-primary-600" />
          </div>
          <h4 className="text-lg font-semibold text-gray-900 mb-2">
            Ready to analyze your waste?
          </h4>
          <p className="text-gray-600 mb-6">
            We'll process your waste data and provide personalized recommendations for optimal energy conversion.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              onClick={runAnalysis}
              disabled={totalWaste === 0}
              size="lg"
            >
              <SparklesIcon className="w-5 h-5 mr-2" />
              Start AI Analysis
            </Button>
            <Button
              variant="outline"
              onClick={() => setShowSmartDetector(true)}
              size="lg"
            >
              <CameraIcon className="w-5 h-5 mr-2" />
              Smart Detection
            </Button>
          </div>

          {totalWaste === 0 && (
            <p className="text-sm text-gray-500 mt-4">
              Please select waste types first to enable analysis
            </p>
          )}
        </CardContent>
      </Card>

      {/* Smart Detector Modal */}
      {showSmartDetector && (
        <SmartWasteDetector
          onDetectionComplete={handleSmartDetection}
          onClose={() => setShowSmartDetector(false)}
          userType={userType}
        />
      )}
    </div>
  );
};
