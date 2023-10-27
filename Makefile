REGISTRY=ghcr.io/almazkun
IMAGE_NAME=django-chat
CONTAINER_NAME=django-chat-container
VERSION=latest


lint:
	pipenv run ruff check --fix -e .
	pipenv run black .
	pipenv run djlint . --reformat

build:
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(VERSION) .

push:
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

run:
	docker run \
		-it \
		--rm \
		-d \
		-p 8000:8000 \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		$(REGISTRY)/$(IMAGE_NAME):$(VERSION)

stop:
	docker stop $(CONTAINER_NAME)

pull:
	docker pull $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

logs:
	docker logs $(CONTAINER_NAME) -f

migrate:
	docker exec $(CONTAINER_NAME) python manage.py migrate