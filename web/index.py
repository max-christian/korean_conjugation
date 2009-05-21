# -*- coding: utf-8 -*-
import sys
import os
import traceback
sys.stdout = sys.stderr
sys.path.append(os.path.realpath(__file__ + '/../../src'))

import atexit
import threading
import cherrypy
import korean_conjugator

cherrypy.config.update({'environment': 'embedded'})

if cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

class Root(object):
    @cherrypy.expose
    def index(self, infinitive='하다'):
        cherrypy.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        try:
            infinitive = infinitive.decode('utf-8')
            results = []
            for x, y, z in korean_conjugator.conjugation.perform(infinitive):
                results.append(x.replace('_', ' ') + ': ' + y + '[' + ' '.join(z) + ']')
            return '<form method="get" action="."><input name="infinitive"></form>' + ('<br>'.join(results)).encode('utf-8')
        except Exception, e:
            return traceback.format_exception(*sys.exc_info())

    
application = cherrypy.Application(Root(), None)
