import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Receipt,
  FileText,
  BarChart3,
  Menu,
  X,
  Sparkles
} from 'lucide-react';
import Dashboard from './components/Dashboard/Dashboard';
import TransactionList from './components/Transactions/TransactionList';
import InvoiceList from './components/Invoices/InvoiceList';
import ReportList from './components/Reports/ReportList';

const App: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);

  const navigation = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Transactions', path: '/transactions', icon: Receipt },
    { name: 'Factures', path: '/invoices', icon: FileText },
    { name: 'Rapports', path: '/reports', icon: BarChart3 },
  ];

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Mobile menu button */}
        <div className="lg:hidden fixed top-4 left-4 z-50">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 bg-white rounded-lg shadow-md"
          >
            {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Sidebar */}
        <aside
          className={`fixed top-0 left-0 z-40 h-screen w-64 bg-gradient-to-b from-blue-900 to-purple-900 text-white transition-transform ${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          } lg:translate-x-0`}
        >
          <div className="p-6">
            <div className="flex items-center space-x-2 mb-8">
              <Sparkles className="w-8 h-8 text-yellow-400" />
              <div>
                <h1 className="text-xl font-bold">FinanceAI</h1>
                <p className="text-xs text-blue-200">Assistant Intelligent</p>
              </div>
            </div>

            <nav className="space-y-2">
              {navigation.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.name}
                    to={item.path}
                    onClick={() => setSidebarOpen(false)}
                    className={({ isActive }) =>
                      `flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
                        isActive
                          ? 'bg-white bg-opacity-20'
                          : 'hover:bg-white hover:bg-opacity-10'
                      }`
                    }
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.name}</span>
                  </NavLink>
                );
              })}
            </nav>

            <div className="mt-8 p-4 bg-blue-800 bg-opacity-50 rounded-lg">
              <p className="text-xs text-blue-200 mb-2">🤖 IA Collaborative</p>
              <p className="text-sm font-medium">
                Orchestration CrewAI avec agents spécialisés
              </p>
            </div>
          </div>
        </aside>

        {/* Main content */}
        <main className="lg:ml-64 min-h-screen">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/transactions" element={<TransactionList />} />
            <Route path="/invoices" element={<InvoiceList />} />
            <Route path="/reports" element={<ReportList />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;