# Implementation Plan

- [ ] 1. Fix datetime deprecation warnings
  - Replace all `datetime.utcnow()` calls with `datetime.now(datetime.timezone.utc)`
  - Update APIResponse class timestamp generation
  - Update system stats and search timing calculations
  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 2. Identify and remove duplicate api_search function
  - Locate all instances of `@app.route("/api/search")` decorators
  - Remove the duplicate/stub api_search function definition
  - Ensure only one api_search function remains
  - _Requirements: 1.1, 1.2, 2.1_

- [ ] 3. Consolidate search endpoint functionality
  - Create unified api_search function that handles both GET and POST
  - Implement proper request method detection
  - Ensure consistent parameter handling between GET query params and POST JSON body
  - _Requirements: 3.1, 3.2, 3.3_

- [ ] 4. Add helper methods for search handling
  - Create `_handle_get_search()` method for GET request processing
  - Create `_handle_post_search()` method for POST request processing  
  - Create `_perform_search()` method for common search logic
  - _Requirements: 2.2, 3.1, 3.2_

- [ ] 5. Test API server startup
  - Run the API server to verify no Flask routing conflicts
  - Test both GET and POST requests to `/api/search` endpoint
  - Verify search functionality works correctly with both methods
  - _Requirements: 1.1, 3.1, 3.2, 3.3_

- [ ] 6. Add error handling and logging
  - Add try-catch blocks around route registration
  - Implement logging for route conflicts and errors
  - Add validation for search parameters
  - _Requirements: 2.1, 2.2_