# Collective Memory v3.0 Enterprise - API Reference

**Version:** v3.0 Enterprise  
**Last Updated:** January 15, 2025  
**Base URL:** `http://localhost:8000/api/`  

---

## 🆕 **v3.0 Enterprise API Yenilikleri**

- **🔐 Enterprise Authentication API** - User management, role-based access control
- **👥 Team Collaboration API** - Team management, member operations
- **📊 Enterprise Analytics API** - Advanced metrics, user activity tracking
- **🔄 Real-time WebSocket API** - Live collaboration, messaging
- **☁️ Cloud Sync API** - Data synchronization endpoints

---

## 🔐 **Authentication & Authorization**

### **POST** `/auth/login`
**Description:** Enterprise user login  
**Body:**
```json
{
  "username": "admin",
  "password": "secure_password"
}
```
**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "role": "ADMIN",
      "team_id": 1
    },
    "token": "session_token_here"
  }
}
```

### **POST** `/auth/logout`
**Description:** User logout and session cleanup

### **GET** `/auth/verify`
**Description:** Verify current session
**Headers:** `Authorization: Bearer <token>`

---

## 👥 **Team Management API** ⭐ YENİ

### **GET** `/teams/`
**Description:** List all teams (Admin only)

### **POST** `/teams/`
**Description:** Create new team
**Body:**
```json
{
  "name": "Development Team",
  "description": "Core development team"
}
```

### **GET** `/teams/{team_id}/members`
**Description:** Get team members

### **POST** `/teams/{team_id}/members`
**Description:** Add user to team
**Body:**
```json
{
  "user_id": 5,
  "role": "DEVELOPER"
}
```

### **DELETE** `/teams/{team_id}/members/{user_id}`
**Description:** Remove user from team

---

## 👤 **User Management API** ⭐ YENİ

### **GET** `/users/`
**Description:** List all users (Admin/Manager only)

### **POST** `/users/`
**Description:** Create new user
**Body:**
```json
{
  "username": "new_user",
  "email": "user@company.com",
  "role": "DEVELOPER",
  "team_id": 1
}
```

### **PUT** `/users/{user_id}`
**Description:** Update user information

### **DELETE** `/users/{user_id}`
**Description:** Delete user (Admin only)

### **GET** `/users/{user_id}/activity`
**Description:** Get user activity history

---

## 📊 **Enterprise Analytics API** ⭐ YENİ

### **GET** `/analytics/overview`
**Description:** Get enterprise overview metrics
**Response:**
```json
{
  "success": true,
  "data": {
    "total_users": 25,
    "active_teams": 5,
    "total_searches": 1543,
    "system_health": "healthy",
    "performance_score": 9.2
  }
}
```

### **GET** `/analytics/users`
**Description:** User activity analytics

### **GET** `/analytics/teams`
**Description:** Team performance metrics

### **GET** `/analytics/search`
**Description:** Search analytics and patterns

### **GET** `/analytics/performance`
**Description:** System performance metrics

---

## 🔄 **Real-time Collaboration** ⭐ YENİ

### **WebSocket Connection**
**URL:** `ws://localhost:8000/ws/collaboration`
**Authentication:** Session token required

### **WebSocket Events**

#### **Client → Server**

**join_room:**
```json
{
  "event": "join_room",
  "data": {
    "room_id": "team_1_general",
    "user_id": 1
  }
}
```

**send_message:**
```json
{
  "event": "send_message",
  "data": {
    "room_id": "team_1_general",
    "message": "Hello team!",
    "message_type": "text"
  }
}
```

**leave_room:**
```json
{
  "event": "leave_room",
  "data": {
    "room_id": "team_1_general"
  }
}
```

#### **Server → Client**

**user_joined:**
```json
{
  "event": "user_joined",
  "data": {
    "user": {
      "id": 2,
      "username": "john_doe"
    },
    "room_id": "team_1_general",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

**new_message:**
```json
{
  "event": "new_message",
  "data": {
    "message_id": "msg_123",
    "user": {
      "id": 1,
      "username": "admin"
    },
    "message": "Hello team!",
    "room_id": "team_1_general",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

**user_left:**
```json
{
  "event": "user_left",
  "data": {
    "user_id": 2,
    "room_id": "team_1_general",
    "timestamp": "2025-01-15T10:35:00Z"
  }
}
```

---

## ☁️ **Cloud Synchronization API** ⭐ YENİ

### **GET** `/sync/status`
**Description:** Get cloud sync status

### **POST** `/sync/enable`
**Description:** Enable cloud synchronization (Admin only)
**Body:**
```json
{
  "provider": "aws_s3",
  "config": {
    "bucket": "collective-memory-backup",
    "region": "us-east-1"
  }
}
```

### **POST** `/sync/disable`
**Description:** Disable cloud synchronization

### **POST** `/sync/manual`
**Description:** Trigger manual sync

---

## 🔍 **Enhanced Search API** (Updated for v3.0)

### **GET** `/search`
**Description:** Advanced search with enterprise features
**Parameters:**
- `q` (string): Search query
- `team_id` (int): Filter by team (optional)
- `user_id` (int): Filter by user (optional)
- `semantic` (boolean): Enable semantic search
- `date_from` (string): Start date filter
- `date_to` (string): End date filter

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [...],
    "total": 150,
    "query_info": {
      "original_query": "Django models",
      "expanded_query": "Django models database ORM",
      "search_type": "hybrid",
      "team_scope": "team_1"
    }
  }
}
```

---

## 📊 **System Monitoring** (Enhanced for Enterprise)

### **GET** `/system/status`
**Description:** Enhanced system status with enterprise metrics

### **GET** `/system/health/enterprise`
**Description:** Enterprise health check
**Response:**
```json
{
  "success": true,
  "data": {
    "overall_health": "healthy",
    "components": {
      "database": "healthy",
      "authentication": "healthy",
      "websocket": "healthy",
      "cloud_sync": "healthy"
    },
    "metrics": {
      "active_users": 15,
      "active_sessions": 23,
      "message_queue_size": 0,
      "sync_status": "up_to_date"
    }
  }
}
```

---

## 🔒 **Security Features**

### **Role-Based Access Control**
- **ADMIN**: Full system access, user management
- **MANAGER**: Team management, analytics access
- **DEVELOPER**: Team collaboration, search access
- **VIEWER**: Read-only access to team resources

### **Session Management**
- Secure session tokens
- Automatic session timeout (8 hours)
- Session tracking and monitoring

### **Data Privacy**
- Team-scoped data access
- Audit logging for all actions
- Encrypted sensitive data

---

## 🧪 **Testing the Enterprise API**

### **Authentication Test**
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use session token for subsequent requests
curl -X GET http://localhost:8000/api/teams/ \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN"
```

### **WebSocket Test (JavaScript)**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/collaboration');

ws.onopen = () => {
  // Join team room
  ws.send(JSON.stringify({
    event: 'join_room',
    data: {
      room_id: 'team_1_general',
      user_id: 1
    }
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

---

## 📈 **Enterprise API Metrics**

- **Total Endpoints**: 45+ (25 new in v3.0)
- **Authentication Methods**: Session-based + Role-based
- **Real-time Features**: WebSocket support
- **Response Time**: <200ms average
- **Uptime Target**: 99.9%
- **Rate Limiting**: 1000 requests/hour per user

---

*API Documentation generated for Collective Memory v3.0 Enterprise* 