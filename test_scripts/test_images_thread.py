import requests
from threading import Thread, Lock
import json
from os.path import join as os_path_join
from os import listdir as os_listdir
from time import time

URL = "http://127.0.0.1:5555/upload_image"
THREADS = 4
FOLDER = "test_images"

results = {}

def send_req(lock, image):
    file = {'file': open(os_path_join(FOLDER, image),'rb')}
    
    r = requests.post(URL, files=file)
    # print(r.json())

    lock.acquire()
    global results
    if(r.status_code == 200):
        results[image] = r.json()
    else:
        results[image] = f"ERROR code -> {r.status_code}"
    lock.release()

def main():
    # images = [f"qr{id}.PNG" for id in range(26,41)]
    time_start = time()

    images = os_listdir(FOLDER)

    images_slice = [images[i:i+THREADS] for i in range(0, len(images), THREADS)]

    lock = Lock()

    for i in images_slice:
        threads = []
        for j in i:
            threads.append(Thread(target=send_req, args=(lock, j,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
    global results
    print(json.dumps(results, indent=2))
    print(f"\n[+] Threads = {THREADS}\n[+] length = {len(results)} \n[+] Time = {time()-time_start}")

if __name__ == "__main__":
    main()