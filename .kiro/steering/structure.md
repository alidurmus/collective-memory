# Project Structure & Organization

## Root Directory Layout
```
collective-memory/
├── .kiro/                      # Kiro IDE configuration and steering
├── collective-memory-app/      # Main application directory
├── docs/                       # Centralized documentation hub
├── context-engineering/        # Context Engineering Template implementation
├── frontend/                   # Standalone frontend (legacy)
└── tests/                      # Root-level tests
```

## Main Application Structure (`collective-memory-app/`)
```
collective-memory-app/
├── src/                        # Core source code
│   ├── cursor/                 # Cursor integration modules
│   ├── database/               # Database management
│   ├── integrations/           # External service integrations
│   ├── memory/                 # Memory management components
│   ├── chat_api.py             # Chat system API
│   ├── smart_context_bridge.py # Smart Context Bridge core
│   ├── context_bridge_cli.py   # CLI interface
│   ├── api_server.py           # Main Flask API server
│   └── main.py                 # Application entry point
├── frontend/                   # React web dashboard
│   ├── src/                    # React components and logic
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js          # Build configuration
├── tests/                      # Application tests
├── .collective-memory/         # JSON Chat System storage
├── .cursor/                    # Cursor integration files
│   └── rules/                  # Auto-generated context rules
├── config/                     # Configuration files
├── requirements.txt            # Python dependencies
├── package.json                # Node.js scripts and dependencies
└── docker-compose.yml          # Container orchestration
```

## Documentation Organization (`docs/`)
```
docs/
├── INDEX.md                    # Central documentation navigation
├── user-guides/                # End-user documentation
├── technical/                  # Technical documentation
│   ├── api/                    # API reference
│   └── architecture/           # System architecture
├── reports/                    # Status and analysis reports
│   ├── completion/             # Feature completion reports
│   ├── system-health/          # System monitoring
│   └── error-reports/          # Error tracking
├── testing/                    # Test documentation
├── deployment/                 # Deployment guides
└── project-management/         # Project planning and management
```

## Key Conventions

### File Naming
- **Python modules**: `snake_case.py`
- **React components**: `PascalCase.jsx`
- **Documentation**: `UPPERCASE_WITH_UNDERSCORES.md`
- **Configuration**: `lowercase.json`, `lowercase.yml`
- **CLI scripts**: `snake_case_cli.py`

### Directory Patterns
- **Source code**: Organized by functional domain (chat, search, enterprise, etc.)
- **Tests**: Mirror source structure with `test_` prefix
- **Documentation**: Categorized by audience and purpose
- **Configuration**: Centralized in `config/` or root-level files

### Import Conventions
- **Relative imports**: Used within the same module/package
- **Absolute imports**: Used for cross-module dependencies
- **Path management**: `sys.path.append()` for local imports in scripts

### Data Storage
- **SQLite databases**: `.db` files in app root
- **JSON storage**: `.collective-memory/` directory
- **Logs**: Application-specific log files
- **Cache**: `.mypy_cache/`, `.pytest_cache/` for tooling

### Enterprise Features
- **Multi-tenancy**: User and team-based data separation
- **Role-based access**: Admin, Manager, Developer, Viewer roles
- **API versioning**: Structured endpoint organization
- **WebSocket rooms**: Team-based real-time communication