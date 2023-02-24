import dns
import dns.resolver
from ipwhois import IPWhois

def is_malicous(url):
    url="facebook.com"
    ##Recommended number, between 2 and 7 name servers 
    #(RFC 2182 recommends to have at least 3 authoritative name servers for domains).
    NS_records = dns.resolver.resolve(url, 'NS')
    #print(len(NS_records))
    if len(NS_records) > 2 and len(NS_records) <= 7:
        print("OK. Name Servers between 2 and 7.")
    else:
        print("NOT OK. Name Servers not between 2 and 7.")

    # Print the name servers
    #for rdata in NS_records:
    #    print(rdata.target)

    ##Each name server should return identical NS records.
    NS_TLD  = []
    NS_names = (([rdata.target.to_text() for rdata in NS_records]))

    for i in range(0,len(NS_names)):
        #print(NS_names[i].split('.'))
        domains = list(reversed(NS_names[i].split('.')))
        NS_TLD.append(domains[2])

    if all(element == NS_TLD[0] for element in NS_TLD):
        print("OK. NS Records are identical:", NS_TLD[0])
    else:
        print("NOT OK. NS Records are not identical:", NS_TLD)

    ##To reach your name servers via IPv4 an A record is needed for each name server.

    ns_a_flag = 0
    for ns in NS_names:
        try:
            result_ns = dns.resolver.resolve(ns, 'A')
            #for ipval in result_ns:
            #    print('IP', ipval.to_text())
        except dns.resolver.NoAnswer:
            ns_a_flag = 1

    if ns_a_flag == 1:
        print("NOT OK. A records for each name servers NOT found")
    elif ns_a_flag == 0:
        print("OK. Found A records for each name servers.")

    ##To reach your name servers via IPv6 an AAAA record is needed for each name server.

    ns_aaaa_flag = 0
    for ns in NS_names:
        try:
            result_ns = dns.resolver.resolve(ns, 'AAAA')
            #for ipval in result_ns:
            #    print('IP', ipval.to_text())
        except dns.resolver.NoAnswer:
            ns_aaaa_flag = 1

    if ns_aaaa_flag == 1:
        print("NOT OK. AAAA records for each name servers NOT found")
    elif ns_aaaa_flag == 0:
        print("OK. Found AAAA records for each name servers.")

    # RFC 2181, section 10.3 says that host name must map directly to one 
    # or more address record (A or AAAA) and must not point to any CNAME 
    # records. RFC 1034, section 3.6.2 says if a name appears in the 
    # right-hand side of RR (Resource Record) it should not appear in the 
    # left-hand name of CNAME RR, thus CNAME records should not be used with 
    # NS and MX records. Despite this restrictions, there are many working 
    # configuration using CNAME with NS and MX records.

    ns_cname_flag = 0
    for ns in NS_names:
        try:
            result_cname = dns.resolver.resolve(ns, 'CNAME')
            ns_aaaa_flag = 1
            #for ipval in result_ns:
            #    print('IP', ipval.to_text())
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.NoAnswer:
            pass

    if ns_aaaa_flag == 1:
        print("NOT OK. CNAMEs found in NS record.")
    elif ns_aaaa_flag == 0:
        print("OK. No CNAMEs found in NS record.")

    ##Name servers should be dispersed (topologically and geographically) 
    ##across the Internet to avoid risk of single point of failure (RFC 2182).

    asn_list = []
    for ns in NS_names:
        resolver = dns.resolver.Resolver()
        result = resolver.resolve(ns, "A")
        ip_address = str(result[0])

        ipwhois = IPWhois(ip_address)
        result = ipwhois.lookup_rdap()
        asn_list.append(result['asn'])

    if all(element == asn_list[0] for element in asn_list):
        print("NOT OK. All name servers are located in one Autonomous System:", asn_list[0])
    else:
        print("OK. Name servers are dispersed:", asn_list)

    ###

    ##The MNAME field defines the Primary Master name server for the zone, 
    ##this name server should be found in your NS records.

    # Perform a DNS query to get the SOA record for the domain
    soa_response = dns.resolver.resolve(url, 'SOA')

    # Extract the serial number from the SOA record
    soa_resp = str(soa_response.response.answer[0])
    #print(soa_resp.split(" "))
    parent_ns = soa_resp.split(" ")[4]

    if parent_ns in NS_names:
        print("OK. Primary name server is listed at the parent name servers")
    else:
        print("NOT OK. Primary name server is not listed at the parent name servers")

