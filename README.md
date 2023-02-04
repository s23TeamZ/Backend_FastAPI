# Backend_FastAPI


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


## TODO
### Coding
- [ ] Image scanning technique
### Docker
- [ ] Improve syntax
### README
- [ ] add/update API Methods, add output samples