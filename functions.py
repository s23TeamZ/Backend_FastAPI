
import uuid
import cv2
from url_tests import dnscheck
from features import check_redirection,dnscheck1,virustotal
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
    return text



def url_testing(url) -> bool:
    # -- Check redirect 
    # -- DNS test, url_tests
    # -- Virus Total
    # -- Alien Vault Based on input
    # -- Calculate a total passive scan
    r_url=check_redirection.check_redirect(url)
    if r_url:
        dns_score = dnscheck1.dns_init_check(r_url)
        virus_status = virustotal.is_malicious(r_url)
        # alien_vault
        if score > threshold:


    