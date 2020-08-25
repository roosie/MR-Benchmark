import redis # interface with rabbit
import math # calculate trading partners max visists
import time # benchmarking, waiting
import os # get env variables 
from ast import literal_eval as make_tuple # because why remake deserailizign tuples
id = int(os.environ['self'])
c = int(os.environ['count'])
time.sleep(5)
print("Worker", id, "has started")
t0 = time.time()
val = id
cache = redis.Redis(host='redis', port=6379)
future = {}

for i in range(int(math.log2(c))):
  partner = id ^ ( 1 << i)
  cache.lpush(str(partner), str((id,val)))
  print("sent:", str(val), "to", str(partner))
  while future.get(partner, -1) == -1:
    while(cache.llen(str(id))!=0):
      temp = make_tuple(cache.lpop(str(id)).decode())
      temp = (int(temp[0]), int(temp[1]))
      future[temp[0]] = temp[1]
  val += future[partner]
  future.pop(partner)
t1 = time.time()

print(val, t1-t0)