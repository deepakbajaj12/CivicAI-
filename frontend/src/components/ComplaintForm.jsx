import React, { useState } from 'react';
import { complaintService } from '../services/api';

const ComplaintForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    citizen_name: '',
    citizen_email: '',
    location: '',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);
    setAnalysis(null);

    try {
      const response = await complaintService.submitComplaint(formData);
      setSuccess(true);
      setAnalysis(response.complaint);
      
      // Reset form
      setFormData({
        citizen_name: '',
        citizen_email: '',
        location: '',
        description: '',
      });

      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit complaint');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Submit a Complaint</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Name
          </label>
          <input
            type="text"
            name="citizen_name"
            value={formData.citizen_name}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Your name"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email
          </label>
          <input
            type="email"
            name="citizen_email"
            value={formData.citizen_email}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="your.email@example.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Location
          </label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Street address or landmark"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description <span className="text-red-500">*</span>
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            rows="5"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe your complaint in detail..."
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Submitting...' : 'Submit Complaint'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {success && analysis && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
          <h3 className="text-lg font-semibold text-green-800 mb-3">
            ✓ Complaint Submitted Successfully!
          </h3>
          
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-gray-700">Category</p>
                <p className="mt-1 text-lg font-semibold text-blue-600">{analysis.category}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Urgency</p>
                <p className={`mt-1 text-lg font-semibold ${
                  analysis.urgency === 'Critical' ? 'text-red-600' :
                  analysis.urgency === 'High' ? 'text-orange-600' :
                  analysis.urgency === 'Medium' ? 'text-yellow-600' :
                  'text-green-600'
                }`}>
                  {analysis.urgency}
                </p>
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-700">AI Summary</p>
              <p className="mt-1 text-gray-800">{analysis.summary}</p>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-700">Analysis Reasoning</p>
              <p className="mt-1 text-sm text-gray-600">{analysis.reasoning}</p>
            </div>

            <div className="pt-2 text-xs text-gray-500">
              <p>Complaint ID: {analysis._id}</p>
              <p>Status: {analysis.status}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComplaintForm;
