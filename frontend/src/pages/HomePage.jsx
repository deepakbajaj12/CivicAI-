import React, { useState } from 'react';
import ComplaintForm from '../components/ComplaintForm';
import AdminDashboard from '../components/AdminDashboard';

const HomePage = () => {
  const [activeTab, setActiveTab] = useState('submit');

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold">CivicAI</h1>
          <p className="text-blue-100 mt-1">Smart City Complaint Intelligence System</p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="container mx-auto px-4">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('submit')}
              className={`py-4 px-2 border-b-2 font-medium text-sm ${
                activeTab === 'submit'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Submit Complaint
            </button>
            <button
              onClick={() => setActiveTab('admin')}
              className={`py-4 px-2 border-b-2 font-medium text-sm ${
                activeTab === 'admin'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Admin Dashboard
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {activeTab === 'submit' && (
          <div className="max-w-2xl mx-auto">
            <ComplaintForm onSuccess={() => setActiveTab('admin')} />
          </div>
        )}
        {activeTab === 'admin' && <AdminDashboard />}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center">
            <p className="text-sm">
              © 2024 CivicAI - Smart City Complaint Intelligence System
            </p>
            <p className="text-xs text-gray-400 mt-2">
              Powered by GenAI (OpenAI/Gemini/Cohere) • Built with React & Flask
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
