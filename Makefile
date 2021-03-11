IMAGE_NAME=bakery

default:
	pip3 install -r requirements.txt && ./entrypoint.sh

image:
	docker build . -t $(IMAGE_NAME)

container: image
	docker run -p 8000:8000 --name demo $(IMAGE_NAME)