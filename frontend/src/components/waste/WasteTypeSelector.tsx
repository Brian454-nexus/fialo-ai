import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { WasteTypeCard } from './WasteTypeCard';
import { WasteWeightInput } from './WasteWeightInput';
import { SmartWasteDetector } from './SmartWasteDetector';

interface WasteTypeSelectorProps {
  selectedTypes: Record<string, number>;
  onTypesChange: (types: Record<string, number>) => void;
  userType: 'individual' | 'company';
}

const wasteTypes = [
  {
    id: 'food_scraps',
    name: 'Food Scraps',
    icon: '🍎',
    description: 'Kitchen waste, leftovers, peels',
    energyPotential: '1.2 kWh/kg',
    color: 'from-orange-400 to-red-500',
    examples: ['Vegetable peels', 'Leftover food', 'Fruit scraps', 'Coffee grounds'],
  },
  {
    id: 'market_waste',
    name: 'Market Waste',
    icon: '🥬',
    description: 'Fresh produce waste from markets',
    energyPotential: '1.8 kWh/kg',
    color: 'from-green-400 to-emerald-500',
    examples: ['Damaged vegetables', 'Unsold produce', 'Market trimmings'],
  },
  {
    id: 'agricultural_biomass',
    name: 'Agricultural Waste',
    icon: '🌾',
    description: 'Crop residues, straw, husks',
    energyPotential: '3.5 kWh/kg',
    color: 'from-yellow-400 to-amber-500',
    examples: ['Rice husks', 'Corn stalks', 'Wheat straw', 'Sugarcane bagasse'],
  },
  {
    id: 'animal_waste',
    name: 'Animal Waste',
    icon: '🐄',
    description: 'Manure, animal byproducts',
    energyPotential: '0.8 kWh/kg',
    color: 'from-brown-400 to-amber-600',
    examples: ['Cow manure', 'Poultry waste', 'Pig manure'],
  },
  {
    id: 'wood_biomass',
    name: 'Wood & Biomass',
    icon: '🌳',
    description: 'Wood chips, sawdust, branches',
    energyPotential: '4.2 kWh/kg',
    color: 'from-green-600 to-green-800',
    examples: ['Wood chips', 'Sawdust', 'Tree branches', 'Paper waste'],
  },
];

export const WasteTypeSelector: React.FC<WasteTypeSelectorProps> = ({
  selectedTypes,
  onTypesChange,
  userType,
}) => {
  const [showWeightInput, setShowWeightInput] = useState(false);
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [showSmartDetector, setShowSmartDetector] = useState(false);

  const handleTypeSelect = (typeId: string) => {
    if (selectedTypes[typeId]) {
      // Remove type if already selected
      const newTypes = { ...selectedTypes };
      delete newTypes[typeId];
      onTypesChange(newTypes);
    } else {
      // Add type with default weight
      const defaultWeight = userType === 'individual' ? 5 : 50;
      onTypesChange({
        ...selectedTypes,
        [typeId]: defaultWeight,
      });
    }
  };

  const handleWeightChange = (typeId: string, weight: number) => {
    if (weight <= 0) {
      const newTypes = { ...selectedTypes };
      delete newTypes[typeId];
      onTypesChange(newTypes);
    } else {
      onTypesChange({
        ...selectedTypes,
        [typeId]: weight,
      });
    }
  };

  const handleSmartDetection = (detectedTypes: Record<string, number>) => {
    onTypesChange(detectedTypes);
    setShowSmartDetector(false);
  };

  const totalWeight = Object.values(selectedTypes).reduce((sum, weight) => sum + weight, 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          What types of waste do you have?
        </h3>
        <p className="text-gray-600 mb-6">
          {userType === 'individual'
            ? 'Select the waste types you typically generate at home'
            : 'Select the waste types your company processes'}
        </p>

        {/* Smart Detection Button */}
        <Button
          variant="outline"
          onClick={() => setShowSmartDetector(true)}
          className="mb-6"
        >
          <span className="mr-2">🤖</span>
          AI Waste Detection
          <span className="ml-2 text-xs bg-primary-100 text-primary-600 px-2 py-1 rounded-full">
            NEW
          </span>
        </Button>
      </div>

      {/* Waste Type Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {wasteTypes.map((wasteType, index) => (
          <motion.div
            key={wasteType.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <WasteTypeCard
              wasteType={wasteType}
              isSelected={!!selectedTypes[wasteType.id]}
              weight={selectedTypes[wasteType.id] || 0}
              onSelect={() => handleTypeSelect(wasteType.id)}
              onWeightClick={() => {
                setSelectedType(wasteType.id);
                setShowWeightInput(true);
              }}
              userType={userType}
            />
          </motion.div>
        ))}
      </div>

      {/* Selected Types Summary */}
      {Object.keys(selectedTypes).length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="bg-gradient-to-r from-primary-50 to-secondary-50">
            <div className="p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">
                Your Waste Profile
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-600">
                    {Object.keys(selectedTypes).length}
                  </div>
                  <div className="text-sm text-gray-600">Waste Types</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-secondary-600">
                    {totalWeight.toFixed(1)} kg
                  </div>
                  <div className="text-sm text-gray-600">Total Daily</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-accent-600">
                    {(totalWeight * 2.1).toFixed(1)} kWh
                  </div>
                  <div className="text-sm text-gray-600">Energy Potential</div>
                </div>
              </div>
              
              <div className="space-y-2">
                {Object.entries(selectedTypes).map(([typeId, weight]) => {
                  const type = wasteTypes.find(t => t.id === typeId);
                  return (
                    <div key={typeId} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <span className="text-lg mr-2">{type?.icon}</span>
                        <span className="font-medium">{type?.name}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-600">{weight} kg/day</span>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => {
                            setSelectedType(typeId);
                            setShowWeightInput(true);
                          }}
                        >
                          Edit
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </Card>
        </motion.div>
      )}

      {/* Weight Input Modal */}
      {showWeightInput && selectedType && (
        <WasteWeightInput
          wasteType={wasteTypes.find(t => t.id === selectedType)!}
          currentWeight={selectedTypes[selectedType] || 0}
          onWeightChange={(weight) => handleWeightChange(selectedType, weight)}
          onClose={() => {
            setShowWeightInput(false);
            setSelectedType(null);
          }}
          userType={userType}
        />
      )}

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
