from flask import Flask, make_response
from flask import request
from flask import jsonify  
from consumers import ConsumerOps
from producers import ProducerOps

import hashlib
import uuid 

app = Flask(__name__) 

# Prepares response object to be returned
def prepareResponse(message, statuscode):
    resp = make_response(jsonify(message), statuscode) 
    #adding CORS related headers
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true' 
    print resp
    return resp

#generates the hash for any given string
def getHash(inputText):    
    # Random string used for hashing whch makes brute force even more tougher 
    secretKey = "@hashgenerator factory individual private positive"    
    #get the algo object
    sha256 = hashlib.sha256()      
    # Get string and put into givenString. 
    sha256.update(inputText + secretKey)    
    #return the hash from algo object
    return sha256.hexdigest() 

#generates randdom UUID everytimg
def getUUID():
    return uuid.uuid4();

'''
===============================================================================
Api methods related to consumers. All consumers infromation will be stored on 
blockchain. sonsumers infromation can be stored in an external database, and the 
Blockchain hash can be used reference key to external database [Future]
===============================================================================
'''
# retruns all the consumers in the network
@app.route('/api/v1/consumers/all', methods = ['POST']) 
def api_getAllConsumers():
    try : 
        app.logger.info('Info : Consumers lists request received ')
        
        # Ethereum based consumers list
        cop = ConsumerOps('config.ini')
        status, consumers = cop.getAllConsumers() 
 
        # if successfully gets the list of consumers
        if status:  
            return prepareResponse({'message' :'SUCCESS', 'result': consumers}, 200)  
        # if there are any errors
        return prepareResponse({'message' :'unable to extract consumers list'}, 500)
    except: 
        return prepareResponse({'message' :'unable to extract consumers list'}, 500)

# retruns the specific consumer by his unique id
@app.route('/api/v1/consumers/get', methods = ['POST']) 
def api_getConsumerByID():
    try :  
        # read the POST request payload
        inputjson = request.get_json(force=True)
        app.logger.info('Info : consumers information request received for '+ str(inputjson))
        
        # Ethereum based consumers list
        cop = ConsumerOps('config.ini')
        exists, consumer = cop.getConsumerById(inputjson['consumerid']) 
        # if consumers exists and gets his info
        if exists:
            return prepareResponse({'message' : 'SUCCESS', 'result': consumer}, 200) 
        # if there is any errors
        return prepareResponse({'message' : 'unable to extract consumers information'}, 500)
    except: 
        return prepareResponse({'message' : 'unable to extract consumers information'}, 500)

# adds or registers a new consumer
@app.route('/api/v1/consumers/register', methods = ['POST']) 
def api_registerConsumer():
    try : 
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : consumers registration req received. payload: ' + str(inputJson)) 
        
        # Ethereum based consumers list
        cop = ConsumerOps('config.ini')
        registered, msg = cop.registerConsumer(inputJson['consumer']) 
        #if consumer registered sucessfully
        if registered: 
            return prepareResponse({'message' :'SUCCESS'}, 200)
         # in case of any errors
        return prepareResponse({'message' :'unable to register a consumers', 'info': msg}, 500) 
    except: 
        return prepareResponse({'message' :'unable to register new consumers'}, 500)
        
# returns all the orders 
@app.route('/api/v1/orders/all', methods = ['POST']) 
def api_getAllOrders():
    try:
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : get all orders info updation req received. payload: ' + str(inputJson)) 
        
        # Ethereum based orders list
        cop = ConsumerOps('config.ini')
        updated, orders = cop.getAllOrders()
        #if consumer updated sucessfully
        if updated: 
           return prepareResponse({'message' :'SUCCESS', 'result': orders}, 200) 
         # in case of any errors
        return prepareResponse({'message' :'unable to get the orders information', 'info': orders}, 500) 
    except:
        return prepareResponse({'message' :'unable to get the orders information'}, 500) 

# creates a new order
@app.route('/api/v1/orders/create', methods = ['POST']) 
def api_placeOrder(): 
    try : 
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info :place order request received for '+ str(inputJson))
        
        # Ethereum based orders list
        cop = ConsumerOps('config.ini') 
        placed, msg = cop.placeOrder(inputJson['consumrID'], inputJson['order'], inputJson['producerID'] )
        #if placed order successfully
        if placed:
             return prepareResponse({'message' :'SUCCESS'}, 200) 
        # if in case of any errors
        return prepareResponse({'message' : 'unable to place order', 'info': str(msg)}, 500)
    except:
        return prepareResponse({'message' :'unable to place order'}, 500) 

# update the order and return the status
@app.route('/api/v1/orders/updateOrder', methods = ['POST']) 
def api_updateOrder():
    try :  
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : update orders request received for  '+ str(inputJson)) 
        
        # Ethereum based orders operations
        cop = ConsumerOps('config.ini')  
        flag, msg = cop.updateOrder(inputJson['consumrID'], inputJson['order'], inputJson['producerID'] )
        # if parts fetched successfully
        if flag:
            return prepareResponse({'message' :'SUCCESS', 'result': msg}, 200) 
        # in case of any error
        return prepareResponse({'message' :'unable to update orders', 'info': str(msg)}, 500)
    except: 
        return prepareResponse({'message' :'unable to update orders'}, 500)

# returns the order soecific informtion by its ID
@app.route('/api/v1/orders/get', methods= ['POST']) 
def api_getOrderyID(supid):
    try : 
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : get order by id request received for  '+ str(inputJson)) 
        
        # Ethereum based orders operations
        cop = ConsumerOps('config.ini')  
        exists, order = cop.getOrderByID(inputJson['orderid'])
        # if order info fetched successfully
        if exists:
            return prepareResponse({'message' :'SUCCESS', 'result': order}, 200) 
        # in case of any error
        return prepareResponse({'message' :'unable to fetch order infromation', 'info': str(order)}, 500)
    except: 
        return prepareResponse({'message' :'unable to fetch order infromation'}, 500)

'''
===============================================================================
Api methods related to producers. All producer infromation will be stored on 
blockchain. producer infromation can be stored in an external database, and the 
Blockchain hash can be used reference key to external database [Future]
===============================================================================
'''
# retruns all the prodcers in the network
@app.route('/api/v1/producers/all', methods = ['POST']) 
def api_getAllProducers():
    try :
        # read the POST request payload
        inputjson = request.get_json(force=True)
        app.logger.info('Info : prodcuers lists request received ' + str(inputjson))
        
        # Ethereum based producers list
        cop = ProducerOps('config.ini')
        status, producers = cop.getAllProducers()  
        # if successfully gets the list of producers
        if status:  
            return prepareResponse({'message' :'SUCCESS', 'result': producers}, 200)  
        # if there are any errors
        return prepareResponse({'message' :'unable to extract producers list'}, 500)
    except: 
        return prepareResponse({'message' :'unable to extract producers list'}, 500)  

# retruns the specific producer by his unique hashkey
@app.route('/api/v1/producers/get', methods = ['POST']) 
def api_getProducerByID():
    try :  
        # read the POST request payload
        inputjson = request.get_json(force=True)
        app.logger.info('Info : producer information request received for '+ str(inputjson))
        
        # Ethereum based producers list
        cop = ProducerOps('config.ini')
        exists, producer = cop.getProducerById(inputjson['producerID']) 
        # if producer exists and gets his info
        if exists:
            return prepareResponse({'message' : 'SUCCESS', 'result': producer}, 200) 
        # if there is any errors
        return prepareResponse({'message' : 'unable to extract producer information'}, 500)
    except: 
        return prepareResponse({'message' : 'unable to extract producer information'}, 500) 
    
# adds or registers a new producer
@app.route('/api/v1/producers/register', methods = ['POST']) 
def api_registerProducer():
    try : 
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : producer registration req received. payload: ' + str(inputJson)) 
        
        # Ethereum based producers list
        cop = ProducerOps('config.ini')
        registered, msg = cop.registerProducer(inputJson['producer']) 
        #if producers registered sucessfully
        if registered: 
            return prepareResponse({'message' :'SUCCESS'}, 200)
         # in case of any errors
        return prepareResponse({'message' :'unable to register a producer', 'info': msg}, 500) 
    except: 
        return prepareResponse({'message' :'unable to register new producer'}, 500)
 

# retruns the specific crop season by his unique hashkey
@app.route('/api/v1/seasons/get', methods = ['POST']) 
def api_getCropSeasonByID():
    try :  
        # read the POST request payload
        inputjson = request.get_json(force=True)
        app.logger.info('Info : season information request received for '+ str(inputjson))
        
        # Ethereum based seasons list
        cop = ProducerOps('config.ini')
        exists, seasons = cop.getCropSeasonByID(inputjson['seasonID']) 
        # if seasons exists and gets his info
        if exists:
            return prepareResponse({'message' : 'SUCCESS', 'result': seasons}, 200) 
        # if there is any errors
        return prepareResponse({'message' : 'unable to extract season information'}, 500)
    except: 
        return prepareResponse({'message' : 'unable to extract season information'}, 500) 
    

# retruns all the cropsfor a given season
@app.route('/api/v1/seasons/allcrops', methods = ['POST']) 
def api_getAllCrops():
    try :
        # read the POST request payload
        inputjson = request.get_json(force=True)
        app.logger.info('Info : season crop lists request received ' + str(inputjson))
        
        # Ethereum based producers list
        cop = ProducerOps('config.ini')
        status, crops = cop.getAllCrops(inputjson['seasonID'])  
        # if successfully gets the list of crops
        if status:  
            return prepareResponse({'message' :'SUCCESS', 'result': crops}, 200)  
        # if there are any errors
        return prepareResponse({'message' :'unable to extract crops list'}, 500)
    except: 
        return prepareResponse({'message' :'unable to extract crops list'}, 500)  
 
# adds or registers a new crop season
@app.route('/api/v1/seasons/add', methods = ['POST']) 
def api_registerCropSeason():
    try : 
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : crops season registration req received. payload: ' + str(inputJson)) 
        
        # Ethereum based seasons list
        cop = ProducerOps('config.ini')
        print inputJson['season']
        registered, msg = cop.registerCropSeason(inputJson['season'])
        print msg
        #if season registered sucessfully
        if registered: 
            return prepareResponse({'message' :'SUCCESS'}, 200)
         # in case of any errors
        return prepareResponse({'message' :'unable to register a crop season', 'info': msg}, 500) 
    except: 
        return prepareResponse({'message' :'unable to register a crop season'}, 500)
 
# updates crop season details
@app.route('/api/v1/seasons/update', methods = ['POST']) 
def api_updateCropSeason():
    try : 
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : crops season update req received. payload: ' + str(inputJson)) 
        
        # Ethereum based producers list
        cop = ProducerOps('config.ini')
        updated, msg = cop.updateCropSeason(inputJson['season']) 
        #if season updated sucessfully
        if updated: 
            return prepareResponse({'message' :'SUCCESS'}, 200)
         # in case of any errors
        return prepareResponse({'message' :'unable to update crop season information', 'info': msg}, 500) 
    except: 
        return prepareResponse({'message' :'unable to update crop season information'}, 500)

# updates crop season's worklog
@app.route('/api/v1/seasons/log', methods = ['POST']) 
def api_updateWorkLog():
    try : 
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : write to worklog req received. payload: ' + str(inputJson)) 
        
        # Ethereum based producers list
        cop = ProducerOps('config.ini')
        updated, msg = cop.updateWorkLog(inputJson['wroklog'], inputJson['seasonID'], inputJson['cropID']) 
        #if worklog updated sucessfully
        if updated: 
            return prepareResponse({'message' :'SUCCESS'}, 200)
         # in case of any errors
        return prepareResponse({'message' :'unable to update worklog', 'info': msg}, 500) 
    except: 
        return prepareResponse({'message' :'unable to update worklog'}, 500)       
    
# updates crop season's investments
@app.route('/api/v1/seasons/investments', methods = ['POST']) 
def api_updateInvestments():
    try : 
        # read the POST request payload
        inputJson = request.get_json(force=True) 
        app.logger.info('Info : update invetments req received. payload: ' + str(inputJson)) 
        
        # Ethereum based seasons list
        cop = ProducerOps('config.ini')
        updated, msg = cop.updateInvestments(inputJson['investment'], inputJson['seasonID'], inputJson['cropID']) 
        #if investments updated sucessfully
        if updated: 
            return prepareResponse({'message' :'SUCCESS'}, 200)
         # in case of any errors
        return prepareResponse({'message' :'unable to update invetments information', 'info': msg}, 500) 
    except: 
        return prepareResponse({'message' :'unable to update investment iformation'}, 500)       
    
'''
===============================================================================
          Main Function - starts the Flask application
===============================================================================
'''
# main function that starts the Flask application
if __name__ == '__main__':
    app.run()