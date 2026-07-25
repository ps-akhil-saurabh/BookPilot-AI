import React from 'react';
import { Bot, CheckCircle2, Loader2, Sparkles } from 'lucide-react';
import type { AgentStatus } from '../types';

interface AgentMonitorProps {
  agents?: AgentStatus[];
}

export const AgentMonitor: React.FC<AgentMonitorProps> = ({ agents }) => {
  const defaultAgents: AgentStatus[] = [
    { agent: 'Planner', status: 'completed' },
    { agent: 'Metadata', status: 'completed' },
    { agent: 'Scheduling', status: 'active' },
    { agent: 'Learning', status: 'idle' },
    { agent: 'Recommendation', status: 'idle' },
    { agent: 'Analytics', status: 'completed' },
    { agent: 'Reflection', status: 'active' },
  ];

  const agentList = agents && agents.length > 0 ? agents : defaultAgents;

  return (
    <div className="glass-panel p-5 rounded-2xl border">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-indigo-500" />
          <h3 className="font-semibold text-sm text-slate-800 dark:text-slate-200">
            Agent Activity Monitor ⭐
          </h3>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-500 font-medium">
          LangGraph Multi-Agent
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        {agentList.map((item) => {
          const isActive = item.status === 'active' || item.status === 'running';
          const isCompleted = item.status === 'completed';

          return (
            <div
              key={item.agent}
              className={`p-3 rounded-xl border flex flex-col items-center justify-center text-center transition-all ${
                isActive
                  ? 'bg-indigo-500/10 border-indigo-500/40 text-indigo-600 dark:text-indigo-400 shadow-md shadow-indigo-500/10 scale-105'
                  : isCompleted
                  ? 'bg-emerald-500/5 border-emerald-500/20 text-slate-700 dark:text-slate-300'
                  : 'bg-slate-100/50 dark:bg-slate-800/40 border-slate-200 dark:border-slate-700/60 text-slate-400'
              }`}
            >
              <div className="mb-2">
                {isActive ? (
                  <Loader2 className="w-5 h-5 animate-spin text-indigo-500" />
                ) : isCompleted ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                ) : (
                  <Sparkles className="w-4 h-4 text-slate-400" />
                )}
              </div>
              <p className="text-xs font-semibold">{item.agent}</p>
              <p className="text-[10px] capitalize opacity-80 mt-0.5">{item.status}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
