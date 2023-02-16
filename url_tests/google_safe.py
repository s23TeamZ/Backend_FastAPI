import requests
import json

def is_url_safe(url):
    API_KEY = "AIzaSyCKxmAa9APCEZOL_47rnD19p07uoHoM8Fg"
    API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + API_KEY

    headers = {'Content-Type': 'application/json'}
    payload = {
        "client": {
            "clientId":      "406606588071-0mtmhlj5glj3bakl7n2l787j98d804tm.apps.googleusercontent.com",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes":      ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes":    ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    #print(response.status_code)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        #print(response_json)
        if response_json.get('matches') is not None:
            return f"{url} is a malicious URL"
        else:
            return f"{url} is a safe URL"
    else:
        return f"{url} is not OK status"
