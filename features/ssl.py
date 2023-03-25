import requests
import ssl
import socket
import datetime
import hashlib

def check_website(url, domain1):
    log_msgs = ''
    # Check the SSL/TLS certificate
    try:
        # Extract the domain and port from the URL
        # domain, port = url.split(":")[1].strip("/"), 443
        domain, port = domain1, 443
        if url.startswith("http://"):
            port = 80
            log_msgs += f"The website {url} is using HTTP and does not have an SSL/TLS certificate.\n"
        # Create a socket and wrap it with an SSL context if using HTTPS
        else:
            context = ssl.create_default_context()
            with socket.create_connection((domain, port)) as sock:
                if port == 443:
                    with context.wrap_socket(sock, server_hostname=domain) as ssl_sock:
                        # Check the certificate's expiration date
                        cert = ssl_sock.getpeercert()
                        ssl_version = ssl_sock.version()
                        cert_expiry = cert['notAfter']
                        cert_expiry_datetime = datetime.datetime.strptime(cert_expiry, '%b %d %H:%M:%S %Y %Z')
                        ssl_valid = cert_expiry_datetime > datetime.datetime.now()

    except Exception as e:
        log_msgs += f"Error validating certificate: {str(e)}\n"
        ssl_valid = False

    # Check the HTTP response code
    try:
        response = requests.get(url)
        http_valid = response.status_code == 200
    except Exception as e:
        log_msgs += f"Error checking HTTP response code: {str(e)}\n"
        http_valid = False

    # Print the results
    if port == 443:
        if ssl_valid and http_valid:
            log_msgs += f"The SSL/TLS certificate for website {url} is not expired and the website is accessible!\n"
            flag1 = True
        elif not ssl_valid:
            log_msgs += f"The SSL/TLS certificate for {url} is invalid or has expired.\n"
            flag1 = False
        elif not http_valid:
            log_msgs += f"The website {url} is not accessible (HTTP response code {response.status_code}).\n"
            flag1 = False

        if ssl_version == "TLSv1.2" or ssl_version == "TLSv1.3":
            log_msgs += f"The SSL/TLS protocol version for {url} is {ssl_version} and is secure\n"
            flag2 = True
        else:
            log_msgs += f"The SSL/TLS protocol version for {url} is not secure. Protocol version: {ssl_version}\n"
            flag2 = False

        
        if flag1 and flag2:
            return True, log_msgs
        else:
            return False, log_msgs



# Possible outputs for ssl_version could include:

# (2, 0) - indicating the use of SSLv2 protocol.
# (3, 0) - indicating the use of SSLv3 protocol.
# (3, 1) - indicating the use of TLSv1.0 protocol.
# (3, 2) - indicating the use of TLSv1.1 protocol.
# (3, 3) - indicating the use of TLSv1.2 or TLSv1.3 protocol.