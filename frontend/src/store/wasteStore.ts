import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface WasteEntry {
  id: string;
  date: string;
  wasteTypes: Record<string, number>;
  totalWeight: number;
  energyGenerated: number;
  co2Avoided: number;
  costSavings: number;
  description?: string;
  imageUrl?: string;
  aiAnalysis?: {
    recommendations: string[];
    confidence: number;
    conversionMethod: string;
  };
}

interface WasteState {
  entries: WasteEntry[];
  addEntry: (entry: Omit<WasteEntry, 'id'>) => void;
  updateEntry: (id: string, updates: Partial<WasteEntry>) => void;
  deleteEntry: (id: string) => void;
  getTotalStats: () => {
    totalWaste: number;
    totalEnergy: number;
    totalCo2Avoided: number;
    totalSavings: number;
  };
  getEntriesByDateRange: (startDate: string, endDate: string) => WasteEntry[];
}

export const useWasteStore = create<WasteState>()(
  persist(
    (set, get) => ({
      entries: [],

      addEntry: (entry) => {
        const newEntry: WasteEntry = {
          ...entry,
          id: Date.now().toString(),
        };
        
        set((state) => ({
          entries: [newEntry, ...state.entries],
        }));
      },

      updateEntry: (id, updates) => {
        set((state) => ({
          entries: state.entries.map((entry) =>
            entry.id === id ? { ...entry, ...updates } : entry
          ),
        }));
      },

      deleteEntry: (id) => {
        set((state) => ({
          entries: state.entries.filter((entry) => entry.id !== id),
        }));
      },

      getTotalStats: () => {
        const { entries } = get();
        return entries.reduce(
          (acc, entry) => ({
            totalWaste: acc.totalWaste + entry.totalWeight,
            totalEnergy: acc.totalEnergy + entry.energyGenerated,
            totalCo2Avoided: acc.totalCo2Avoided + entry.co2Avoided,
            totalSavings: acc.totalSavings + entry.costSavings,
          }),
          {
            totalWaste: 0,
            totalEnergy: 0,
            totalCo2Avoided: 0,
            totalSavings: 0,
          }
        );
      },

      getEntriesByDateRange: (startDate, endDate) => {
        const { entries } = get();
        return entries.filter(
          (entry) => entry.date >= startDate && entry.date <= endDate
        );
      },
    }),
    {
      name: 'waste-storage',
    }
  )
);

