import { ColumnDef } from '@tanstack/react-table';
import { DataTable } from '../components/DataTable';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { ENDPOINTS } from '../api/endpoints';

interface Session {
  id: string;
  userId: string;
  startTime: string;
  endTime: string;
  eventCount: number;
  duration: number;
  device: string;
  browser: string;
}

const columns: ColumnDef<Session>[] = [
  {
    header: 'Session ID',
    accessorKey: 'id',
  },
  {
    header: 'User ID',
    accessorKey: 'userId',
  },
  {
    header: 'Start Time',
    accessorKey: 'startTime',
  },
  {
    header: 'End Time',
    accessorKey: 'endTime',
  },
  {
    header: 'Events',
    accessorKey: 'eventCount',
  },
  {
    header: 'Duration (s)',
    accessorKey: 'duration',
  },
  {
    header: 'Device',
    accessorKey: 'device',
  },
  {
    header: 'Browser',
    accessorKey: 'browser',
  },
];

export function Sessions() {
  const { data, isLoading } = useQuery({
    queryKey: ['sessions'],
    queryFn: async () => {
      const response = await apiClient.get(ENDPOINTS.SESSIONS);
      return response.data;
    },
  });

  const sessions = data || [
    {
      id: 'sess_001',
      userId: 'user_123',
      startTime: '2024-01-15 10:30:00',
      endTime: '2024-01-15 11:45:00',
      eventCount: 245,
      duration: 4500,
      device: 'Desktop',
      browser: 'Chrome',
    },
    {
      id: 'sess_002',
      userId: 'user_456',
      startTime: '2024-01-15 12:00:00',
      endTime: '2024-01-15 12:30:00',
      eventCount: 89,
      duration: 1800,
      device: 'Mobile',
      browser: 'Safari',
    },
    {
      id: 'sess_003',
      userId: 'user_789',
      startTime: '2024-01-15 14:15:00',
      endTime: '2024-01-15 15:00:00',
      eventCount: 312,
      duration: 2700,
      device: 'Desktop',
      browser: 'Firefox',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-neutral-900 mb-1">Sessions</h1>
        <p className="text-neutral-600">View and manage user sessions</p>
      </div>

      <DataTable
        columns={columns}
        data={sessions}
        isLoading={isLoading}
        onRowClick={(session) => console.log('Clicked session:', session.id)}
      />
    </div>
  );
}
