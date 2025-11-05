import React from 'react';
import { KPIData } from '../../types/analytics';
import { formatCurrency, formatPercentage } from '../../utils/formatters';
import { TrendingUp, TrendingDown, DollarSign, PiggyBank } from 'lucide-react';

interface KPICardsProps {
  kpis: KPIData;
}

const KPICards: React.FC<KPICardsProps> = ({ kpis }) => {
  const cards = [
    {
      title: 'Revenus Total',
      value: formatCurrency(kpis.total_income),
      icon: TrendingUp,
      color: 'bg-green-500',
      textColor: 'text-green-600',
    },
    {
      title: 'Dépenses Total',
      value: formatCurrency(kpis.total_expenses),
      icon: TrendingDown,
      color: 'bg-red-500',
      textColor: 'text-red-600',
    },
    {
      title: 'Solde Net',
      value: formatCurrency(kpis.net_balance),
      icon: DollarSign,
      color: kpis.net_balance >= 0 ? 'bg-blue-500' : 'bg-orange-500',
      textColor: kpis.net_balance >= 0 ? 'text-blue-600' : 'text-orange-600',
    },
    {
      title: 'Taux d\'Épargne',
      value: formatPercentage(kpis.savings_rate),
      icon: PiggyBank,
      color: 'bg-purple-500',
      textColor: 'text-purple-600',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{card.title}</p>
                <p className={`text-2xl font-bold ${card.textColor}`}>
                  {card.value}
                </p>
              </div>
              <div className={`${card.color} bg-opacity-10 p-3 rounded-lg`}>
                <Icon className={`w-6 h-6 ${card.textColor}`} />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default KPICards;