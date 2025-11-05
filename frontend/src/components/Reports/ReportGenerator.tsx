import React, { useState } from 'react';
import { reportService } from '../../services/reportService';
import { FileText, Calendar } from 'lucide-react';

interface ReportGeneratorProps {
  onReportGenerated: () => void;
}

const ReportGenerator: React.FC<ReportGeneratorProps> = ({ onReportGenerated }) => {
  const [formData, setFormData] = useState({
    title: '',
    type: 'monthly',
    start_date: '',
    end_date: '',
  });
  const [generating, setGenerating] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);

    try {
      await reportService.create({
        ...formData,
        start_date: new Date(formData.start_date).toISOString(),
        end_date: new Date(formData.end_date).toISOString(),
      });
      
      setFormData({
        title: '',
        type: 'monthly',
        start_date: '',
        end_date: '',
      });
      
      onReportGenerated();
      alert('Rapport en cours de génération! L\'IA analyse vos données...');
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Erreur lors de la génération du rapport.');
    } finally {
      setGenerating(false);
    }
  };

  const quickPeriods = [
    {
      label: 'Ce mois',
      onClick: () => {
        const now = new Date();
        const start = new Date(now.getFullYear(), now.getMonth(), 1);
        const end = now;
        setFormData({
          ...formData,
          start_date: start.toISOString().split('T')[0],
          end_date: end.toISOString().split('T')[0],
          title: `Rapport ${now.toLocaleString('fr-FR', { month: 'long', year: 'numeric' })}`,
        });
      },
    },
    {
      label: 'Mois dernier',
      onClick: () => {
        const now = new Date();
        const start = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        const end = new Date(now.getFullYear(), now.getMonth(), 0);
        setFormData({
          ...formData,
          start_date: start.toISOString().split('T')[0],
          end_date: end.toISOString().split('T')[0],
          title: `Rapport ${start.toLocaleString('fr-FR', { month: 'long', year: 'numeric' })}`,
        });
      },
    },
    {
      label: 'Ce trimestre',
      onClick: () => {
        const now = new Date();
        const quarter = Math.floor(now.getMonth() / 3);
        const start = new Date(now.getFullYear(), quarter * 3, 1);
        const end = now;
        setFormData({
          ...formData,
          start_date: start.toISOString().split('T')[0],
          end_date: end.toISOString().split('T')[0],
          title: `Rapport Q${quarter + 1} ${now.getFullYear()}`,
        });
      },
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex items-center space-x-2 mb-6">
        <FileText className="w-6 h-6 text-blue-600" />
        <h3 className="text-lg font-bold text-gray-900">Générer un Rapport</h3>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Titre du rapport *
          </label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Ex: Rapport mensuel Mars 2024"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Périodes rapides
          </label>
          <div className="flex flex-wrap gap-2">
            {quickPeriods.map((period, idx) => (
              <button
                key={idx}
                type="button"
                onClick={period.onClick}
                className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
              >
                {period.label}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date début *
            </label>
            <input
              type="date"
              required
              value={formData.start_date}
              onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date fin *
            </label>
            <input
              type="date"
              required
              value={formData.end_date}
              onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={generating}
          className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
        >
          {generating ? 'Génération en cours...' : 'Générer le rapport (IA)'}
        </button>
      </form>

      <div className="mt-4 bg-purple-50 rounded-lg p-4">
        <p className="text-sm text-purple-800">
          <strong>🤖 Analyse IA:</strong> L'assistant analysera vos données et générera
          un rapport complet avec insights, tendances et recommandations personnalisées.
        </p>
      </div>
    </div>
  );
};

export default ReportGenerator;