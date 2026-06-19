import { Bell, HelpCircle, Search, Menu } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { Input } from './Input';

export function Header() {
  const { toggleSidebar } = useAppStore();

  return (
    <header className="h-16 border-b border-neutral-200 bg-neutral-50 px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-4">
        <button onClick={toggleSidebar} className="md:hidden text-neutral-600 hover:text-neutral-900">
          <Menu className="h-5 w-5" />
        </button>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden md:block w-64">
          <Input
            icon={<Search className="h-4 w-4" />}
            placeholder="Search sessions..."
            className="bg-neutral-100 border-none h-9 rounded-full"
          />
        </div>
        <button className="text-neutral-600 hover:text-neutral-900">
          <Bell className="h-5 w-5" />
        </button>
        <button className="text-neutral-600 hover:text-neutral-900">
          <HelpCircle className="h-5 w-5" />
        </button>
        <div className="h-8 w-8 rounded-full bg-neutral-300 overflow-hidden">
          <img src="https://i.pravatar.cc/100" alt="User Avatar" />
        </div>
      </div>
    </header>
  );
}
