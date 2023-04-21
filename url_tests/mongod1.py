import pymongo
import sys
import time

time_init = time.time()


try:
    client=pymongo.MongoClient("mongodb://user:pass@localhost:27017/?authMechanism=DEFAULT")


except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)


db=client["scan_db"]

if('url_col' in db.list_collection_names()):
    collection=db["url_col"]
    collection.drop()

collection=db["url_col"]

url_list=[]

with open("urlhaus.abuse.ch.txt","r") as f1:
    for line in f1:
        line = line.strip()
        url_list.append({"url":line})


result=collection.insert_many(url_list)


if('domain_col' in db.list_collection_names()):
    collection=db["domain_col"]
    collection.drop()

collection=db["domain_col"]
url_list=[]

with open("delisted.txt","r") as f1:
    for line in f1:
        line = line.strip()
        if(line.startswith('www.')):
            line = line[4:]
        url_list.append({"domain":line})


result=collection.insert_many(url_list)

collection=db["url_col_our"]
collection=db["domain_col_our"]

print(f"[+] Time : {time.time() - time_init}")


# try:
#     collection.drop()  

# # return a friendly error if an authentication error is thrown
# except pymongo.errors.OperationFailure:
#   print("An authentication error was received. Are your username and password correct in your connection string?")
#   sys.exit(1)

print(result)

# r_url=collection.find_one({'url':"http://www.ugr.leszczynskie.net/mapa/Upfhbfhbavc1.png"})

# print(r_url)

# if r_url is None:
#     collection.insert_one({'url':"http://www.ugr.leszczynskie.net/mapa/Upfhbfhbavc1.png"})







