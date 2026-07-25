import React, { useState } from 'react';
import { Calendar as CalendarIcon, Sparkles, RefreshCw, Clock } from 'lucide-react';
import { api } from '../services/api';

export const ReadingPlanPage: React.FC = () => {
  const [deadline, setDeadline] = useState('2026-09-01');
  const [dailyMinutes, setDailyMinutes] = useState(30);
  const [planResult, setPlanResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGeneratePlan = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.generatePlan({
        book_ids: [1, 2],
        deadline,
        daily_minutes: Number(dailyMinutes),
      });
      setPlanResult(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">AI Reading Plan Generator</h1>
          <p className="text-xs text-slate-500">Autonomous multi-agent roadmap generator with reflection validation.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="glass-panel p-6 rounded-2xl border space-y-4">
          <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-500" /> Configure Goals
          </h2>
          <form onSubmit={handleGeneratePlan} className="space-y-4 text-sm">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Target Deadline</label>
              <input
                type="date"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 border focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Available Minutes Per Day</label>
              <input
                type="number"
                value={dailyMinutes}
                onChange={(e) => setDailyMinutes(Number(e.target.value))}
                className="w-full px-3 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 border focus:outline-none"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md transition flex items-center justify-center gap-2"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              Generate Plan with LangGraph
            </button>
          </form>
        </div>

        {/* Schedule Result Display */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border space-y-4">
          <h2 className="text-base font-bold text-slate-900 dark:text-white">Generated Reading Roadmap</h2>
          {planResult ? (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-between text-xs text-emerald-600 dark:text-emerald-400 font-semibold">
                <span>Confidence Score: {Math.round((planResult.confidence || 0.92) * 100)}%</span>
                <span>Target: {planResult.daily_target_pages} Pages / Day</span>
              </div>
              <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
                {planResult.schedule?.map((item: any, idx: number) => (
                  <div key={idx} className="p-3 rounded-xl bg-slate-100/60 dark:bg-slate-800/40 border flex items-center justify-between text-xs">
                    <div className="flex items-center gap-3">
                      <CalendarIcon className="w-4 h-4 text-indigo-500" />
                      <div>
                        <p className="font-semibold text-slate-800 dark:text-slate-200">{item.day_name}, {item.date}</p>
                        <p className="text-[10px] text-slate-500">{item.is_weekend ? 'Weekend Bonus Schedule' : 'Regular Workday'}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-indigo-600 dark:text-indigo-400">{item.pages_to_read} Pages</p>
                      <p className="text-[10px] text-slate-400">~{item.estimated_minutes} mins</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="h-64 flex flex-col items-center justify-center text-slate-400 text-xs text-center space-y-2">
              <Clock className="w-8 h-8 text-slate-300 dark:text-slate-600 animate-pulse" />
              <p>Configure your target deadline and daily time above to generate an adaptive reading plan.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
