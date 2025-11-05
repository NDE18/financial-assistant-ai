export interface Invoice {
  id: number;
  filename: string;
  file_path: string;
  file_type: string;
  vendor?: string;
  invoice_number?: string;
  invoice_date?: string;
  due_date?: string;
  total_amount?: number;
  tax_amount?: number;
  currency: string;
  confidence_score?: number;
  extraction_status: 'pending' | 'success' | 'failed';
  is_processed: boolean;
  is_paid: boolean;
  created_at: string;
}
