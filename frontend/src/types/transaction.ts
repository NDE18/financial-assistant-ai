export interface Transaction {
  id: number;
  description: string;
  amount: number;
  type: 'income' | 'expense';
  date: string;
  category_id?: number;
  category_name?: string;
  tags?: string;
  notes?: string;
  is_recurring: boolean;
  is_verified: boolean;
  confidence_score?: number;
  invoice_id?: number;
  created_at: string;
  updated_at: string;
}

export interface TransactionCreate {
  description: string;
  amount: number;
  type: 'income' | 'expense';
  date: string;
  category_id?: number;
  tags?: string;
  notes?: string;
}

export interface TransactionUpdate {
  description?: string;
  amount?: number;
  type?: 'income' | 'expense';
  date?: string;
  category_id?: number;
  tags?: string;
  notes?: string;
  is_verified?: boolean;
}