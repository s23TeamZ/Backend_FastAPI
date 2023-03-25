import pymongo
import sys


try:
    client=pymongo.MongoClient("mongodb://user:pass@localhost:27017/?authMechanism=DEFAULT")


except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)


db=client["scan_db"]

collection=db["url_col"]

url_list=[]

with open("urlhaus.abuse.ch.txt","r") as f1:
    for line in f1:
        line = line.strip()
        url_list.append(line)


url_lis_dict=[]


for i in url_list:
    url_lis_dict.append({"url":i})

# try:
#     collection.drop()  

# # return a friendly error if an authentication error is thrown
# except pymongo.errors.OperationFailure:
#   print("An authentication error was received. Are your username and password correct in your connection string?")
#   sys.exit(1)

result=collection.insert_many(url_lis_dict)
print(result)

r_url=collection.find_one({'url':"http://www.ugr.leszczynskie.net/mapa/Upfhbfhbavc1.png"})

print(r_url)

# if r_url is None:
#     collection.insert_one({'url':"http://www.ugr.leszczynskie.net/mapa/Upfhbfhbavc1.png"})







