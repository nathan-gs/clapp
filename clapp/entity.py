import re

class Company:
    
     def __init__(self, vat, name = None, address = None, links = []):
        self.vat = vat
        self.name = name
        self.address = address
        self.links = links
    

        
class Vat:
     REGEX = {
          'BE' : '/^0?[0-9]{*}$/'
     }
     
     def __init__(self, number, country_code=None):
          self.number = number
          self._country_code = country_code
        
     def get_country_code(self):
          if self._country_code == None:
               self._country_code = self.number[0:2]
          
          return self._country_code
     
     country_code = property(get_country_code)

     def valid(self):
          if len(self.country_code) != 2:
               return False
          if self.REGEX.has_key(self.country_code):
               if re.match(self.REGEX[self.country_code], self.number) != None:
                    return True
          return False


class InvalidVatError(Exception):
    
    def __init__(self, countryCode, vat):
        self.countryCode = countryCode
        self.vat = vat