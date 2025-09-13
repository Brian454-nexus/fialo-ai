import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../ui/Card';
import { Button } from '../ui/Button';
import { XIcon } from 'lucide-react';

interface WasteType {
  id: string;
  name: string;
  icon: string;
  description: string;
  energyPotential: string;
  color: string;
  examples: string[];
}

interface WasteWeightInputProps {
  wasteType: WasteType;
  currentWeight: number;
  onWeightChange: (weight: number) => void;
  onClose: () => void;
  userType: 'individual' | 'company';
}

const weightPresets = {
  individual: [
    { label: 'Small household', value: 2, description: '1-2 people' },
    { label: 'Medium household', value: 5, description: '3-4 people' },
    { label: 'Large household', value: 10, description: '5+ people' },
    { label: 'Small business', value: 20, description: 'Restaurant, shop' },
  ],
  company: [
    { label: 'Small operation', value: 50, description: 'Local collector' },
    { label: 'Medium operation', value: 200, description: 'Regional company' },
    { label: 'Large operation', value: 500, description: 'City-wide service' },
    { label: 'Industrial scale', value: 1000, description: 'Major facility' },
  ],
};

export const WasteWeightInput: React.FC<WasteWeightInputProps> = ({
  wasteType,
  currentWeight,
  onWeightChange,
  onClose,
  userType,
}) => {
  const [weight, setWeight] = useState(currentWeight);
  const [customWeight, setCustomWeight] = useState(currentWeight > 0 ? currentWeight.toString() : '');

  useEffect(() => {
    setWeight(currentWeight);
    setCustomWeight(currentWeight > 0 ? currentWeight.toString() : '');
  }, [currentWeight]);

  const handlePresetSelect = (presetWeight: number) => {
    setWeight(presetWeight);
    setCustomWeight(presetWeight.toString());
  };

  const handleCustomWeightChange = (value: string) => {
    setCustomWeight(value);
    const numValue = parseFloat(value);
    if (!isNaN(numValue) && numValue >= 0) {
      setWeight(numValue);
    }
  };

  const handleSave = () => {
    onWeightChange(weight);
    onClose();
  };

  const energyPotential = weight * parseFloat(wasteType.energyPotential.split(' ')[0]);
  const co2Avoided = weight * 0.5; // Approximate CO2 avoided per kg

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="w-full max-w-md"
      >
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <span className="text-2xl mr-3">{wasteType.icon}</span>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {wasteType.name}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Set daily amount
                  </p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
              >
                <XIcon className="w-4 h-4" />
              </Button>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Quick Presets */}
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-3">
                Quick Select ({userType === 'individual' ? 'Household size' : 'Operation size'})
              </h4>
              <div className="grid grid-cols-2 gap-2">
                {weightPresets[userType].map((preset, index) => (
                  <Button
                    key={index}
                    variant={weight === preset.value ? 'primary' : 'outline'}
                    size="sm"
                    onClick={() => handlePresetSelect(preset.value)}
                    className="text-left justify-start"
                  >
                    <div>
                      <div className="font-medium">{preset.label}</div>
                      <div className="text-xs opacity-75">{preset.description}</div>
                    </div>
                  </Button>
                ))}
              </div>
            </div>

            {/* Custom Weight Input */}
            <div>
              <label className="label">
                Custom Amount (kg/day)
              </label>
              <div className="flex items-center space-x-2">
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  value={customWeight}
                  onChange={(e) => handleCustomWeightChange(e.target.value)}
                  className="input flex-1"
                  placeholder="Enter amount"
                />
                <span className="text-sm text-gray-500">kg</span>
              </div>
            </div>

            {/* Impact Preview */}
            {weight > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gradient-to-r from-primary-50 to-secondary-50 p-4 rounded-lg"
              >
                <h4 className="text-sm font-medium text-gray-900 mb-3">
                  Expected Impact
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-lg font-bold text-primary-600">
                      {energyPotential.toFixed(1)} kWh
                    </div>
                    <div className="text-xs text-gray-600">Daily Energy</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-secondary-600">
                      {co2Avoided.toFixed(1)} kg
                    </div>
                    <div className="text-xs text-gray-600">CO₂ Avoided</div>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-3">
              <Button
                variant="outline"
                onClick={onClose}
                className="flex-1"
              >
                Cancel
              </Button>
              <Button
                onClick={handleSave}
                disabled={weight <= 0}
                className="flex-1"
              >
                Save
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};
