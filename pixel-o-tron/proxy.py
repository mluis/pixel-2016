#!/usr/bin/env python3
import configparser

# GLOBAL VARIABLES
SERVER_CONF = 'conf/bot.conf'
#.
# CONFIGURATION BEHAVIOUR
config = configparser.ConfigParser()
config.read(SERVER_CONF)

HOST = config['HTTP']['HOST']
assert HOST is not None

PORT = int(config['HTTP']['PORT'])
assert PORT is not None

ENDPOINT = config['API']['ENDPOINT']
assert ENDPOINT is not None

TOKEN = config['SLACK']['TOKEN']
assert TOKEN is not None
# found at https://api.slack.com/web#authentication
from slackclient import SlackClient
sc = SlackClient(TOKEN)

if not sc.api_call("api.test")['ok']:
    import sys
    sys.exit('API (token?) is not ok.')

if __name__ == '__main__':
    import cherrypy
    from libs.rest import REST

    routing = {
        '/': {
            'tools.sessions.on': True,
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf-8',
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }
    }

    webapp = REST(sc, ENDPOINT)
    # webapp.auth = webapp.auth(webapp)

    cherrypy.tree.mount(webapp, '/', routing)

    server_config = {
        'server.socket_host': HOST,
        'server.socket_port': PORT,
        'tools.encode.on': True,
        'tools.encode.encoding': 'UTF-8',
        'tools.sessions.on': True,
        'tools.sessions.timeout': 60
    }

    cherrypy.config.update(server_config)
    cherrypy.engine.start()
