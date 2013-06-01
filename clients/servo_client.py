import json
import argparse
import urllib2
from urlparse import urljoin

class ServoClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.entryPoint = "http://%s:%s" % (host, port)
        motorsUrl = self.query("/")["motors"]["url"]
        motors = self.query(motorsUrl)
        self.motorurl = motors[0]["url"]

    def query(self, url, verb="GET", json_data = None):
        data = None
        data_content_type = None
        # Encode json data object
        if json_data is not None:
            data = json.dumps(json_data)
            data_content_type = 'text/json'

        headers = {}
        if data_content_type:
            headers['Content-Type'] = data_content_type

        # create the url
        url = urljoin(self.entryPoint, url)
        
        # prepare the request
        req = urllib2.Request(url, data, headers=headers)
        req.get_method = lambda: verb
        
        # issue the request and return the response
        resp = urllib2.urlopen(req)
        body = resp.read()
        
        if body:
            return json.loads(body)
        
    def isOn(self):
        return self.query(self.motorurl)["status"] == "on"
        
    def set_state(self, st):
        self.query(self.motorurl, "PUT", {"status":st})
        
    def pulse(self, dt):
        self.query(self.motorurl, "PUT", {"status":"on", "duration": dt})
        
    def start(self):
        self.set_state("on")
        
    def stop(self):
        self.set_state("off")
        

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('host', type=str, help='The host to connect too')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server', default=8080, nargs='?')
    parser.add_argument('state', help='The new state of the servo',  type=str)
    args = parser.parse_args()
    
    s = ServoClient(args.host, args.port)
    s.set_state(args.state)
    
