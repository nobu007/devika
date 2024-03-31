
.PHONY = setup deps compose-up compose-down compose-destroy

# to check if docker is installed on the machine 
DOCKER := $(shell command -v docker)
DOCKER_COMPOSE := $(shell command -v docker-compose)
deps:
ifndef DOCKER
	@echo "Docker is not available. Please install docker"
	@echo "try running sudo apt-get install docker"
	@exit 1
endif
ifndef DOCKER_COMPOSE
	@echo "docker-compose is not available. Please install docker-compose"
	@echo "try running sudo apt-get install docker-compose"
	@exit 1
endif

setup:
	sh +x build

compose-down: deps
	docker volume ls
	docker-compose ps
	docker images
	docker-compose down;

compose-up: deps compose-down
	docker-compose up --build

compose-destroy: deps
	docker images | grep -i devika | awk '{print $$3}' | xargs docker rmi -f
	docker volume prune

compose-up-opendevin: deps
	docker-compose -f docker-compose-opendevin.yaml up --build --remove-orphans

compose-up-opendevin-test: deps
	docker-compose -f docker-compose-opendevin.yaml up --build --remove-orphans opendevin-test

compose-up-plandex: deps
	docker-compose -f docker-compose-plandex.yaml up --build --remove-orphans

compose-up-plandex-test: deps
	docker-compose -f docker-compose-plandex.yaml up --build --remove-orphans plandex-test


compose-down-plandex: deps
	docker-compose -f docker-compose-plandex.yaml down

compose-down-opendevin: deps
	docker-compose -f docker-compose-opendevin.yaml down
