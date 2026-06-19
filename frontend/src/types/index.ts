export interface Session {
  sessionId: string;
  createdAt: string;
  updatedAt: string;
  eventCount: number;
  duration: number; // in seconds
  status: 'Active' | 'Completed' | 'Idle' | 'Inactive';
  lastActivity?: string;
}

export interface Event {
  eventId: string;
  sessionId: string;
  eventType: 'page_view' | 'click' | 'custom';
  pageUrl: string;
  timestamp: string;
  coordinates?: { x: number; y: number }; // for clicks
  userAgent: string;
  targetElement?: string;
  interactionType?: string;
  device?: string;
  browser?: string;
  location?: string;
}

export interface AnalyticsSummary {
  totalSessions: number;
  totalEvents: number;
  avgEventsPerSession: number;
  topPages: Array<{ url: string; count: number }>;
  peakHours: Array<{ hour: number; count: number }>;
}

export interface ClickCoordinate {
  x: number;
  y: number;
  count: number;
}
