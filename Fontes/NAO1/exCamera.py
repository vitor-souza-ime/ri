from RobotInterface import RobotInterface 
import sys

ip = "172.15.1.80"
port = 9559
model = "NAOV6"
nao = RobotInterface(ip, port, model)  

nao.test_camera_info()
nao.show_camera("top")
nao.show_camera_stream("top", 10)


