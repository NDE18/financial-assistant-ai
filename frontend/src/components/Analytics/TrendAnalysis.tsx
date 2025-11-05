import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { CategoryBreakdown } from '../../types/analytics';
import { formatCurrency } from '../../utils/formatters';
import { TrendingUp } from 'lucide-react';

interface TrendAnalysisProps {
  breakdown: CategoryBreakdown[];
}

const TrendAnalysis: React.FC<TrendAnalysisProps> = ({ breakdown }) => {
  const chartData = breakdown.slice(0, 10).map(item => ({
    category: item.category.length > 15 ? item.category.substring(0, 15) + '...' : item.category,
    amount: item.amount,
    count: item.transaction_count,
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-900">{payload[0].payload.category}</p>
          <p className="text-sm text-blue-600">
            Montant: {formatCurrency(payload[0].value)}
          </p>
          <p className="text-sm text-gray-600">
            Transactions: {payload[1].value}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex items-center space-x-2 mb-6">
        <TrendingUp className="w-5 h-5 text-green-600" />
        <h2 className="text-xl font-bold text-gray-900">Analyse par Catégorie</h2>
      </div>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="category" angle={-45} textAnchor="end" height={100} />
          <YAxis yAxisId="left" orientation="left" stroke="#3b82f6" />
          <YAxis yAxisId="right" orientation="right" stroke="#10b981" />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar yAxisId="left" dataKey="amount" fill="#3b82f6" name="Montant (€)" />
          <Bar yAxisId="right" dataKey="count" fill="#10b981" name="Nb Transactions" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendAnalysis;