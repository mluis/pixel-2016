import cherrypy
import requests
import json
import re

class REST:

    def __init__(self, slackclient, endpoint):
        self.sc = slackclient
        self.api = endpoint
        self.cache = None
        return None

    @cherrypy.expose
    def index(self, **data):
        if len(data) > 0:
            if data is not None:
                if data['text'] is None:
                    return None

                r = requests.get(self.api);
                
                if r.status_code == 200:
                    self.cache = r.json()

                if self.cache is not None:
                    m = [x for x in self.cache['results'] if x['username_value'] == data['text']]
                    if(len(m)> 0):
                        m = m[0]
                        c = re.sub('_value', '', str(m))
                        c = re.sub('_label', '', c)
                        c = re.sub('\'', '"', c)
                        c = json.loads(c)
                        skey = sorted(c);
                        sval = [(key, c[key]) for key in skey]
                        message = "@"+data['user_name']+" :spock-hand: "+m['username_value']+ " status is "
                        l = len(sval) - 1;

                        for i in range(0,l):
                            result = ""
                            if sval[i][1] == 'Accepted':
                                result = ':white_check_mark:'
                            elif sval[i][1] == 'Rejected':
                                result = ':x:'
                            elif sval[i][1] == 'Waiting':
                                result = ':hourglass:'
                            else:
                                result = ':white_large_square:'

                            message = message + sval[i][0] + ": " + result + " "

                        self.sc.api_call(
                            "chat.postMessage",
                            channel='#'+data['channel_name'],
                            text=message,
                            username='P1X3L O\' TR0N',
                            icon_emoji=':robot_face:'
                        )
        return None
