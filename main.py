import sys
import logging
from logging import handlers
import os, os.path

import cherrypy
from cherrypy import _cplogging
from cherrypy.lib import httputil

class Server(object):
    def __init__(self, options):
        self.base_dir = os.path.normpath(os.path.abspath(options.basedir))

        self.conf_path = os.path.join(self.base_dir, "conf")

        log_dir = os.path.join(self.base_dir, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        cherrypy.config.update(os.path.join(self.conf_path, "sever.cfg"))

        engine = cherrypy.engine

        sys.path.insert(0, self.base_dir)

        from lib.tool.db import SATool
        cherrypy.tools.db =SATool()

        from lib.tool.user import UserTool
        cherrypy.tools.user = UserTool()

        from webapp.survey import Survey
        webapp = Survey()

        app = cherrypy.tree.mount(webapp, '/' os.path.join(self,conf_path, "app.cfg"))

        self.make_rotate_logs(app)

        from lib.plugin.db import SAEnginePlugin
        engine.db = SAEnginePlugin(engine)
        engine.db.subscribe()

    def run(self)
        engine = cherrypy.engine

        if hasattr(engine, "signal_handler"):
            engine.signal_handler.subscribe()

        if hasattr(engine, "console_constrol_handler"):
            engine.console_control_hadler.subscribe()
        
        engine.start()
        #main loop of engine
        engine.block()

    def on_error(self, status, message, traceback, version):
        code = '404' if status.startswith('404') else 'error'
        return "error page"

    def make_rotate_logs(self, app):
        # see http://www.cherrypy.org/wiki/Logging#CustomHandlers
        log = app.log
        
        # Remove the default FileHandlers if present.
        log.error_file = ""
        log.access_file = ""
        
        maxBytes = getattr(log, "rot_maxBytes", 10485760)
        backupCount = getattr(log, "rot_backupCount", 5)
        
        # Make a new RotatingFileHandler for the error log.
        fname = getattr(log, "rot_error_file", "error.log")
        h = handlers.RotatingFileHandler(fname, 'a', maxBytes, backupCount)
        h.setLevel(logging.DEBUG)
        h.setFormatter(_cplogging.logfmt)
        log.error_log.addHandler(h)
        
        # Make a new RotatingFileHandler for the access log.
        fname = getattr(log, "rot_access_file", "access.log")
        h = handlers.RotatingFileHandler(fname, 'a', maxBytes, backupCount)
        h.setLevel(logging.DEBUG)
        h.setFormatter(_cplogging.logfmt)
        log.access_log.addHandler(h)
            
if __name__ == '__main__':
    from optparse import OptionParser
    
    def parse_commandline():
        curdir = os.path.normpath(os.path.abspath(os.path.curdir))
        
        parser = OptionParser()
        parser.add_option("-b", "--base-dir", dest="basedir",
                          help="Base directory in which the server "\
                          "is launched (default: %s)" % curdir)
        parser.set_defaults(basedir=curdir)
        (options, args) = parser.parse_args()

        return options

    Server(parse_commandline()).run()

