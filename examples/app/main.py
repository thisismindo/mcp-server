from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import agent

app = FastAPI(title="Agent Server", description="Agent server using LLM and MCP tools")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    success: bool

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Process user query using agent with LLM and MCP tools
    """
    try:
        result = await agent.process_query(request.query)
        return QueryResponse(response=result, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "message": "Agent server is running"}

@app.get("/")
async def root():
    """
    Root endpoint with usage information
    """
    return {
        "message": "Agent Server",
        "description": "Send POST requests to /query with JSON body: {\"query\": \"your question here\"}",
        "examples": [
            "Check server status",
            "List all users",
            "Create user with username: john email: john@example.com",
            "Get user by id: 123e4567-e89b-12d3-a456-658964313152",
            "Update user id: 123e4567-e89b-12d3-a456-789798653135 email: newemail@example.com",
            "Delete user id: 123e4567-e89b-12d3-a456-855649879879"
        ]
    }
