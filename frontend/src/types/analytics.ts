export interface KPIData {
  total_income: number;
  total_expenses: number;
  net_balance: number;
  savings_rate: number;
  largest_expense?: {
    description: string;
    amount: number;
    date: string;
  };
  largest_income?: {
    description: string;
    amount: number;
    date: string;
  };
}

export interface CategoryBreakdown {
  category: string;
  amount: number;
  percentage: number;
  transaction_count: number;
}

export interface TrendData {
  date: string;
  income: number;
  expenses: number;
  balance: number;
}

export interface AnalyticsData {
  period_start: string;
  period_end: string;
  kpis: KPIData;
  category_breakdown: CategoryBreakdown[];
  trends: TrendData[];
  insights: string[];
  alerts: string[];
}