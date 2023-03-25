import requests
import json

def is_malicious_main(url):
    # print(url)
    api_key = "80e01a0c552fb22c48e9d84bff950fffc0e7df3012a97c51d96e74057265d593"
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent" : "gzip,  My Python requests library example client or username"
    }
    params = {'apikey': api_key, 'resource':url}
    response = requests.get('https://www.virustotal.com/vtapi/v2/url/report',params=params, headers=headers)
    json_response = response.json()
    # print(json_response)
    if json_response.get('positives') is not None:
        if json_response['positives'] > 3:
            return False, f"{url} is a malicious URL, Positives={json_response['positives']}"
            
        else:
            return True, f"{url} is a safe URL"
            
    else:
        return True, f"{url} is a safe URL"
         

def is_malicious(url, domain=None, ipaddr=None):
    url_c = False
    domain_c = False
    ip_c = False
    result_c = False
    log_msgs = ''
    try:
        result_c, log_m = is_malicious_main({'url':url})
        log_msgs += f"URL : {log_m}\n" 
    except:
        pass
    if(domain!=None and domain!=''):
        try:
            domain_c, log_m = is_malicious_main({'host':domain})
            result_c = result_c & domain_c
            log_msgs += f"Host : {log_m}\n" 
        except:
            pass
    if(ipaddr!=None and ipaddr!='' and ipaddr!=domain):    
        try:
            ip_c, log_m = is_malicious_main({'ip':ipaddr})
            result_c = result_c & ip_c
            log_msgs += f"IP : {log_m}\n"
        except:
            pass
    return result_c, log_msgs
   
