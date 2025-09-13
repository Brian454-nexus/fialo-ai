import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type UserType = 'individual' | 'company' | null;

interface UserProfile {
  userType: UserType;
  location: string;
  wasteTypes: Record<string, number>;
  energyNeeds: number;
  companyName?: string;
  currentProcessingMethod?: string;
  operationalCost?: number;
}

interface UserState {
  profile: UserProfile | null;
  setUserType: (userType: UserType) => void;
  updateProfile: (profile: Partial<UserProfile>) => void;
  resetProfile: () => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      profile: null,

      setUserType: (userType: UserType) => {
        set((state) => ({
          profile: {
            ...state.profile,
            userType,
          } as UserProfile,
        }));
      },

      updateProfile: (profile: Partial<UserProfile>) => {
        set((state) => ({
          profile: {
            ...state.profile,
            ...profile,
          } as UserProfile,
        }));
      },

      resetProfile: () => {
        set({ profile: null });
      },
    }),
    {
      name: 'user-storage',
    }
  )
);

// Selector for userType
export const useUserType = () => useUserStore((state) => state.profile?.userType);

