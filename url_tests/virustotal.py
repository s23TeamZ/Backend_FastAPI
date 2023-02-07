import requests
import json

def is_malicious(url):
    api_key = "2cfa54713bf045034cec8489e5d4d1fa2a23cd0aa84d52c4fcce76e8cf507ead"
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent" : "gzip,  My Python requests library example client or username"
    }
    params = {'apikey': api_key, 'resource':url}
    response = requests.get('https://www.virustotal.com/vtapi/v2/url/report',
                            params=params, headers=headers)
    json_response = response.json()
    print(json_response)
    if json_response['positives'] > 0:
        return True
    else:
        return False
