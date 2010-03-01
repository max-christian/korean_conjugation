# -*- coding: utf-8 -*-
import sys
import os
import traceback
sys.stdout = sys.stderr
sys.path.append(os.path.realpath(__file__ + '/../../../'))
from jinja2 import Environment, FileSystemLoader
import urllib

import atexit
import threading
import cherrypy
import korean.conjugator
import korean.hangeul
from datetime import datetime
import simplejson

env = Environment(loader=FileSystemLoader(os.path.realpath(__file__ + '/../../templates')))

class Root(object):
    favicon_ico = cherrypy.tools.staticfile.handler(os.path.realpath(__file__ + '/../favicon.ico'))

    @cherrypy.expose
    def index(self, infinitive='하다', regular=False, json=False, **everything_else):
        cherrypy.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        try:
            infinitive = infinitive.decode('utf-8')
        except:
            pass
        infinitive = korean.conjugator.base(infinitive) + u'다'
        results = korean.conjugator.conjugation.perform(infinitive, 
                                                        regular=regular)

        if json:
            return simplejson.dumps([[],[],[],[u'', u'<a href="http://dongsa.net?infinitive=' + infinitive + '">Click to conjugate!</a>', u'', u''], ensure_ascii=False).encode('utf-8')
        
        template = env.get_template('index.html')
        both_regular_and_irregular = infinitive[:-1] in \
                                     korean.conjugator.both_regular_and_irregular
        not_korean = not all((korean.hangeul.is_hangeul(x) or x == ' '
                              for x in infinitive))
        verb_type = korean.conjugator.verb_type(infinitive[:-1])
        return template.render(year=datetime.now().year,
                               results=results,
                               infinitive=infinitive,
                               regular=regular,
                               not_korean=not_korean,
                               verb_type=verb_type,
                               both_regular_and_irregular=both_regular_and_irregular
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
