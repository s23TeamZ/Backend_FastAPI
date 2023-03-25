import pymongo



def db_check(url):
        try:
            client=pymongo.MongoClient("mongodb://user:pass@localhost:27017/?authMechanism=DEFAULT")        
        except pymongo.errors.ConfigurationError:
            print("Db connection error")
          sys.exit(1)                
        db=client.get_database("scan_db")
        collection=db.get_collection("url_col")
        url_dict={'url':url}
        r_url=collection.find_one(url_dict)
        if r_url is None:
            collection.insert_one(url_dict)
            return False
        else:
            return True



