import pika # interface with rabbit
import math # calculate trading partners max visists
import time # benchmarking, waiting
import os # get env variables 

from ast import literal_eval as make_tuple # because why remake deserailizign tuples
s = int(os.environ['self'])
c = int(os.environ['count'])
time.sleep(10)
def run_worker(s,c):
  print("Worker", s, "has started")
  t0 = time.time()
  id = s
  val = id
  #needs to wait for rabbitmq to start

  future = {}
  partner = id ^ ( 1 << 0)
  connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
  channel = connection.channel()
  channel.queue_declare(queue=str(id))

  for i in range(int(math.log2(c))):
    # send current val 
    partner = id ^ ( 1 << i)
    channel.queue_declare(queue=str(partner))
    channel.basic_publish(exchange='', routing_key=str(partner), body=str((id,val)))
    # get trade val 
    print("sent:", str(val), "to", str(partner))
    body = None
    while future.get(partner, -1) == -1:
      method_frame, header_frame, body = channel.basic_get(str(id), auto_ack=TRUE)
      if body != None:
        temp = make_tuple(body.decode())
        temp = (int(temp[0]), int(temp[1]))
        future[temp[0]] = temp[1]
    val += future[partner]
    future.pop(partner)
  t1 = time.time()
  print(val, t1-t0)
  connection.close()
run_worker(s,c)