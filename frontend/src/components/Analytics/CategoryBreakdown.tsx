import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { CategoryBreakdown as CategoryBreakdownType } from '../../types/analytics';
import { formatCurrency, formatPercentage } from '../../utils/formatters';
import { PieChartIcon } from 'lucide-react';

interface CategoryBreakdownProps {
  breakdown: CategoryBreakdownType[];
}

const COLORS = [
  '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6',
  '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'
];

const CategoryBreakdown: React.FC<CategoryBreakdownProps> = ({ breakdown }) => {
  const chartData = breakdown.slice(0, 10).map((item, index) => ({
    name: item.category,
    value: item.amount,
    percentage: item.percentage,
    fill: COLORS[index % COLORS.length],
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-900">{data.name}</p>
          <p className="text-sm text-gray-600">
            {formatCurrency(data.value)} ({formatPercentage(data.percentage)})
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex items-center space-x-2 mb-6">
        <PieChartIcon className="w-5 h-5 text-purple-600" />
        <h2 className="text-xl font-bold text-gray-900">Répartition par Catégorie</h2>
      </div>

      {breakdown.length === 0 ? (
        <p className="text-gray-500 text-center py-8">Aucune donnée disponible</p>
      ) : (
        <div className="flex flex-col lg:flex-row items-center">
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>

          <div className="lg:ml-6 mt-4 lg:mt-0 w-full lg:w-auto">
            <div className="space-y-2">
              {breakdown.slice(0, 5).map((item, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: COLORS[index % COLORS.length] }}
                    ></div>
                    <span className="text-sm text-gray-700">{item.category}</span>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-gray-900">
                      {formatCurrency(item.amount)}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatPercentage(item.percentage)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CategoryBreakdown;