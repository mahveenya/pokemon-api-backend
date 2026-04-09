COMPOSE_FILE = docker-compose.yml

up:
	docker compose -f $(COMPOSE_FILE) up -d --build
down:
	docker compose -f $(COMPOSE_FILE) down -v
rebuild: down up