# Agent Server

An intelligent agent server that uses a Mock-like LLM to process natural language queries and interact with an MCP (Model Context Protocol) server as tools.

## Features

- **Natural Language Processing**: Understands user queries in plain English
- **MCP Integration**: Uses MCP server as tools for user management operations
- **Async Operations**: Full async/await support for high performance
- **RESTful API**: FastAPI-based HTTP API
- **Tool Selection**: Automatically selects appropriate MCP tools based on user intent

## Supported Operations

- Check MCP server status
- List all users (with pagination)
- Create new users
- Get user by ID
- Update user email addresses
- Delete users
- Natural language query processing

## Project Structure

```
examples/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app with endpoints
│   ├── agent.py          # LLM agent logic and tool selection
│   ├── mcp_client.py     # MCP server client
│   └── openapi_parser.py # (Stub) For future dynamic tool use
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Prerequisites

- Python 3.10+
- MCP server running on `http://localhost:8080`
- pipenv (recommended) or pip

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r src/requirements.txt
   ```

2. **Start the agent server:**
   ```bash
   cd example/
   ./start.sh
   ```

3. **Verify the server is running:**
   ```bash
   curl http://localhost:8000/health
   ```

## Usage

### API Endpoints

- `GET /` - Root endpoint with usage information
- `GET /health` - Health check
- `POST /query` - Process natural language queries

### Example Queries

```bash
# Check server status
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Check server status"}'

# List all users
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "List all users"}'

# Create a new user
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Create user with username: itsmindo email: itsmindo@example.com"}'

# Get user by ID
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Get user by id: 593218b8-ea24-4401-9cf1-39579abce3cd"}'

# Update user email
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Update user id: 593218b8-ea24-4401-9cf1-39579abce3cd email: itsmindo@example.com"}'

# Delete user
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Delete user id: 593218b8-ea24-4401-9cf1-39579abce3cd"}'
```

## Architecture

### Components

1. **MockLLM**: Simulates LLM for query analysis and response generation
2. **Agent**: Orchestrates LLM and MCP tool usage
3. **MCPClient**: Async client for MCP server operations
4. **FastAPI App**: HTTP API for query processing

### Query Flow

1. User sends natural language query
2. MockLLM analyzes intent and extracts parameters
3. Agent selects appropriate MCP tool
4. MCPClient executes operation on MCP server
5. MockLLM generates natural language response
6. Response returned to user

## Configuration

- **MCP Server URL**: Configured in `app/mcp_client.py` (default: `http://localhost:8080`)
- **Agent Server Port**: Default 8000 (configurable via uvicorn)
- **LLM Integration**: Currently uses mock LLM (replace with actual LLM SDK)

### Replacing Mock LLM

Replace `MockLLM` with actual Mock SDK:

```python
# In agent.py
from mock_sdk import MockClient  # Replace with actual SDK

class GrokLLM:
    def __init__(self):
        self.client = MockClient(api_key="your-key")

    def analyze_query(self, query: str):
        # Use actual Mock API
        pass
```

## Troubleshooting

- **Connection Error**: Ensure MCP server is running on port 8080
- **Import Error**: Install all requirements with `pip install -r src/requirements.txt`
- **Port Conflict**: Change port with `uvicorn app.main:app --port 8001`
