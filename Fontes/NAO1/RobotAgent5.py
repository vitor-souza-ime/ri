import qi
import torch
import clip
import pkgutil
import importlib
import inspect

# ===== Carregar CLIP =====
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Rodando com GPU" if device == "cuda" else "Rodando com CPU")
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)


class RobotAgent:
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

        print("Robô configurado e pronto!")


# ===== Importar dinamicamente todos os módulos "robot_*" =====
import robot

for loader, module_name, is_pkg in pkgutil.iter_modules(robot.__path__):
    if module_name.startswith("robot_"):
        module = importlib.import_module(f"robot.{module_name}")
        for name, func in inspect.getmembers(module, inspect.isfunction):
            setattr(RobotAgent, name, func)

