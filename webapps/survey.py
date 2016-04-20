import cgi

import cherrypy


__all__ = ['Survey']

class Survey(object):
  def __init__(self):
      self.login = Login()

  @cherrypy.expose
  @cherrypy.tools.user()
  def index(self):
    pass

  @cherrypy.expose
  def logout(self):
    cherrypy.lib.sessions.expire()
  
  @cherrypy.expose
  @cherrypy.tools.json_out()
  def mentions(self):


