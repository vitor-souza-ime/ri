import qi

# =======================================================
# ================== say
# =======================================================
def say(self, text: str):
        #asr = self.session.service("ALSpeechRecognition")   
        #asr.pause(True) 
        self.tts.say(text)
        #asr.pause(False) 

# =======================================================
# ================== CONTROLE DE VOZ E ÁUDIO AVANÇADO
# =======================================================

def set_voice_parameters(self, pitch: float = 100.0, speed: float = 100.0, volume: float = 100.0):
#Configura parâmetros da voz
        try:
                self.tts.setParameter("pitchShift", pitch)
                self.tts.setParameter("speed", speed)
                self.tts.setParameter("volume", volume)
                return True
        except Exception as e:
                print(f"Erro ao configurar voz: {e}")
                return False

def whisper(self, text: str):
        """Fala sussurrando"""
        original_volume = self.tts.getParameter("volume")
        self.tts.setParameter("volume", 30)  # bem mais baixo
        self.tts.setParameter("pitchShift", 0.9)  # opcional
        self.say(text)
        self.tts.setParameter("volume", original_volume)

def shout(self, text: str):
        """Fala gritando"""
        original_volume = self.tts.getParameter("volume")
        self.tts.setParameter("volume", 90)  # quase máximo
        self.tts.setParameter("speed", 110)  # opcional
        self.say(text)
        self.tts.setParameter("volume", original_volume)


def robot_voice(self, text: str):
        """Fala com voz robótica"""
        self.set_voice_parameters(pitch=50.0, speed=80.0)
        self.say(text)
        self.set_voice_parameters(pitch=100.0, speed=100.0)

def play_sound_effect(self, effect: str):
        """Reproduz efeitos sonoros"""
        effects = {
                "beep": "\\pau=200\\ \\rspd=80\\ beep beep",
                "robot": "\\pau=200\\ \\rspd=60\\ \\vct=92\\ robot sound",
                "happy": "\\pau=100\\ \\rspd=120\\ yay!",
                "sad": "\\pau=300\\ \\rspd=60\\ oh no...",
                "thinking": "\\pau=200\\ hmm..."
        }

        sound = effects.get(effect, effect)
        self.say(sound)        