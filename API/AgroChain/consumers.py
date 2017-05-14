from MongoConnector import MongoDBServer
from configReader import ConfReader  
import datetime
import helpers 

from producers import ProducerOps

'''
All consumers and sales related operations..  
'''  
class ConsumerOps:
    # default constructor 
    def __init__(self, confFile):  
        
        # initialize and read the configuration
        self.confReader = ConfReader(confFile) 
        self.database = str(self.confReader.GetConfigValue('configuration','agroChainDB'))  
        self.collConsumers = str(self.confReader.GetConfigValue('collections','consumers'))    
        self.collOrders = str(self.confReader.GetConfigValue('collections','orders'))   
        # Create mongodb connection
        self.mongo = MongoDBServer(str(self.confReader.GetConfigValue('configuration','mongosource')), int(self.confReader.GetConfigValue('configuration','mongoport')), '', '', True, False) 
        # for all producer related operations
        self.ProdOps = ProducerOps(confFile)
        
     # fetch concumers based on ID
    def getConsumerById (self, consumerID ):  
        # query data base and fetch producer details
        coll = self.mongo.GetCollection(self.database, self.collConsumers) 
        records = coll.find({"concumerid" : consumerID }, {"_id": False}) 
        # if there is no conumer exists
        if records.count() <= 0:
            return False, 'consumer doesnt exist' 
        # extract the producers
        consumer = records.next() 
        # if all checks passed
        return True, consumer 
    
    # adds or registers a new consumer
    def registerConsumer(self, consumer):   
        # generate the hashkey - only aadhar code and Name uniqly identifies the consumer
        hashkey = str(helpers.getHash(consumer["aadhar"] + consumer["name"])) 
        #print hashkey
        # check for existing producers or duplicate entriess
        coll = self.mongo.GetCollection(self.database, self.collConsumers)   
        records = coll.find({"hashkey" : str(hashkey)}, {'_id': False}) 
        # if already exists
        if records.count() > 0 :
            return False, 'Consumer already exists' 
        # if no one exists with the current information 
        # generate the information 
        consumer["concumerid"] = str(helpers.getUUID())
        consumer["hashkey"] = str(hashkey)
        consumer["registered"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
        consumer["updated"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   
        # save this json to mongoDB 
        self.mongo.Write2Collection(self.database, self.collConsumers, consumer) 
        # if everything goes fine
        return True, 'SUCCESS' 
    
    # returns all the Blockchain registered producers from the database
    def getAllConsumers(self):  
        #reading the data from orders collection
        coll = self.mongo.GetCollection(self.database, self.collConsumers)  
        records = coll.find({}, {'_id': False}) 
        data = [] 
        # for every consumer in the database
        for consumer in records:  
            data.append(consumer)  
        # return filtered consumers
        return True, data
    
    # returns all the Blockchain registered orders from the database
    def getAllOrders(self):  
        #reading the data from orders collection
        coll = self.mongo.GetCollection(self.database, self.collOrders)  
        records = coll.find({}, {'_id': False}) 
        data = [] 
        # for every order in the database
        for order in records:  
            data.append(order)  
        # return filtered order
        return True, data
    
    def getOrderByID(self, orderID) :
        # query data base and fetch producer details
        coll = self.mongo.GetCollection(self.database, self.collOrders) 
        records = coll.find({"orderID" : orderID }, {"_id": False}) 
        # if there is no conumer exists
        if records.count() <= 0:
            return False, 'order doesnt exist' 
        # extract the producers
        order = records.next() 
        # if all checks passed
        return True, order 
        
    def placeOrder(self, consumrID, order, producerID):
        #check whether the given consumer 
        flag, consumer = self.getConsumerById(consumrID)
        if not flag:
            return flag, str(consumer)
        
        # just verify the items lit to make sure one items has been added to the order
        order['items'] =  order['items'] if order.get('items') else [] 
        if len(order['items'] ) <= 0:
            return False, "Cant create an order no items added"
        
        #check whether the producer exists or not
        flag, producer = self.ProdOps.getProducerById(producerID)
        if not flag:
            return flag, str(producer)
        
        #generate the unique hash key
        hashkey =  str(helpers.getHash(order["datetime"] +  producer['hashkey'] + order["items"])) 
        # if no one exists with the current information 
        # generate the information 
        order["orderid"] = str(helpers.getUUID())
        order["hashkey"] = str(hashkey)
        order["registered"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
        order["updated"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   
        
        # save this json to mongoDB 
        self.mongo.Write2Collection(self.database, self.collOrders, order) 
        # if everything goes fine
        return True, 'SUCCESS' 
    
    #updates the order
    def updateOrder(self, consumrID, order, producerID): 
        # check whether the given consumer 
        flag, consumer = self.getConsumerById(consumrID)
        if not flag:
            return flag, str(consumer)  
        #check whether the producer exists or not
        flag, producer = self.ProdOps.getProducerById(producerID)
        if not flag:
            return flag, str(producer)
        # if no order exists or some error
        flag, currentOrder = self.getOrderByID(order['orderID'])    
        if not flag:
            return flag, str(producer)
        
        # if no one exists with the current information 
        # generate the information   
        currentOrder["updated"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  
        currentOrder['items'] =  order['items'] if order.get('items') else [] 
        currentOrder['status'] =  order['status'] if order.get('status') else "created"
        currentOrder['total'] =  order['total'] if order.get('total') else "0"
        currentOrder['shipDate'] =  order['shipDate'] if order.get('shipDate') else None
        
        if len(currentOrder['items'] ) <= 0:
            return False, "Cant create an order no items added"  
        # save this json to mongoDB  
        self.mongo.Update2Collection(self.database, self.collSeasons, {"orderID" : currentOrder["orderID"]},  currentOrder)
        
        # if everything goes fine
        return True, 'SUCCESS' 

'''
        
 # Ethereum based consumers list
cop = ConsumerOps('config.ini')
#status, consumers = cop.getAllConsumers()  
#print status
#print consumers

inputdata = {

 "consumer" : {
 	"aadhar" : "7678998798798",
 	"name" : "jaskjkjkjalkjls",
 	"password" : "pass123",
 	"address" : "gfgfh",
 	"contact" : "545765757"
 	
 }
 }
 
flag, data = cop.registerConsumer(inputdata['consumer']) 
print flag
print data
'''