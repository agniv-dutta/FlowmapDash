import { useParams } from 'react-router-dom';
import { Card, CardContent } from '../components/Card';
import { useRealtimeEvents } from '../hooks/useRealtimeEvents';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { ENDPOINTS } from '../api/endpoints';

export function SessionDetail() {
  const { sessionId } = useParams<{ sessionId: string }>();

  // Enable real-time updates for this session
  useRealtimeEvents({
    sessionId: sessionId || '',
    onNewEvent: (event) => {
      console.log('New event received:', event);
      // Could show a toast notification here
    },
  });

  const { data, isLoading } = useQuery({
    queryKey: ['session', sessionId],
    queryFn: async () => {
      const response = await apiClient.get(ENDPOINTS.SESSION_DETAIL(sessionId || ''));
      return response.data;
    },
    enabled: !!sessionId,
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 mb-1">Session Details</h1>
          <p className="text-neutral-600">Viewing session {sessionId}</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-sm text-neutral-600">Live</span>
        </div>
      </div>

      <Card>
        <CardContent>
          {isLoading ? (
            <div className="h-64 bg-neutral-50 animate-pulse rounded-lg" />
          ) : data ? (
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-neutral-900">Session Information</h3>
                <pre className="mt-2 p-4 bg-neutral-50 rounded-lg overflow-auto text-sm">
                  {JSON.stringify(data, null, 2)}
                </pre>
              </div>
            </div>
          ) : (
            <p className="text-neutral-900">Session not found</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
