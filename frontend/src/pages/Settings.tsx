import { Card, CardContent } from '../components/Card';

export function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-neutral-900 mb-1">Settings</h1>
        <p className="text-neutral-600">Configure your application settings</p>
      </div>

      <Card>
        <CardContent>
          <p className="text-neutral-900">Settings page (WIP)</p>
        </CardContent>
      </Card>
    </div>
  );
}
