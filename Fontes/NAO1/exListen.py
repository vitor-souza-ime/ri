from RobotInterface import RobotInterface 
import sys

ip = "172.15.1.80"
port = 9559
model = "NAOV6"
nao = RobotInterface(ip, port, model)  

nao.say("Say no to stop process!")

while True:    
    extras = ["robot", "ball", "stop"]
    words = nao.listen(3, extra_vocabulary=extras)
    print("O NAO reconheceu:", words)

    if "no" in words:
        nao.say("Stopping the loop")
        break       # Sai do loop

nao.shutdown()
