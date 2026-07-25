import React, { useEffect, useState } from 'react';
import {
  Flame,
  BookOpen,
  TrendingUp,
  Clock,
  Sparkles,
  ArrowRight,
  ShieldAlert,
  BrainCircuit,
  CheckCircle2,
} from 'lucide-react';
import { AgentMonitor } from '../components/AgentMonitor';
import { ThinkingTimeline } from '../components/ThinkingTimeline';
import { api } from '../services/api';
import type { DashboardStats, Recommendation } from '../types';

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  useEffect(() => {
    api.getDashboardStats().then(setStats).catch(console.error);
    api.getRecommendations().then((res) => setRecommendations(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6 pb-12">
      {/* Hero Welcome Card */}
      <div className="relative overflow-hidden rounded-3xl p-8 bg-gradient-to-r from-indigo-600 via-indigo-700 to-cyan-600 text-white shadow-xl shadow-indigo-500/20">
        <div className="relative z-10 max-w-2xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-xs font-semibold text-cyan-200 border border-white/20">
            <Sparkles className="w-3.5 h-3.5" />
            AI Reading Mentor Active
          </div>
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Good Evening, Akhil 👋
          </h1>
          <p className="text-indigo-100 text-sm leading-relaxed">
            Your personalized goal: Read <span className="font-semibold text-white">22 pages</span> of{' '}
            <span className="underline decoration-cyan-400 font-semibold text-white">Atomic Habits</span> today.
            Estimated time: <span className="font-semibold text-white">35 minutes</span>.
          </p>
          <div className="pt-2 flex flex-wrap gap-4">
            <a
              href="/reader"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-indigo-700 font-bold text-sm hover:bg-slate-100 transition shadow-md"
            >
              Start Reading Session <ArrowRight className="w-4 h-4" />
            </a>
            <a
              href="/ai-workspace"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/10 backdrop-blur-md text-white font-medium text-sm border border-white/20 hover:bg-white/20 transition"
            >
              Consult AI Mentor
            </a>
          </div>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-card p-5 rounded-2xl border flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Reading Streak</p>
            <h3 className="text-2xl font-bold text-slate-800 dark:text-white mt-1">
              {stats?.reading_streak || 12} Days
            </h3>
            <p className="text-xs text-emerald-500 font-medium mt-1">↑ +3 days this week</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-500 flex items-center justify-center">
            <Flame className="w-6 h-6 fill-amber-500" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Reading Speed</p>
            <h3 className="text-2xl font-bold text-slate-800 dark:text-white mt-1">
              {stats?.reading_speed || 28.5} <span className="text-sm font-normal">pph</span>
            </h3>
            <p className="text-xs text-emerald-500 font-medium mt-1">Optimal focus range</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-cyan-500/10 text-cyan-500 flex items-center justify-center">
            <TrendingUp className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Books Completed</p>
            <h3 className="text-2xl font-bold text-slate-800 dark:text-white mt-1">
              {stats?.completed_books || 2} / {stats?.total_books || 5}
            </h3>
            <p className="text-xs text-indigo-500 font-medium mt-1">40% of target</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-500 flex items-center justify-center">
            <BookOpen className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Time Invested</p>
            <h3 className="text-2xl font-bold text-slate-800 dark:text-white mt-1">
              {stats?.total_reading_hours || 15.8} <span className="text-sm font-normal">hrs</span>
            </h3>
            <p className="text-xs text-emerald-500 font-medium mt-1">~35 mins / day</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-500 flex items-center justify-center">
            <Clock className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Live Agent Monitor Card ⭐ */}
      <AgentMonitor />

      {/* Two Column Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* AI Thinking Timeline ⭐ */}
          <ThinkingTimeline />

          {/* AI Recommendation Card */}
          <div className="glass-panel p-6 rounded-2xl border space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BrainCircuit className="w-5 h-5 text-cyan-500" />
                <h3 className="font-semibold text-sm text-slate-800 dark:text-slate-200">
                  AI Recommendation & Priority Optimization
                </h3>
              </div>
              <span className="text-xs text-cyan-500 font-semibold">95% Confidence</span>
            </div>
            {recommendations.length > 0 ? (
              <div className="p-4 rounded-xl bg-slate-100/80 dark:bg-slate-800/60 border space-y-1">
                <p className="font-semibold text-sm text-slate-900 dark:text-white">
                  Read "{recommendations[0].book_title || 'Atomic Habits'}" today.
                </p>
                <p className="text-xs text-slate-600 dark:text-slate-400">
                  {recommendations[0].reason || 'Optimal non-fiction choice after 2 dense technical sessions.'}
                </p>
              </div>
            ) : (
              <p className="text-xs text-slate-500">Loading recommendations...</p>
            )}
          </div>
        </div>

        {/* Sidebar Insights */}
        <div className="space-y-6">
          {/* AI Reflection Console ⭐ */}
          <div className="glass-panel p-5 rounded-2xl border space-y-4">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-amber-500" />
              <h3 className="font-semibold text-sm text-slate-800 dark:text-slate-200">
                AI Reflection Console ⭐
              </h3>
            </div>
            <div className="space-y-2.5 text-xs">
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                <span className="font-medium">Schedule Feasible</span>
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                <span className="font-medium">Deadline Achievable</span>
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <div className="p-3 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400 space-y-1">
                <p className="font-semibold">Workload Balancing Suggestion</p>
                <p className="opacity-90">
                  Your reading speed drops on Fridays. Reduced Friday target to 15 pages.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
