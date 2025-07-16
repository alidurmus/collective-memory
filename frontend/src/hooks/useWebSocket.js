import { useEffect, useRef, useState, useCallback } from 'react';
import { toast } from 'react-hot-toast';

const useWebSocket = (url = 'ws://localhost:8000/ws') => {
  const [socket, setSocket] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');
  const [lastMessage, setLastMessage] = useState(null);
  const [messageHistory, setMessageHistory] = useState([]);
  const reconnectTimeoutRef = useRef(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;
  const reconnectInterval = 3000;

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);
      
      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('Connected');
        setSocket(ws);
        reconnectAttempts.current = 0;
        
        toast.success('Real-time bağlantı kuruldu', {
          duration: 2000,
        });
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('WebSocket message received:', data);
          
          setLastMessage(data);
          setMessageHistory(prev => [...prev.slice(-49), data]); // Son 50 mesaj
          
          // Mesaj türüne göre işlem
          handleMessage(data);
        } catch (error) {
          console.error('WebSocket message parse error:', error);
        }
      };

      ws.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        setConnectionStatus('Disconnected');
        setSocket(null);
        
        // Otomatik yeniden bağlantı
        if (reconnectAttempts.current < maxReconnectAttempts) {
          reconnectAttempts.current++;
          console.log(`Reconnecting... Attempt ${reconnectAttempts.current}`);
          
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        } else {
          toast.error('Real-time bağlantı kesildi', {
            duration: 4000,
          });
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('Error');
        
        toast.error('Bağlantı hatası', {
          duration: 3000,
        });
      };

      return ws;
    } catch (error) {
      console.error('WebSocket connection error:', error);
      setConnectionStatus('Error');
      return null;
    }
  }, [url]);

  const handleMessage = useCallback((data) => {
    switch (data.type) {
      case 'search_performed':
        toast.success(`Arama tamamlandı: ${data.results_count} sonuç`, {
          duration: 3000,
        });
        break;
        
      case 'indexing_started':
        toast.loading('Dosya indeksleme başladı...', {
          id: 'indexing',
        });
        break;
        
      case 'indexing_progress':
        toast.loading(`İndeksleme: ${data.progress}% (${data.current_file})`, {
          id: 'indexing',
        });
        break;
        
      case 'indexing_completed':
        toast.success(`İndeksleme tamamlandı: ${data.processed_files} dosya`, {
          id: 'indexing',
          duration: 4000,
        });
        break;
        
      case 'system_status_change':
        if (data.status === 'error') {
          toast.error(`Sistem hatası: ${data.message}`, {
            duration: 6000,
          });
        } else if (data.status === 'warning') {
          toast.warning(`Sistem uyarısı: ${data.message}`, {
            duration: 4000,
          });
        }
        break;
        
      case 'file_change':
        toast.info(`Dosya değişikliği: ${data.filename}`, {
          duration: 2000,
        });
        break;
        
      case 'cache_cleared':
        toast.success('Önbellek temizlendi', {
          duration: 2000,
        });
        break;
        
      case 'reindex_requested':
        toast.loading('Yeniden indeksleme başlatılıyor...', {
          id: 'reindex',
        });
        break;
        
      default:
        console.log('Unknown message type:', data.type);
    }
  }, []);

  const sendMessage = useCallback((message) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message));
      return true;
    } else {
      console.error('WebSocket is not connected');
      toast.error('Bağlantı kesildi, mesaj gönderilemedi');
      return false;
    }
  }, [socket]);

  const sendSearch = useCallback((query, options = {}) => {
    return sendMessage({
      type: 'search_request',
      query,
      semantic: options.semantic || false,
      limit: options.limit || 50,
      timestamp: Date.now()
    });
  }, [sendMessage]);

  const sendHeartbeat = useCallback(() => {
    return sendMessage({
      type: 'heartbeat',
      timestamp: Date.now()
    });
  }, [sendMessage]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    
    if (socket) {
      socket.close();
    }
    
    setSocket(null);
    setConnectionStatus('Disconnected');
    reconnectAttempts.current = 0;
  }, [socket]);

  const reconnect = useCallback(() => {
    disconnect();
    setTimeout(connect, 1000);
  }, [connect, disconnect]);

  // Connection establishment
  useEffect(() => {
    connect();
    
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socket) {
        socket.close();
      }
    };
  }, [connect]);

  // Heartbeat mechanism
  useEffect(() => {
    const heartbeatInterval = setInterval(() => {
      if (connectionStatus === 'Connected') {
        sendHeartbeat();
      }
    }, 30000); // 30 saniye

    return () => clearInterval(heartbeatInterval);
  }, [connectionStatus, sendHeartbeat]);

  // Connection status monitoring
  useEffect(() => {
    const checkConnection = () => {
      if (socket) {
        switch (socket.readyState) {
          case WebSocket.CONNECTING:
            setConnectionStatus('Connecting');
            break;
          case WebSocket.OPEN:
            setConnectionStatus('Connected');
            break;
          case WebSocket.CLOSING:
            setConnectionStatus('Disconnecting');
            break;
          case WebSocket.CLOSED:
            setConnectionStatus('Disconnected');
            break;
        }
      }
    };

    const statusInterval = setInterval(checkConnection, 1000);
    return () => clearInterval(statusInterval);
  }, [socket]);

  return {
    socket,
    connectionStatus,
    lastMessage,
    messageHistory,
    sendMessage,
    sendSearch,
    sendHeartbeat,
    connect,
    disconnect,
    reconnect,
    isConnected: connectionStatus === 'Connected',
    isConnecting: connectionStatus === 'Connecting',
    isDisconnected: connectionStatus === 'Disconnected',
    hasError: connectionStatus === 'Error'
  };
};

export default useWebSocket; 