import clapp.bootstrap
from clapp.entity import Vat, InvalidVatError

import unittest

class TestVat(unittest.TestCase):
    
    def test_country_code_from_vat(self):
        vat = Vat('BE0888048856')
        
        self.assertEquals('BE', vat.country_code)
        
        
    
    def test_country_code_from_argument(self):
        vat = Vat('BE0888048856', 'BE')
        
        self.assertEquals('BE', vat.country_code)
        
        vat = Vat('0888048856', 'BE')
        
        self.assertEquals('BE', vat.country_code)
