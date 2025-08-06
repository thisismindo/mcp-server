#!/bin/bash

echo "Starting Agent Server..."
echo "Make sure MCP server is running on http://localhost:8080"
echo ""

if curl -s http://localhost:8080/mcp/status/ > /dev/null; then
    echo "MCP server is running"
else
    echo "MCP server is not running on http://localhost:8080"
    echo "Please start the MCP server first"
    exit 1
fi

echo ""
echo "Starting agent server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
