import React from 'react';
import { Check, Clock, Play, ShieldCheck } from 'lucide-react';

export interface TimelineStep {
  label: string;
  agent: string;
  status: 'completed' | 'running' | 'pending';
  detail?: string;
}

interface ThinkingTimelineProps {
  steps?: TimelineStep[];
}

export const ThinkingTimeline: React.FC<ThinkingTimelineProps> = ({ steps }) => {
  const defaultSteps: TimelineStep[] = [
    { label: 'Intent Analysis & Task Planning', agent: 'Planner Agent', status: 'completed', detail: 'Identified reading_plan goal' },
    { label: 'External Metadata Retrieval', agent: 'Metadata Agent (Browser MCP)', status: 'completed', detail: 'Fetched page count & difficulty' },
    { label: 'Schedule Optimization', agent: 'Scheduling Agent (Calendar MCP)', status: 'completed', detail: 'Calculated 22 pages/day target' },
    { label: 'Plan Validation & Feasibility Check', agent: 'Reflection Agent', status: 'running', detail: 'Validating workload sustainability' },
  ];

  const list = steps || defaultSteps;

  return (
    <div className="glass-panel p-5 rounded-2xl border">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-sm text-slate-800 dark:text-slate-200 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-indigo-500" />
          AI Thinking & Reflection Timeline ⭐
        </h3>
        <span className="text-xs text-slate-500">Live Execution Graph</span>
      </div>

      <div className="relative border-l-2 border-indigo-500/20 ml-4 space-y-4 py-1">
        {list.map((step, idx) => {
          const isDone = step.status === 'completed';
          const isRunning = step.status === 'running';

          return (
            <div key={idx} className="relative pl-6">
              {/* Timeline Dot */}
              <div
                className={`absolute -left-[9px] top-0.5 w-4 h-4 rounded-full flex items-center justify-center text-white ${
                  isDone
                    ? 'bg-emerald-500'
                    : isRunning
                    ? 'bg-indigo-500 animate-pulse'
                    : 'bg-slate-300 dark:bg-slate-700'
                }`}
              >
                {isDone ? (
                  <Check className="w-2.5 h-2.5 stroke-[3]" />
                ) : isRunning ? (
                  <Play className="w-2 h-2 fill-white ml-0.5" />
                ) : (
                  <Clock className="w-2 h-2" />
                )}
              </div>

              {/* Step Content */}
              <div>
                <div className="flex items-center gap-2">
                  <p className="text-xs font-semibold text-slate-800 dark:text-slate-200">
                    {step.label}
                  </p>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 border border-slate-200 dark:border-slate-700">
                    {step.agent}
                  </span>
                </div>
                {step.detail && (
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    {step.detail}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
