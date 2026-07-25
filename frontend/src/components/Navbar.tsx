import React from 'react';
import { Sun, Moon, Search, Bell, Flame } from 'lucide-react';
import { useAppStore } from '../stores/appStore';

export const Navbar: React.FC = () => {
  const { theme, toggleTheme } = useAppStore();

  return (
    <header className="h-16 ml-64 glass-panel sticky top-0 z-20 border-b flex items-center justify-between px-6">
      {/* Search Bar */}
      <div className="relative w-72">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          type="text"
          placeholder="Search books, concepts, topics..."
          className="w-full pl-9 pr-4 py-2 rounded-xl text-sm bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-900 dark:text-white"
        />
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        {/* Streak Pill */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-400 text-sm font-semibold">
          <Flame className="w-4 h-4 fill-amber-500 text-amber-500 animate-bounce" />
          <span>12 Day Streak</span>
        </div>

        {/* Notifications */}
        <button className="p-2 rounded-xl text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
          <Bell className="w-5 h-5" />
        </button>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-xl text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
          title="Toggle Theme"
        >
          {theme === 'dark' ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-indigo-600" />}
        </button>

        {/* Profile Avatar */}
        <div className="flex items-center gap-3 pl-2 border-l border-slate-200 dark:border-slate-700">
          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm shadow">
            AK
          </div>
          <div className="hidden md:block text-left text-xs">
            <p className="font-semibold text-slate-800 dark:text-slate-200">Akhil</p>
            <p className="text-slate-500 dark:text-slate-400">Lead Reader</p>
          </div>
        </div>
      </div>
    </header>
  );
};
