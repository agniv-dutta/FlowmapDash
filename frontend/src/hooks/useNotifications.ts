import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';

export function useNotifications() {
  return useQuery({
    queryKey: ['notifications'],
    queryFn: async () => {
      try {
        const response = await apiClient.get('/v1/notifications');
        return response.data.notifications;
      } catch (error) {
        console.error('Failed to fetch notifications:', error);
        return [];
      }
    },
    staleTime: 1000 * 30,
  });
}
