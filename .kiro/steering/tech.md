# Technology Stack & Build System

## Backend Stack
- **Python 3.9+**: Core application language
- **Flask**: REST API server with WebSocket support via Flask-SocketIO
- **SQLite**: Database for conversation storage and indexing
- **scikit-learn**: Machine learning for search relevance
- **NLTK & sentence-transformers**: Natural language processing
- **Watchdog**: File system monitoring for real-time updates

## Frontend Stack
- **React 18**: Modern UI framework
- **Vite**: Build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **React Query**: Data fetching and caching
- **Axios**: HTTP client for API communication

## Testing & Quality
- **Playwright**: End-to-end testing for web UI
- **pytest**: Python unit and integration testing
- **ESLint**: JavaScript/React code linting
- **Black & Flake8**: Python code formatting and linting

## Development Environment
- **Docker**: Containerized development and deployment
- **Node.js/npm**: Frontend package management
- **pip**: Python package management

## Common Commands

### Backend Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start API server (development)
python api_server.py --debug

# Start API server (enterprise mode)
python api_server.py --enterprise --data-folder /path/to/data

# Run Python tests
python -m pytest tests/ -v

# Smart Context Bridge CLI
python src/context_bridge_cli.py start
python src/context_bridge_cli.py status
```

### Frontend Development
```bash
# Install frontend dependencies
cd frontend && npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run Playwright tests
npm run test
npm run test:ui
```

### Full Stack Development
```bash
# Install all dependencies
npm run install:all

# Start both API and frontend
npm run start:full

# Run all tests
npm test && cd frontend && npm test
```

## Architecture Patterns
- **Modular Design**: Separate modules for different concerns (search, indexing, chat, etc.)
- **API-First**: REST API with comprehensive endpoints
- **Real-time Updates**: WebSocket integration for live features
- **Enterprise Architecture**: Role-based access control and multi-tenancy
- **Performance Optimization**: Caching, indexing, and async processing