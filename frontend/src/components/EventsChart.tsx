import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useAnalytics } from '../hooks/useAnalytics';

const EventsChart = () => {
  const [timeRange, setTimeRange] = useState<'7d' | '30d'>('7d');
  const { data, isLoading } = useAnalytics();

  if (isLoading) return <div className="h-80 bg-neutral-50 animate-pulse rounded-lg" />;

  // Transform backend data to chart format
  const chartData = data?.chartData || [
    { day: 'Mon', events: 1200 },
    { day: 'Tue', events: 1900 },
    { day: 'Wed', events: 1100 },
    { day: 'Thu', events: 2100 },
    { day: 'Fri', events: 1800 },
    { day: 'Sat', events: 900 },
    { day: 'Today', events: 2900 },
  ];

  return (
    <div className="bg-neutral-50 rounded-lg border border-neutral-200 p-6">
      <div className="flex justify-between items-center mb-2">
        <div>
          <h3 className="text-lg font-bold text-neutral-900">Events Over Time</h3>
          <p className="text-sm text-neutral-600">Daily event volume for the last {timeRange === '7d' ? '7' : '30'} days</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={() => setTimeRange('7d')}
            className={`text-sm px-3 py-1 rounded ${timeRange === '7d' ? 'bg-neutral-200 text-neutral-900' : 'text-neutral-500 hover:text-neutral-900'}`}
          >
            7 Days
          </button>
          <button 
            onClick={() => setTimeRange('30d')}
            className={`text-sm px-3 py-1 rounded ${timeRange === '30d' ? 'bg-neutral-200 text-neutral-900' : 'text-neutral-500 hover:text-neutral-900'}`}
          >
            30 Days
          </button>
        </div>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E8E4E0" />
          <XAxis dataKey="day" stroke="#6B6B6B" />
          <YAxis stroke="#6B6B6B" />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#FAFBF9', 
              border: '1px solid #E8E4E0',
              borderRadius: '6px'
            }}
            formatter={(value: any) => [Number(value)?.toLocaleString() || '0', 'Events']}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="events" 
            stroke="#8B5A3C" 
            strokeWidth={3}
            dot={{ fill: '#8B5A3C', r: 5 }}
            activeDot={{ r: 7 }}
            name="Events"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EventsChart;
