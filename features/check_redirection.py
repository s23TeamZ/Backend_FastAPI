from requests import get as requests_get

HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
def check_redirect(url1):
    count = 0
    while(count<=2):
        try:
            r1=requests_get(url1, allow_redirects=False, headers=HEADERS)
        except:
            # return "URL Error"
            return False
        if(r1.status_code == 301 and count <3):
            url1=r1.headers['location']
            count+=1
        else:
            # print(count)
            return r1.headers.get("location",url1)
    return False

