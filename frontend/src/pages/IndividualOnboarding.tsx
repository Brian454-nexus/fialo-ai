import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useUserStore } from '../store/userStore';
import { useWasteStore } from '../store/wasteStore';
import { WasteTypeSelector } from '../components/waste/WasteTypeSelector';
import { AIWasteAnalyzer } from '../components/ai/AIWasteAnalyzer';
import {
  MapPinIcon,
  BoltIcon,
  ChartBarIcon,
  SparklesIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
} from '@heroicons/react/24/outline';

interface FormData {
  location: string;
  dailyEnergyNeeds: number;
  currentEnergyCost: number;
  wasteDescription?: string;
}

const locations = [
  'Nairobi, Kenya',
  'Kampala, Uganda',
  'Dar es Salaam, Tanzania',
  'Kigali, Rwanda',
  'Addis Ababa, Ethiopia',
  'Lagos, Nigeria',
  'Accra, Ghana',
  'Cairo, Egypt',
  'Other',
];

export const IndividualOnboarding: React.FC = () => {
  const navigate = useNavigate();
  const { updateProfile } = useUserStore();
  const { addEntry } = useWasteStore();
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedWasteTypes, setSelectedWasteTypes] = useState<Record<string, number>>({});
  const [aiAnalysis, setAiAnalysis] = useState<any>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<FormData>({
    defaultValues: {
      dailyEnergyNeeds: 10,
      currentEnergyCost: 0.15,
    },
  });

  const dailyEnergyNeeds = watch('dailyEnergyNeeds');

  const steps = [
    { number: 1, title: 'Location & Energy Needs', icon: MapPinIcon },
    { number: 2, title: 'Waste Types', icon: ChartBarIcon },
    { number: 3, title: 'AI Analysis', icon: SparklesIcon },
    { number: 4, title: 'Complete Setup', icon: BoltIcon },
  ];

  const onSubmit = async (data: FormData) => {
    try {
      // Update user profile
      updateProfile({
        location: data.location,
        energyNeeds: data.dailyEnergyNeeds,
        wasteTypes: selectedWasteTypes,
      });

      // Create initial waste entry if AI analysis is available
      if (aiAnalysis) {
        addEntry({
          date: new Date().toISOString(),
          wasteTypes: selectedWasteTypes,
          totalWeight: Object.values(selectedWasteTypes).reduce((sum, weight) => sum + weight, 0),
          energyGenerated: aiAnalysis.energyGenerated || 0,
          co2Avoided: aiAnalysis.co2Avoided || 0,
          costSavings: aiAnalysis.costSavings || 0,
          description: data.wasteDescription,
          aiAnalysis: {
            recommendations: aiAnalysis.recommendations || [],
            confidence: aiAnalysis.confidence || 0.8,
            conversionMethod: aiAnalysis.conversionMethod || 'biogas',
          },
        });
      }

      navigate('/dashboard');
    } catch (error) {
      console.error('Onboarding failed:', error);
    }
  };

  const nextStep = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
          >
            <div>
              <label className="label">Your Location</label>
              <select
                {...register('location', { required: 'Please select your location' })}
                className={`input ${errors.location ? 'input-error' : ''}`}
              >
                <option value="">Select your location</option>
                {locations.map((location) => (
                  <option key={location} value={location}>
                    {location}
                  </option>
                ))}
              </select>
              {errors.location && (
                <p className="text-danger-500 text-sm mt-1">{errors.location.message}</p>
              )}
            </div>

            <div>
              <label className="label">
                Daily Energy Needs (kWh)
                <span className="text-sm text-gray-500 ml-2">
                  Current: {dailyEnergyNeeds} kWh/day
                </span>
              </label>
              <input
                type="range"
                min="1"
                max="50"
                step="1"
                {...register('dailyEnergyNeeds')}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-sm text-gray-500 mt-1">
                <span>1 kWh</span>
                <span>50 kWh</span>
              </div>
            </div>

            <div>
              <label className="label">Current Energy Cost (USD/kWh)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                {...register('currentEnergyCost', {
                  required: 'Please enter your current energy cost',
                  min: { value: 0, message: 'Cost must be positive' },
                })}
                className={`input ${errors.currentEnergyCost ? 'input-error' : ''}`}
                placeholder="0.15"
              />
              {errors.currentEnergyCost && (
                <p className="text-danger-500 text-sm mt-1">{errors.currentEnergyCost.message}</p>
              )}
            </div>

            <div className="bg-primary-50 p-4 rounded-lg">
              <h4 className="font-semibold text-primary-900 mb-2">💡 Energy Usage Guide</h4>
              <ul className="text-sm text-primary-800 space-y-1">
                <li>• 1-5 kWh: Small household (lights, phone charging)</li>
                <li>• 5-15 kWh: Medium household (refrigerator, TV, basic appliances)</li>
                <li>• 15-30 kWh: Large household (air conditioning, multiple appliances)</li>
                <li>• 30+ kWh: Small business or energy-intensive home</li>
              </ul>
            </div>
          </motion.div>
        );

      case 2:
        return (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <WasteTypeSelector
              selectedTypes={selectedWasteTypes}
              onTypesChange={setSelectedWasteTypes}
              userType="individual"
            />
          </motion.div>
        );

      case 3:
        return (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <AIWasteAnalyzer
              wasteTypes={selectedWasteTypes}
              onAnalysisComplete={setAiAnalysis}
              userType="individual"
            />
          </motion.div>
        );

      case 4:
        return (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
          >
            {aiAnalysis && (
              <div className="bg-gradient-to-r from-primary-50 to-secondary-50 p-6 rounded-xl">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  🎉 Your AI Analysis is Ready!
                </h3>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-primary-600">
                      {aiAnalysis.energyGenerated?.toFixed(1) || '0'} kWh
                    </div>
                    <div className="text-sm text-gray-600">Daily Energy</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-secondary-600">
                      ${aiAnalysis.costSavings?.toFixed(2) || '0'}
                    </div>
                    <div className="text-sm text-gray-600">Daily Savings</div>
                  </div>
                </div>
                <p className="text-gray-700 text-sm">
                  Based on your waste types, our AI predicts you can generate{' '}
                  <strong>{aiAnalysis.energyGenerated?.toFixed(1) || '0'} kWh</strong> of energy daily,
                  saving you <strong>${aiAnalysis.costSavings?.toFixed(2) || '0'}</strong> per day!
                </p>
              </div>
            )}

            <div>
              <label className="label">Tell us about your waste (optional)</label>
              <textarea
                {...register('wasteDescription')}
                rows={3}
                className="input"
                placeholder="Describe your typical waste: 'We have a lot of food scraps from cooking, some garden waste, and occasional paper products...'"
              />
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2">🚀 What's Next?</h4>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Get personalized recommendations for waste conversion</li>
                <li>• Track your daily waste and energy generation</li>
                <li>• Monitor your environmental impact</li>
                <li>• Connect with local suppliers and resources</li>
              </ul>
            </div>
          </motion.div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      <div className="px-6 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-8"
          >
            <div className="flex items-center justify-center mb-4">
              <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
                <span className="text-2xl">♻️</span>
              </div>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Welcome to Fialo AI!
            </h1>
            <p className="text-gray-600">
              Let's set up your personalized waste-to-energy profile
            </p>
          </motion.div>

          {/* Progress Steps */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              {steps.map((step, index) => (
                <div key={step.number} className="flex items-center">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      currentStep >= step.number
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 text-gray-500'
                    }`}
                  >
                    {currentStep > step.number ? (
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      step.number
                    )}
                  </div>
                  <div className="ml-3 hidden sm:block">
                    <div className={`text-sm font-medium ${
                      currentStep >= step.number ? 'text-primary-600' : 'text-gray-500'
                    }`}>
                      {step.title}
                    </div>
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`w-8 h-0.5 mx-4 ${
                      currentStep > step.number ? 'bg-primary-600' : 'bg-gray-200'
                    }`} />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Step Content */}
          <Card className="mb-8">
            <CardHeader>
              <div className="flex items-center">
                <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center mr-3">
                  <steps[currentStep - 1].icon className="w-5 h-5 text-primary-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">
                    {steps[currentStep - 1].title}
                  </h2>
                  <p className="text-gray-600 text-sm">
                    Step {currentStep} of {steps.length}
                  </p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit(onSubmit)}>
                {renderStepContent()}
              </form>
            </CardContent>
          </Card>

          {/* Navigation */}
          <div className="flex justify-between">
            <Button
              type="button"
              variant="ghost"
              onClick={prevStep}
              disabled={currentStep === 1}
            >
              <ArrowLeftIcon className="w-4 h-4 mr-2" />
              Previous
            </Button>

            {currentStep < 4 ? (
              <Button
                type="button"
                onClick={nextStep}
                disabled={
                  (currentStep === 1 && !watch('location')) ||
                  (currentStep === 2 && Object.keys(selectedWasteTypes).length === 0)
                }
              >
                Next
                <ArrowRightIcon className="w-4 h-4 ml-2" />
              </Button>
            ) : (
              <Button
                type="submit"
                onClick={handleSubmit(onSubmit)}
                className="bg-gradient-to-r from-primary-600 to-secondary-600 hover:from-primary-700 hover:to-secondary-700"
              >
                Complete Setup
                <ArrowRightIcon className="w-4 h-4 ml-2" />
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
