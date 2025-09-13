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
  BuildingOfficeIcon,
  ChartBarIcon,
  SparklesIcon,
  BoltIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  CurrencyDollarIcon,
  UsersIcon,
} from '@heroicons/react/24/outline';

interface FormData {
  companyName: string;
  location: string;
  currentProcessingMethod: string;
  operationalCost: number;
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

const processingMethods = [
  'Landfill',
  'Incineration',
  'Composting',
  'Recycling',
  'Biogas Production',
  'Pyrolysis',
  'Other',
];

export const CompanyOnboarding: React.FC = () => {
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
  } = useForm<FormData>({
    defaultValues: {
      operationalCost: 0,
    },
  });

  const steps = [
    { number: 1, title: 'Company Information', icon: BuildingOfficeIcon },
    { number: 2, title: 'Waste Types & Quantities', icon: ChartBarIcon },
    { number: 3, title: 'AI Optimization', icon: SparklesIcon },
    { number: 4, title: 'Complete Setup', icon: BoltIcon },
  ];

  const onSubmit = async (data: FormData) => {
    try {
      // Update user profile
      updateProfile({
        userType: 'company',
        companyName: data.companyName,
        location: data.location,
        wasteTypes: selectedWasteTypes,
        currentProcessingMethod: data.currentProcessingMethod,
        operationalCost: data.operationalCost,
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
              <label className="label">Company Name</label>
              <input
                {...register('companyName', { required: 'Company name is required' })}
                type="text"
                className={`input ${errors.companyName ? 'input-error' : ''}`}
                placeholder="Enter your company name"
              />
              {errors.companyName && (
                <p className="text-danger-500 text-sm mt-1">{errors.companyName.message}</p>
              )}
            </div>

            <div>
              <label className="label">Location</label>
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
              <label className="label">Current Processing Method</label>
              <select
                {...register('currentProcessingMethod', { required: 'Please select current processing method' })}
                className={`input ${errors.currentProcessingMethod ? 'input-error' : ''}`}
              >
                <option value="">Select current method</option>
                {processingMethods.map((method) => (
                  <option key={method} value={method}>
                    {method}
                  </option>
                ))}
              </select>
              {errors.currentProcessingMethod && (
                <p className="text-danger-500 text-sm mt-1">{errors.currentProcessingMethod.message}</p>
              )}
            </div>

            <div>
              <label className="label">Daily Operational Cost (USD)</label>
              <input
                {...register('operationalCost', {
                  required: 'Please enter operational cost',
                  min: { value: 0, message: 'Cost must be positive' },
                })}
                type="number"
                step="0.01"
                min="0"
                className={`input ${errors.operationalCost ? 'input-error' : ''}`}
                placeholder="0.00"
              />
              {errors.operationalCost && (
                <p className="text-danger-500 text-sm mt-1">{errors.operationalCost.message}</p>
              )}
            </div>

            <div className="bg-secondary-50 p-4 rounded-lg">
              <h4 className="font-semibold text-secondary-900 mb-2">💼 Company Benefits</h4>
              <ul className="text-sm text-secondary-800 space-y-1">
                <li>• Optimize waste processing operations</li>
                <li>• Maximize energy generation and revenue</li>
                <li>• Reduce operational costs significantly</li>
                <li>• Access advanced analytics and reporting</li>
                <li>• Scale operations with AI recommendations</li>
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
              userType="company"
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
              userType="company"
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
              <div className="bg-gradient-to-r from-secondary-50 to-primary-50 p-6 rounded-xl">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  🎉 Your AI Optimization Plan is Ready!
                </h3>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-secondary-600">
                      {aiAnalysis.energyGenerated?.toFixed(1) || '0'} kWh
                    </div>
                    <div className="text-sm text-gray-600">Daily Energy</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-primary-600">
                      ${aiAnalysis.costSavings?.toFixed(2) || '0'}
                    </div>
                    <div className="text-sm text-gray-600">Daily Revenue</div>
                  </div>
                </div>
                <p className="text-gray-700 text-sm">
                  Based on your waste processing, our AI predicts you can generate{' '}
                  <strong>{aiAnalysis.energyGenerated?.toFixed(1) || '0'} kWh</strong> of energy daily,
                  generating <strong>${aiAnalysis.costSavings?.toFixed(2) || '0'}</strong> in revenue per day!
                </p>
              </div>
            )}

            <div>
              <label className="label">Describe your waste operations (optional)</label>
              <textarea
                {...register('wasteDescription')}
                rows={3}
                className="input"
                placeholder="Describe your current waste processing operations, challenges, and goals..."
              />
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2">🚀 What's Next?</h4>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Get detailed optimization recommendations</li>
                <li>• Access advanced analytics dashboard</li>
                <li>• Monitor operational efficiency in real-time</li>
                <li>• Connect with suppliers and partners</li>
                <li>• Scale operations with AI guidance</li>
              </ul>
            </div>
          </motion.div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 via-white to-primary-50">
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
              <div className="w-12 h-12 bg-gradient-to-br from-secondary-500 to-primary-500 rounded-xl flex items-center justify-center">
                <BuildingOfficeIcon className="w-6 h-6 text-white" />
              </div>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Welcome to Fialo AI for Companies!
            </h1>
            <p className="text-gray-600">
              Let's optimize your waste processing operations with AI
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
                        ? 'bg-secondary-600 text-white'
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
                      currentStep >= step.number ? 'text-secondary-600' : 'text-gray-500'
                    }`}>
                      {step.title}
                    </div>
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`w-8 h-0.5 mx-4 ${
                      currentStep > step.number ? 'bg-secondary-600' : 'bg-gray-200'
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
                <div className="w-8 h-8 bg-secondary-100 rounded-lg flex items-center justify-center mr-3">
                  <steps[currentStep - 1].icon className="w-5 h-5 text-secondary-600" />
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
                  (currentStep === 1 && (!watch('companyName') || !watch('location') || !watch('currentProcessingMethod'))) ||
                  (currentStep === 2 && Object.keys(selectedWasteTypes).length === 0)
                }
                variant="secondary"
              >
                Next
                <ArrowRightIcon className="w-4 h-4 ml-2" />
              </Button>
            ) : (
              <Button
                type="submit"
                onClick={handleSubmit(onSubmit)}
                className="bg-gradient-to-r from-secondary-600 to-primary-600 hover:from-secondary-700 hover:to-primary-700"
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
