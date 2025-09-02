import qi
import time
import math
import sys
import select
import cv2
import numpy
from robot_say import *
from robot_listen import *
from robot_move import *
from robot_camera import *
from robot_leds import *
from robot_util import *

class RobotAgent:
    # =======================================================
    # ================== __init__
    # =======================================================
    def __init__(self, ip: str, port: int, model: str):
        self.app = qi.Application(["RobotAgentApp", f"--qi-url=tcp://{ip}:{port}"])
        self.app.start()
        self.session = self.app.session

        # Serviços básicos
        self.tts = self.session.service("ALTextToSpeech")
        #self.tts.setLanguage("Portuguese")
        self.motion = self.session.service("ALMotion")
        self.posture = self.session.service("ALRobotPosture")
        self.leds = self.session.service("ALLeds")
        self.video = self.session.service("ALVideoDevice")
        self.memory = self.session.service("ALMemory")
        
# =======================================================
# ================== métodos externos
# =======================================================

RobotAgent.say = say
RobotAgent.listen=listen
RobotAgent.move_head=move_head
RobotAgent.move_arm=move_arm
RobotAgent.open_hand=open_hand
RobotAgent.close_hand=close_hand
RobotAgent.go_to_posture=go_to_posture
RobotAgent.move_to=move_to
RobotAgent.show_camera=show_camera
RobotAgent.show_camera_stream=show_camera_stream
RobotAgent.test_camera_info=test_camera_info
RobotAgent.set_led=set_led
RobotAgent.off_led=off_led
RobotAgent.loop_until_keypress=loop_until_keypress
RobotAgent.wait_ms=wait_ms
RobotAgent.wait_s=wait_s
RobotAgent.wait_min=wait_min

