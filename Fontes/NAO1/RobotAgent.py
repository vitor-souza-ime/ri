import qi

class RobotAgent:
    def __init__(self, ip: str, port: int, model: str):
        self.app = qi.Application(["RobotAgentApp", f"--qi-url=tcp://{ip}:{port}"])
        self.app.start()
        self.session = self.app.session
        self.tts = self.session.service("ALTextToSpeech")

    def say(self, text: str):
        self.tts.say(text)
    
    
