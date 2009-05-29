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

env = Environment(loader=FileSystemLoader(os.path.realpath(__file__ + '/../../templates')))

class Root(object):
    favicon_ico = cherrypy.tools.staticfile.handler(os.path.realpath(__file__) + '/../favicon.ico')

    @cherrypy.expose
    def index(self, infinitive='하다', regular=False):
        cherrypy.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        try:
            try:
                infinitive = infinitive.decode('utf-8')
            except:
                pass
            results = korean_conjugator.conjugation.perform(infinitive, 
                                                            regular=regular)
            template = env.get_template('index.html')
            return template.render(results=results,
                                   infinitive=infinitive,
                                   regular=regular
                                  ).encode('utf-8')
        except Exception, e:
            return traceback.format_exception(*sys.exc_info())

    
def setup_server():
    cherrypy.config.update({'environment': 'production',
                            'log.screen': False,
                            'show_tracebacks': False})
    cherrypy.tree.mount(Root())
    cherrypy.tree.mount(Root(), '/index.py')
