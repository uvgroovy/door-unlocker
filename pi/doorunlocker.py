from servo_client import ServoClient
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Door unlocker!')
    parser.add_argument('host', type=str, help='The host to connect too')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server', default=8080, nargs='?')
    args = parser.parse_args()
    
    s = ServoClient(args.host, args.port)
    
    s.pulse(.5)


