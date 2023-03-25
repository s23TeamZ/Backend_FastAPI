# Backend_FastAPI

####Mongo docker

- https://www.mongodb.com/languages/python
- docker run --name mongodb -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=pass mongodb/mongodb-community-server:6.0-ubi8
- mongodb://user:pass@localhost:27017/?authMechanism=DEFAULT (Connection String)
Use the network flag while running the qrcode scanner app and mongodb container.
 -  docker run --name mongodb -d --network mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=pass mongodb/mongodb-community-server:6.0-ubi8
 - docker run -it --rm --name capstone-backend-fastapi -v $PWD/upload_images:/app/upload_images:rw --network mongodb  backend-fastapi:latest
## Install Dependencies
- `pip install -r requirements.txt`
- create folders `upload_images`, `test_images`

## Running code
- create above files
- Run in production
- `uvicorn main:app --host 0.0.0.0 --port 5555 --workers 4 --log-level critical`
- Run for testing
- `uvicorn main:app --host 0.0.0.0 --port 5555 --reload`

## API Methods
- Test GET request
    - GET `http://127.0.0.1:5555/`
    - `curl --request GET 'http://127.0.0.1:5555/'`
- Upload image request
    - POST `http://127.0.0.1:5555/upload_image` with file upload
    - `curl --location --request POST 'http://127.0.0.1:5555/upload_image' --form 'file=@"test_images/qr4.PNG"'`
- QR Read request
    - POST `http://127.0.0.1:5555/qr_read/{image_name}` change `{image_name}` to string from upload request response 
    - `curl --request POST 'http://127.0.0.1:5555/qr_read/{image_name}'`
- Delete image request
    - DELETE `http://127.0.0.1:5555/delete_image/{image_name}` change `{image_name}` to string from upload request response 
    - `curl --request DELETE 'http://127.0.0.1:5555/delete_image/{image_name}'`

## Docker
- create folder `upload_images`
- Build the Docker container
- `docker build -t backend-fastapi .`
- Run the Docker container
- `docker run -it --rm --name capstone-backend-fastapi -v $PWD/upload_images:/app/upload_images:rw --network host  backend-fastapi:latest`
- access via `http://127.0.0.1:8055/`

## Testing Scripts
- Send Multi Threaded Requests with images in folder `test_images`
    - from main directory run -
    - `python3 test_scripts/test_images_thread.py`
    - edit the variables `THREADS`, `FOLDER`, `URL` if needed
    - sample output -
        ```bash
        {
            ...
            "qr46.PNG": {
                "Text Detected": [
                "BEGIN:VEVENT\nSUMMARY:test\nLOCATION:bosotn\nDTSTART:20230209T195800\nDTEND:20230303T195800\nEND:VEVENT\n"
                ]
            },
            "qr26.PNG": {
                "Text Detected": [
                "https://duckduckgo.com",
                "https://google.com"
                ]
            },
            "qr29.PNG": {
                "Text Detected": [   "bitcoin:1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX?amount=0.05&message=test msg"
                ]
            },
            ...
        }
        [+] Threads = 4
        [+] length = 21
        [+] Time = 0.7661190032958984
        ```
## TODO
### Coding
- [ ] Image scanning technique
### Docker
- [ ] Improve syntax
### README
- [ ] add/update API Methods, add output samples
