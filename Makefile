.PHONY: build up down restart logs ps sh clean

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

ps:
	docker compose ps

sh:
	docker compose exec api sh

clean:
	docker compose down -v
