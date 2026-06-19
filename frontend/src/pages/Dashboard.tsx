import { ArrowUpRight, Zap, BarChart2 } from 'lucide-react';
import { Card, CardContent } from '../components/Card';

export function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-neutral-900 mb-1">Dashboard</h1>
        <p className="text-neutral-600">Real-time overview of your user sessions</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-neutral-600 mb-2">Total Sessions</p>
              <h2 className="text-4xl font-bold text-neutral-900 mb-4">2,847</h2>
              <div className="flex items-center text-accent-sage text-sm">
                <ArrowUpRight className="h-4 w-4 mr-1" />
                <span>12% increase from last week</span>
              </div>
            </div>
            <div className="h-10 w-10 rounded-full bg-primary-500/20 text-primary-500 flex items-center justify-center">
              <BarChart2 className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-neutral-600 mb-2">Total Events</p>
              <h2 className="text-4xl font-bold text-neutral-900 mb-4">28,471</h2>
              <div className="flex items-center text-accent-sage text-sm">
                <ArrowUpRight className="h-4 w-4 mr-1" />
                <span>8.4k new events today</span>
              </div>
            </div>
            <div className="h-10 w-10 rounded-full bg-accent-teal/20 text-accent-teal flex items-center justify-center">
              <Zap className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-neutral-600 mb-2">Avg Events/Session</p>
              <h2 className="text-4xl font-bold text-neutral-900 mb-4">10.0</h2>
              <div className="flex items-center text-neutral-600 text-sm">
                <span className="flex items-center justify-center h-4 w-4 rounded-full border border-neutral-600 mr-1 text-[10px]">✓</span>
                <span>Optimal performance stable</span>
              </div>
            </div>
            <div className="h-10 w-10 rounded-full bg-accent-sand/20 text-accent-sand flex items-center justify-center">
              <BarChart2 className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Chart mock */}
      <Card>
        <CardContent>
          <div className="flex justify-between items-center mb-6">
            <div>
              <h3 className="text-lg font-semibold text-neutral-900">Events Over Time</h3>
              <p className="text-sm text-neutral-600">Daily event volume for the last 7 days</p>
            </div>
            <div className="flex space-x-2">
              <button className="px-3 py-1 bg-neutral-200 text-neutral-900 text-sm rounded">7 Days</button>
              <button className="px-3 py-1 text-neutral-600 hover:text-neutral-900 text-sm rounded">30 Days</button>
            </div>
          </div>
          <div className="h-64 flex items-end justify-between px-2 gap-4">
             {/* Chart bars mock */}
             {[1, 1.2, 0.8, 1.5, 1.1, 0.5, 2].map((v, i) => (
                <div key={i} className="w-full bg-primary-700/50 rounded-t-lg relative flex items-end justify-center group hover:bg-primary-600/50 transition-colors" style={{ height: `${v * 40}%` }}>
                  <span className="absolute -bottom-6 text-xs text-neutral-600">
                    {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Today'][i]}
                  </span>
                </div>
             ))}
          </div>
          <div className="h-6"></div>
        </CardContent>
      </Card>
    </div>
  );
}
