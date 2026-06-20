import { ArrowUpRight, Zap, BarChart2, Check } from 'lucide-react';
import { Card, CardContent } from '../components/Card';
import EventsChart from '../components/EventsChart';

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
                <span className="flex items-center justify-center h-4 w-4 rounded-full border border-neutral-600 mr-1"><Check size={10} /></span>
                <span>Optimal performance stable</span>
              </div>
            </div>
            <div className="h-10 w-10 rounded-full bg-accent-sand/20 text-accent-sand flex items-center justify-center">
              <BarChart2 className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Events Chart */}
      <EventsChart />
    </div>
  );
}
