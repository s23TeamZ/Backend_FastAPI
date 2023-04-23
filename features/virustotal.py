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
            return False, max(100-(json_response['positives']*25),0), f"{url} is a malicious URL, Positives={json_response['positives']}"
            
        else:
            return True, 100, f"{url} is a safe URL"
            
    else:
        return True, 100, f"{url} is a safe URL"
         

def is_malicious(url, domain=None, ipaddr=None):
    url_c = True
    domain_c = True
    ip_c = True
    result_c = True
    tot_score = 0
    tot_cnt = 0
    log_msgs = ''
    try:
        result_c, score, log_m = is_malicious_main({'url':url})
        tot_score+=score
        tot_cnt+=1
        log_msgs += f"URL : {log_m}\n" 
    except:
        pass
    if(domain!=None and domain!=''):
        try:
            domain_c, score, log_m = is_malicious_main({'host':domain})
            tot_score+=score
            tot_cnt+=1
            result_c = result_c & domain_c
            log_msgs += f"Host : {log_m}\n" 
        except:
            pass
    if(ipaddr!=None and ipaddr!='' and ipaddr!=domain):    
        try:
            ip_c, score, log_m = is_malicious_main({'ip':ipaddr})
            tot_score+=score
            tot_cnt+=1
            result_c = result_c & ip_c
            log_msgs += f"IP : {log_m}\n"
        except:
            pass
    return result_c, 0 if(tot_cnt==0) else (tot_score/tot_cnt), log_msgs
   
