import qi
import time
import math
import sys
import select
import cv2
import numpy as np
import torch
import clip
import pkgutil
import importlib
import inspect
from PIL import Image

class RobotInterface:
    def __init__(self, ip: str, port: int, model: str):
        self.app = qi.Application(["RobotAgentApp", f"--qi-url=tcp://{ip}:{port}"])
        self.app.start()
        self.session = self.app.session

        self.tts = self.session.service("ALTextToSpeech")
        self.motion = self.session.service("ALMotion")
        self.posture = self.session.service("ALRobotPosture")
        self.leds = self.session.service("ALLeds")
        self.video = self.session.service("ALVideoDevice")
        self.memory = self.session.service("ALMemory")
        self.animation_player = self.session.service("ALAnimationPlayer")

        # ===== Carregar CLIP antes de importar dinamicamente outros módulos =====
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print("Rodando com GPU" if self.device == "cuda" else "Rodando com CPU")
        self.clip_module = clip
        self.clip_model, self.clip_preprocess = clip.load("ViT-B/32", device=self.device)

        print("Robô configurado e pronto!")

    def agent(self, rules: list, listen_duration: float = 3.0, camera_name: str = "top"):
        """
        Agente simplificado: passa lista de pares (detecção, frase).
        :param rules: lista de tuplas (string_condicao, string_frase, stop_flag)
                    string_condicao: nome do objeto ou palavra
                    string_frase: frase que o robô fala
                    stop_flag: se True, para o agente após executar
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

# ===== Importar dinamicamente todos os módulos "robot_*" =====
import robot
for loader, module_name, is_pkg in pkgutil.iter_modules(robot.__path__):
    if module_name.startswith("robot_"):
        module = importlib.import_module(f"robot.{module_name}")
        for name, func in inspect.getmembers(module, inspect.isfunction):
            setattr(RobotInterface, name, func)

# ===== Exemplo de uso =====
if __name__ == "__main__":
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
