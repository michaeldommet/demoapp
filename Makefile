# Makefile for ToDo App

# Variables
APP_NAME := todo-app
DOCKER_IMAGE := $(APP_NAME):latest
ECR_REPO := <your-private-repo-url>

# Run the app locally
run:
	FLASK_ENV=development python src/app.py

# Build Docker image
build:
	docker build -t $(DOCKER_IMAGE) .

# Push Docker image to private repo
push:
	docker tag $(DOCKER_IMAGE) $(ECR_REPO)/$(DOCKER_IMAGE)
	docker push $(ECR_REPO)/$(DOCKER_IMAGE)

# Deploy to EKS
deploy:
	helm upgrade --install $(APP_NAME) ./ --values values.prod.yaml

# Start MySQL container
mysql-up:
	docker-compose up -d

# Stop MySQL container
mysql-down:
	docker-compose down

.PHONY: run build push deploy mysql-up mysql-down
