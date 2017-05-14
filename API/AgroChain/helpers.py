import hashlib
import uuid 
from configReader import ConfReader

#generates the hash for any given string
def getHash(inputText):    
    # configure Reader
    confReader = ConfReader('config.ini') 
    # Random string used for hashing whch makes brute force even more tougher 
    secretKey = confReader.GetConfigValue('security','hashSalt') 
    #get the algo object
    sha256 = hashlib.sha256()      
    # Get string and put into givenString. 
    sha256.update(inputText + secretKey)    
    #return the hash from algo object
    return sha256.hexdigest()


#generates randdom UUID everytimg
def getUUID():
    return uuid.uuid4();

#function for converting str to boolean... Especially True and False strings to thier correaspanding boolean values
def str2Bool(self, inputStr):
    if inputStr == 'True':
         return True
    elif inputStr == 'False':
         return False
    else:
         raise ValueError # evil ValueError that doesn't tell you what the wrong value was

#print getHash('Dinesh')