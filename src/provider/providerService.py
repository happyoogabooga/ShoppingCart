from db import get_db
from .providerRepository import providerRepository

class providerService:
    def __init__(self):
        self.providerRepository = providerRepository(get_db)

    def getProviderById(self, id):
        return self.providerRepository.getProviderById(id)
    
    def getProviderByName(self, name):
        return self.providerRepository.getProviderByName(name)
    
    def makeProvider(self, username, password, name):
        return self.providerRepository.makeProvider(username, password, name)

    def updateProvider(self, id, username, password, name):
        return self.providerRepository.updateProvider(id, username, password, name)