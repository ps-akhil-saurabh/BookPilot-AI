export interface Book {
  id: number;
  title: string;
  author?: string;
  genre?: string;
  description?: string;
  total_pages: number;
  language?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  rating?: number;
  cover_url?: string;
  is_uploaded: boolean;
  progress: number;
}

export interface ReadingPlan {
  id: number;
  plan_name: string;
  deadline?: string;
  daily_target_pages: number;
  daily_reading_minutes: number;
  estimated_hours?: number;
  priority_order?: number[];
  book_ids?: number[];
  status: 'active' | 'completed' | 'paused' | 'cancelled';
  confidence?: number;
  ai_notes?: string;
  schedule_data?: any[];
  created_at: string;
}

export interface DashboardStats {
  total_books: number;
  completed_books: number;
  in_progress_books: number;
  total_pages_read: number;
  reading_streak: number;
  longest_streak: number;
  reading_speed: number;
  total_reading_hours: number;
  avg_pages_per_day: number;
  goal_completion_percentage?: number;
}

export interface Recommendation {
  id: number;
  recommendation_type: string;
  book_title?: string;
  content: string;
  reason?: string;
  confidence: number;
  generated_at: string;
}

export interface AgentStatus {
  agent: string;
  status: 'idle' | 'running' | 'completed' | 'failed' | 'active';
}

export interface QuizQuestion {
  id: number;
  question: string;
  question_type: 'mcq' | 'true_false' | 'short_answer';
  options?: string[];
  book_id: number;
  chapter?: string;
}

export interface VocabularyWord {
  id: number;
  word: string;
  meaning: string;
  example?: string;
  mastered: boolean;
}
