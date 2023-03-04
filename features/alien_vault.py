#!/usr/bin/env python
#  This script tells if a File, IP, Domain or URL may be malicious according to the data in OTX

from OTXv2 import OTXv2
import argparse
from features import get_malicious
import hashlib


# Your API key
API_KEY = '6511109af4908aa781b8bfafd11def3cdcd8ccf22294cd4082612d6a51b4f5b5'
OTX_SERVER = 'https://otx.alienvault.com/'
otx = OTXv2(API_KEY, server=OTX_SERVER)

def check_malicious_main(params):
    param_keys = params.keys()
    if("ip" in param_keys):
        if(params['ip']):
            alerts = get_malicious.ip(otx, params['ip'])
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
                return True
            else:
                print('Unknown or not identified as malicious')
                return False
    if("host" in param_keys):
        if(params['host']):
            alerts = get_malicious.hostname(otx, params['host'])
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
                return True
            else:
                print('Unknown or not identified as malicious')
                return False
    if("url" in param_keys):
        if(params['url']):
            alerts = get_malicious.url(otx, params['url'])
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
                return True
            else:
                print('Unknown or not identified as malicious')
                return False
    if("hash" in param_keys):
        if(params['hash']):
            alerts =  get_malicious.file(otx, params['hash'])
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
                return True
            else:
                print('Unknown or not identified as malicious')
                return False
    
    if("file" in param_keys):
        if(params['file']):
            hash = hashlib.md5(open(params['file'], 'rb').read()).hexdigest()
            alerts =  get_malicious.file(otx, hash)
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
                return True
            else:
                print('Unknown or not identified as malicious')
                return False

def check_malicious(url, domain=None, ipaddr=None):
    url_c = False
    domain_c = False
    ip_c = False
    result_c = False
    try:
        result_c = check_malicious_main({'url':url})
    except:
        pass
    if(domain!=None and domain!=''):
        try:
            domain_c = check_malicious_main({'host':domain})
            result_c = result_c | domain_c
        except:
            pass
    if(ipaddr!=None and ipaddr!='' and ipaddr!=domain):    
        try:
            ip_c = check_malicious_main({'ip':ipaddr})
            result_c = result_c | ip_c
        except:
            pass
    return result_c

# if __name__ == "__main__":
#     params={'ip':'185.209.29.94'}
#     check_malicious(params)


#main()    


