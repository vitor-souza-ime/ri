from RobotInterface import RobotInterface 
import sys

ip = "172.15.1.80"
port = 9559
model = "NAOV6"
nao = RobotInterface(ip, port, model)  

nao.say("I will move my arm")
nao.move_arm("R", shoulder_pitch=1.0, shoulder_roll=0.2, speed=0.2)
nao.wait_s(2)

nao.say("I will move my arm, again.")
nao.move_arm("R", shoulder_pitch=0.0, shoulder_roll=0.0, elbow_yaw=0.0, elbow_roll=0.0, wrist_yaw=0.0, speed=0.2)
nao.wait_s(2)

nao.say("Introduce my self")
nao.introduce_self()
nao.wait_s(2)

nao.say("Greet person")
nao.greet_person()
nao.wait_s(2)

nao.say("A reverecence to you")
nao.bow()
nao.wait_s(2)

nao.say("I will celebrate")
nao.celebrate()
nao.wait_s(2)

nao.say("Look my emotion")
nao.express_emotion("thinking")
nao.wait_s(2)

nao.say("I will look around")
nao.look_around()
nao.wait_s(2)

nao.say("Bye, see you later")
nao.goodbye()
nao.wait_s(2)

nao.say("Press any key to quit")
nao.loop_until_keypress()



