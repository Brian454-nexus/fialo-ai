import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../ui/Card';
import { Button } from '../ui/Button';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import {
  CameraIcon,
  MicrophoneIcon,
  PencilIcon,
  XIcon,
  SparklesIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

interface SmartWasteDetectorProps {
  onDetectionComplete: (detectedTypes: Record<string, number>) => void;
  onClose: () => void;
  userType: 'individual' | 'company';
}

const detectionModes = [
  {
    id: 'camera',
    title: 'Camera Detection',
    icon: CameraIcon,
    description: 'Take a photo of your waste and let AI identify the types',
    color: 'from-blue-400 to-blue-600',
  },
  {
    id: 'voice',
    title: 'Voice Description',
    icon: MicrophoneIcon,
    description: 'Describe your waste verbally and AI will analyze it',
    color: 'from-green-400 to-green-600',
  },
  {
    id: 'text',
    title: 'Text Description',
    icon: PencilIcon,
    description: 'Type a description of your waste for AI analysis',
    color: 'from-purple-400 to-purple-600',
  },
];

const mockDetectedWaste = {
  individual: {
    food_scraps: 3.2,
    market_waste: 1.5,
    agricultural_biomass: 0.8,
  },
  company: {
    food_scraps: 45.0,
    market_waste: 32.0,
    agricultural_biomass: 18.0,
    wood_biomass: 12.0,
  },
};

export const SmartWasteDetector: React.FC<SmartWasteDetectorProps> = ({
  onDetectionComplete,
  onClose,
  userType,
}) => {
  const [currentMode, setCurrentMode] = useState<string | null>(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [detectionStep, setDetectionStep] = useState(0);
  const [detectedTypes, setDetectedTypes] = useState<Record<string, number> | null>(null);
  const [textDescription, setTextDescription] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const detectionSteps = [
    { title: 'Processing input...', icon: SparklesIcon },
    { title: 'Analyzing waste composition...', icon: CameraIcon },
    { title: 'Identifying waste types...', icon: CheckCircleIcon },
    { title: 'Calculating quantities...', icon: ExclamationTriangleIcon },
  ];

  const handleModeSelect = (modeId: string) => {
    setCurrentMode(modeId);
  };

  const handleCameraCapture = () => {
    fileInputRef.current?.click();
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      startDetection();
    }
  };

  const handleVoiceRecord = () => {
    setIsRecording(true);
    // Simulate voice recording
    setTimeout(() => {
      setIsRecording(false);
      startDetection();
    }, 3000);
  };

  const handleTextSubmit = () => {
    if (textDescription.trim()) {
      startDetection();
    }
  };

  const startDetection = async () => {
    setIsDetecting(true);
    setDetectionStep(0);

    // Simulate AI detection process
    for (let i = 0; i < detectionSteps.length; i++) {
      setDetectionStep(i);
      await new Promise(resolve => setTimeout(resolve, 1500));
    }

    // Mock detection results
    const results = mockDetectedWaste[userType];
    setDetectedTypes(results);
    setIsDetecting(false);
  };

  const handleAcceptResults = () => {
    if (detectedTypes) {
      onDetectionComplete(detectedTypes);
    }
  };

  const handleRetry = () => {
    setCurrentMode(null);
    setDetectedTypes(null);
    setIsDetecting(false);
    setDetectionStep(0);
    setTextDescription('');
  };

  const renderModeSelection = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          🤖 AI Waste Detection
        </h3>
        <p className="text-gray-600">
          Choose how you'd like to describe your waste to our AI
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {detectionModes.map((mode, index) => (
          <motion.div
            key={mode.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card
              hover
              className="cursor-pointer"
              onClick={() => handleModeSelect(mode.id)}
            >
              <CardContent className="p-6 text-center">
                <div className={`w-16 h-16 bg-gradient-to-br ${mode.color} rounded-full flex items-center justify-center mx-auto mb-4`}>
                  <mode.icon className="w-8 h-8 text-white" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">
                  {mode.title}
                </h4>
                <p className="text-sm text-gray-600">
                  {mode.description}
                </p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );

  const renderCameraMode = () => (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          📸 Camera Detection
        </h3>
        <p className="text-gray-600">
          Take a clear photo of your waste for AI analysis
        </p>
      </div>

      <Card>
        <CardContent className="p-8">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <CameraIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h4 className="text-lg font-semibold text-gray-900 mb-2">
              Upload Waste Photo
            </h4>
            <p className="text-gray-600 mb-4">
              Take a clear photo showing your waste types
            </p>
            <Button onClick={handleCameraCapture}>
              <CameraIcon className="w-4 h-4 mr-2" />
              Take Photo
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              capture="environment"
              onChange={handleFileUpload}
              className="hidden"
            />
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );

  const renderVoiceMode = () => (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          🎤 Voice Description
        </h3>
        <p className="text-gray-600">
          Describe your waste verbally and AI will analyze it
        </p>
      </div>

      <Card>
        <CardContent className="p-8 text-center">
          <div className={`w-32 h-32 rounded-full flex items-center justify-center mx-auto mb-6 ${
            isRecording 
              ? 'bg-red-500 animate-pulse' 
              : 'bg-gradient-to-br from-green-400 to-green-600'
          }`}>
            <MicrophoneIcon className="w-16 h-16 text-white" />
          </div>
          <h4 className="text-lg font-semibold text-gray-900 mb-2">
            {isRecording ? 'Listening...' : 'Tap to Record'}
          </h4>
          <p className="text-gray-600 mb-4">
            {isRecording 
              ? 'Speak clearly about your waste types and quantities'
              : 'Describe your waste: "We have food scraps, vegetable peels, and some paper waste"'
            }
          </p>
          <Button
            onClick={handleVoiceRecord}
            disabled={isRecording}
            variant={isRecording ? 'secondary' : 'primary'}
          >
            {isRecording ? 'Recording...' : 'Start Recording'}
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  );

  const renderTextMode = () => (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          ✍️ Text Description
        </h3>
        <p className="text-gray-600">
          Describe your waste in detail for AI analysis
        </p>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="space-y-4">
            <div>
              <label className="label">Describe your waste</label>
              <textarea
                value={textDescription}
                onChange={(e) => setTextDescription(e.target.value)}
                rows={4}
                className="input"
                placeholder="Example: 'We have about 2kg of food scraps daily from cooking, 1kg of vegetable peels, some garden waste, and occasional paper products. We also have some wood chips from our backyard.'"
              />
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2">💡 Tips for better detection:</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Mention specific waste types (food scraps, paper, wood, etc.)</li>
                <li>• Include approximate quantities (kg, daily, weekly)</li>
                <li>• Describe the source (kitchen, garden, office, etc.)</li>
                <li>• Mention any special characteristics</li>
              </ul>
            </div>
            <Button
              onClick={handleTextSubmit}
              disabled={!textDescription.trim()}
              className="w-full"
            >
              <SparklesIcon className="w-4 h-4 mr-2" />
              Analyze with AI
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );

  const renderDetectionProgress = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="text-center">
        <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
          <SparklesIcon className="w-10 h-10 text-white" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          AI is analyzing your waste...
        </h3>
        <p className="text-gray-600">
          Our advanced AI is processing your input to identify waste types and quantities
        </p>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="space-y-4">
            {detectionSteps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0.3 }}
                animate={{ 
                  opacity: index <= detectionStep ? 1 : 0.3,
                  scale: index === detectionStep ? 1.05 : 1,
                }}
                transition={{ duration: 0.5 }}
                className={`flex items-center p-3 rounded-lg ${
                  index <= detectionStep 
                    ? 'bg-primary-50 border border-primary-200' 
                    : 'bg-gray-50'
                }`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                  index < detectionStep 
                    ? 'bg-primary-600 text-white' 
                    : index === detectionStep
                    ? 'bg-primary-100 text-primary-600'
                    : 'bg-gray-200 text-gray-400'
                }`}>
                  {index < detectionStep ? (
                    <CheckCircleIcon className="w-5 h-5" />
                  ) : index === detectionStep ? (
                    <LoadingSpinner size="sm" />
                  ) : (
                    <step.icon className="w-5 h-5" />
                  )}
                </div>
                <div>
                  <h4 className="font-medium text-gray-900">{step.title}</h4>
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );

  const renderResults = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="text-center">
        <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircleIcon className="w-10 h-10 text-white" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          🎉 Detection Complete!
        </h3>
        <p className="text-gray-600">
          AI has identified your waste types and estimated quantities
        </p>
      </div>

      <Card>
        <CardHeader>
          <h4 className="text-lg font-semibold text-gray-900">
            Detected Waste Types
          </h4>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {detectedTypes && Object.entries(detectedTypes).map(([type, weight]) => (
              <div key={type} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <span className="text-lg mr-3">
                    {type === 'food_scraps' && '🍎'}
                    {type === 'market_waste' && '🥬'}
                    {type === 'agricultural_biomass' && '🌾'}
                    {type === 'animal_waste' && '🐄'}
                    {type === 'wood_biomass' && '🌳'}
                  </span>
                  <span className="font-medium capitalize">
                    {type.replace('_', ' ')}
                  </span>
                </div>
                <span className="text-sm text-gray-600">
                  {weight} kg/day
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="flex space-x-4">
        <Button
          variant="outline"
          onClick={handleRetry}
          className="flex-1"
        >
          Try Again
        </Button>
        <Button
          onClick={handleAcceptResults}
          className="flex-1"
        >
          Accept Results
        </Button>
      </div>
    </motion.div>
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="w-full max-w-2xl max-h-[90vh] overflow-y-auto"
      >
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">
                AI Waste Detection
              </h2>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
              >
                <XIcon className="w-4 h-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <AnimatePresence mode="wait">
              {!currentMode && !isDetecting && !detectedTypes && renderModeSelection()}
              {currentMode === 'camera' && !isDetecting && !detectedTypes && renderCameraMode()}
              {currentMode === 'voice' && !isDetecting && !detectedTypes && renderVoiceMode()}
              {currentMode === 'text' && !isDetecting && !detectedTypes && renderTextMode()}
              {isDetecting && renderDetectionProgress()}
              {detectedTypes && renderResults()}
            </AnimatePresence>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};
