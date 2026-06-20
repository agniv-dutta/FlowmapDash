import { Card, CardContent } from '../components/Card';
import { HeatmapCanvas } from '../components/HeatmapCanvas';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { ENDPOINTS } from '../api/endpoints';

interface ClickData {
  x: number;
  y: number;
  count: number;
  timestamp: string;
}

export function Heatmap() {
  const { data, isLoading } = useQuery({
    queryKey: ['heatmap'],
    queryFn: async () => {
      const response = await apiClient.get(ENDPOINTS.HEATMAP);
      return response.data;
    },
  });

  // Mock data for development
  const mockClickData: ClickData[] = [
    { x: 100, y: 150, count: 45, timestamp: '2024-01-15T10:30:00' },
    { x: 200, y: 250, count: 78, timestamp: '2024-01-15T10:31:00' },
    { x: 300, y: 180, count: 23, timestamp: '2024-01-15T10:32:00' },
    { x: 150, y: 350, count: 56, timestamp: '2024-01-15T10:33:00' },
    { x: 400, y: 120, count: 89, timestamp: '2024-01-15T10:34:00' },
    { x: 250, y: 400, count: 34, timestamp: '2024-01-15T10:35:00' },
    { x: 500, y: 280, count: 67, timestamp: '2024-01-15T10:36:00' },
    { x: 350, y: 320, count: 12, timestamp: '2024-01-15T10:37:00' },
    { x: 450, y: 200, count: 91, timestamp: '2024-01-15T10:38:00' },
    { x: 180, y: 280, count: 45, timestamp: '2024-01-15T10:39:00' },
  ];

  const clickData = data || mockClickData;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-neutral-900 mb-1">Heatmap</h1>
        <p className="text-neutral-600">Visualize user activity patterns with interactive click analysis</p>
      </div>

      <Card>
        <CardContent>
          {isLoading ? (
            <div className="h-96 bg-neutral-50 animate-pulse rounded-lg" />
          ) : (
            <HeatmapCanvas clickData={clickData} />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
