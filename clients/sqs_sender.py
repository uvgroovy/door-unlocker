import boto
from boto.sqs.message import Message

execfile("aws_keys.py")

conn = boto.sqs.connect_to_region(
     "us-west-2",
     aws_access_key_id = AWS_KEY,
     aws_secret_access_key = AWS_SECRET)
q = conn.create_queue('frontdoor')

while True:
    i = raw_input()
    if not i:
        i = 'pulse 1'
    m = Message()
    m.set_body(i)
    status = q.write(m)

