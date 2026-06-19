import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, ListFilter, Activity, Settings } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { cn } from '../lib/utils';

export function Sidebar() {
  const { isSidebarOpen } = useAppStore();
  const location = useLocation();

  const navItems = [
    { label: 'Dashboard', path: '/', icon: LayoutDashboard },
    { label: 'Sessions', path: '/sessions', icon: ListFilter },
    { label: 'Heatmap', path: '/heatmap', icon: Activity },
    { label: 'Settings', path: '/settings', icon: Settings },
  ];

  if (!isSidebarOpen) return null;

  return (
    <aside className="w-64 border-r border-neutral-200 bg-neutral-50 h-screen flex flex-col fixed md:sticky top-0 z-40">
      <div className="p-6">
        <h1 className="text-xl font-bold text-primary-500">FlowmapDash</h1>
        <p className="text-xs text-neutral-600 mt-1">User Analytics</p>
      </div>

      <nav className="flex-1 px-4 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 px-3 py-2 rounded-base text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary-500 text-neutral-900'
                  : 'text-neutral-600 hover:bg-neutral-200 hover:text-neutral-900'
              )}
            >
              <item.icon className="h-5 w-5" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 mt-auto">
        <div className="bg-neutral-100 rounded-lg p-3 border border-neutral-200 flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-accent-sage/20 text-accent-sage flex items-center justify-center font-bold text-sm">
            F
          </div>
          <div>
            <p className="text-sm font-semibold text-neutral-900">Flow State</p>
            <p className="text-xs text-neutral-600">Team Plan</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
