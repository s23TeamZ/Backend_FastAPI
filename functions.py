
import uuid
import cv2

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
    for url in url_list:
        break
    pass_l
    