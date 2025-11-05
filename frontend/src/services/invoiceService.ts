import api from './api';
import { Invoice } from '../types/invoice';

export const invoiceService = {
  getAll: async (params?: { skip?: number; limit?: number; status?: string }) => {
    const response = await api.get<Invoice[]>('/invoices', { params });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await api.get<Invoice>(`/invoices/${id}`);
    return response.data;
  },

  upload: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<Invoice>('/invoices/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  delete: async (id: number) => {
    await api.delete(`/invoices/${id}`);
  },
};