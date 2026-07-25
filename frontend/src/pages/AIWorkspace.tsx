import React, { useState } from 'react';
import { Bot, Send, User, Cpu } from 'lucide-react';
import { api } from '../services/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  grounded?: boolean;
}

export const AIWorkspace: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your AI Reading Mentor. Ask me any question, request concept explanations, or ask for book summaries.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userText }]);
    setLoading(true);

    try {
      const res = await api.askQuestion(1, userText);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: res.answer, grounded: res.grounded }
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an issue processing your request.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-6rem)] grid grid-cols-1 lg:grid-cols-3 gap-6 pb-4">
      {/* Chat Conversation Panel */}
      <div className="lg:col-span-2 glass-panel rounded-2xl border flex flex-col justify-between overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bot className="w-5 h-5 text-indigo-500" />
            <h2 className="font-bold text-sm text-slate-800 dark:text-slate-200">AI Reading Mentor</h2>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-500 font-semibold">
            RAG Grounded Active
          </span>
        </div>

        {/* Message History */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                  msg.role === 'user' ? 'bg-indigo-600' : 'bg-gradient-to-tr from-indigo-500 to-cyan-500'
                }`}
              >
                {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`max-w-md p-4 rounded-2xl text-xs leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white rounded-tr-none'
                    : 'bg-slate-100 dark:bg-slate-800/80 text-slate-800 dark:text-slate-200 border rounded-tl-none'
                }`}
              >
                <p>{msg.content}</p>
                {msg.grounded && (
                  <span className="inline-block mt-2 px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-600 dark:text-cyan-400 font-semibold text-[10px]">
                    Verified with RAG Context
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSend} className="p-3 border-t flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask AI mentor about your books or concepts..."
            className="flex-1 px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 border focus:outline-none text-xs text-slate-900 dark:text-white"
          />
          <button
            type="submit"
            disabled={loading}
            className="p-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold transition disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

      {/* Side Panels: Live Workflow & Tools */}
      <div className="space-y-6">
        <div className="glass-panel p-5 rounded-2xl border space-y-3">
          <div className="flex items-center gap-2 text-slate-800 dark:text-slate-200 font-semibold text-xs">
            <Cpu className="w-4 h-4 text-cyan-500" />
            Live Workflow & Tool Activity Panel
          </div>
          <div className="space-y-2 text-xs">
            <div className="p-2.5 rounded-xl bg-slate-100/60 dark:bg-slate-800/40 border flex justify-between">
              <span>Browser MCP</span>
              <span className="text-emerald-500 font-semibold">Ready</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-100/60 dark:bg-slate-800/40 border flex justify-between">
              <span>Calendar MCP</span>
              <span className="text-emerald-500 font-semibold">Ready</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-100/60 dark:bg-slate-800/40 border flex justify-between">
              <span>Filesystem MCP</span>
              <span className="text-emerald-500 font-semibold">Ready</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-100/60 dark:bg-slate-800/40 border flex justify-between">
              <span>ChromaDB Vector Store</span>
              <span className="text-emerald-500 font-semibold">Indexed</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
