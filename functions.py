
import uuid
import cv2
from features import check_redirection, dnscheck1, virustotal, alien_vault, csp, ssl, dbcheck
from features import categorize_qr_type
import time
from threading import Thread
from multiprocessing.pool import ThreadPool
import requests
import base64
import numpy as np

DYN_TEST_URL = "http://127.0.0.1:7077/upload_url"

def get_file_name(file_name: str) -> str:
    if(file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi'))):
        return f"{uuid.uuid4().hex[:10].upper()}{file_name[file_name.rfind('.'):]}"
    return ""

def format_return_opt(rtd):
    final_d = []
    def ext_url_data(qq):
        fin_s = f"URL : {qq['Data']['URL']}\n\n"
        if(qq['Data'].get('Redirect URL',None)!=None):
            fin_s+=f"Redirect URL :\n {qq['Data']['Redirect URL']}\n\n"
        if(qq['Data']['log']!=''):
            fin_s+=f"Msg :\n {qq['Data']['log']}\n\n"
        qq_r = qq['Result_p']
        if(qq_r.get('DB',False)==True):
            fin_s+=f"Database :\n URL found in malicious list DB\n\n"
        else:
            if(qq_r.get('dwn_test',[False])[0] == False):
                fin_s+=f"Downloads :\n URL does not download anything\n\n"
            else:
                fin_s+=f"Downloads :\n URL downloads filetype - {qq_r['dwn_test'][1]} ; size - {qq_r['dwn_test'][2]}"
                fin_s+= "\n\n" if(qq_r['dwn_test'][3]=='') else f" ; filename - {qq_r['dwn_test'][3]}\n\n"
            if(qq_r.get('phishing_data',[False])[0] == False):
                fin_s+=f"Phishing :\n URL is not likely Phishing site\n\n"
            else:
                fin_s+=f"Phishing :\n URL is likely Phishing site matches {qq_r['phishing_data'][1]}% of {qq_r['phishing_data'][2][:-5]}\n\n"
        return fin_s, qq['Data']['URL']
    for qr in rtd:
        qr_d = {}
        if(rtd[qr]['QR Type']=="URL"):
            qr_d['QR Type'] = "URL"
            qr_d['data'], url_ext = ext_url_data(rtd[qr])
            qr_d['score'] = rtd[qr]['Result_p']['TOTAL_SCORE']
            qr_d['URL'] = url_ext
        else:
            qr_d['QR Type'] = rtd[qr]['QR Type']
            qr_d['data'] = rtd[qr]['Data']
            qr_d['score'] = 100
            qr_d['URL'] = ''
        final_d.append(qr_d)
    return final_d


def qr_cv_detect(img) -> str:
    detector = cv2.QRCodeDetector()
    retrivel, decoded_info, points,st_qrcode = detector.detectAndDecodeMulti(img)
    if(len(decoded_info)>0):
        return decoded_info
    else:
        return ""

def qr_reader(image_name: str) -> str:
    img = cv2.imread(image_name)
    text = qr_cv_detect(img)
    if(text==""):
        org_image_read = cv2.imread(image_name)
        grayImage = cv2.cvtColor(org_image_read, cv2.COLOR_BGR2GRAY)
        (thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        text = qr_cv_detect(img)
    text_l = [i for i in text]
    # text_l = [i for i in text]
    return text_l

def qr_cv_detect1(img) -> str:
    detector = cv2.QRCodeDetector()
    retrivel, decoded_info, points,st_qrcode = detector.detectAndDecodeMulti(img)
    if(len(decoded_info)>0):
        return decoded_info
    else:
        return ""

def qr_reader1(img_txt: str) -> str:
    # img = cv2.imread(image_name)
    img = from_base64(img_txt)
    text = qr_cv_detect1(img)
    if(text==""):
        # org_image_read = cv2.imread(image_name)
        org_image_read = img
        grayImage = cv2.cvtColor(org_image_read, cv2.COLOR_BGR2GRAY)
        (thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        text = qr_cv_detect1(img)
    text_l = [i for i in text]
    # text_l = [i for i in text]
    return text_l

def to_image_string(image_filepath):
    return base64.b64encode(open(image_filepath, 'rb').read())

def from_base64(base64_data):
    nparr = np.fromstring(base64.b64decode(base64_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

def url_testing_func(url_list: dict):
    
    #####
    #   URL Testing
    #   - check redirect initially, get the final URL or max redirect limit reached
    #   - DNS test, url_tests/dnscheck.py
    #       - percentage % trust worthiness
    #   - virustotal check
    #        - based on positives and total scan calculate %
    #   - Alien Vault
    #       - based on the input, cvalculate the maliciousness
    #   - calculate a total passive scan - % of trust worthiness
    #####
    results = {}
    for qr_idx in url_list:
        url1 = url_list[qr_idx]["URL"]
        url_access_flag = False
        results[qr_idx] = {}
        results[qr_idx]['data'] = {'URL':url1, 'log':''}
        results[qr_idx]['results'] = {"TOTAL_SCORE":0}
        r_url, r_score =check_redirection.check_redirect(url1)
        if(r_url==False):
            url_access_flag = True
            results[qr_idx]['data']['log'] = "Cannot Access the URL"
            
        elif(r_url!=url1):
            __1, url_data = categorize_qr_type.test_url(r_url)
            url_list[qr_idx] = url_data
            results[qr_idx]['data']['Redirect URL'] = url_list[qr_idx]["URL"]
        print(f"\n\n[+] Checks for - {url_list[qr_idx]['URL']}\n")
        db_ck, db_log = dbcheck.db_check(url=url_list[qr_idx]["URL"], 
                                        domain=url_list[qr_idx]["Domain"])
        print(f"[~] DB check : [{db_ck}] :")
        print(db_log)
        total_score_tests = 0
        if(db_ck == False):
            # results[qr_idx]['results'].update
            results_tests = url_testing_core_func(url_list[qr_idx],
                        url_access_flag,
                        dyn_test = True)
            if((results_tests["VirusTotal"]<50 or results_tests["AlienVault"]<75) and url_list[qr_idx]["Domain"] not in ['google.com']):
                dbcheck.add_to_db(url=url_list[qr_idx]["URL"], domain=url_list[qr_idx]["Domain"])
                print("[~] Added to Malicious Database")
            if(results_tests["Dynamic_tests"]['score']!=0):
                dwn_test_file = url_list[qr_idx]["File"]["Name"] if(results_tests["Dynamic_tests"]['dwn_data'][0] and url_list[qr_idx]["File"]["check"]) else ''
                results[qr_idx]['results']['dwn_test'] = results_tests["Dynamic_tests"]['dwn_data'][:-1] + [dwn_test_file]
                results[qr_idx]['results']['phishing_data'] = results_tests["Dynamic_tests"]['phishing_data'][:-1]
            total_score_tests = results_tests['TOTAL_SCORE']
        else:
            results[qr_idx]['results'].update({'DB':True})
            r_score = 0
        results[qr_idx]['results']["TOTAL_SCORE"] = total_score_tests + r_score*0.1*0.4
        
        # results[qr_idx]['results']["URL Redirect"] = r_score
        print(f"[=] Results : {results[qr_idx]}\n\n")
    return results

def url_testing_core_func(url_d, flag=False, dyn_test=False):
    results = {"DNS":0, "VirusTotal":0, "AlienVault":0,"csp":0, "ssl":0,"Dynamic_tests":{'score':0}}
    threads = []
    log_msgs = {}
    dyn_oth_log = {}
    def check_dns():
        init_time = time.time()
        try:
            dns_score,log_m = dnscheck1.dns_init_check(url_d["Domain"])
            results["DNS"] = dns_score
            log_msgs["DNS"] = log_m
        except Exception as e:
            results["DNS"] = 0
            log_msgs["DNS"] = f"\n[x] Error : {e}"
        print(f"[+] Time - DNS : {time.time() - init_time}")
    
    def check_virustotal():
        init_time = time.time()
        try: 
            virus_status,vt_score,log_m = virustotal.is_malicious(url=url_d["URL"],
                                domain=url_d["Domain"],
                                ipaddr=url_d["IP"] if(url_d["IP"]!='') else None)
            results["VirusTotal"] = vt_score
            log_msgs["VirusTotal"] = log_m
        except:
            results["VirusTotal"] = 0
        print(f"[+] Time - Virus Total : {time.time() - init_time}")
    
    def check_alien_vault():
        init_time = time.time()
        try:
            alien_vault_status, av_score, log_m = alien_vault.check_malicious(url=url_d["URL"],
                                domain=url_d["Domain"],
                                ipaddr=url_d["IP"] if(url_d["IP"]!='') else None)
                                            
            results["AlienVault"] = av_score
            log_msgs["AlienVault"] = log_m
        except:
            results["AlienVault"] = 0
        print(f"[+] Time - Alien Vault : {time.time() - init_time}")
    
    def check_csp():
        init_time = time.time()
        try:
            csp_status, csp_score, log_m = csp.check_csp_headers(url_d["URL"])
            results["csp"] = csp_score
            dyn_oth_log["csp"] = log_m
        except:
            results["csp"] = 0
        print(f"[+] Time - CSP : {time.time() - init_time}")
    
    def check_ssl():
        init_time = time.time()
        try:
            ssl_status, ssl_score, log_m = ssl.check_website(url_d["URL"], url_d["Domain"])
            results["ssl"] = ssl_score
            dyn_oth_log["ssl"] = log_m
        except:
            results["ssl"] = 0
        print(f"[+] Time - SSL : {time.time() - init_time}")
    
    def dynamic_testing():
        init_time = time.time()
        try:
            dyn_test_status = requests.post(url=DYN_TEST_URL, data={'url':url_d["URL"]})
            # dyn_test_status, log_m = alien_vault.check_malicious(url=url_d["URL"],)
                                # domain=url_d["Domain"],
                                # ipaddr=url_d["IP"] if(url_d["IP"]!='') else None)
            if(dyn_test_status.status_code <200 and dyn_test_status.status_code >299):
                raise Exception(f"Status code : {dyn_test_status.status_code()}")
            try:
                res_json = dyn_test_status.json()   # add final score in json
            except:
                raise Exception("Data recieved is not JSON")                          
            results["Dynamic_tests"] = res_json
            # log_msgs["Dynamic_tests"] = ''
        except Exception as e:
            results["Dynamic_tests"] = {'score':0}
            # log_msgs["Dynamic_tests"] = f"ERROR : {e}"
        print(f"[+] Time - Dynamic Testing : {time.time() - init_time}")

    def display_dynamic_test():
        if(results["Dynamic_tests"].get('score',0)==0):
            return
        dtr = results["Dynamic_tests"]
        print(f"[~] Dynamic Test check : ")
        for log in dyn_oth_log:
            print(f"[~] {log} Check : [{results[log]}] :")
            print("\t",end='')
            print(dyn_oth_log[log])
        print(f" Aggregate Score for below : [{dtr['score']}]")
        print(f"[~] Download Check : ")
        if(len(dtr['dwn_data'])==0):
            pass
        elif(len(dtr['dwn_data'])!=0 and dtr['dwn_data'][0]):
            print(f"\tURL Downloads Files, Type: {dtr['dwn_data'][1]}, Size: {dtr['dwn_data'][2]}, log: {dtr['dwn_data'][3]}")
        else:
            print("\nURL Does not Downlaod Files")
        print("[~] Ads/Tracker Check : ")
        if(len(dtr['chrome_data'])==0):
            pass
        elif(dtr['chrome_data'][0]):
            print(f"\tPercentage of Ads/Trackers : {dtr['chrome_data'][1]}")
        else:
            print(f"\tError: log : {dtr['chrome_data'][0]}")
        print("[~] Phishing Check : ")
        if(len(dtr['phishing_data'])==0):
            pass
        elif(len(dtr['phishing_data'])!=0 and dtr['phishing_data'][0]):
            print(f"\tPercentage of likely Phishing : {dtr['phishing_data'][1]} , Website: {dtr['phishing_data'][2][:-5]}")
        else:
            print(f"\nNot Likely Phishing Website")
    check_list = [check_virustotal, check_alien_vault, check_dns]
    if(not flag):
        check_list =  check_list + [check_csp, check_ssl]
        if(dyn_test):
            check_list = [dynamic_testing] + check_list

    tot_time_init = time.time()
    thread_pool = ThreadPool(processes=len(check_list))
    async_result = []
    for func_ in check_list:
        async_result.append(thread_pool.apply_async(func_, ()))
    for func_ in async_result:
        func_.get()

    # if(flag):
    #     for i in [check_virustotal, check_alien_vault]:
    #         threads.append(Thread(target=i))
    # else:
    #     for i in [check_dns, check_virustotal, check_alien_vault, check_csp, check_ssl]:
    #         threads.append(Thread(target=i))
    
    # for thread in threads:
    #     thread.start()
    
    # for thread in threads:
    #     thread.join()
    print(f"[+] Total tests time : {time.time() - tot_time_init}")
    print()
    for log in log_msgs:
        print(f"[~] {log} check : [{results[log]}] :")
        print(log_msgs[log])
    display_dynamic_test()
    total_score = 0
    total_score+= results["DNS"]*0.25*0.4
    total_score+= results["VirusTotal"]*0.5*0.65*0.4
    total_score+= results["AlienVault"]*0.5*0.65*0.4
    total_score+= results["csp"]*0.15*0.6
    total_score+= results["ssl"]*0.4*0.6
    total_score+= results["Dynamic_tests"]['score']
    results["TOTAL_SCORE"] = total_score
    return results
    

# def url_testing(url) -> bool:
#     # -- Check redirect 
#     # -- DNS test, url_tests
#     # -- Virus Total
#     # -- Alien Vault Based on input
#     # -- Calculate a total passive scan
#     r_url=check_redirection.check_redirect(url)
#     if r_url:
#         dns_score = dnscheck1.dns_init_check(r_url)
#         virus_status = virustotal.is_malicious(r_url)
#         # alien_vault
#         if score > threshold:


    