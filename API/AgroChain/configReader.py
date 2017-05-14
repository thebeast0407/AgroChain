from ConfigParser import SafeConfigParser

class ConfReader :  
    parser = None
    
    # Constructor
    def __init__(self, confFile):
        self.parser = SafeConfigParser()
        self.parser.read(confFile) 
    
    #Reads the configuration values for the specified key
    def GetConfigValue(self, group, key):
        return self.parser.get(group,key)
    
''' smoke test
confReader = ConfReader('config.ini')
print confReader.GetConfigValue('blockchain','rpcPersonalServer')
'''