
import re


def test_vcard(text: str):
    if(text[0:11].upper() == "BEGIN:VCARD"):
        return True, {"Text": text}
    return False, {}

def test_mecard(text: str):
    if(text[0:7].upper() == "MECARD:"):
        return True, {"Text": text}
    return False, {}

def test_coin(text: str):
    detect = re.search(r'([a-zA-Z]+):([\w]+)(\?amount=([\d\.]+))?(&message=([\S ]+))?', text, flags=re.I|re.A)
    if(detect==None):
        return False, {}
    detect_g = detect.groups()
    return_val = {}
    return_val["Currency"] = detect_g[0]
    return_val["Coin Address"] = detect_g[1]
    if(detect_g[3]!=None):
        return_val["Amount"] = detect_g[3]
    if(detect_g[5]!=None):
        return_val["Message"] = detect_g[5]
    return True, return_val

def test_sms(text: str):
    detect = re.search(r'(SMSTO):([\d +]+):?([\S ]+)?', text, flags=re.I|re.A)
    if(detect==None):
        return False, {}
    detect_g = detect.groups()
    return_val = {}
    return_val["Phone No"] = detect_g[1]
    if(detect_g[2]!=None):
        return_val["Message"] = detect_g[2]
    return True, return_val
    

list_functions = [test_vcard, test_mecard, test_sms, test_coin,]
list_func_type = ["V-Card", "ME-Card", "SMS", "Crypto Currency",]

def categ_qr_helper(text: str):
    ret_bool = False
    ret_val = {}
    for test_func, func_name in zip(list_functions,list_func_type):
        ret_bool, ret_val = test_func(text=text)
        if(ret_bool==True):
            return [func_name, ret_val]
    
    return ["Text", {"Text":text}]

def categorize_qr(text_l):
    return_v = []
    for text_d in text_l:
        return_v.append(categ_qr_helper(text=text_d))
    return return_v
    
    
