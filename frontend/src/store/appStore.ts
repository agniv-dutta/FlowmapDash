import { create } from 'zustand';
import { Session } from '../types';

interface AppState {
  selectedSession: Session | null;
  setSelectedSession: (session: Session | null) => void;
  dateRange: { from: string; to: string } | null;
  setDateRange: (range: { from: string; to: string } | null) => void;
  browserFilter: string;
  setBrowserFilter: (browser: string) => void;
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  selectedSession: null,
  setSelectedSession: (session) => set({ selectedSession: session }),
  dateRange: null,
  setDateRange: (range) => set({ dateRange: range }),
  browserFilter: 'All Browsers',
  setBrowserFilter: (browser) => set({ browserFilter: browser }),
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
}));
