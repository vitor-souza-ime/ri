from RobotInterface import RobotInterface 
import sys

ip = "172.15.1.80"
port = 9559
model = "NAOV6"
nao = RobotInterface(ip, port, model)  

rules = [
    ("a ball", "I can see a ball", False),    
    ("no", "Stopping the loop", True)  
]

nao.agent(rules)
nao.loop_until_keypress()
