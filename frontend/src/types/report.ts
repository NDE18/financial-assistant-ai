export interface Report {
  id: number;
  title: string;
  type: string;
  start_date: string;
  end_date: string;
  summary?: string;
  insights?: string;
  recommendations?: string;
  file_path?: string;
  status: 'generating' | 'completed' | 'failed';
  is_favorite: boolean;
  created_at: string;
  completed_at?: string;
}