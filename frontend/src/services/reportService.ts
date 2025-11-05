import api from './api';
import { Report } from '../types/report';

export const reportService = {
  getAll: async (params?: { skip?: number; limit?: number; type?: string }) => {
    const response = await api.get<Report[]>('/reports', { params });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await api.get<Report>(`/reports/${id}`);
    return response.data;
  },

  create: async (report: { title: string; type: string; start_date: string; end_date: string }) => {
    const response = await api.post<Report>('/reports', report);
    return response.data;
  },

  delete: async (id: number) => {
    await api.delete(`/reports/${id}`);
  },
};