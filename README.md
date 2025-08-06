# MCP Server with FastAPI

## Overview
This project provides a boilerplate and guidance for setting up an MCP (Model Context Protocol) server using FastAPI. It is designed to be a lightweight, local development environment that is simple to deploy and configure. The server is containerized with Docker, making it easy to manage dependencies and ensure a consistent environment across different machines/nodes. The purpose of this server is to expose a set of tools and resources to AI agents or MCP clients (such as Cursor).

## Prequisites
Before you begin, make sure you have the following software installed:
- Docker >= v28.3.x

## Setup
The project uses a Makefile to simplify common development tasks.
Note: This project uses Docker Swarm, so make sure your environment is set up to support it.

#### Initial Build
To set up the project for the first time, run the following command. This will perform all necessary one-time setup tasks, including creating the required Docker networks, building the server images and start this project.

```bash
make initial-setup
```

### Start MCP Server
To start the MCP server and its container, use this command:

```bash
make start-mcp-server
```

### Stop MCP Server
To stop the server and its containers, use this command:

```bash
make stop-mcp-server
```

### Remove Project
To fully remove this project from your local environment, run this command:

```bash
make remove-project
```

### MCP Client Configuration
The following information is for configuring a client to connect to your locally running MCP server.

#### Cursor Client
If you are using the Cursor client, you can configure it to connect to your local server by updating its settings with the following JSON snippet.

```json
  {
    "mcpServers": {
      "local-mcp": {
        "url": "http://localhost:8080/mcp/",
        "headers": {},
        "openapi": "http://localhost:8080/openapi.json"
      }
    }
  }
```

For more details on the Cursor client, refer to the [official documentation](https://docs.cursor.com/en/context/mcp).

#### Custom Agent
If you'd like to integrate this with your own Agent, you can find a helpful example in the [README.md](/examples/README.md) file. This example demonstrates how to set it up and use it as one of your tools.

When working with different large language models (LLMs), it's important to note that they may have different expectations for how to handle streaming data. Some LLMs are designed to process `text/stream` (a continuous flow of text tokens) while others might expect `text/json` (a series of JSON objects) for their streaming output. This example helps you build an agent that can handle these various requirements.

### Documentation
The FastAPI server provides self-generated, interactive documentation to help you understand and interact with the exposed tools and resources.

- Swagger: [http://localhost:8080/docs](http://localhost:8080/docs)
- Open Api: [http://localhost:8080/openapi.json](http://localhost:8080/openapi.json)

### Disclaimer

This project provides a foundational example for building and deploying a Model Context Protocol (MCP) server with FastAPI. It's intended for **local** development, serving as a **boilerplate** and **guide** to help you get started.
