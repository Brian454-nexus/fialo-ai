import React from 'react';
import { motion } from 'framer-motion';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { EditIcon, CheckIcon } from 'lucide-react';

interface WasteType {
  id: string;
  name: string;
  icon: string;
  description: string;
  energyPotential: string;
  color: string;
  examples: string[];
}

interface WasteTypeCardProps {
  wasteType: WasteType;
  isSelected: boolean;
  weight: number;
  onSelect: () => void;
  onWeightClick: () => void;
  userType: 'individual' | 'company';
}

export const WasteTypeCard: React.FC<WasteTypeCardProps> = ({
  wasteType,
  isSelected,
  weight,
  onSelect,
  onWeightClick,
  userType,
}) => {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <Card
        className={`cursor-pointer transition-all duration-200 ${
          isSelected
            ? 'ring-2 ring-primary-500 bg-primary-50'
            : 'hover:shadow-lg hover:border-primary-200'
        }`}
        onClick={onSelect}
      >
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="text-3xl mr-3">{wasteType.icon}</div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {wasteType.name}
                </h3>
                <p className="text-sm text-gray-600">
                  {wasteType.description}
                </p>
              </div>
            </div>
            {isSelected && (
              <div className="w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center">
                <CheckIcon className="w-4 h-4 text-white" />
              </div>
            )}
          </div>

          {/* Energy Potential */}
          <div className="mb-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Energy Potential</span>
              <span className="text-sm font-medium text-primary-600">
                {wasteType.energyPotential}
              </span>
            </div>
            <div className={`w-full h-2 bg-gray-200 rounded-full mt-1`}>
              <div
                className={`h-2 bg-gradient-to-r ${wasteType.color} rounded-full`}
                style={{ width: '100%' }}
              />
            </div>
          </div>

          {/* Examples */}
          <div className="mb-4">
            <p className="text-xs text-gray-500 mb-2">Examples:</p>
            <div className="flex flex-wrap gap-1">
              {wasteType.examples.slice(0, 2).map((example, index) => (
                <span
                  key={index}
                  className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded"
                >
                  {example}
                </span>
              ))}
              {wasteType.examples.length > 2 && (
                <span className="text-xs text-gray-400">
                  +{wasteType.examples.length - 2} more
                </span>
              )}
            </div>
          </div>

          {/* Weight Input */}
          {isSelected && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="border-t border-gray-200 pt-4"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    Daily Amount
                  </p>
                  <p className="text-xs text-gray-600">
                    {weight > 0 ? `${weight} kg/day` : 'Not set'}
                  </p>
                </div>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={(e) => {
                    e.stopPropagation();
                    onWeightClick();
                  }}
                >
                  <EditIcon className="w-4 h-4 mr-1" />
                  {weight > 0 ? 'Edit' : 'Set'}
                </Button>
              </div>
            </motion.div>
          )}

          {/* Selection Indicator */}
          {!isSelected && (
            <div className="text-center">
              <p className="text-sm text-gray-500">
                Click to select
              </p>
            </div>
          )}
        </div>
      </Card>
    </motion.div>
  );
};
