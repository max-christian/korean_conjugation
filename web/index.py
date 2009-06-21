# -*- coding: utf-8 -*-
import sys
import os
import traceback
sys.stdout = sys.stderr
sys.path.append(os.path.realpath(__file__ + '/../../src'))
from jinja2 import Environment, FileSystemLoader
import urllib

import atexit
import threading
import cherrypy
import korean_conjugator
from datetime import datetime

env = Environment(loader=FileSystemLoader(os.path.realpath(__file__ + '/../../templates')))

class Root(object):
    favicon_ico = cherrypy.tools.staticfile.handler(os.path.realpath(__file__ + '/../favicon.ico'))

    @cherrypy.expose
    def index(self, infinitive='하다', regular=False):
        cherrypy.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        try:
            infinitive = infinitive.decode('utf-8')
        except:
            pass
        results = korean_conjugator.conjugation.perform(infinitive, 
                                                        regular=regular)

        samples = ', '.join(map(lambda verb: '<a href="/?%(urlencoded)s">%(verb)s</a>' \
           % {'urlencoded': urllib.urlencode({'infinitive': verb.encode('utf-8')}), 
              'verb': verb},
           [u'살다', u'오다', u'걷다', u'짓다', u'돕다', 
            u'번거롭다', u'푸르다', u'오르다']))
        template = env.get_template('index.html')
        return template.render(year=datetime.now().year,
                               results=results,
                               samples=samples,
                               infinitive=infinitive,
                               regular=regular
                              ).encode('utf-8')

    
def setup_server():
    cherrypy.config.update({'environment': 'production',
                            'log.screen': False,
                            'show_tracebacks': False})
    cherrypy.tree.mount(Root())
    cherrypy.tree.mount(Root(), '/index.py')

def dev_server():
    cherrypy.config.update({'server.socket_port': 8888})
    cherrypy.quickstart(Root())
