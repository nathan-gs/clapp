import unittest
import clapp.bootstrap

from clapp.vies import ViesRepository, InvalidVatError


class TestViesRepository(unittest.TestCase):
    
    def setUp(self):
        self.client = ViesRepository()
        
        
    def testExistingVat(self):
        viesR = self.client.lookup(countryCode='BE', vat='0888048856')
        
        self.assertEqual('BVBA SERVS', viesR.name)
        
    def testIncorrectVat(self):
        with self.assertRaises(InvalidVatError):
        
            r = self.client.lookup(countryCode='BE', vat='0000')
        
