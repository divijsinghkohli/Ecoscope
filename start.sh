#!/bin/bash

# ESG Risk Analyzer Startup Script

echo "🚀 Starting ESG Risk Analyzer..."
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

echo "✅ Docker is running"
echo "✅ Docker Compose is available"

# Create data directory if it doesn't exist
mkdir -p backend/data

echo "📦 Building and starting services..."
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "🎉 ESG Risk Analyzer is now running!"
    echo ""
    echo "📊 Frontend Dashboard: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "💡 To stop the services, run: docker-compose down"
    echo "📝 To view logs, run: docker-compose logs -f"
else
    echo "❌ Failed to start services. Check the logs with: docker-compose logs"
    exit 1
fi
