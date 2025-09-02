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
from robot.robot_agent import *

import torch
import clip
from PIL import Image
import random
import threading
from collections import deque

# Configuração global do CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
if device:
    print("Rodando com GPU")
else:
    print("Rodando com CPU")
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

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
        self.motion = self.session.service("ALMotion")
        self.posture = self.session.service("ALRobotPosture")
        self.leds = self.session.service("ALLeds")
        self.video = self.session.service("ALVideoDevice")
        self.memory = self.session.service("ALMemory")
        self.animation_player = self.session.service("ALAnimationPlayer")        

        # Serviços avançados
        try:
            self.audio = self.session.service("ALAudioDevice")
            self.speech_rec = self.session.service("ALSpeechRecognition")
            self.sound_detection = self.session.service("ALSoundDetection")
            self.face_detection = self.session.service("ALFaceDetection")
            self.people_perception = self.session.service("ALPeoplePerception")
            self.sensors = self.session.service("ALSensors")
            self.sonar = self.session.service("ALSonar")
            #self.laser = self.session.service("ALLaser")
            self.tracker = self.session.service("ALTracker")
            self.autonomous_life = self.session.service("ALAutonomousLife")
            self.animation_player = self.session.service("ALAnimationPlayer")
            self.behavior_manager = self.session.service("ALBehaviorManager")
            self.dialog = self.session.service("ALDialog")
            #self.tablet = self.session.service("ALTabletService")
            self.navigation = self.session.service("ALNavigation")
        except Exception as e:
            print(f"Alguns serviços avançados não estão disponíveis: {e}")
            
        # Estados internos
        self.is_autonomous = False
        self.current_behavior = None
        self.face_tracking_active = False
        self.sound_localization_active = False
        self.emotion_state = "neutral"
        self.battery_level = 100
        
        # Configurações iniciais
        self.motion.wakeUp()
        self.motion.setStiffnesses("Body", 1.0)
        print("Robô configurado e pronto!")        
      
# =======================================================
# ================== MÉTODOS EXTERNOS (ORIGINAIS)
# =======================================================
RobotAgent.say = say
RobotAgent.agent = agent
RobotAgent.listen = listen
RobotAgent.move = move_head
RobotAgent.move_arm = move_arm
RobotAgent.open_hand = open_hand
RobotAgent.close_hand = close_hand
RobotAgent.go_to_posture = go_to_posture
RobotAgent.move_to = move_to
RobotAgent.show_camera = show_camera
RobotAgent.show_camera_stream = show_camera_stream
RobotAgent.test_camera_info = test_camera_info
RobotAgent.set_led = set_led
RobotAgent.off_led = off_led
RobotAgent.loop_until_keypress = loop_until_keypress
RobotAgent.wait_ms = wait_ms
RobotAgent.wait_s = wait_s
RobotAgent.wait_min = wait_min

