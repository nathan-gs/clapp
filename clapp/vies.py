#from suds.client import Client

from suds_memcache import Client
from clapp.entity import InvalidVatError

class ViesRepository:
    def __init__(self):
        url = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
        self.client = Client(url, cache=None)
        
    def lookup(self, countryCode, vat):
        viesR = self.client.service.checkVat(countryCode=countryCode, vatNumber=vat)
        
        if viesR.valid == False:
            raise InvalidVatError(countryCode, vat)
            
        return viesR
    
    
