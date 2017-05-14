from MongoConnector import MongoDBServer
from configReader import ConfReader  
import datetime
import helpers 

'''
All producers and Crops related operations..  
'''  
class ProducerOps:
    # default constructor 
    def __init__(self, confFile):  
        
        # initialize and read the configuration
        self.confReader = ConfReader(confFile) 
        self.database = str(self.confReader.GetConfigValue('configuration','agroChainDB')) 
        self.collProducers = str(self.confReader.GetConfigValue('collections','farmers'))
        self.collCropSeasons = str(self.confReader.GetConfigValue('collections','seasons'))     
        # Create mongodb connection
        self.mongo = MongoDBServer(str(self.confReader.GetConfigValue('configuration','mongosource')), int(self.confReader.GetConfigValue('configuration','mongoport')), '', '', True, False) 
       
    
    # fetch producers based on ID
    def getProducerById (self, producerID ):  
        # query data base and fetch producer details
        coll = self.mongo.GetCollection(self.database, self.collProducers) 
        records = coll.find({"producerid" : producerID }, {"_id": False}) 
        # if there is no consumer exists
        if records.count() <= 0:
            return False, 'producer doesnt exist'
            
        # extract the producers
        producer = records.next() 
        # if all checks passed
        return True, producer
     
    
    # adds or registers a new producer
    def registerProducer(self, producer):   
        # generate the hashkey - only aadhar code and Name uniqly identifies producers
        hashkey = str(helpers.getHash(producer["aadhar"] + producer["name"])) 
        #print hashkey
        # check for existing producers or duplicate entriess
        coll = self.mongo.GetCollection(self.database, self.collProducer)   
        records = coll.find({"hashkey" : str(hashkey)}, {'_id': False}) 
        # if already exists
        if records.count() > 0 :
            return False, 'producesr already exists' 
        # if no one exists with the current information 
        # generate the information 
        producer["producerid"] = str(helpers.getUUID())
        producer["hashkey"] = str(hashkey)
        producer["registered"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
        producer["updated"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   
        # save this json to mongoDB 
        self.mongo.Write2Collection(self.database, self.collProducers, producer) 
        # if everything goes fine
        return True, 'SUCCESS' 
    
    # returns all the Blockchain registered producers from the database
    def getAllProducers(self):  
        #reading the data from suppliers collection
        coll = self.mongo.GetCollection(self.database, self.collProducers)  
        records = coll.find({}, {'_id': False}) 
        data = [] 
        # for every producer in the database
        for producer in records:  
            data.append(producer)  
        # return filtered producers
        return True, data   
    
    # returns the seasons 
    def getCropSeasonByID(self, seasonID): 
        # query data base and fetch season details
        coll = self.mongo.GetCollection(self.database, self.collCropSeasons) 
        records = coll.find({"seasonID" : seasonID }, {"_id": False}) 
        # if there is no seasons exists
        if records.count() <= 0:
            return False, 'season information doesnt exist' 
        # extract the seaon details
        seasonCrops = records.next()   
        # if all checks passed
        return True, seasonCrops
    
    # returns all the crops from a particular season, since season already verfied
    # we will not verify again
    def getAllCrops(self, seasonID):
        # get the data from mongodb and display
        flag, season = self.getCropSeasonByID(seasonID)
        if not flag:
            return False, str(season)
        return True, season['crops']  
     
    # adds or registers a new season which invloves calling FarmProduce Contract
    def registerCropSeason(self, season):    
        # check whether season exists or not
        flag, producer =  self.getProducerById(season['producerID'])
        if not flag :
            return flag, str(producer)
        
        # generate the hashkey 
        hashkey = str(helpers.getHash(season["name"] + producer["hashkey"] + season["startDate"] + season["seeder"])) 
         
        # check for existing season or duplicate entriess
        coll = self.mongo.GetCollection(self.database, self.collSeasons)   
        records = coll.find({"hashkey" : str(hashkey)}, {'_id': False}) 
        # if already exists
        if records.count() > 0 :
            return False, 'Season already exists'
        
        # if no one exists with the current information 
        # generate the information  
        season["hashkey"] = str(hashkey)
        season["seasonID"] =  str(helpers.getUUID())
        season["registered"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
        season["updated"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  
        season["crops"] = season['crops'] if season.get('crops') else [] 
        season["status"] = season['status'] if season.get('status') else "Created"
        
        if len(season["crops"]) <= 0 :
            return False, "a season must have atleast one crop"  
        
        # save this json to mongoDB and BlockChain
        self.mongo.Write2Collection(self.database, self.collSeasons, season) 
    
        # if everything goes fine
        return True, 'SUCCESS'  
    
    # updates the crop season details
    def updateCropSeason(self, season):
        # check whether season exists or not
        flag, producer =  self.getProducerById(season['producerID'])
        if not flag :
            return flag, str(producer)
        
        # check whether we have that season exists or not
        flag, currentSeason = self.getCropSeasonByID(season['seasonID'])
        if not flag:
            return flag, str(currentSeason) 
        
        # if no one exists with the current information generate the information  
        currentSeason["updated"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  
        currentSeason["crops"] = season['crops'] if season.get('crops') else currentSeason['crops']
        currentSeason["status"] = season['status'] if season.get('status') else currentSeason['status']  
        
        if len(season["crops"]) <= 0 :
            return False, "a season must have atleast one crop"  
        # save this json to mongoDB and BlockChain
        self.mongo.Update2Collection(self.database, self.collSeasons, {"seasonID" : currentSeason["seasonID"]},  currentSeason)
        
        # if everything goes fine
        return True, 'SUCCESS'  
    
    def updateWorkLog(self, wroklog, seasonID, cropID) :         
        # check whether we have that season exists or not
        flag, currentSeason = self.getCropSeasonByID(seasonID)
        if not flag:
            return flag, str(currentSeason) 
         
        #sert log into respective product log
        for crop in currentSeason["crops"]:
            if crop['cropID'] == cropID :
                currentSeason["crops"]["log"].append(wroklog)
                
        # season must have atleast one crop 
        if len(currentSeason["crops"]) <= 0 :
            return False, "a season must have atleast one crop"  
        # save this json to mongoDB and BlockChain
        self.mongo.Update2Collection(self.database, self.collSeasons, {"seasonID" : currentSeason["seasonID"]},  currentSeason)
        
        # if everything goes fine
        return True, 'SUCCESS'       
    
    # updates the investments of the season
    def updateInvestments(self, investment, seasonID, cropID) :         
        # check whether we have that season exists or not
        flag, currentSeason = self.getCropSeasonByID(seasonID)
        if not flag:
            return flag, str(currentSeason) 
         
        #sert log into respective product log
        for crop in currentSeason["crops"]:
            if crop['cropID'] == cropID :
                currentSeason["crops"]["investments"].append(investment)
                
        # season must have atleast one crop 
        if len(currentSeason["crops"]) <= 0 :
            return False, "a season must have atleast one crop"  
        # save this json to mongoDB and BlockChain
        self.mongo.Update2Collection(self.database, self.collSeasons, {"seasonID" : currentSeason["seasonID"]},  currentSeason)
        
        # if everything goes fine
        return True, 'SUCCESS'       
'''
pop = ProducerOps('config.ini')
data = {u'crops': [{u'status': u'created', u'startDate': u'2017-06-05 00:00:00', u'storageHashkey': u'SOMETHING', u'name': u'small corn', u'quantity ': 250, u'pType': u'corn', u'seeder': u'62da7c15-74f4-4819-9dfe-58c4076c8e52', u'endTime': u'2017-10-10 12:00:00', u'unitPrice': u'1200INR', u'unit': u'100KG', u'log': []}, {u'status': u'created', u'startDate': u'2017-06-05 00:00:00', u'storageHashkey': u'SOMETHING', u'name': u'Moong Dal', u'quantity ': 10, u'pType': u'dal', u'seeder': u'62da7c15-74f4-4819-9dfe-58c4076c8e52', u'endTime': u'2017-10-10 12:00:00', u'unitPrice': u'4200INR', u'unit': u'100KG', u'log': []}], u'startDate': u'2017-05-14 15:50:44', u'hashkey': u'SOMETHING', u'status': u'cretaed', u'name': u'Season Jun17-Oct17', 'producerID':'xyz'}
flag, output = pop.registerCropSeason(data)

print flag
print output
'''