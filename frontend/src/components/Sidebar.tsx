import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  BookOpen,
  Calendar,
  Bot,
  GraduationCap,
  BarChart3,
  BookMarked,
  Sparkles,
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { label: 'Dashboard', path: '/', icon: LayoutDashboard },
    { label: 'Library', path: '/library', icon: BookOpen },
    { label: 'Reading Plan', path: '/plan', icon: Calendar },
    { label: 'AI Mentor', path: '/ai-workspace', icon: Bot },
    { label: 'Learning Hub', path: '/learning', icon: GraduationCap },
    { label: 'Analytics', path: '/analytics', icon: BarChart3 },
    { label: 'Reader', path: '/reader', icon: BookMarked },
  ];

  return (
    <aside className="w-64 h-screen glass-panel fixed left-0 top-0 z-30 flex flex-col justify-between p-4 border-r">
      <div>
        {/* Brand Header */}
        <div className="flex items-center gap-3 px-3 py-4 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h1 className="font-bold text-lg leading-tight text-slate-900 dark:text-white">
              BookPilot AI
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">AI Reading Mentor</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/20'
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60'
                }`
              }
            >
              <item.icon className="w-5 h-5" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Footer Status */}
      <div className="p-3 glass-card rounded-xl border flex items-center gap-3">
        <div className="relative flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
        </div>
        <div className="text-xs">
          <p className="font-semibold text-slate-800 dark:text-slate-200">7 AI Agents Active</p>
          <p className="text-slate-500 dark:text-slate-400">LangGraph Engine Online</p>
        </div>
      </div>
    </aside>
  );
};
