import requests

count = 0
def check_redirect(url1,count):
    print(count)
    r1=requests.get(url1,allow_redirects=False)
    if str(r1.status_code) == "301" and count <2:
        location=r1.headers['location']
        count+=1
        check_redirect(location,count)
        
    else:
        print(url1)
    return