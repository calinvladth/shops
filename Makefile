docker-build:
	docker build -t upload-image . 

docker-run:
	docker run -v ${PWD}/data:/code/data  -d --name upload-container -p 8000:80 upload-image 