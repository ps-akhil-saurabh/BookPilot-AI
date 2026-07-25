import React, { useState } from 'react';
import { Layers, HelpCircle, BookMarked, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export const LearningWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'flashcards' | 'quiz' | 'vocabulary'>('flashcards');

  React.useEffect(() => {
    api.getVocabulary().catch(console.error);
  }, []);

  return (
    <div className="space-y-6 pb-12">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Learning Hub & Knowledge Retention</h1>
          <p className="text-xs text-slate-500">AI-generated quizzes, revision flashcards, and vocabulary mastery.</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-200 dark:border-slate-700 pb-2">
        <button
          onClick={() => setActiveTab('flashcards')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition ${
            activeTab === 'flashcards' ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <Layers className="w-4 h-4" /> Flashcards
        </button>
        <button
          onClick={() => setActiveTab('quiz')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition ${
            activeTab === 'quiz' ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <HelpCircle className="w-4 h-4" /> Quiz Mode
        </button>
        <button
          onClick={() => setActiveTab('vocabulary')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition ${
            activeTab === 'vocabulary' ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <BookMarked className="w-4 h-4" /> Vocabulary Builder
        </button>
      </div>

      {/* Content based on Tab */}
      {activeTab === 'flashcards' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="glass-card p-6 rounded-2xl border flex flex-col justify-between h-56 hover:scale-105 transition cursor-pointer">
            <div>
              <span className="text-[10px] font-bold text-indigo-500 uppercase">Atomic Habits • Chapter 1</span>
              <h3 className="font-bold text-base text-slate-900 dark:text-white mt-2">What is the 1% rule?</h3>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800/80 p-3 rounded-xl">
              Answer: Getting 1% better every day results in a 37x improvement over a year.
            </p>
          </div>
        </div>
      )}

      {activeTab === 'quiz' && (
        <div className="glass-panel p-6 rounded-2xl border space-y-4 max-w-2xl">
          <h2 className="font-bold text-base text-slate-900 dark:text-white">Chapter 1 Knowledge Quiz</h2>
          <div className="p-4 rounded-xl bg-slate-100 dark:bg-slate-800 space-y-3">
            <p className="font-semibold text-sm text-slate-900 dark:text-white">
              Q1: What is the core habit loop described by James Clear?
            </p>
            <div className="space-y-2 text-xs">
              <label className="flex items-center gap-2 p-3 rounded-xl bg-white dark:bg-slate-700 border cursor-pointer">
                <input type="radio" name="q1" className="text-indigo-600" />
                <span>Trigger, Craving, Response, Reward</span>
              </label>
              <label className="flex items-center gap-2 p-3 rounded-xl bg-white dark:bg-slate-700 border cursor-pointer">
                <input type="radio" name="q1" className="text-indigo-600" />
                <span>Plan, Do, Check, Act</span>
              </label>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'vocabulary' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="glass-card p-4 rounded-xl border space-y-2">
            <div className="flex justify-between items-center">
              <h3 className="font-bold text-base text-indigo-600 dark:text-indigo-400">Compounding</h3>
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300">
              The process in which an asset's earnings, from either capital gains or interest, are reinvested to generate additional earnings over time.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
