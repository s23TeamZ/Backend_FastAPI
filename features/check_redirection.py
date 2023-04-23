from requests import get as requests_get
import re
HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
def check_redirect(url1):
    count = 1
    r_score_table = {1:100, 2:90, 3:70, 4:50, 5:20}
    #####
    # RFC 1945
    # https://www.rfc-editor.org/rfc/rfc1945
    # 9.3  Redirection 3xx
    # A user agent should never automatically redirect a request more than 5 times, since such redirections usually indicate an infinite loop.
    #####
    while(count<=5):    
        try:
            r1=requests_get(url1, allow_redirects=False, headers=HEADERS, timeout=2)
        except Exception as e:
            # return "URL Error"
            print(f"[!] Error Check Redirect : \n{str(e)}")
            return False, 0
        if((r1.status_code >=300 and r1.status_code<=399) and count <=5):
            url1=r1.headers['location']
            if(not url1.startswith('http')):
                web_url_raw = re.findall(r'https:\/\/|http:\/\/|www\.|([\w\d\._-]+\.[\w\d]{1,9})', url1)
                web_url = [i for i in web_url_raw if(i!='')]
                url1 = f"https://{url1[url1.find(web_url[0]):]}"
            count+=1
        else:
            # print(count)
            return r1.headers.get("location",url1), r_score_table[count]
    return False, 0

