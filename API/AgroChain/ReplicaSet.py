
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.read_preferences import ReadPreference 
import pymongo 

class ReplicaSet:
    
    def __init__(self, hosts, replicaSet, uname, pwd):
         self.hostString = hosts
         self.replicaSet = replicaSet
         self.user = uname
         self.pwd = pwd
    
    def __enter__(self):
        return self
        
    def createConnection(self):
        try:
            self.rsClient = MongoReplicaSetClient(self.hostString, replicaSet=self.replicaSet, read_preference=ReadPreference.SECONDARY_PREFERRED) 
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to Replicaset: %s" % e 
    
    def getPrimary(self):
        if self.rsClient is None:
                return 
        return self.rsClient.primary 
    
    def getSecondaries(self):
        if self.rsClient is None:
                return 
        return self.rsClient.secondaries
    
    def closeConnection(self):
        try: 
            if self.rsClient is None:
                return
            self.rsClient.close();
        except pymongo.errors.ConnectionFailure, e:
            print "Unable to close the replica set connection: %s" % e 

    def __exit__(self, type, value, traceback):
        try: 
            if self.rsClient is None:
                return
            self.rsClient.close();
        except pymongo.errors.ConnectionFailure, e:
            print "Unable to close the replica set connection: %s" % e 