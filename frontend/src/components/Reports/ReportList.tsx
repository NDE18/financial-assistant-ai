import React, { useEffect, useState } from 'react';
import { reportService } from '../../services/reportService';
import { Report } from '../../types/report';
import { formatDate } from '../../utils/formatters';
import { FileText, Clock, CheckCircle, XCircle, Trash2 } from 'lucide-react';
import ReportGenerator from './ReportGenerator';

const ReportList: React.FC = () => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      const data = await reportService.getAll();
      setReports(data);
    } catch (error) {
      console.error('Error loading reports:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Supprimer ce rapport ?')) {
      try {
        await reportService.delete(id);
        await loadReports();
      } catch (error) {
        console.error('Error deleting report:', error);
      }
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return <Clock className="w-5 h-5 text-orange-600 animate-spin" />;
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Rapports Financiers</h1>
        <p className="text-gray-500 mt-1">Générez des rapports automatisés avec l'IA</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <ReportGenerator onReportGenerated={loadReports} />
        </div>

        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-md">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">Rapports Générés</h2>
            </div>

            {loading ? (
              <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : reports.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                Aucun rapport généré
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {reports.map((report) => (
                  <div
                    key={report.id}
                    className="p-6 hover:bg-gray-50 transition"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4 flex-1">
                        <FileText className="w-6 h-6 text-blue-600 mt-1" />
                        <div className="flex-1">
                          <h3 className="font-bold text-gray-900">{report.title}</h3>
                          <p className="text-sm text-gray-600 mt-1">
                            {formatDate(report.start_date)} - {formatDate(report.end_date)}
                          </p>
                          {report.summary && (
                            <p className="text-sm text-gray-700 mt-2 line-clamp-2">
                              {report.summary}
                            </p>
                          )}
                          <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                            <span>Créé le {formatDate(report.created_at)}</span>
                            {report.completed_at && (
                              <span>Complété le {formatDate(report.completed_at)}</span>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3 ml-4">
                        {getStatusIcon(report.status)}
                        <button
                          onClick={() => handleDelete(report.id)}
                          className="p-1 text-red-600 hover:bg-red-50 rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportList;