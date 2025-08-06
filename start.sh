#!/bin/bash

echo "Starting MCP server on port 8080..."
uvicorn src.main:app --host 0.0.0.0 --port 8080 &

wait
