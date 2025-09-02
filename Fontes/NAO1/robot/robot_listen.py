import qi
import time

# =======================================================
# ================== listen
# =======================================================
def listen(self, duration: float = 5.0, extra_vocabulary=None) -> list:
    """
    Escuta por 'duration' segundos e retorna todas as palavras reconhecidas.
    :param duration: tempo em segundos para escuta
    :param extra_vocabulary: lista de palavras adicionais a serem reconhecidas
    :return: lista de palavras reconhecidas como strings
    """
    asr = self.session.service("ALSpeechRecognition")
    self.memory = self.session.service("ALMemory")

    # Vocabulário base
    vocabulary = ["yes", "no", "hi", "bye", "test"]

    # Adiciona vocabulário extra se fornecido
    if extra_vocabulary:
        vocabulary.extend(extra_vocabulary)

    # Para o ASR antes de configurar vocabulário
    asr.pause(True)
    asr.setVocabulary(vocabulary, False)
    asr.pause(False)

    # Limpa memória
    self.memory.insertData("WordRecognized", [])

    # Assinar o ASR
    asr.subscribe("Python_ASR")

    print(f"Escutando por {duration} segundos...")
    start_time = time.time()
    recognized_words = []

    try:
        while time.time() - start_time < duration:
            time.sleep(0.1)
            words = self.memory.getData("WordRecognized")
            if words and len(words) >= 2:
                word = words[0]
                if word not in recognized_words:
                    recognized_words.append(word)
    finally:
        asr.unsubscribe("Python_ASR")

    print(recognized_words)
    return recognized_words

# =======================================================
# ================== DETECÇÃO E RASTREAMENTO
# =======================================================

def start_face_tracking(self):
    """Inicia rastreamento de face"""
    try:
        self.face_detection.subscribe("face_tracker")
        self.tracker.registerTarget("Face", 0.1)
        self.tracker.track("Face")
        self.face_tracking_active = True
        print("Rastreamento de face iniciado")
        return True
    except Exception as e:
        print(f"Erro ao iniciar rastreamento de face: {e}")
        return False

def stop_face_tracking(self):
    """Para rastreamento de face"""
    try:
        self.tracker.stopTracker()
        self.face_detection.unsubscribe("face_tracker")
        self.face_tracking_active = False
        print("Rastreamento de face parado")
        return True
    except Exception as e:
        print(f"Erro ao parar rastreamento de face: {e}")
        return False

def detect_faces(self):
    """Detecta faces na imagem"""
    try:
        self.face_detection.subscribe("face_detection")
        time.sleep(1)
        faces = self.memory.getData("FaceDetected")
        self.face_detection.unsubscribe("face_detection")
        return faces if faces else []
    except Exception as e:
        print(f"Erro na detecção de faces: {e}")
        return []

def track_red_ball(self):
    """Rastreia uma bola vermelha"""
    try:
        self.tracker.registerTarget("RedBall", 0.06)
        self.tracker.track("RedBall")
        return True
    except Exception as e:
        print(f"Erro ao rastrear bola vermelha: {e}")
        return False


# =======================================================
# ================== SENSORES E INFORMAÇÕES
# =======================================================

def get_battery_level(self):
    """Obtém nível da bateria"""
    try:
        self.battery_level = self.memory.getData("Device/SubDeviceList/Battery/Charge/Sensor/Value")
        return self.battery_level
    except Exception as e:
        print(f"Erro ao obter nível da bateria: {e}")
        return 0

def get_temperature(self):
    """Obtém temperatura dos motores"""
    try:
        temp_head = self.memory.getData("Device/SubDeviceList/HeadYaw/Temperature/Sensor/Value")
        return temp_head
    except Exception as e:
        print(f"Erro ao obter temperatura: {e}")
        return 0

def get_touch_sensors(self):
    """Obtém estado dos sensores de toque"""
    try:
        head_touched = self.memory.getData("Device/SubDeviceList/Head/Touch/Front/Sensor/Value")
        chest_touched = self.memory.getData("Device/SubDeviceList/ChestBoard/Button/Sensor/Value")
        left_foot = self.memory.getData("Device/SubDeviceList/LFoot/Bumper/Left/Sensor/Value")
        right_foot = self.memory.getData("Device/SubDeviceList/RFoot/Bumper/Right/Sensor/Value")
        
        return {
            "head": head_touched,
            "chest": chest_touched,
            "left_foot": left_foot,
            "right_foot": right_foot
        }
    except Exception as e:
        print(f"Erro ao obter sensores de toque: {e}")
        return {}

def get_sonar_data(self):
    """Obtém dados do sonar"""
    try:
        left_sonar = self.memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        right_sonar = self.memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        return {"left": left_sonar, "right": right_sonar}
    except Exception as e:
        print(f"Erro ao obter dados do sonar: {e}")
        return {}

def is_obstacle_ahead(self, distance_threshold: float = 0.3):
    """Verifica se há obstáculo à frente"""
    sonar_data = self.get_sonar_data()
    if sonar_data:
        return (sonar_data.get("left", 1.0) < distance_threshold or 
                sonar_data.get("right", 1.0) < distance_threshold)
    return False