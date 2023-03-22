import requests
import re

def check_csp_headers(url):
    #url="https://mail.google.com/mail/u/0/"
    # Make a request to the URL and extract the Content Security Policy headers
    response = requests.get(url)
    headers = response.headers
    csp_headers = headers.get('Content-Security-Policy') or headers.get('Content-Security-Policy-Report-Only') or ''
    
    flag_only_valid_directive = False
    if not csp_headers:
        print(f"No Content Security Policy headers found for {url}")
        flag_no_csp_headers = True 
        flag_only_valid_directive = False

    # Check if the CSP headers are valid
    valid_directives = ['default-src', 'script-src', 'style-src', 'img-src', 'connect-src', 'font-src', 'object-src', 'media-src', 'frame-src', 'sandbox', 'plugin-types', 'report-uri', 'base-uri', 'form-action', 'frame-ancestors', 'manifest-src', 'worker-src', 'navigate-to']
    flag1 = False
    for directive in valid_directives:
        if re.search(fr"{directive}\s", csp_headers):
            flag1 = True
            break
    
    if not flag1:
        print(f"Invalid Content Security Policy header for {url}. Missing valid directive(s).")
        flag_missing_valid_directives = True
        flag_only_valid_directive = False

         # Check for known malicious directives
        malicious_directives = ['unsafe-inline', 'unsafe-eval']
        flag2 = False
        for directive in malicious_directives:
            if re.search(fr"{directive}", csp_headers):
                print(f"Content Security Policy header contains malicious directive for {url}: {directive}")
                flag2 = True
                flag_only_malicious_directive = True
                flag_only_valid_directive = False
                break
        
        if not flag2:
            print(f"Content Security Policy headers do not contain any known valid or malicious directives for {url}.")
            flag_no_valid_or_invalid_directives = True
            flag_only_valid_directive = False

    else:
        # Check for known malicious directives
        malicious_directives = ['unsafe-inline', 'unsafe-eval']
        flag3 = False
        for directive in malicious_directives:
            if re.search(fr"{directive}", csp_headers):
                print(f"Content Security Policy header contains malicious directiv efor {url}: {directive}")
                flag3 = True
                flag_both_valid_and_invalid_directive = True
                flag_only_valid_directive = False
                break
        
        if not flag3:
            print(f"Content Security Policy headers are valid and do not contain any known malicious directives for {url}.")
            flag_only_valid_directive = True
            
    if flag_only_valid_directive:
        return True
    else:
        return False