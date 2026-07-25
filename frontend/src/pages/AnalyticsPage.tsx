import React from 'react';
import { BarChart3, TrendingUp } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  LineChart,
  Line,
} from 'recharts';

export const AnalyticsPage: React.FC = () => {
  const pagesData = [
    { day: 'Mon', pages: 25 },
    { day: 'Tue', pages: 30 },
    { day: 'Wed', pages: 18 },
    { day: 'Thu', pages: 22 },
    { day: 'Fri', pages: 15 },
    { day: 'Sat', pages: 40 },
    { day: 'Sun', pages: 35 },
  ];

  return (
    <div className="space-y-6 pb-12">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Reading Analytics & Insights</h1>
          <p className="text-xs text-slate-500">Visual performance charts, reading speed trends, and consistency metrics.</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Pages Chart */}
        <div className="glass-panel p-5 rounded-2xl border space-y-4">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-indigo-500" />
            <h3 className="font-semibold text-sm text-slate-800 dark:text-slate-200">
              Daily Pages Read (This Week)
            </h3>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pagesData}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e293b', borderRadius: '12px', borderColor: '#334155', color: '#fff' }}
                />
                <Bar dataKey="pages" fill="#4F46E5" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Speed Trend Chart */}
        <div className="glass-panel p-5 rounded-2xl border space-y-4">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-cyan-500" />
            <h3 className="font-semibold text-sm text-slate-800 dark:text-slate-200">
              Reading Speed Trend (Pages / Hour)
            </h3>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={pagesData}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e293b', borderRadius: '12px', borderColor: '#334155', color: '#fff' }}
                />
                <Line type="monotone" dataKey="pages" stroke="#06B6D4" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
