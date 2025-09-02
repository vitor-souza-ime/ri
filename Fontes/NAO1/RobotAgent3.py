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

import torch
import clip
from PIL import Image

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
        #self.tts.setLanguage("Portuguese")
        self.motion = self.session.service("ALMotion")
        self.posture = self.session.service("ALRobotPosture")
        self.leds = self.session.service("ALLeds")
        self.video = self.session.service("ALVideoDevice")
        self.memory = self.session.service("ALMemory")

    # =======================================================
    # ================== captura de frame
    # =======================================================
    def get_camera_frame(self, camera_name: str = "top"):
        if camera_name == "top":
            camera_index = 0
        elif camera_name == "bottom":
            camera_index = 1
        else:
            print("Escolha 'top' ou 'bottom'")
            return None

        resolution = 1      # 320x240
        color_space = 11    # RGB
        fps = 15
        name_id = None

        try:
            name_id = self.video.subscribeCamera("clip_frame", camera_index, resolution, color_space, fps)
            time.sleep(0.3)  # aguarda estabilização
            image = self.video.getImageRemote(name_id)
            self.video.unsubscribe(name_id)

            if image is None or len(image) < 7:
                return None

            width, height, channels = image[0], image[1], image[2]
            array = numpy.frombuffer(image[6], dtype=numpy.uint8).reshape((height, width, channels))
            array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
            return array

        except Exception as e:
            print("Erro ao capturar frame:", e)
            if name_id is not None:
                try:
                    self.video.unsubscribe(name_id)
                except:
                    pass
            return None

    # =======================================================
    # ================== detecção de pessoa
    # =======================================================
    def is_person_in_room(self, camera_name: str = "top") -> bool:
        image_array = self.get_camera_frame(camera_name)
        if image_array is None:
            print("Erro ao capturar a imagem")
            return False

        image = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
        image_input = clip_preprocess(image).unsqueeze(0).to(device)
        text_inputs = clip.tokenize(["a person", "no person"]).to(device)

        with torch.no_grad():
            image_features = clip_model.encode_image(image_input)
            text_features = clip_model.encode_text(text_inputs)
            similarity = (image_features @ text_features.T).softmax(dim=-1)
            values, indices = similarity[0].topk(1)
            return indices.item() == 0  # True se "a person" for o mais similar
        
    def is_object_in_frame(self, object_name: str, camera_name: str = "top") -> bool:
        """
        Verifica se o objeto especificado está presente na imagem capturada.
        :param object_name: string descrevendo o objeto (ex: "a person")
        :param camera_name: "top" ou "bottom"
        :return: True se o objeto for detectado, False caso contrário
        """
        image_array = self.get_camera_frame(camera_name)
        if image_array is None:
            print("Erro ao capturar a imagem")
            return False

        image = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
        image_input = clip_preprocess(image).unsqueeze(0).to(device)

        # Cria inputs de texto comparativos
        text_inputs = clip.tokenize([object_name, f"no {object_name}"]).to(device)

        with torch.no_grad():
            image_features = clip_model.encode_image(image_input)
            text_features = clip_model.encode_text(text_inputs)
            similarity = (image_features @ text_features.T).softmax(dim=-1)
            values, indices = similarity[0].topk(1)
            return indices.item() == 0  # True se object_name for o mais similar
        
    def agent(self, rules: list, listen_duration: float = 3.0, camera_name: str = "top"):
        """
        Agente simplificado: passa lista de pares (detecção, frase).
        :param rules: lista de tuplas (string_condicao, string_frase)
                    string_condicao: nome do objeto ou palavra
                    string_frase: frase que o robô fala
        :param listen_duration: tempo em segundos para escuta
        :param camera_name: câmera para verificações
        """
        print("Agente simplificado iniciado. Pressione Ctrl+C para encerrar.")
        try:
             
            while True:
                words = self.listen(listen_duration)

                for cond, phrase, stop_flag in rules:
                    detected = False
                    # Verifica áudio
                    if cond in words:
                        detected = True
                    # Verifica câmera
                    elif self.is_object_in_frame(cond, camera_name):
                        if not stop_flag:
                            detected = True

                    if detected:
                        self.say(phrase)
                        if stop_flag:
                            print("Encerrando o agente.")
                            return
        except KeyboardInterrupt:
            print("Agente finalizado pelo usuário.")


# =======================================================
# ================== métodos externos
# =======================================================
RobotAgent.say = say
RobotAgent.listen = listen
RobotAgent.move_head = move_head
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
