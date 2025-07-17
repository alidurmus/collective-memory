# Design Document

## Overview

This design addresses the Flask routing conflicts in the Collective Memory API server, specifically the duplicate `api_search` function definitions that prevent the server from starting. The solution involves consolidating duplicate endpoints, fixing datetime deprecation warnings, and ensuring clean routing architecture.

## Architecture

### Current Issues
- Duplicate `@app.route("/api/search")` decorators causing Flask AssertionError
- Multiple `api_search()` function definitions with identical names
- Deprecated `datetime.utcnow()` usage throughout the codebase
- Inconsistent endpoint naming and organization

### Proposed Solution
- Consolidate duplicate `/api/search` endpoints into a single, well-structured handler
- Replace all `datetime.utcnow()` with timezone-aware `datetime.now(datetime.timezone.utc)`
- Implement consistent endpoint naming conventions
- Add proper error handling and logging

## Components and Interfaces

### 1. Route Consolidation
```python
@self.app.route("/api/search", methods=["GET", "POST"])
def api_search():
    """Unified search endpoint handling both GET and POST requests"""
    if request.method == "GET":
        return self._handle_get_search()
    elif request.method == "POST":
        return self._handle_post_search()
```

### 2. Helper Methods
```python
def _handle_get_search(self):
    """Handle GET requests with query parameters"""
    query = request.args.get("q", "").strip()
    return self._perform_search(query)

def _handle_post_search(self):
    """Handle POST requests with JSON body"""
    data = request.get_json() or {}
    query = data.get("q", "").strip()
    return self._perform_search(query)

def _perform_search(self, query):
    """Common search logic for both GET and POST"""
    # Existing search implementation
```

### 3. DateTime Standardization
```python
# Replace all instances of:
datetime.utcnow()

# With:
datetime.now(datetime.timezone.utc)
```

## Data Models

### APIResponse Enhancement
```python
@dataclass
class APIResponse:
    success: bool
    data: Any = None
    error: Optional[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(datetime.timezone.utc).isoformat()
```

### Search Request Model
```python
@dataclass
class SearchRequest:
    query: str
    method: str  # GET or POST
    semantic: bool = False
    limit: int = 50
    offset: int = 0
```

## Error Handling

### Route Conflict Prevention
- Implement route registration validation
- Add logging for duplicate route detection
- Provide clear error messages for routing conflicts

### Graceful Degradation
```python
try:
    # Route registration
    @self.app.route("/api/search", methods=["GET", "POST"])
    def api_search():
        # Implementation
except AssertionError as e:
    logger.error(f"Route conflict detected: {e}")
    # Handle gracefully
```

## Testing Strategy

### Unit Tests
- Test consolidated search endpoint with both GET and POST methods
- Verify datetime timezone awareness
- Test error handling for malformed requests

### Integration Tests
- Test Flask application startup without routing conflicts
- Verify search functionality works correctly
- Test API response consistency

### Regression Tests
- Ensure no duplicate route definitions
- Verify all datetime operations use timezone-aware objects
- Test backward compatibility with existing API consumers