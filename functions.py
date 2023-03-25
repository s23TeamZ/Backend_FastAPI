
import uuid
import cv2
from features import check_redirection, dnscheck1, virustotal, alien_vault, csp, ssl, dbcheck
from features import categorize_qr_type
import time
from threading import Thread

def get_file_name(file_name: str) -> str:
    if(file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi'))):
        return f"{uuid.uuid4().hex[:10].upper()}{file_name[file_name.rfind('.'):]}"
    return ""

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
    text_l = [i for i in text]
    return text_l

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
        results[qr_idx] = {}
        results[qr_idx]['results'] = {}
        r_url=check_redirection.check_redirect(url1)
        if(r_url==False):
            results[qr_idx]['results'] = {"ERROR":"URL Redirection error"}
            
        elif(r_url!=url1):
            __1, url_data = categorize_qr_type.test_url(r_url)
            url_list[qr_idx] = url_data
            results[qr_idx]['url_data'] = url_data 
        print(f"\n\n[+] Checks for - {url_list[qr_idx]['URL']}\n")
        db_ck, db_log = dbcheck.db_check(url=url_list[qr_idx]["URL"], 
                                        domain=url_list[qr_idx]["Domain"])
        print(f"[~] DB check : [{db_ck}] :")
        print(db_log)
        if(db_ck == False):
            results[qr_idx]['results'].update(url_testing_core_func(url_list[qr_idx],
                        True if(results[qr_idx]['results'].get("ERROR",None)!=None) else False))
            if(not results[qr_idx]['results']["VirusTotal"] or not results[qr_idx]['results']["AlienVault"]):
                dbcheck.add_to_db(url=url_list[qr_idx]["URL"], domain=url_list[qr_idx]["Domain"])
        else:
            results[qr_idx]['results'].update({'DB':True})
        print(f"[=] Results : {results[qr_idx]}\n\n")
    return results

def url_testing_core_func(url_d, flag=False):
    results = {}
    threads = []
    log_msgs = {}
    def check_dns():
        init_time = time.time()
        try:
            dns_score,log_m = dnscheck1.dns_init_check(url_d["Domain"])
            results["DNS"] = dns_score
            log_msgs["DNS"] = log_m
        except Exception as e:
            results["DNS"] = "ERROR"
            log_msgs["DNS"] = f"\n[x] Error : {e}"
        print(f"[+] Time - DNS : {time.time() - init_time}")
    
    def check_virustotal():
        init_time = time.time()
        try: 
            virus_status,log_m = virustotal.is_malicious(url=url_d["URL"],
                                domain=url_d["Domain"],
                                ipaddr=url_d["IP"] if(url_d["IP"]!='') else None)
            results["VirusTotal"] = virus_status
            log_msgs["VirusTotal"] = log_m
        except:
            results["VirusTotal"] = "ERROR"
        print(f"[+] Time - Virus Total : {time.time() - init_time}")
    
    def check_alien_vault():
        init_time = time.time()
        try:
            alien_vault_status, log_m = alien_vault.check_malicious(url=url_d["URL"],
                                domain=url_d["Domain"],
                                ipaddr=url_d["IP"] if(url_d["IP"]!='') else None)
                                            
            results["AlienVault"] = alien_vault_status
            log_msgs["AlienVault"] = log_m
        except:
            results["AlienVault"] = "ERROR"
        print(f"[+] Time - Alien Vault : {time.time() - init_time}")
    
    def check_csp():
        init_time = time.time()
        try:
            csp_status, log_m = csp.check_csp_headers(url_d["URL"])
            results["csp"] = csp_status
            log_msgs["csp"] = log_m
        except:
            results["csp"] = "ERROR"
        print(f"[+] Time - CSP : {time.time() - init_time}")
    
    def check_ssl():
        init_time = time.time()
        try:
            ssl_status, log_m = ssl.check_website(url_d["URL"], url_d["Domain"])
            results["ssl"] = ssl_status
            log_msgs["ssl"] = log_m
        except:
            results["ssl"] = "ERROR"
        print(f"[+] Time - SSL : {time.time() - init_time}")

    if(flag):
        for i in [check_virustotal, check_alien_vault]:
            threads.append(Thread(target=i))
    else:
        for i in [check_dns, check_virustotal, check_alien_vault, check_csp, check_ssl]:
            threads.append(Thread(target=i))
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    print()
    for log in log_msgs:
        print(f"[~] {log} check : [{results[log]}] :")
        print(log_msgs[log])
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


    