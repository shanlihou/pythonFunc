import pymongo


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://192.168.17.22:27017/")
    mydb = myclient['leanote']
    collist = mydb.list_collection_names()
    print(collist)