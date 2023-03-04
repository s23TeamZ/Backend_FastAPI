import requests
import json

def is_malicious(url):
    print(url)
    api_key = "80e01a0c552fb22c48e9d84bff950fffc0e7df3012a97c51d96e74057265d593"
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent" : "gzip,  My Python requests library example client or username"
    }
    params = {'apikey': api_key, 'resource':url}
    response = requests.get('https://www.virustotal.com/vtapi/v2/url/report',params=params, headers=headers)
    json_response = response.json()
    print(json_response)
    if json_response.get('positives') is not None:
        if json_response['positives'] > 3:
            print(f"{url} is a malicious URL")
            return False
        else:
            print(f"{url} is a safe URL")
            return True
    else:
         print(f"{url} is a safe URL")
         return True
   
