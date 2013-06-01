#!/usr/bin/python

import os
import servo
import argparse
import web
import json

urls = (
    '/', 'Index',
    '/motors', 'Motors',
    '/motors/1', 'Motor',
    '/test', 'TestEngine',
)

class TestEngine:
    
    def GET(self):
        return """<html><body>
         <script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
<script>
function test() {

$.ajax({
    type: "PUT",
    url: '/motors/1',
    contentType: "application/json",
    data: '{"status":"on", "duration": 1}'
});

}
</script>
<button onclick="test()">test</button>
</body></html>"""

class Index:
    
    def GET(self):
        web.header('Content-Type', 'application/json')
        return json.dumps({"motors": {"url":"/motors"}})

class Motors:
    
    def GET(self):
        web.header('Content-Type', 'application/json')
        return json.dumps([{"url":"/motors/1"}])

#motor = servo.DummyServoControl()
motor = servo.ServoControl()

class Motor:
    
    def GET(self):
        web.header('Content-Type', 'application/json')
        return json.dumps({"status": "on" if motor.is_on() else "off"})
        
    def PUT(self):
        
        sentData = web.data()
        query = json.loads(sentData)
        if query["status"] == "on":
            if not query.get("duration", False):
                motor.start()
            else:
                dt = float(query["duration"])
                motor.pulse(dt)
        elif query["status"] == "off":
            motor.stop()
        else:
            raise Exception("No such property")
        return self.GET()

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('--port', dest="port", type=int, help='Listening port for HTTP Server', default=8080)
    parser.add_argument('--pidfile', dest="pidfile", help='Write the pid to the specified file',  type=argparse.FileType('w'))
    args = parser.parse_args()
    
    if args.pidfile:
        with args.pidfile:
            args.pidfile.write("%s"%os.getpid())

    try:
        # http://stackoverflow.com/questions/14444913/web-py-specify-address-and-port
        app = MyApplication(urls, globals())
        app.run(port=args.port)
    finally:
        if args.pidfile:
            os.unlink(args.pidfile)
