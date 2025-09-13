import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useUserStore } from '../store/userStore';
import {
  UserGroupIcon,
  BuildingOfficeIcon,
  HomeIcon,
  ChartBarIcon,
  BoltIcon,
  GlobeAltIcon,
} from '@heroicons/react/24/outline';

const userTypes = [
  {
    type: 'individual',
    title: 'Individual User',
    subtitle: 'Personal & Household',
    icon: UserGroupIcon,
    description: 'Perfect for households, small businesses, and individuals looking to convert their personal waste into energy.',
    features: [
      'Convert 1-100 kg of waste daily',
      'Generate energy for your home',
      'Track personal environmental impact',
      'Get personalized AI recommendations',
      'Join a community of eco-conscious users',
      'Save money on energy bills',
    ],
    color: 'primary',
    examples: ['Households', 'Small restaurants', 'Farmers', 'Students', 'Homeowners'],
  },
  {
    type: 'company',
    title: 'Waste Company',
    subtitle: 'Business & Commercial',
    icon: BuildingOfficeIcon,
    description: 'Optimize large-scale waste processing operations and maximize energy generation for commercial use.',
    features: [
      'Process 100+ kg of waste daily',
      'Optimize conversion strategies',
      'Maximize ROI and efficiency',
      'Advanced analytics and reporting',
      'Scale operations effectively',
      'Generate revenue from energy sales',
    ],
    color: 'secondary',
    examples: ['Waste collectors', 'Recycling companies', 'Municipal services', 'NGOs', 'Industrial facilities'],
  },
];

const benefits = [
  {
    icon: BoltIcon,
    title: 'AI-Powered Optimization',
    description: 'Advanced machine learning algorithms optimize your waste-to-energy conversion process.',
  },
  {
    icon: ChartBarIcon,
    title: 'Real-time Analytics',
    description: 'Track your impact with detailed analytics, energy generation, and environmental metrics.',
  },
  {
    icon: GlobeAltIcon,
    title: 'Environmental Impact',
    description: 'Reduce carbon footprint and contribute to a sustainable future for our planet.',
  },
];

export const UserTypeSelection: React.FC = () => {
  const navigate = useNavigate();
  const { setUserType } = useUserStore();

  const handleUserTypeSelect = (userType: 'individual' | 'company') => {
    setUserType(userType);
    navigate('/onboarding');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      {/* Header */}
      <div className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <div className="flex items-center justify-center mb-6">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center">
                <span className="text-3xl">♻️</span>
              </div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              How will you use{' '}
              <span className="gradient-text">Fialo AI</span>?
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Choose your user type to get personalized recommendations and 
              optimize your waste-to-energy conversion journey.
            </p>
          </motion.div>

          {/* User Type Cards */}
          <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto mb-16">
            {userTypes.map((userType, index) => (
              <motion.div
                key={userType.type}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="h-full"
              >
                <Card hover className="p-8 h-full flex flex-col">
                  {/* Header */}
                  <div className="text-center mb-6">
                    <div className={`w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 ${
                      userType.color === 'primary' 
                        ? 'bg-gradient-to-br from-primary-100 to-primary-200' 
                        : 'bg-gradient-to-br from-secondary-100 to-secondary-200'
                    }`}>
                      <userType.icon className={`w-10 h-10 ${
                        userType.color === 'primary' ? 'text-primary-600' : 'text-secondary-600'
                      }`} />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {userType.title}
                    </h3>
                    <p className="text-lg text-gray-600 mb-4">
                      {userType.subtitle}
                    </p>
                    <p className="text-gray-700">
                      {userType.description}
                    </p>
                  </div>

                  {/* Features */}
                  <div className="flex-1 mb-8">
                    <h4 className="font-semibold text-gray-900 mb-4">What you'll get:</h4>
                    <ul className="space-y-3">
                      {userType.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-start">
                          <div className={`w-2 h-2 rounded-full mt-2 mr-3 flex-shrink-0 ${
                            userType.color === 'primary' ? 'bg-primary-500' : 'bg-secondary-500'
                          }`} />
                          <span className="text-gray-700">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Examples */}
                  <div className="mb-8">
                    <h4 className="font-semibold text-gray-900 mb-3">Perfect for:</h4>
                    <div className="flex flex-wrap gap-2">
                      {userType.examples.map((example, exampleIndex) => (
                        <span
                          key={exampleIndex}
                          className={`px-3 py-1 rounded-full text-sm ${
                            userType.color === 'primary'
                              ? 'bg-primary-100 text-primary-700'
                              : 'bg-secondary-100 text-secondary-700'
                          }`}
                        >
                          {example}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* CTA Button */}
                  <Button
                    onClick={() => handleUserTypeSelect(userType.type as 'individual' | 'company')}
                    variant={userType.color === 'primary' ? 'primary' : 'secondary'}
                    size="lg"
                    className="w-full"
                  >
                    Choose {userType.title}
                  </Button>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Benefits Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose Fialo AI?
            </h2>
            <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
              Our advanced AI technology makes waste-to-energy conversion simple, 
              efficient, and accessible to everyone.
            </p>
            
            <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              {benefits.map((benefit, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.5 + index * 0.1 }}
                >
                  <Card className="p-6 text-center">
                    <div className="w-12 h-12 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                      <benefit.icon className="w-6 h-6 text-primary-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {benefit.title}
                    </h3>
                    <p className="text-gray-600 text-sm">
                      {benefit.description}
                    </p>
                  </Card>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Back to Home */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.8 }}
            className="text-center"
          >
            <Button
              variant="ghost"
              onClick={() => navigate('/')}
              className="text-gray-600 hover:text-gray-900"
            >
              ← Back to Home
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
};
