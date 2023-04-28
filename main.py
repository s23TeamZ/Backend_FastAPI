#!/usr/bin/env python3

from fastapi import FastAPI, UploadFile, File, Form
from shutil import copyfileobj as shutil_copyfileobj
from os.path import join as os_path_join
from os import remove as os_remove
from functions import get_file_name, qr_reader, url_testing_func, qr_reader1, format_return_opt
from features import categorize_qr_type
import time
import uuid
import json

UPLOAD_FOLDER = "upload_images"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    return_data = {}
    url_list = {}
    file_name = get_file_name(str(file.filename))
    if(file_name == ""):
        return {"Error": "Check image extention","file_name": file.filename}
    with open(os_path_join(UPLOAD_FOLDER, file_name), "wb") as buffer:
        shutil_copyfileobj(file.file, buffer)
    text_found_l = qr_reader(os_path_join(UPLOAD_FOLDER, file_name))
    # return_data["Text Detected"] = text_found_l
    print(f"[+] Text Detected : \n{text_found_l}")
    qr_data_ret = categorize_qr_type.categorize_qr(text_found_l)
    print(f"[+] {qr_data_ret}")
    for idx,dat in enumerate(qr_data_ret):
        idx_n = f"QR_{idx+1}"
        return_data[idx_n] = {}
        return_data[idx_n]["QR Type"] = dat[0]
        return_data[idx_n]["Data"] = dat[1]
        if(dat[0] == "URL"):
            url_list[idx_n] = dat[1]

    results_testing = url_testing_func(url_list)
    for qr_idx in results_testing:
        return_data[qr_idx]["Result_p"] = results_testing[qr_idx]['results']
        return_data[qr_idx]["Data"] = results_testing[qr_idx]['data']
        # if(results_testing[qr_idx].get('url_data', None)!=None):
        #     return_data[qr_idx]["Data_Updated"] = results_testing[qr_idx]['url_data']
        # print(results_testing[qr_idx]) #print the result of the URL tests 
    # return data 
    return_data = format_return_opt(return_data)
    print("[+] Return data :")
    print({"opt":return_data}) 
    return {"opt":return_data}



@app.post("/upload_text")
async def upload_url(text: str = Form()):
    # text = to_image_string("upload_images/0A2897B0D9.png")
    # print(f"[+] recv text : {text[:100]}")
    # print(f"[~] {time.time()}")
    # data = {"text_echo":text[:100]}
    # return_data = {"text_echo":text[:500]}
    return_data = {}
    url_list = {}
    # file_name = get_file_name(str(file.filename))
    file_name = f"{uuid.uuid4().hex[:10].upper()}.png"
    # if(file_name == ""):
    #     return {"Error": "Check image extention","file_name": file.filename}
    # with open(os_path_join(UPLOAD_FOLDER, file_name), "wb") as buffer:
    #     shutil_copyfileobj(text, buffer)
    # print(f"[+] Image Name : {file_name}")
    # text_found_l = qr_reader(os_path_join(UPLOAD_FOLDER, file_name))
    text_found_l = qr_reader1(text)
    # return_data["Text Detected"] = text_found_l
    print(f"[+] Text Detected : \n{text_found_l}")
    qr_data_ret = categorize_qr_type.categorize_qr(text_found_l)
    print(f"[+] {qr_data_ret}")
    for idx,dat in enumerate(qr_data_ret):
        idx_n = f"QR_{idx+1}"
        return_data[idx_n] = {}
        return_data[idx_n]["QR Type"] = dat[0]
        return_data[idx_n]["Data"] = dat[1]
        if(dat[0] == "URL"):
            url_list[idx_n] = dat[1]
    results_testing = url_testing_func(url_list)
    for qr_idx in results_testing:
        return_data[qr_idx]["Result_p"] = results_testing[qr_idx]['results']
        return_data[qr_idx]["Data"] = results_testing[qr_idx]['data']
        # if(results_testing[qr_idx].get('url_data', None)!=None):
        #     return_data[qr_idx]["Data_Updated"] = results_testing[qr_idx]['url_data']
        print(results_testing[qr_idx]) #print the result of the URL tests 
    # return data 
    return_data = format_return_opt(return_data)
    print("[+] Return data :")
    print({"opt":return_data})
    # time.sleep(2)
    return {"opt":return_data}
    # return json.dumps(return_data, indent=4)

  
