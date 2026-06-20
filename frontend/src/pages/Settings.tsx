import { useState } from 'react';
import { Moon, Lock, Key, Download, Trash2, Mail, Shield } from 'lucide-react';

export function Settings() {
  const [settings, setSettings] = useState({
    darkMode: true,
    emailNotifications: true,
    sessionTracking: true,
    dataRetention: '90',
  });

  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved'>('idle');

  const handleChange = (key: string, value: any) => {
    setSettings({ ...settings, [key]: value });
  };

  const handleSave = () => {
    setSaveStatus('saving');
    setTimeout(() => {
      localStorage.setItem('appSettings', JSON.stringify(settings));
      setSaveStatus('saved');
      setTimeout(() => setSaveStatus('idle'), 2000);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-neutral-950 p-8">
      <div className="max-w-2xl">
        <h1 className="text-4xl font-bold text-white mb-2">Settings</h1>
        <p className="text-neutral-400 mb-8">Configure your FlowmapDash preferences</p>

        {/* Dark Mode */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 mb-6 hover:border-neutral-700 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-neutral-800 p-3 rounded-lg">
                <Moon size={20} className="text-neutral-400" />
              </div>
              <div>
                <span className="text-white font-medium block">Dark Mode</span>
                <span className="text-neutral-500 text-sm">Use dark theme for better visibility</span>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.darkMode}
                onChange={(e) => handleChange('darkMode', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
            </label>
          </div>
        </div>

        {/* Email Notifications */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 mb-6 hover:border-neutral-700 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-neutral-800 p-3 rounded-lg">
                <Mail size={20} className="text-neutral-400" />
              </div>
              <div>
                <span className="text-white font-medium block">Email Notifications</span>
                <span className="text-neutral-500 text-sm">Receive alerts for activity</span>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.emailNotifications}
                onChange={(e) => handleChange('emailNotifications', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
            </label>
          </div>
        </div>

        {/* Session Tracking */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 mb-6 hover:border-neutral-700 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-neutral-800 p-3 rounded-lg">
                <Shield size={20} className="text-neutral-400" />
              </div>
              <div>
                <span className="text-white font-medium block">Session Tracking</span>
                <span className="text-neutral-500 text-sm">Enable session recording</span>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.sessionTracking}
                onChange={(e) => handleChange('sessionTracking', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
            </label>
          </div>
        </div>

        {/* Data Retention */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 mb-6 hover:border-neutral-700 transition-colors">
          <div className="flex items-center gap-4 mb-4">
            <div className="bg-neutral-800 p-3 rounded-lg">
              <Lock size={20} className="text-neutral-400" />
            </div>
            <label className="text-white font-medium">Data Retention Period</label>
          </div>
          <select
            value={settings.dataRetention}
            onChange={(e) => handleChange('dataRetention', e.target.value)}
            className="bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-2 text-white w-full hover:border-neutral-600 transition-colors focus:border-primary-500 focus:outline-none"
          >
            <option value="30">30 days</option>
            <option value="90">90 days</option>
            <option value="180">6 months</option>
            <option value="365">1 year</option>
          </select>
          <p className="text-neutral-500 text-sm mt-2">How long to keep your session data</p>
        </div>

        {/* API Key Management */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 mb-8 hover:border-neutral-700 transition-colors">
          <h3 className="text-white font-medium mb-4 flex items-center gap-2">
            <Key size={18} />
            API Key Management
          </h3>
          <div className="bg-neutral-950 border border-neutral-700 rounded-lg p-3 font-mono text-sm text-neutral-400 mb-4 break-all">
            fmd_api_example_placeholder_key_12345...
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => navigator.clipboard.writeText('fmd_api_example_placeholder_key_12345')}
              className="flex items-center gap-2 px-4 py-2 bg-neutral-800 text-neutral-100 rounded-lg hover:bg-neutral-700 transition-colors text-sm font-medium"
            >
              Copy API Key
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-neutral-800 text-neutral-100 rounded-lg hover:bg-neutral-700 transition-colors text-sm font-medium">
              <Key size={14} />
              Regenerate
            </button>
          </div>
        </div>

        {/* Danger Zone */}
        <div className="bg-red-950 border border-red-800 rounded-lg p-6 mb-8">
          <h3 className="text-red-200 font-medium mb-4 flex items-center gap-2">
            <Trash2 size={18} />
            Danger Zone
          </h3>
          <p className="text-red-300 text-sm mb-4">Irreversible actions. Be careful.</p>
          <button className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium">
            <Download size={14} />
            Export My Data
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-red-900 text-red-100 rounded-lg hover:bg-red-800 transition-colors text-sm font-medium mt-2">
            <Trash2 size={14} />
            Delete Account
          </button>
        </div>

        {/* Save Button */}
        <button
          onClick={handleSave}
          disabled={saveStatus === 'saving'}
          className={`px-6 py-3 rounded-lg font-medium text-white transition-colors ${
            saveStatus === 'saved'
              ? 'bg-green-600 hover:bg-green-700'
              : saveStatus === 'saving'
              ? 'bg-primary-600 opacity-75 cursor-not-allowed'
              : 'bg-primary-500 hover:bg-primary-600'
          }`}
        >
          {saveStatus === 'saving' ? 'Saving...' : saveStatus === 'saved' ? 'Saved' : 'Save Settings'}
        </button>
      </div>
    </div>
  );
}
