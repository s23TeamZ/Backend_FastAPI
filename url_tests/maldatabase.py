def is_maldatabase(url):
    with open('E:/NEU - MSCY/Capstone Project - CY7900 35732/Capstone/Backend_FastAPI/url_tests/urlhaus.abuse.ch.txt') as f:
        urls = [line.strip() for line in f]
    if url in urls:
        flag = 1
    else:
        flag = 2


    with open('E:/NEU - MSCY/Capstone Project - CY7900 35732/Capstone/Backend_FastAPI/url_tests/delisted.txt') as f:
        domains = [line.strip() for line in f]
    url_to_check = url.replace('https://', '').replace('http://', '').strip()  
    if url_to_check in domains:
        flag1 = 3
    else:
        flag1 = 4


    if flag == 1 or flag1 == 3:
        return f'The URL {url} is in the malware database.'
    else:
        return f'The URL {url} is not in the malware database.'


