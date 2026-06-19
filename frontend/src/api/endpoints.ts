export const ENDPOINTS = {
  SESSIONS: '/sessions',
  SESSION_DETAIL: (id: string) => `/sessions/${id}`,
  EVENTS: (sessionId: string) => `/sessions/${sessionId}/events`,
  HEATMAP: '/heatmap',
  ANALYTICS: '/analytics/summary',
};
