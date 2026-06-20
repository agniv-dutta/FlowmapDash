import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { ENDPOINTS } from '../api/endpoints';

export interface AnalyticsData {
  chartData: Array<{ day: string; events: number }>;
  totalSessions: number;
  totalEvents: number;
  avgEventsPerSession: number;
}

export function useAnalytics() {
  return useQuery({
    queryKey: ['analytics'],
    queryFn: async (): Promise<AnalyticsData> => {
      const response = await apiClient.get(ENDPOINTS.ANALYTICS);
      return response.data;
    },
  });
}
