import { create } from 'zustand';

interface AppState {
  theme: 'dark' | 'light';
  toggleTheme: () => void;
  activeBookId: number | null;
  setActiveBookId: (id: number | null) => void;
  isFocusMode: boolean;
  setFocusMode: (mode: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  theme: 'dark',
  toggleTheme: () =>
    set((state) => {
      const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
      if (nextTheme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      return { theme: nextTheme };
    }),
  activeBookId: null,
  setActiveBookId: (id) => set({ activeBookId: id }),
  isFocusMode: false,
  setFocusMode: (mode) => set({ isFocusMode: mode }),
}));
