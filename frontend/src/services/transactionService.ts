import api from './api';
import { Transaction, TransactionCreate, TransactionUpdate } from '../types/transaction';

export const transactionService = {
  getAll: async (params?: {
    skip?: number;
    limit?: number;
    type?: string;
    category_id?: number;
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await api.get<Transaction[]>('/transactions', { params });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await api.get<Transaction>(`/transactions/${id}`);
    return response.data;
  },

  create: async (transaction: TransactionCreate) => {
    const response = await api.post<Transaction>('/transactions', transaction);
    return response.data;
  },

  update: async (id: number, transaction: TransactionUpdate) => {
    const response = await api.put<Transaction>(`/transactions/${id}`, transaction);
    return response.data;
  },

  delete: async (id: number) => {
    await api.delete(`/transactions/${id}`);
  },

  createBatch: async (transactions: TransactionCreate[]) => {
    const response = await api.post<Transaction[]>('/transactions/batch', transactions);
    return response.data;
  },
};
