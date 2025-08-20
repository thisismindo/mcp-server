# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [Unreleased]

### ToDo

### Work In Progress

### Bugs/Hotfix

### Updated
08/20/2025
- update `adk-agent` README.md

08/19/2025
- bump cockroachdb to `v25.3.0`.

08/12/2025
- validate input using pydantic and update data type.
- rebuild image when starting the mcp server.
- reorganize the routes into new groups.

### Added
08/19/2025
- implement agent using Google Agent Development Kit (ADK).

08/06/2025
- initial implementation of MCP server using FastAPI.
- implement a sample agent that uses a mock LLM and an MCP server as its tools.
