SHELL := /bin/bash

.PHONY: all
all: up-local-db-bootstrap init-local-db up-local-db down-local-db apply-db-schemas initial-setup remove-project start-mcp-server stop-mcp-server

project-backend-local = demo-backend-local
project-dbname-local = demodb-local
project-dbname = demodb
project-container = demodb-node1

DB_NAME := ${project-dbname}
DB_HOST := ${project-container}
DB_PORT := 26257
DB_NAME := defaultdb
SQL_FILES := schema/internal-user.sql schema/schema.sql

set-env-vars-local:
	@echo "Setting local environment variables..." && \
	echo "DATABASE_RO_DSN=postgresql://reader_user@demodb-node1:26257/demodb?sslmode=disable" > .env && \
	echo "DATABASE_RW_DSN=postgresql://writer_user@demodb-node1:26257/demodb?sslmode=disable" >> .env && \
	echo "MCP_SERVER_HOST=http://localhost:8080" >> .env && \
	echo "Generated .env file"

up-backend-local:
	@echo Start ${project-backend-local} Service: && \
	docker stack deploy --detach=false -c docker-compose-backend.yml ${project-backend-local}
down-backend-local:
	@echo Shut down ${project-backend-local} app: && \
	docker stack rm ${project-backend-local}
build-backend-local: set-env-vars-local
	@echo Build ${project-backend-local} Service image: && \
    export DOCKER_BUILDKIT=1 && \
    set -a && source .env && set +a && docker compose -f docker-compose-backend.yml build \
        --no-cache \
        mcp-server1

start-adk-web:
	@echo Start ADK Web
	@nohup adk web &
	@echo ADK Web successfully started

stop-adk-web:
	@cho Stop ADK web
	@-pkill -f "adk web"
	@echo ADK Web successfully stopped

up-local-db-bootstrap:
	@echo "Starting demodb-node1 only..." && \
	docker stack deploy --detach=false -c docker-compose-db-bootstrap.yml ${project-dbname-local}

init-local-db:
	@echo "Initialize ${project-dbname-local} cluster..." && \
	docker exec -it $$(docker ps --filter name=demodb-node1 --format '{{.ID}}') \
		cockroach init --insecure --host=demodb-node1

up-local-db:
	@echo "Starting full ${project-dbname-local} cluster..." && \
	docker stack deploy --detach=false -c docker-compose-db-local.yml ${project-dbname-local}

apply-db-schemas:
	@echo "Checking if SQL files exist..."
	@for file in $(SQL_FILES); do \
		if [ ! -f $$file ]; then \
			echo "Error: $$file not found"; \
			exit 1; \
		fi; \
	done
	@echo "Finding CockroachDB container..."
	@DB_CONTAINER=$$(docker ps -q --filter "name=demodb-local_demodb-node1"); \
	if [ -z "$$DB_CONTAINER" ]; then \
		echo "Error: No container found for demodb-local_demodb-node1"; \
		docker ps -a --filter "name=demodb-local_demodb-node1"; \
		exit 1; \
	fi; \
	echo "Using container: $$DB_CONTAINER"; \
	echo "Waiting for CockroachDB to be ready (timeout 60s)..."; \
	timeout 60s docker exec $$DB_CONTAINER cockroach sql --insecure --host=$(DB_HOST):$(DB_PORT) --database=$(DB_NAME) --execute="SELECT 1" >/dev/null 2>&1; \
	if [ $$? -ne 0 ]; then \
		echo "Error: CockroachDB not ready after 60s. Check logs with 'docker logs $$DB_CONTAINER'"; \
		docker logs $$DB_CONTAINER; \
		exit 1; \
	fi; \
	echo "CockroachDB is ready. Applying schema files..."; \
	for file in $(SQL_FILES); do \
		echo "Applying $$file..."; \
		docker cp $$file $$DB_CONTAINER:/tmp/$$(basename $$file); \
		docker exec $$DB_CONTAINER cockroach sql --insecure --host=$(DB_HOST):$(DB_PORT) --database=$(DB_NAME) --file=/tmp/$$(basename $$file); \
		if [ $$? -ne 0 ]; then \
			echo "Error: Failed to apply $$file"; \
			docker logs $$DB_CONTAINER; \
			exit 1; \
		fi; \
		docker exec $$DB_CONTAINER rm /tmp/$$(basename $$file); \
	done; \
	echo "All schemas applied successfully."

down-local-db:
	@echo "Shut down ${project-dbname-local} app..." && \
	docker stack rm ${project-dbname-local}

create-network:
	@echo "Create database network..."
	@docker network create --driver=overlay --subnet=10.30.0.0/24 net_roachnet || { echo "Error: Failed to create database network"; exit 1; }
	@echo "Create backend network..."
	@docker network create --driver=overlay --subnet=10.31.0.0/24 net_backend || { echo "Error: Failed to create backend network"; exit 1; }

remove-network:
	@sleep 5
	@echo "Remove database network..."
	@docker network rm net_roachnet || { echo "Error: Failed to remove database network"; exit 1; }
	@echo "Remove backend network..."
	@docker network rm net_backend || { echo "Error: Failed to remove backend network"; exit 1; }

remove-backend:
	@echo "Remove MCP server..."
	@sleep 5
	@docker image rm mcp-server
	@docker volume rm demodb-local_demodb-data1
	@docker volume rm demodb-local_demodb-data2
	@docker volume rm demodb-local_demodb-data3

initial-setup:
	@echo "Initial MCP server setup..."
	@echo "Create network..."
	@make create-network
	@echo "Network created..."
	@make up-local-db-bootstrap || { echo "Error: Failed to start CockroachDB cluster"; exit 1; }
	@echo "Waiting for CockroachDB bootstrap to be ready..."
	@sleep 10
	@echo "Initialize CockroachDB cluster..."
	@make init-local-db
	@sleep 5
	@echo "Adding additional CockroachDB nodes to the cluster..."
	@make up-local-db || { echo "Error: Failed to add CockroachDB nodes"; exit 1; }
	@echo "Waiting for nodes to join cluster..."
	@sleep 10
	@echo "Applying CockroachDB schema..."
	@make apply-db-schemas || { echo "Error: Failed to apply schemas"; exit 1; }
	@echo "Waiting for schema application to complete..."
	@sleep 5
	@echo "Creating Backend image..."
	@make build-backend-local || { echo "Error: Failed to build backend image"; exit 1; }
	@echo "Waiting for backend image creation..."
	@sleep 5
	@echo "Starting MCP server..."
	@make up-backend-local || { echo "Error: Failed to start MCP server"; exit 1; }
	@echo "MCP server setup complete."

remove-project:
	@echo "Reset MCP Server project..."
	@make stop-mcp-server
	@make remove-backend
	@make remove-network
	@echo "Done..."

start-mcp-server:
	@echo "Start MCP server..."
	@make up-local-db-bootstrap
	@sleep 5
	@make build-backend-local
	@sleep 5
	@make up-local-db
	@sleep 10
	@make up-backend-local
	@echo "Done..."

stop-mcp-server:
	@echo "Stop MCP server..."
	@make down-backend-local
	@sleep 10
	@make down-local-db
	@sleep 20
	@echo "Done..."
