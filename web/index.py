# -*- coding: utf-8 -*-
import sys
import os
import traceback
sys.stdout = sys.stderr
sys.path.append(os.path.realpath(__file__ + '/../../src'))
from jinja2 import Environment, FileSystemLoader

import atexit
import threading
import cherrypy
import korean_conjugator

cherrypy.config.update({'environment': 'embedded'})
env = Environment(loader=FileSystemLoader(os.path.realpath(__file__ + '/../../templates')))

if cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

class Root(object):
    @cherrypy.expose
    def index(self, infinitive='하다'):
        cherrypy.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        try:
            try:
                infinitive = infinitive.decode('utf-8')
            except:
                pass
            template = env.get_template('index.html')
            return template.render(results=korean_conjugator.conjugation.perform(infinitive)).encode('utf-8')
        except Exception, e:
            return traceback.format_exception(*sys.exc_info())

    
application = cherrypy.Application(Root(), None)
