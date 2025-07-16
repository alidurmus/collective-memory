# Collective Memory v3.0 - Enterprise Knowledge Management System

Collective Memory is a powerful, AI-enhanced knowledge management and search system that helps you organize, index, and quickly find information across your digital workspace. **Version 3.0 Enterprise** introduces comprehensive team collaboration, user management, real-time features, and **JSON Chat System** for structured conversation management.

![Collective Memory Dashboard](docs/images/dashboard-preview.png)

## 🌟 Enterprise Features (NEW v3.0)

### 🏢 Enterprise Authentication & User Management
- **🔐 Role-Based Access Control**: 4-tier permission system (Admin, Manager, Developer, Viewer)
- **👥 User Management**: Complete user lifecycle with team assignments
- **🔒 Secure Authentication**: Session-based login with encrypted passwords
- **📊 Activity Tracking**: Comprehensive audit trails and user analytics
- **🎭 Team-Based Permissions**: Granular access control by team membership

### 👥 Team Collaboration Infrastructure
- **🏢 Multi-Team Support**: Create and manage multiple teams
- **💬 Real-time Messaging**: WebSocket-powered instant messaging
- **🏠 Collaboration Rooms**: Team-based and general chat rooms
- **📱 Responsive Team Dashboard**: Mobile-friendly team management interface
- **🔔 Live Notifications**: Real-time user join/leave notifications

### 📊 Advanced Enterprise Analytics
- **📈 Usage Metrics**: Detailed user activity and system performance
- **👤 User Analytics**: Individual and team performance insights
- **🎯 Search Analytics**: Query patterns and result effectiveness
- **⚡ Performance Monitoring**: Real-time system health metrics
- **📊 Executive Dashboard**: High-level enterprise overview

### ☁️ Cloud Synchronization Foundation
- **🌐 Multi-Provider Support**: AWS S3, Azure Blob, Google Cloud
- **🔄 Real-time Sync**: Automatic data synchronization
- **⚙️ Admin Controls**: Enable/disable sync with proper permissions
- **📊 Sync Monitoring**: Status tracking and error reporting

### 💬 JSON Chat System (NEW v3.0)
- **📁 Structured Storage**: Conversations stored in organized JSON format
- **🔍 Advanced Search**: Full-text search across all conversations
- **📤 Export Capabilities**: JSON and Markdown export with filtering
- **🔗 Cursor Integration**: Import existing Cursor chat history
- **⚙️ CLI Management**: Complete terminal-based conversation management
- **🔌 REST API**: Programmatic access with comprehensive endpoints
- **📊 Analytics**: Conversation metrics and usage statistics
- **🏷️ Tagging System**: Organize conversations with custom tags

## 🌟 Core Features (v2.1 & Earlier)

### Core Search & Indexing
- **🔍 Advanced Search Engine**: Fast full-text search with relevance scoring
- **🧠 Semantic Search**: AI-powered contextual understanding
- **📁 Auto-Discovery**: Automatic file detection and real-time indexing
- **⚡ Lightning Fast**: Sub-100ms search responses with intelligent caching
- **📊 Rich Metadata**: Comprehensive file analysis and content extraction

### Modern Web Dashboard
- **🎨 Beautiful UI**: Modern React-based interface with dark/light modes
- **📈 Analytics Dashboard**: Usage statistics and performance metrics
- **🔄 Real-time Updates**: WebSocket integration for live status updates
- **📱 Responsive Design**: Optimized for desktop, tablet, and mobile
- **⚙️ Advanced Settings**: Comprehensive system configuration

### AI-Powered Intelligence
- **🎯 Smart Relevance**: Machine learning-based result ranking
- **💡 Query Suggestions**: Intelligent search recommendations
- **🔗 Entity Recognition**: Automatic extraction of key concepts
- **📝 Content Snippets**: Contextual result previews

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/collective-memory.git
cd collective-memory
```

2. **Install dependencies**:
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies (for web dashboard)
cd frontend
npm install
```

3. **Start the system**:
```bash
# Enterprise API server (recommended for v3.0)
python api_server.py --enterprise --data-folder /path/to/your/data

# Development server
python api_server.py --debug
```

4. **Access the web dashboard**:
```bash
cd frontend
npm run dev
# Open http://localhost:3000 in your browser
```

5. **Enterprise Setup** (NEW v3.0):
```bash
# Create admin user
python -c "
from src.enterprise_features import EnterpriseManager
em = EnterpriseManager()
em.create_user('admin', 'admin@company.com', 'secure_password', 'ADMIN')
"

# Access Enterprise Login at http://localhost:3000/enterprise/login
```

6. **JSON Chat System Setup** (NEW v3.0):
```bash
# Create your first conversation
python src/chat_cli.py create "Project Planning" --project-path "/my/project"

# Search conversations
python src/chat_cli.py search "API design" --export markdown

# Import Cursor chat history
python src/chat_cli.py import-cursor --workspace-path "/cursor/workspace"
```

## 🏢 Enterprise Usage

### Team Management
1. **Admin Login**: Use enterprise login interface
2. **Create Teams**: Set up organizational teams
3. **Add Users**: Invite team members with appropriate roles
4. **Configure Permissions**: Set up role-based access control

### Real-time Collaboration
1. **Join Team Room**: Access team collaboration space
2. **Instant Messaging**: Real-time team communication
3. **Live Activity Feed**: See team member activities
4. **Shared Workspaces**: Collaborative knowledge management

### Analytics & Monitoring
1. **Enterprise Dashboard**: High-level metrics and KPIs
2. **User Activity Tracking**: Individual and team performance
3. **Search Analytics**: Query optimization insights
4. **System Health Monitoring**: Real-time performance metrics

### JSON Chat System Management
1. **Conversation Organization**: Create, tag, and organize chats
2. **Advanced Search**: Full-text search across all conversations
3. **Export & Import**: Backup and migrate conversation data
4. **API Integration**: Programmatic conversation management

## 📋 Changelog

### v3.0.0 (Current - Enterprise Release)
- ✨ **NEW**: Enterprise authentication with role-based access control
- ✨ **NEW**: Multi-user team collaboration infrastructure
- ✨ **NEW**: Real-time collaboration with WebSocket integration
- ✨ **NEW**: Advanced enterprise analytics dashboard
- ✨ **NEW**: Cloud synchronization foundation
- ✨ **NEW**: JSON Chat System for structured conversation management
- ✨ **NEW**: Modern enterprise UI components (TeamDashboard, EnterpriseAnalytics, EnterpriseLogin)
- 🔧 **IMPROVED**: Enhanced API with 25+ new enterprise endpoints
- 🔧 **IMPROVED**: WebSocket support for real-time features
- 🛡️ **SECURITY**: Enterprise-grade security and audit trails

### v2.1.0 (Previous)
- ✨ **NEW**: Modern React web dashboard
- ✨ **NEW**: Semantic search with AI-powered relevance
- ✨ **NEW**: REST API with WebSocket support
- ✨ **NEW**: Real-time indexing status and system monitoring
- ✨ **NEW**: Advanced analytics and usage statistics
- ✨ **NEW**: Export functionality for search results
- 🔧 **IMPROVED**: Enhanced query engine with ML capabilities
- 🔧 **IMPROVED**: Automatic directory management
- 🔧 **IMPROVED**: Cross-platform compatibility
- 🐛 **FIXED**: Memory optimization and performance improvements 