import webapp2
import jinja2
import os
import sys
import clapp.bootstrap

from google.appengine.api import users
from clapp.vies import ViesRepository




jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    #if user:    
    #  template = jinja_environment.get_template('view/index.html')
    #  self.response.out.write(template.render({
    #    'user': user
    #  }))
    #else:
    #  self.redirect(users.create_login_url(self.request.uri))
    
    countryCode = 'BE'
    vat = '0888048856'
    countryCode = self.request.get('countryCode')
    vat = self.request.get('vat')
    
    
    vies = ViesRepository()
    r = vies.lookup(countryCode, vat)
    self.response.out.write(r.name)
    
class TestPage(webapp2.RequestHandler):
  def get(self):
    
    self.response.out.write(self.request)

app = webapp2.WSGIApplication([('/', MainPage), ('/test', TestPage)],
                              debug=True)

