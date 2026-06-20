import { Bell, HelpCircle, User, LogOut, Menu, X } from 'lucide-react';
import { useState } from 'react';

export function Header() {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [notifications] = useState([
    { id: 1, message: '5 new sessions recorded', time: '2 min ago' },
    { id: 2, message: 'High click volume on /products', time: '1 hour ago' },
  ]);

  return (
    <header className="h-16 bg-neutral-950 border-b border-neutral-800 flex items-center justify-between px-8 sticky top-0 z-40">
      {/* Left: Search */}
      <div className="flex-1 max-w-md">
        <input
          type="text"
          placeholder="Search sessions..."
          className="w-full bg-neutral-900 border border-neutral-700 rounded-lg px-4 py-2 text-neutral-100 placeholder-neutral-500 text-sm"
        />
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-4 ml-8">

        {/* NOTIFICATIONS */}
        <div className="relative">
          <button
            onClick={() => {
              setShowNotifications(!showNotifications);
              setShowHelp(false);
              setShowUserMenu(false);
            }}
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
            <div className="absolute right-0 mt-2 w-80 bg-neutral-900 border border-neutral-700 rounded-lg shadow-xl z-50">
              <div className="p-4 border-b border-neutral-700">
                <h3 className="text-neutral-100 font-semibold">Notifications</h3>
              </div>
              
              {notifications.length > 0 ? (
                <div className="max-h-96 overflow-y-auto">
                  {notifications.map(notif => (
                    <div key={notif.id} className="p-4 border-b border-neutral-800 hover:bg-neutral-800 transition-colors">
                      <p className="text-neutral-200 text-sm">{notif.message}</p>
                      <p className="text-neutral-500 text-xs mt-1">{notif.time}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center">
                  <p className="text-neutral-400 text-sm">No notifications</p>
                </div>
              )}
              
              <div className="p-4 border-t border-neutral-700">
                <button className="w-full text-center text-primary-500 hover:text-primary-400 text-sm font-medium">
                  View All
                </button>
              </div>
            </div>
          )}
        </div>

        {/* HELP */}
        <div className="relative">
          <button
            onClick={() => {
              setShowHelp(!showHelp);
              setShowNotifications(false);
              setShowUserMenu(false);
            }}
            className="p-2 hover:bg-neutral-800 rounded-lg transition-colors group"
            title="Help & Documentation"
          >
            <HelpCircle size={20} className="text-neutral-400 group-hover:text-neutral-200" />
          </button>

          {showHelp && (
            <div className="absolute right-0 mt-2 w-80 bg-neutral-900 border border-neutral-700 rounded-lg shadow-xl z-50">
              <div className="p-6">
                <h3 className="text-neutral-100 font-semibold mb-4">Help & Resources</h3>
                
                <div className="space-y-3">
                  <a href="#docs" className="block p-3 bg-neutral-800 rounded-lg hover:bg-neutral-700 transition-colors">
                    <p className="text-neutral-100 font-medium text-sm">📚 Documentation</p>
                    <p className="text-neutral-400 text-xs mt-1">Complete guides and API docs</p>
                  </a>
                  
                  <a href="#guide" className="block p-3 bg-neutral-800 rounded-lg hover:bg-neutral-700 transition-colors">
                    <p className="text-neutral-100 font-medium text-sm">🎯 Getting Started</p>
                    <p className="text-neutral-400 text-xs mt-1">Setup your first tracking</p>
                  </a>
                  
                  <a href="#faq" className="block p-3 bg-neutral-800 rounded-lg hover:bg-neutral-700 transition-colors">
                    <p className="text-neutral-100 font-medium text-sm">❓ FAQ</p>
                    <p className="text-neutral-400 text-xs mt-1">Common questions answered</p>
                  </a>
                </div>

                <div className="mt-4 pt-4 border-t border-neutral-700">
                  <p className="text-neutral-400 text-xs">Need more help?</p>
                  <a href="mailto:support@example.com" className="text-primary-500 hover:text-primary-400 text-sm font-medium">
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
            onClick={() => {
              setShowUserMenu(!showUserMenu);
              setShowNotifications(false);
              setShowHelp(false);
            }}
            className="p-2 hover:bg-neutral-800 rounded-lg transition-colors group"
            title="Account"
          >
            <User size={20} className="text-neutral-400 group-hover:text-neutral-200" />
          </button>

          {showUserMenu && (
            <div className="absolute right-0 mt-2 w-64 bg-neutral-900 border border-neutral-700 rounded-lg shadow-xl z-50">
              {/* User Info */}
              <div className="p-4 border-b border-neutral-700">
                <p className="text-neutral-100 font-semibold">Demo User</p>
                <p className="text-neutral-400 text-sm">demo@flowmapdash.app</p>
                <p className="text-neutral-500 text-xs mt-2">Plan: Free</p>
              </div>

              {/* Menu Items */}
              <div className="p-2">
                <a href="/settings" className="flex items-center gap-3 px-4 py-3 hover:bg-neutral-800 rounded-lg transition-colors">
                  <User size={16} className="text-neutral-400" />
                  <span className="text-neutral-100 text-sm">Profile Settings</span>
                </a>
                
                <a href="/settings" className="flex items-center gap-3 px-4 py-3 hover:bg-neutral-800 rounded-lg transition-colors">
                  <Menu size={16} className="text-neutral-400" />
                  <span className="text-neutral-100 text-sm">Preferences</span>
                </a>
                
                <a href="/api-keys" className="flex items-center gap-3 px-4 py-3 hover:bg-neutral-800 rounded-lg transition-colors">
                  <Menu size={16} className="text-neutral-400" />
                  <span className="text-neutral-100 text-sm">API Keys</span>
                </a>
              </div>

              {/* Logout */}
              <div className="p-2 border-t border-neutral-700">
                <button
                  onClick={() => {
                    alert('Logged out');
                    setShowUserMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-neutral-800 rounded-lg transition-colors text-red-400 hover:text-red-300"
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
