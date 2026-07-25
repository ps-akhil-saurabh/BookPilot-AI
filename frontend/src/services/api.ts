import type { Book, DashboardStats, Recommendation, AgentStatus, VocabularyWord } from '../types';

const API_BASE = '/api/v1';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP ${response.status}`);
  }

  return response.json();
}

export const api = {
  // Books
  getBooks: async (): Promise<Book[]> => fetchJson('/books'),
  getBook: async (id: number): Promise<Book> => fetchJson(`/books/${id}`),
  addBook: async (data: Partial<Book>) =>
    fetchJson<{ data: any }>('/books', { method: 'POST', body: JSON.stringify(data) }),
  deleteBook: async (id: number) => fetchJson(`/books/${id}`, { method: 'DELETE' }),

  // Upload
  uploadBook: async (formData: FormData) => {
    const res = await fetch(`${API_BASE}/upload/book`, {
      method: 'POST',
      body: formData,
    });
    return res.json();
  },

  // Planner
  generatePlan: async (data: { book_ids: number[]; deadline?: string; daily_minutes: number }) =>
    fetchJson<{ data: any }>('/planner/generate', { method: 'POST', body: JSON.stringify(data) }),
  replan: async (planId: number, missedDays: number) =>
    fetchJson('/planner/replan', { method: 'POST', body: JSON.stringify({ plan_id: planId, missed_days: missedDays }) }),

  // Progress
  updateProgress: async (data: { book_id: number; current_page: number; minutes?: number; chapter?: string; notes?: string }) =>
    fetchJson('/reading/progress', { method: 'POST', body: JSON.stringify(data) }),
  getTodaySchedule: async () => fetchJson<{ pages: number; estimated_minutes: number; book: string; book_id: number; progress_percentage: number }>('/schedule/today'),

  // Learning
  askQuestion: async (bookId: number, question: string) =>
    fetchJson<{ answer: string; sources?: string[]; grounded: boolean }>('/learning/question', {
      method: 'POST',
      body: JSON.stringify({ book_id: bookId, question }),
    }),
  getVocabulary: async () => fetchJson<{ data: VocabularyWord[] }>('/learning/vocabulary'),

  // Analytics & Recommendations
  getDashboardStats: async (): Promise<DashboardStats> => fetchJson('/analytics/dashboard'),
  getRecommendations: async (): Promise<{ data: Recommendation[] }> => fetchJson('/recommendation'),
  getMoodRecommendation: async (mood: string): Promise<{ data: Recommendation[] }> =>
    fetchJson('/recommendation/mood', { method: 'POST', body: JSON.stringify({ mood }) }),

  // Workflow & Agents
  getAgentStatus: async (): Promise<{ data: AgentStatus[] }> => fetchJson('/workflow/agents'),
  runWorkflow: async (requestText: string) =>
    fetchJson('/workflow/run', { method: 'POST', body: JSON.stringify({ request_text: requestText }) }),
};
