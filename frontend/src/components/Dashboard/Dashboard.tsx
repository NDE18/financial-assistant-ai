import React, { useEffect, useState } from 'react';
import { analyticsService } from '../../services/analyticsService';
import { transactionService } from '../../services/transactionService';
import { AnalyticsData, Transaction } from '../../types';
import KPICards from './KPICards';
import ExpenseChart from '../Analytics/ExpenseChart';
import CategoryBreakdown from '../Analytics/CategoryBreakdown';
import RecentTransactions from './RecentTransactions';
import { AlertCircle, TrendingUp } from 'lucide-react';

const Dashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [recentTransactions, setRecentTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [analyticsData, transactions] = await Promise.all([
        analyticsService.getDashboard(),
        transactionService.getAll({ limit: 10 }),
      ]);
      
      setAnalytics(analyticsData);
      setRecentTransactions(transactions);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="flex items-center justify-center h-screen text-gray-500">
        Impossible de charger les données
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tableau de Bord</h1>
          <p className="text-gray-500 mt-1">Vue d'ensemble de vos finances</p>
        </div>
        <button
          onClick={loadDashboardData}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Actualiser
        </button>
      </div>

      {/* Alerts */}
      {analytics.alerts.length > 0 && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 mr-3" />
            <div className="flex-1">
              <h3 className="font-semibold text-red-800">Alertes</h3>
              <ul className="mt-2 space-y-1">
                {analytics.alerts.map((alert, idx) => (
                  <li key={idx} className="text-sm text-red-700">{alert}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Insights */}
      {analytics.insights.length > 0 && (
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg">
          <div className="flex items-start">
            <TrendingUp className="w-5 h-5 text-blue-500 mt-0.5 mr-3" />
            <div className="flex-1">
              <h3 className="font-semibold text-blue-800">Insights AI</h3>
              <ul className="mt-2 space-y-1">
                {analytics.insights.map((insight, idx) => (
                  <li key={idx} className="text-sm text-blue-700">{insight}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* KPIs */}
      <KPICards kpis={analytics.kpis} />

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ExpenseChart trends={analytics.trends} />
        <CategoryBreakdown breakdown={analytics.category_breakdown} />
      </div>

      {/* Recent Transactions */}
      <RecentTransactions transactions={recentTransactions} />
    </div>
  );
};

export default Dashboard;