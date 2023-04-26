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

## Mongo docker

- https://www.mongodb.com/languages/python
- docker run --name mongodb -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=pass mongodb/mongodb-community-server:6.0-ubi8
- mongodb://user:pass@localhost:27017/?authMechanism=DEFAULT (Connection String)
#### Use the network flag while running the qrcode scanner app and mongodb container.
-  docker run --name mongodb -d --network mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=pass mongodb/mongodb-community-server:6.0-ubi8
- docker run -it --rm --name capstone-backend-fastapi -v $PWD/upload_images:/app/upload_images:rw --network mongodb  backend-fastapi:latest

#### Run command MongoDB
- `docker run --name mongodb -d --network host -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=pass mongodb/mongodb-community-server:6.0-ubi8`
- start container again - 
    - `docker start -a -i <Container ID>` --> -a attach, -i interactive

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
- create folder `upload_images` - not required
- Build the Docker container
- `docker build -t backend-fastapi .`
- Run the Docker container
- `docker run -it --rm --name capstone-backend-fastapi --network host backend-fastapi:latest`
- access via `http://127.0.0.1:8055/`

## Scoring
```
Passive Tests - 40% 
if (URL Redirection == true or Database Check == True):
    URL redirection - 10%
        {1:100, 2:90, 3:70, 4:50, 5:20}
    DNS Check - 25% 
    External APIs - 65%
        Virus Total - 50% 
            Start score: 100; -25 for each negative;
        Alien Vault - 50%
            Start score: 100; -50 for each negative;
else 0

 

Active Tests - 60%
    TLS Certificates - 40%
        Certificate Expired - 0
        else SSL Version TLSv1.2, v1.3 - 100, TLSv1.1 - 70, TLSv1.0 - 35, SSLv* - 10
    Any Downloads - 25%
    CSP Headers - 15%
    AdBlocker comparison - 10%
    Phishing Detector - 10%
```
```
DNS - 8.574 (10)	0.25*0.4
VT - 13			0.5*0.65*0.4
AV - 9.75 (13)		0.5*0.65*0.4
URL r - 3.6 (4)		0.1*0.4
CSP - 0 (9)		0.15*0.6
SSL - 24		0.4*0.6
DYN - 27		(0.3+0.15)*0.6
```


## TODO
### Coding
- [x] Image scanning technique
### Docker
- [x] Improve syntax
- [ ] Automate MongoDB entries when container started
- [ ] Write Docker compose
### README
- [x] add/update API Methods, add output samples
