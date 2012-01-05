'''
Created on Aug 25, 2010

@author: jesse.j.wattenbarger@gmail.com (Jesse Wattenbarger)
'''

"""
Overrides some stuff in suds to make suds play well with app engine
"""

from google.appengine.api import memcache
import suds
from suds import client
from suds import cache
from suds import transport
from suds.reader import DefinitionsReader
from suds.client import ServiceSelector
from suds.client import Factory
from suds.transport.https import HttpAuthenticated
from suds.servicedefinition import ServiceDefinition
from suds.wsdl import Definitions
from suds.options import Options
# uncomment this for 0.4+
from suds.plugin import PluginContainer

# create a new u2open function to override the default http transport's
# u2open because the version check and subsequent usage of
# tm.setdefaulttimeout() doesn't work on app engine.
def new_u2open(self, u2request):
    """
    Open a connection.
    @param u2request: A urllib2 request.
    @type u2request: urllib2.Requet.
    @return: The opened file-like urllib2 object.
    @rtype: fp
    """
    tm = self.options.timeout
    url = self.u2opener()
    if self.u2ver() < 2.6:
        return url.open(u2request)
    else:
        return url.open(u2request, timeout=tm)

# tell transport.http.HttpTransport to use the new_u2open
transport.http.HttpTransport.u2open = new_u2open

# Override suds Client contstructor just so we can change 
# options.cache to use our own Cache implementation.
class Client(client.Client):
    def __init__(self, url, **kwargs):
        options = Options()
        options.transport = HttpAuthenticated()
        self.options = options
        options.cache = MemCache()
        self.set_options(**kwargs)
        reader = DefinitionsReader(options, Definitions)
        self.wsdl = reader.open(url)
        # uncomment this for 0.4+
#        plugins = PluginContainer(options.plugins)
#        plugins.init.initialized(wsdl=self.wsdl)
        self.factory = Factory(self.wsdl)
        self.service = ServiceSelector(self, self.wsdl.services)
        self.sd = []
        for s in self.wsdl.services:
            sd = ServiceDefinition(self.wsdl, s)
            self.sd.append(sd)
        self.messages = dict(tx=None, rx=None)

client.Client = Client

# override suds.reader.ObjectId so it has a __str__ representaiton
#class ObjectId(suds.reader.ObjectId):
#  def __str__(self):
#    return self.name + self.suffix

# set ObjectId to be the new ObjectId
#suds.reader.ObjectId = ObjectId

# create a new Cache implementation using app engines MemCache()
class MemCache(cache.Cache):
    '''
    attempt to implement a memcache cache in suds
    '''
    def __init__(self, duration=3600):
        self.duration = duration
        self.client = memcache.Client()
    
    def get(self, id):
        """
        Get a object from the cache by ID.
        @param id: The object ID.
        @type id: str
        @return: The object, else None
        @rtype: any
        """
        string_id = str(id)
        thing = self.client.get(string_id)
        return thing


    def getf(self, id):
        """
        Get a object from the cache by ID.
        @param id: The object ID.
        @type id: str
        @return: The object, else None
        @rtype: any
        """
        return self.get(id)
    
    
    def put(self, id, object):
        """
        Put a object into the cache.
        @param id: The object ID.
        @type id: str
        @param object: The object to add.
        @type object: any
        """
        string_id = str(id)
        self.client.set(string_id, object, self.duration)
    
    
    def putf(self, id, fp):
        """
        Write a fp into the cache.
        @param id: The object ID.
        @type id: str
        @param fp: File pointer.
        @type fp: file-like object.
        """
        self.put(id, fp)
    
    def purge(self, id):
        """
        Purge a object from the cache by id.
        @param id: A object ID.
        @type id: str        
        """
        self.client.delete(str(id))
    
    def clear(self):
        """
        Clear all objects from the cache.
        """
        # I know I could implement this with memcache.Client().flush_all()
        # but I didn't want to mess with App Engine's cache because I'm
        # pretty sure it's global.
        # self.client.flush_all()
        pass
