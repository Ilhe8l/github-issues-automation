up:
	docker-compose up
stop:
	docker-compose stop	
build:
	docker-compose up --build
down:
	docker-compose down
destroy:
	docker-compose down -v
rebuild:
	docker compose down
	docker compose build
	docker compose up