import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { useQueryClient } from '@tanstack/react-query';

interface UseRealtimeEventsOptions {
  sessionId: string;
  onNewEvent?: (event: any) => void;
  onSessionUpdate?: (session: any) => void;
  onAnalyticsUpdate?: (analytics: any) => void;
}

export function useRealtimeEvents({
  sessionId,
  onNewEvent,
  onSessionUpdate,
  onAnalyticsUpdate,
}: UseRealtimeEventsOptions) {
  const [isConnected, setIsConnected] = useState(false);
  const [socket, setSocket] = useState<Socket | null>(null);
  const queryClient = useQueryClient();

  useEffect(() => {
    const socketUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
    const newSocket = io(socketUrl, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Connected to WebSocket server');
      setIsConnected(true);
      
      // Subscribe to session updates
      newSocket.emit('subscribe_session', { sessionId });
    });

    newSocket.on('connection_response', (data) => {
      console.log('Connection response:', data);
    });

    newSocket.on('subscribed', (data) => {
      console.log('Subscribed to session:', data.sessionId);
    });

    newSocket.on('new_event', (event) => {
      console.log('New event received:', event);
      
      // Invalidate relevant queries
      queryClient.invalidateQueries({ queryKey: ['session', sessionId] });
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      
      // Call custom callback if provided
      if (onNewEvent) {
        onNewEvent(event);
      }
    });

    newSocket.on('session_update', (session) => {
      console.log('Session update received:', session);
      
      // Invalidate session query
      queryClient.invalidateQueries({ queryKey: ['session', sessionId] });
      
      // Call custom callback if provided
      if (onSessionUpdate) {
        onSessionUpdate(session);
      }
    });

    newSocket.on('analytics_update', (analytics) => {
      console.log('Analytics update received:', analytics);
      
      // Invalidate analytics query
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      
      // Call custom callback if provided
      if (onAnalyticsUpdate) {
        onAnalyticsUpdate(analytics);
      }
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
      setIsConnected(false);
    });

    newSocket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    return () => {
      // Unsubscribe from session before disconnecting
      newSocket.emit('unsubscribe_session', { sessionId });
      newSocket.disconnect();
    };
  }, [sessionId, queryClient, onNewEvent, onSessionUpdate, onAnalyticsUpdate]);

  return { isConnected, socket };
}

// Hook for global analytics updates
export function useAnalyticsUpdates(onUpdate?: (analytics: any) => void) {
  const [isConnected, setIsConnected] = useState(false);
  const queryClient = useQueryClient();

  useEffect(() => {
    const socketUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
    const newSocket = io(socketUrl, {
      transports: ['websocket', 'polling'],
      reconnection: true,
    });

    newSocket.on('connect', () => {
      console.log('Connected to WebSocket for analytics');
      setIsConnected(true);
    });

    newSocket.on('analytics_update', (analytics) => {
      console.log('Analytics update received:', analytics);
      
      // Invalidate analytics query
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      
      // Call custom callback if provided
      if (onUpdate) {
        onUpdate(analytics);
      }
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from WebSocket');
      setIsConnected(false);
    });

    return () => {
      newSocket.disconnect();
    };
  }, [queryClient, onUpdate]);

  return { isConnected };
}
