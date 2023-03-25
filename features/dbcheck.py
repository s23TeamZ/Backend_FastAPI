import pymongo



def db_check(url, domain=''):  # take client as argument from functions.py, to avoid reconnecting again and again
    try:
        client=pymongo.MongoClient("mongodb://user:pass@localhost:27017/?authMechanism=DEFAULT")        
    except pymongo.errors.ConfigurationError:
        # print("Db connection error")
        # sys.exit(1) 
        return False, "DB Connection Error"
    r_url = None
    r_domain = None

    db=client.get_database("scan_db")
    collection1=db.get_collection("url_col")
    url_dict={'url':url}
    r_url=collection1.find_one(url_dict)
    if(r_url == None):
            collection1=db.get_collection("url_col_our")
            r_url=collection1.find_one(url_dict)
    if(domain!=''):
        collection2=db.get_collection("domain_col")
        domain_dict={'domain':domain}
        r_domain=collection2.find_one(domain_dict)
        if(r_domain == None):
            collection2=db.get_collection("domain_col_our")
            r_domain=collection2.find_one(domain_dict)

    client.close()
    if(r_url and r_domain):
        # collection.insert_one(url_dict)
        return True, "URL, Domain Found in DB"
    elif(r_url):
        return True, "URL Found in DB"
    elif(r_domain):
        return True, "Domain Found in DB"
    else:
        return False, "Not found in DB"

def add_to_db(url, domain=''):
    try:
        client=pymongo.MongoClient("mongodb://user:pass@localhost:27017/?authMechanism=DEFAULT")        
    except pymongo.errors.ConfigurationError:
        # print("Db connection error")
        # sys.exit(1) 
        return False, "DB Connection Error"
    
    
    db=client.get_database("scan_db")
    collection1=db.get_collection("url_col_our")
    r_url=collection1.insert_one({'url':url})
    if(domain!=''):
        collection2=db.get_collection("domain_col_our")
        r_domain=collection2.insert_one({'domain':domain})

    return True, "OK"
