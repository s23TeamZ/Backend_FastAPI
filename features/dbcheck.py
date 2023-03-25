import pymongo



def db_check(url):  # take client as argument from functions.py, to avoid reconnecting again and again
    try:
        client=pymongo.MongoClient("mongodb://user:pass@localhost:27017/?authMechanism=DEFAULT")        
    except pymongo.errors.ConfigurationError:
        print("Db connection error")
        # sys.exit(1) 
        return False, "DB Connection Error"               
    db=client.get_database("scan_db")
    collection=db.get_collection("url_col")
    url_dict={'url':url}
    r_url=collection.find_one(url_dict)
    client.close()
    if r_url is None:
        # collection.insert_one(url_dict)
        return False, "Not Found in DB"
    else:
        return True, "Found in DB"



