import pymongo 
import sys 
import traceback
from datetime import datetime  

class MongoDBServer :
    def __init__(self, server, port, user, pwd, slaveOkVal, authEnabled):
        self.Server = server
        self.Port = port
        try:
            if authEnabled:
                uri = 'mongodb://'+user+':'+pwd+'@' + self.Server + ':' + str(self.Port)
                connection = pymongo.MongoClient(uri, slaveOk=slaveOkVal)
            else :
                connection = pymongo.MongoClient(self.Server, self.Port, slaveOk=slaveOkVal) 
            
            self.Connection = connection
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e 
        
    def GetServerInstance(self):
        return self.Connection
    
    def GetAllDatabaseNames(self): 
        return self.Connection.database_names() 
    
    def GetCollectionList(self, dbName):
        db = self.Connection[dbName]
        return db.collection_names() 
    
    def GetCollection(self, dbName, collectionName):
        db = self.Connection[dbName] 
        return db[collectionName] 
    
    #updates the document if it exists else it creas new in specified collection
    def Update2Collection(self, dbName, collectionName,  document, paramDB, paramCollection):  
        logdb = self.Connection[dbName] 
        logdb[collectionName].find_and_modify({'dbName': paramDB, 'collection': paramCollection}, {'$set' : document}, upsert=True)
    
    #updates the document if it exists else it creas new in specified collection
    def Update2Collection2(self, dbName, collectionName,  document, paramDB, paramCollection):  
        logdb = self.Connection[dbName] 
        logdb[collectionName].remove({'dbName': paramDB, 'collection': paramCollection})
        logdb[collectionName].insert(document)        
        
    #creates a document to specified collection
    def Write2Collection(self, dbName, collectionName,  document): 
        try:
            logdb = self.Connection[dbName]
            logdb[collectionName].insert(document) 
        except: 
            print sys.exc_info()
    
    