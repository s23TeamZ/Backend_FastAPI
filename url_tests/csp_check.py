import requests
import re

def check_csp_headers(url):
    # Make a request to the URL and extract the Content Security Policy headers
    response = requests.get(url)
    headers = response.headers
    csp_headers = headers.get('Content-Security-Policy') or headers.get('Content-Security-Policy-Report-Only') or ''
    
    if not csp_headers:
        print(f"No Content Security Policy headers found for {url}")
        return
    
    # Check if the CSP headers are valid
    valid_directives = ['default-src', 'script-src', 'style-src', 'img-src', 'connect-src', 'font-src', 'object-src', 'media-src', 'frame-src', 'sandbox', 'plugin-types', 'report-uri', 'base-uri', 'form-action', 'frame-ancestors', 'manifest-src', 'worker-src', 'navigate-to']
    flag1 = False
    for directive in valid_directives:
        if re.search(fr"{directive}\s", csp_headers):
            flag1 = True
            break
    
    if not flag1:
        print(f"Invalid Content Security Policy header for {url}. Missing valid directive(s).")
         # Check for known malicious directives
        malicious_directives = ['unsafe-inline', 'unsafe-eval']
        flag2 = False
        for directive in malicious_directives:
            if re.search(fr"{directive}", csp_headers):
                print(f"Content Security Policy header contains malicious directive for {url}: {directive}")
                flag2 = True
                break
        
        if not flag2:
            print(f"Content Security Policy headers do not contain any known valid or malicious directives for {url}.")

    else:
        # Check for known malicious directives
        malicious_directives = ['unsafe-inline', 'unsafe-eval']
        flag2 = False
        for directive in malicious_directives:
            if re.search(fr"{directive}", csp_headers):
                print(f"Content Security Policy header contains malicious directive for {url}: {directive}")
                flag2 = True
                break
        
        if not flag2:
            print(f"Content Security Policy headers are valid and do not contain any known malicious directives for {url}.")
