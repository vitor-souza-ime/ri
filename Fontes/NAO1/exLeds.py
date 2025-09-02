from RobotInterface import RobotInterface 
import sys
import time
import psutil
import os
process = psutil.Process(os.getpid())

t0=time.time()

ip = "172.15.1.80"
port = 9559
model = "NAOV6"
nao = RobotInterface(ip, port, model)  

print(time.time()-t0)
print(f"Memória usada: {process.memory_info().rss / 1024 ** 2:.2f} MB")

nao.set_led("FaceLeds","red",0)
nao.wait_s(3)
nao.set_led("ChestLeds","blue",0)
nao.wait_s(3)
nao.set_led("EarLeds","blue",0)
nao.wait_s(3)
nao.set_led("FeetLeds","blue",0)


nao.loop_until_keypress()

