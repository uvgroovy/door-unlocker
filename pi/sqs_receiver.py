import sys
import boto
from boto.sqs.message import Message
import servo

execfile("aws_keys.py")


motor = servo.ServoControl()

def main():
    conn = boto.sqs.connect_to_region(
         "us-west-2",
         aws_access_key_id = AWS_KEY,
         aws_secret_access_key = AWS_SECRET)
    q = conn.create_queue('frontdoor')
    q.set_attribute("MessageRetentionPeriod", 3*60)
    while True:
        rs = []
        while len(rs) == 0:
            rs = q.get_messages()
        print "got",len(rs),"messages"
        bodies = []
        for m in rs:
            body = m.get_body()
            bodies.append(body)
        q.delete_message_batch(rs)
        
        print "messages", bodies
        for body in bodies:
            processBody(body)
            
    conn.delete_queue(q)

def processBody(body):
    if body == "start":
        motor.start()
    elif body == "stop":
        motor.stop()
    elif body[:len("pulse")] == "pulse":
        p = float(body[len("pulse "):])
        print "Pulsing",p
        motor.pulse(p)


if __name__ == "__main__":
    sys.exit(main())
