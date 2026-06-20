export const ENDPOINTS = {
  SESSIONS: '/v1/sessions',
  SESSION_DETAIL: (id: string) => `/v1/sessions/${id}`,
  EVENTS: (sessionId: string) => `/v1/sessions/${sessionId}/events`,
  HEATMAP: '/v1/heatmap',
  ANALYTICS: '/v1/analytics/summary',
};
