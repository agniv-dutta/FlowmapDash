import { useState } from 'react';
import { apiClient } from '../api/client';

export default function ApiTest() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<any>(null);

  const testEndpoints = async () => {
    setLoading(true);
    const results: any = {};
    
    try {
      // Test health check
      const health = await apiClient.get('/health');
      results.health = health.status;
      
      // Test sessions endpoint
      const sessions = await apiClient.get('/api/v1/sessions?limit=5');
      results.sessions = sessions.data;
      
      // Test analytics endpoint
      try {
        const analytics = await apiClient.get('/api/v1/analytics/summary');
        results.analytics = analytics.data;
      } catch (analyticsErr) {
        results.analytics = { error: 'Analytics endpoint may not exist' };
      }
      
      setResult(results);
    } catch (err: any) {
      setError({
        message: err.message,
        status: err.response?.status,
        data: err.response?.data
      });
    } finally {
      setLoading(false);
    }
  };

  const seedData = async () => {
    setLoading(true);
    try {
      const response = await apiClient.post('/api/v1/sessions/seed');
      setResult({ seed: response.data });
    } catch (err: any) {
      setError({
        message: err.message,
        status: err.response?.status,
        data: err.response?.data
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Connection Test</h1>
      
      <div className="space-x-4 mb-4">
        <button 
          onClick={testEndpoints}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Testing...' : 'Test API Endpoints'}
        </button>
        
        <button 
          onClick={seedData}
          disabled={loading}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:opacity-50"
        >
          {loading ? 'Seeding...' : 'Seed Sample Data'}
        </button>
      </div>
      
      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">
          <h3 className="font-bold">Error:</h3>
          <pre>{JSON.stringify(error, null, 2)}</pre>
        </div>
      )}
      
      {result && (
        <div className="bg-green-100 text-green-700 p-4 rounded">
          <h3 className="font-bold">Success:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      
      <div className="mt-8">
        <h2 className="text-xl font-bold mb-2">Manual Testing</h2>
        <div className="space-y-2 text-sm">
          <p>• Health check: <code className="bg-gray-100 px-2 py-1 rounded">GET http://localhost:5000/health</code></p>
          <p>• List sessions: <code className="bg-gray-100 px-2 py-1 rounded">GET http://localhost:5000/api/v1/sessions</code></p>
          <p>• Seed data: <code className="bg-gray-100 px-2 py-1 rounded">POST http://localhost:5000/api/v1/sessions/seed</code></p>
        </div>
      </div>
    </div>
  );
}
