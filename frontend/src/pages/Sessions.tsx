import { ColumnDef } from '@tanstack/react-table';
import { DataTable } from '../components/DataTable';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { ENDPOINTS } from '../api/endpoints';

interface Session {
  session_id: string;
  created_at: string;
  last_activity: string;
  event_count: number;
  metadata?: any;
}

const columns: ColumnDef<Session>[] = [
  {
    header: 'Session ID',
    accessorKey: 'session_id',
  },
  {
    header: 'Created At',
    accessorKey: 'created_at',
  },
  {
    header: 'Last Activity',
    accessorKey: 'last_activity',
  },
  {
    header: 'Events',
    accessorKey: 'event_count',
  },
  {
    header: 'Status',
    accessorKey: 'metadata.status',
  },
];

export function Sessions() {
  console.log('Sessions page rendering');
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['sessions'],
    queryFn: async () => {
      console.log('Making API request to:', ENDPOINTS.SESSIONS);
      try {
        const response = await apiClient.get(ENDPOINTS.SESSIONS);
        console.log('API response received:', response.data);
        return response.data;
      } catch (err) {
        console.error('API call failed:', err);
        throw err;
      }
    },
  });

  console.log('Sessions page state:', { data, isLoading, error });

  if (isLoading) {
    return <div className="p-8">Loading sessions...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-500">Error: {(error as Error).message}</div>;
  }

  const sessions = data?.data || [];

  if (sessions.length === 0) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold text-neutral-900 mb-1">Sessions</h1>
        <p className="text-neutral-600 mb-4">View and manage user sessions</p>
        <p className="text-gray-600 mb-4">No data found</p>
        <a href="/api-test" className="text-blue-500 underline">Test API Connection</a>
      </div>
    );
  }

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
        onRowClick={(session) => console.log('Clicked session:', session.session_id)}
      />
    </div>
  );
}
