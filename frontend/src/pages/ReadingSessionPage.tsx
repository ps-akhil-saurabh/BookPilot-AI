import React, { useState } from 'react';
import { BookOpen, Play, Pause, CheckCircle } from 'lucide-react';
import { api } from '../services/api';

export const ReadingSessionPage: React.FC = () => {
  const [timerSeconds, setTimerSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [currentPage, setCurrentPage] = useState(120);

  React.useEffect(() => {
    let interval: any = null;
    if (isRunning) {
      interval = setInterval(() => {
        setTimerSeconds((prev) => prev + 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  const handleFinishSession = async () => {
    setIsRunning(false);
    await api.updateProgress({
      book_id: 1,
      current_page: currentPage,
      minutes: Math.ceil(timerSeconds / 60) || 1,
    });
    alert('Session finished and saved!');
  };

  const formatTime = (secs: number) => {
    const mins = Math.floor(secs / 60);
    const s = secs % 60;
    return `${mins.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      <div className="glass-panel p-8 rounded-3xl border space-y-6 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-500 font-semibold text-xs">
          <BookOpen className="w-3.5 h-3.5" /> Smart Focus Reading Session
        </div>

        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Atomic Habits</h1>
          <p className="text-xs text-slate-500">By James Clear • Chapter 3</p>
        </div>

        {/* Timer Display */}
        <div className="text-6xl font-black tracking-tight text-indigo-600 dark:text-indigo-400 font-mono">
          {formatTime(timerSeconds)}
        </div>

        {/* Controls */}
        <div className="flex justify-center gap-4">
          <button
            onClick={() => setIsRunning(!isRunning)}
            className="px-6 py-3 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-lg shadow-indigo-500/25 transition flex items-center gap-2"
          >
            {isRunning ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            {isRunning ? 'Pause Session' : 'Start Reading'}
          </button>
          <button
            onClick={handleFinishSession}
            className="px-6 py-3 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow-lg shadow-emerald-500/25 transition flex items-center gap-2"
          >
            <CheckCircle className="w-4 h-4" /> Finish & Log
          </button>
        </div>

        {/* Current Page Control */}
        <div className="pt-4 flex items-center justify-center gap-4 text-xs">
          <span className="font-semibold text-slate-700 dark:text-slate-300">Current Page:</span>
          <input
            type="number"
            value={currentPage}
            onChange={(e) => setCurrentPage(Number(e.target.value))}
            className="w-20 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 border text-center font-bold"
          />
        </div>
      </div>
    </div>
  );
};
