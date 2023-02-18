#!/usr/bin/env python
#  This script tells if a File, IP, Domain or URL may be malicious according to the data in OTX

from OTXv2 import OTXv2
import argparse
import get_malicious
import hashlib


# Your API key
API_KEY = '6511109af4908aa781b8bfafd11def3cdcd8ccf22294cd4082612d6a51b4f5b5'
OTX_SERVER = 'https://otx.alienvault.com/'
otx = OTXv2(API_KEY, server=OTX_SERVER)

def check_malicious(params):
    param_keys = params.keys()
    if "ip" in param_keys:
        if params['ip']:
            alerts = get_malicious.ip(otx, params['ip'])
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
            else:
                print('Unknown or not identified as malicious')
    if "host" in param_keys:
        if params['host']:
            alerts = get_malicious.hostname(otx, params['host'])
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
            else:
                print('Unknown or not identified as malicious')
    if "url" in param_keys:
        if params['url']:
            alerts = get_malicious.url(otx, params['url'])
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
            else:
                print('Unknown or not identified as malicious')
    if "hash" in param_keys:
        if params['hash']:
            alerts =  get_malicious.file(otx, params['hash'])
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
            else:
                print('Unknown or not identified as malicious')
    
    if "file" in param_keys:
        if params['file']:
            hash = hashlib.md5(open(params['file'], 'rb').read()).hexdigest()
            alerts =  get_malicious.file(otx, hash)
            if len(alerts) > 0:
                print('Identified as potentially malicious')
                print(str(alerts))
            else:
                print('Unknown or not identified as malicious')


if __name__ == "__main__":
    params={'ip':'23.228.203.130'}
    check_malicious(params)


#main()    


