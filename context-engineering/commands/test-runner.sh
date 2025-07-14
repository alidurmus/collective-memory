#!/bin/bash

# 🧪 Context Engineering - Test Runner
# Collective Memory Test Suite

echo "🚀 Starting Collective Memory Test Suite..."

# Navigate to main app
cd ../collective-memory-app

echo "📋 Running Python Backend Tests..."
python -m pytest tests/test_basic.py -v

echo "🎭 Running Playwright UI Tests..." 
npx playwright test tests/ui/ --reporter=json > ../context-engineering/output/test-results.json

echo "🔍 Running API Endpoint Tests..."
python -m pytest tests/test_api_endpoints.py -v

echo "✅ Test Suite Complete!"
echo "📊 Results saved to output/test-results.json" 