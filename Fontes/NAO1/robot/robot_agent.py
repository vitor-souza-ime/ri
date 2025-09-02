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