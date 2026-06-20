import { Bell, HelpCircle, User, LogOut, BookOpen, MessageCircle } from 'lucide-react';
import { useState } from 'react';
import { useNotifications } from '../hooks/useNotifications';

export function Header() {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const { data: notifications = [] } = useNotifications();

  const openNotifications = () => {
    setShowNotifications(true);
    setShowHelp(false);
    setShowUserMenu(false);
  };

  const openHelp = () => {
    setShowHelp(true);
    setShowNotifications(false);
    setShowUserMenu(false);
  };

  const openUserMenu = () => {
    setShowUserMenu(true);
    setShowNotifications(false);
    setShowHelp(false);
  };

  return (
    <header className="h-16 bg-neutral-950 border-b border-neutral-800 flex items-center justify-between px-8 sticky top-0 z-40">
      <div className="flex-1 max-w-md">
        <input
          type="text"
          placeholder="Search sessions..."
          className="w-full bg-neutral-900 border border-neutral-700 rounded-lg px-4 py-2 text-neutral-100 placeholder-neutral-500 text-sm"
        />
      </div>

      <div className="flex items-center gap-4 ml-8">

        {/* NOTIFICATIONS */}
        <div className="relative">
          <button
            onClick={openNotifications}
            className="p-2 hover:bg-neutral-800 rounded-lg transition-colors relative group"
            title="Notifications"
          >
            <Bell size={20} className="text-neutral-400 group-hover:text-neutral-200" />
            {notifications.length > 0 && (
              <span className="absolute top-1 right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                {notifications.length}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-neutral-100 border border-neutral-300 rounded-lg shadow-xl z-50">
              <div className="p-4 border-b border-neutral-300">
                <h3 className="text-neutral-900 font-semibold flex items-center gap-2">
                  <Bell size={18} />
                  Notifications
                </h3>
              </div>
              {notifications.length > 0 ? (
                <div className="max-h-96 overflow-y-auto">
                  {notifications.map((notif: any) => (
                    <div key={notif.id} className="p-4 border-b border-neutral-200 hover:bg-neutral-50 transition-colors">
                      <p className="text-neutral-900 text-sm font-medium">{notif.message}</p>
                      <p className="text-neutral-500 text-xs mt-1">{notif.timestamp}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center">
                  <Bell size={32} className="mx-auto text-neutral-300 mb-2" />
                  <p className="text-neutral-600 text-sm">No notifications yet</p>
                </div>
              )}
              <div className="p-4 border-t border-neutral-300">
                <button className="w-full text-center text-primary-500 hover:text-primary-600 text-sm font-medium">
                  View All
                </button>
              </div>
            </div>
          )}
        </div>

        {/* HELP */}
        <div className="relative">
          <button
            onClick={openHelp}
            className="p-2 hover:bg-neutral-800 rounded-lg transition-colors group"
            title="Help & Documentation"
          >
            <HelpCircle size={20} className="text-neutral-400 group-hover:text-neutral-200" />
          </button>

          {showHelp && (
            <div className="absolute right-0 mt-2 w-80 bg-neutral-100 border border-neutral-300 rounded-lg shadow-xl z-50">
              <div className="p-6">
                <h3 className="text-neutral-900 font-semibold mb-4 flex items-center gap-2">
                  <HelpCircle size={20} />
                  Help & Resources
                </h3>
                <div className="space-y-3">
                  <a href="#docs" className="block p-3 bg-neutral-200 rounded-lg hover:bg-neutral-300 transition-colors">
                    <p className="text-neutral-900 font-medium text-sm flex items-center gap-2">
                      <BookOpen size={16} />
                      Documentation
                    </p>
                    <p className="text-neutral-700 text-xs mt-1">Complete guides and API docs</p>
                  </a>
                  <a href="#guide" className="block p-3 bg-neutral-200 rounded-lg hover:bg-neutral-300 transition-colors">
                    <p className="text-neutral-900 font-medium text-sm flex items-center gap-2">
                      <MessageCircle size={16} />
                      Getting Started
                    </p>
                    <p className="text-neutral-700 text-xs mt-1">Setup your first tracking</p>
                  </a>
                  <a href="#faq" className="block p-3 bg-neutral-200 rounded-lg hover:bg-neutral-300 transition-colors">
                    <p className="text-neutral-900 font-medium text-sm flex items-center gap-2">
                      <HelpCircle size={16} />
                      FAQ
                    </p>
                    <p className="text-neutral-700 text-xs mt-1">Common questions answered</p>
                  </a>
                </div>
                <div className="mt-4 pt-4 border-t border-neutral-300">
                  <p className="text-neutral-600 text-xs">Need more help?</p>
                  <a href="mailto:support@example.com" className="text-primary-500 hover:text-primary-600 text-sm font-medium">
                    Contact Support →
                  </a>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* USER MENU */}
        <div className="relative">
          <button
            onClick={openUserMenu}
            className="p-2 hover:bg-neutral-800 rounded-lg transition-colors group"
            title="Account"
          >
            <User size={20} className="text-neutral-400 group-hover:text-neutral-200" />
          </button>

          {showUserMenu && (
            <div className="absolute right-0 mt-2 w-64 bg-neutral-100 border border-neutral-300 rounded-lg shadow-xl z-50">
              <div className="p-4 border-b border-neutral-300">
                <p className="text-neutral-900 font-semibold">Demo User</p>
                <p className="text-neutral-600 text-sm">demo@flowmapdash.app</p>
                <p className="text-neutral-500 text-xs mt-2 flex items-center gap-1">
                  Plan: <span className="font-medium">Free</span>
                </p>
              </div>
              <div className="p-2">
                <a href="/settings" className="flex items-center gap-3 px-4 py-3 hover:bg-neutral-200 rounded-lg transition-colors">
                  <User size={16} className="text-neutral-600" />
                  <span className="text-neutral-900 text-sm">Profile Settings</span>
                </a>
                <a href="/settings" className="flex items-center gap-3 px-4 py-3 hover:bg-neutral-200 rounded-lg transition-colors">
                  <BookOpen size={16} className="text-neutral-600" />
                  <span className="text-neutral-900 text-sm">Preferences</span>
                </a>
                <a href="#api-keys" className="flex items-center gap-3 px-4 py-3 hover:bg-neutral-200 rounded-lg transition-colors">
                  <MessageCircle size={16} className="text-neutral-600" />
                  <span className="text-neutral-900 text-sm">API Keys</span>
                </a>
              </div>
              <div className="p-2 border-t border-neutral-300">
                <button
                  onClick={() => {
                    alert('Logged out');
                    setShowUserMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-red-100 rounded-lg transition-colors text-red-600 hover:text-red-700"
                >
                  <LogOut size={16} />
                  <span className="text-sm font-medium">Logout</span>
                </button>
              </div>
            </div>
          )}
        </div>

      </div>
    </header>
  );
}

export default Header;
