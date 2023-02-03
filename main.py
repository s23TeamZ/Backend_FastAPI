#!/usr/bin/env python3

from fastapi import FastAPI, UploadFile, File
from shutil import copyfileobj as shutil_copyfileobj
from os.path import join as os_path_join
from os import remove as os_remove
from functions import get_file_name, qr_reader

UPLOAD_FOLDER = "upload_images"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    file_name = get_file_name(str(file.filename))
    if(file_name == ""):
        return {"Error": "Check image extention","file_name": file.filename}
    with open(os_path_join(UPLOAD_FOLDER, file_name), "wb") as buffer:
        shutil_copyfileobj(file.file, buffer)
    return {"Success": "Image uploaded successfully", "file_name": file_name}

@app.post("/qr_read/{image_name}")
async def image_qr_reader(image_name: str):
    text_found = qr_reader(os_path_join(UPLOAD_FOLDER, image_name))
    return {"Text Detected" : text_found}

@app.delete("/delete_image/{image_name}")
async def delete_image(image_name: str):
    try:
        os_remove(os_path_join(UPLOAD_FOLDER,image_name))
        return {"Success": "Image deleted from server"}
    except:
        return {"Error": "Image not found on server"}