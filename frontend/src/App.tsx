import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { Library } from './pages/Library';
import { ReadingPlanPage } from './pages/ReadingPlan';
import { AIWorkspace } from './pages/AIWorkspace';
import { LearningWorkspace } from './pages/LearningWorkspace';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { ReadingSessionPage } from './pages/ReadingSessionPage';

const queryClient = new QueryClient();

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex">
          <Sidebar />
          <div className="flex-1 flex flex-col min-w-0">
            <Navbar />
            <main className="flex-1 ml-64 p-6 overflow-y-auto">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/library" element={<Library />} />
                <Route path="/plan" element={<ReadingPlanPage />} />
                <Route path="/ai-workspace" element={<AIWorkspace />} />
                <Route path="/learning" element={<LearningWorkspace />} />
                <Route path="/analytics" element={<AnalyticsPage />} />
                <Route path="/reader" element={<ReadingSessionPage />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </QueryClientProvider>
  );
};

export default App;
