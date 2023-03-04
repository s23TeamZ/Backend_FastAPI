
import uuid
import cv2
from features import check_redirection, dnscheck1, virustotal, alien_vault
from features import categorize_qr_type
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
        r_url=check_redirection.check_redirect(url1)
        if(r_url==False):
            results[qr_idx] = {"ERROR":"URL Redirection error"}
            continue
        if(r_url!=url1):
            __1, url_data = categorize_qr_type.test_url(r_url)
            url_list[qr_idx] = url_data
        try:
            dns_score = dnscheck1.dns_init_check(url_list[qr_idx]["URL"])
            results[qr_idx]["DNS"] = dns_score
        except:
            results[qr_idx]["DNS"] = "ERROR"
        try: 
            virus_status = virustotal.is_malicious(url=url_list[qr_idx]["URL"],
                                domain=url_list[qr_idx]["Domain"],
                                ipaddr=url_list[qr_idx]["IP"] if(url_list[qr_idx]["IP"]!='') else None)
            results[qr_idx]["VirusTotal"] = virus_status
        except:
            results[qr_idx]["VirusTotal"] = "ERROR"
        try:
            alien_vault_status = alien_vault.check_malicious(url=url_list[qr_idx]["URL"],
                                domain=url_list[qr_idx]["Domain"],
                                ipaddr=url_list[qr_idx]["IP"] if(url_list[qr_idx]["IP"]!='') else None)
                                            
            results[qr_idx]["AlienVault"] = alien_vault_status
        except:
            results[qr_idx]["AlienVault"] = "ERROR"
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


    