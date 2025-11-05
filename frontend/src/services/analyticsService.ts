import api from './api';
import { AnalyticsData } from '../types/analytics';

export const analyticsService = {
  getDashboard: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get<AnalyticsData>('/analytics/dashboard', { params });
    return response.data;
  },

  getCategoryAnalysis: async (categoryId: number, params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get(`/analytics/categories/${categoryId}/analysis`, { params });
    return response.data;
  },
};