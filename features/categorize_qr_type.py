
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

def test_phone(text: str):
    if(text[0:4].lower() == "tel:"):
        return True, {"Phone_No": text[4:]}
    return False, {}
    
def test_wifi(text: str):
    if(text[0:5].upper() != "WIFI:"):
        return False, {}
    ssid_s = re.search(r'S:(.*?);(P:|H:|T:|;$)', text, flags=re.A)
    pass_s = re.search(r'P:(\S*?);(S:|H:|T:|;$)', text, flags=re.A)
    enc_s = re.search(r'T:(\w+);', text, flags=re.A)
    hidd_s = re.search(r'H:(true|false|);', text, flags=re.A)
    return_val = {"SSID":"", "Password": "", "Encryption": "", "Hidden":""}
    if(ssid_s==None):
        return False, {}
    return_val["SSID"] = ssid_s.groups()[0].replace("\\;",";").replace("\\:",":").replace("\\\\","\\")
    return_val["Password"] = pass_s.groups()[0] if(pass_s!=None) else ""
    return_val["Encryption"] = enc_s.groups()[0] if(enc_s!=None) else "nopass"
    return_val["Hidden"] = ("false" if(hidd_s.groups()[0]=='') else hidd_s.groups()[0]) if(hidd_s!=None) else "false"

    return True, return_val

def test_vevent(text: str):
    if(text[0:12].upper() == "BEGIN:VEVENT"):
        return True, {"Text": text}
    return False, {}

def test_email(text: str):
    if(text[0:6].upper() == "MATMSG"):
        return True, {"Text": text}     ## TODO extract email, subject, body of mail
    return False, {}

def test_email1(text: str):
    if(text[0:5].upper() == "mail:"):
        return True, {"Email": text[5:]}
    return False, {}

def test_url(text: str):
    web_url_raw = re.findall(r'https::\/\/|http::\/\/|www\.|([\w\d\._-]+\.[\w\d]{1,9})', text, flags=re.A)
    return_val = {"URL":"", "Domain":"", "File":{"check": False, "Name":"", "Ext":""}}
    web_url = [i for i in web_url_raw if(i!='')]
    web_url_len = len(web_url)
    if(web_url_len == 0):
        return False, {}
    
    return_val["URL"] = text
    return_val["Domain"] = web_url[0]
    if(web_url_len > 1):
        return_val["File"]["check"] = True
        return_val["File"]["Name"] = web_url[-1]
        return_val["File"]["Ext"] = web_url[-1][web_url[-1].find('.'):] # false negatives
    return True, return_val
    

list_functions = [test_vcard, test_mecard, test_vevent, test_phone, test_email1, test_email,  test_sms, test_wifi, test_coin, test_url, ]
list_func_type = ["V-Card", "ME-Card", "Event", "Phone", "E-Mail", "E-Mail", "SMS", "WIFI", "Crypto Currency", "URL", ]

def categ_qr_helper(text: str):
    ret_bool = False
    ret_val = {}
    for test_func, func_name in zip(list_functions,list_func_type):
        try:
            ret_bool, ret_val = test_func(text=text)
        except:
            continue
        if(ret_bool==True):
            return [func_name, ret_val]
    
    return ["Text", {"Text":text}]

def categorize_qr(text_l):
    return_v = []
    for text_d in text_l:
        return_v.append(categ_qr_helper(text=text_d))
    return return_v
    
    
