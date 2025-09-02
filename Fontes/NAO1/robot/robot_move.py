import qi

# =======================================================
# ================== move_head
# =======================================================
def move_head(self, yaw: float = 0.0, pitch: float = 0.0, speed: float = 0.2):
    """
    Gira a cabeça do NAO.
    :param yaw: rotação horizontal em radianos (-2.0 a 2.0)
    :param pitch: rotação vertical em radianos (-0.5 a 0.5)
    :param speed: velocidade da movimentação (0.0 a 1.0)
    """
    # Ativa rigidez da cabeça
    self.motion.setStiffnesses("Head", 1.0)

    # Movimenta articulações individualmente com velocidade
    self.motion.angleInterpolationWithSpeed("HeadYaw", yaw, speed)
    self.motion.angleInterpolationWithSpeed("HeadPitch", pitch, speed)

# =======================================================
# ================== move_arm
# =======================================================
def move_arm(self, side: str = "R", shoulder_pitch: float = 0.0, shoulder_roll: float = 0.0,
            elbow_yaw: float = 0.0, elbow_roll: float = 0.0, wrist_yaw: float = 0.0, speed: float = 0.2):
    """
    Movimenta o braço direito ou esquerdo.
    :param side: 'R' para direito, 'L' para esquerdo
    :param speed: velocidade do movimento (0.0 a 1.0)
    """
    # Ativa rigidez do braço
    self.motion.setStiffnesses(f"{side}Arm", 1.0)

    # Movimenta articulações individualmente
    self.motion.angleInterpolationWithSpeed(f"{side}ShoulderPitch", shoulder_pitch, speed)
    self.motion.angleInterpolationWithSpeed(f"{side}ShoulderRoll", shoulder_roll, speed)
    self.motion.angleInterpolationWithSpeed(f"{side}ElbowYaw", elbow_yaw, speed)
    self.motion.angleInterpolationWithSpeed(f"{side}ElbowRoll", elbow_roll, speed)
    self.motion.angleInterpolationWithSpeed(f"{side}WristYaw", wrist_yaw, speed)

# =======================================================
# ================== open_hand
# =======================================================
def open_hand(self, side: str = "R"):
    joint = f"{side}Hand"
    self.motion.angleInterpolation(joint, 1.0, 0.5, True)

# =======================================================
# ================== close_hand
# =======================================================
def close_hand(self, side: str = "R"):
    joint = f"{side}Hand"
    self.motion.angleInterpolation(joint, 0.0, 0.5, True)

# =======================================================
# ================== go_to_posture
# =======================================================
def go_to_posture(self, posture_name: str = "Stand", speed: float = 0.5):
    """
    Faz o NAO assumir uma postura.
    Ex.: "StandInit", "Stand", "Sit", "Crouch"
    """
    self.posture.goToPosture(posture_name, speed)

# =======================================================
# ================== move_to
# =======================================================
def move_to(self, x: float, y: float, theta: float):
    """
    Move o robô no plano XY.
    :param x: distância em metros
    :param y: distância lateral em metros
    :param theta: ângulo de rotação em radianos
    """
    self.motion.moveTo(x, y, theta)

# =======================================================
# ================== CONTROLE DE MOVIMENTO AVANÇADO
# =======================================================

def walk_to(self, x: float, y: float, theta: float = 0.0, speed: float = 0.5):
    """Move o robô para uma posição específica"""
    try:
        self.motion.moveTo(x, y, theta)
        return True
    except Exception as e:
        print(f"Erro ao mover para posição: {e}")
        return False

def walk_forward(self, distance: float, speed: float = 0.5):
    """Caminha para frente uma distância específica"""
    return self.walk_to(distance, 0.0, 0.0)

def walk_backward(self, distance: float, speed: float = 0.5):
    """Caminha para trás uma distância específica"""
    return self.walk_to(-distance, 0.0, 0.0)

def turn_left(self, angle: float = 45.0, speed: float = 0.5):
    """Gira para a esquerda em graus"""
    angle_rad = math.radians(angle)
    return self.walk_to(0.0, 0.0, angle_rad)

def turn_right(self, angle: float = 45.0, speed: float = 0.5):
    """Gira para a direita em graus"""
    angle_rad = math.radians(-angle)
    return self.walk_to(0.0, 0.0, angle_rad)

def strafe_left(self, distance: float, speed: float = 0.5):
    """Move lateralmente para a esquerda"""
    return self.walk_to(0.0, distance, 0.0)

def strafe_right(self, distance: float, speed: float = 0.5):
    """Move lateralmente para a direita"""
    return self.walk_to(0.0, -distance, 0.0)

def stop_walking(self):
    """Para o movimento atual"""
    try:
        self.motion.stopMove()
        return True
    except Exception as e:
        print(f"Erro ao parar movimento: {e}")
        return False

def set_walk_velocity(self, x: float, y: float, theta: float):
    """Define velocidade de caminhada contínua"""
    try:
        self.motion.move(x, y, theta)
        return True
    except Exception as e:
        print(f"Erro ao definir velocidade: {e}")
        return False
"""
def dance(self, dance_name: str = "random"):
    
    dances = [
        "animations/Stand/Gestures/Enthusiastic_4",
        "animations/Stand/Gestures/Dance_1",
        "animations/Stand/Gestures/Dance_2",
        "animations/Stand/Emotions/Positive/Excited_1"
    ]
    
    if dance_name == "random":
        dance = random.choice(dances)
    else:
        dance = dance_name
        
    try:
        self.animation_player.run(dance)
        return True
    except Exception as e:
        print(f"Erro ao executar dança: {e}")
        return False
"""
# =======================================================
# ================== CONTROLE DE POSTURA AVANÇADO
# =======================================================

def crouch(self):
    """Agacha o robô"""
    return self.go_to_posture("Crouch", 1.0)

def sit_down(self):
    """Senta o robô"""
    return self.go_to_posture("Sit", 1.0)

def sit_relax(self):
    """Posição sentada relaxada"""
    return self.go_to_posture("SitRelax", 1.0)

def lie_down_belly(self):
    """Deita de barriga para baixo"""
    return self.go_to_posture("LyingBelly", 1.0)

def lie_down_back(self):
    """Deita de costas"""
    return self.go_to_posture("LyingBack", 0.5)

def stand_up(self):
    """Levanta o robô"""
    return self.go_to_posture("Stand", 0.5)

def stand_init(self):
    """Posição inicial em pé"""
    return self.go_to_posture("StandInit", 1.0)

def stand_zero(self):
    """Posição zero em pé"""
    return self.go_to_posture("StandZero", 1.0)

# =======================================================
# ================== CONTROLE DE BRAÇOS E MÃOS AVANÇADO
# =======================================================


def wave_hand(self, hand: str = "right"):
    #Acena com a mão
    animations = {
        "right": "animations/Stand/Gestures/Hey_1",
        "left": "animations/Stand/Gestures/Hey_6",
        "both": "animations/Stand/Gestures/Hey_3"
    }
    
    try:
        self.animation_player.run(animations.get(hand, animations["right"]))
        return True
    except Exception as e:
        print(f"Erro ao acenar: {e}")
        return False

def point_at(self, direction: str):
    #Aponta em uma direção
    animations = {
        "front": "animations/Stand/Gestures/You_1",
        "left": "animations/Stand/Gestures/Far_1",
        "right": "animations/Stand/Gestures/Far_2"
    }
    
    try:
        self.animation_player.run(animations.get(direction, animations["front"]))
        return True
    except Exception as e:
        print(f"Erro ao apontar: {e}")
        return False

def applaud(self, duration: float = 3.0):
    #Bate palmas
    try:
        self.animation_player.run("animations/Stand/Gestures/Applause_1")
        return True
    except Exception as e:
        print(f"Erro ao bater palmas: {e}")
        return False

def show_tablet(self):
    #Mostra o tablet (se disponível)
    try:
        self.animation_player.run("animations/Stand/Gestures/ShowTablet_1")
        return True
    except Exception as e:
        print(f"Erro ao mostrar tablet: {e}")
        return False

def give_object(self, hand: str = "right"):
    #Gesto de entregar objeto
    try:
        animation = "animations/Stand/Gestures/Give_1" if hand == "right" else "animations/Stand/Gestures/Give_2"
        self.animation_player.run(animation)
        return True
    except Exception as e:
        print(f"Erro ao dar objeto: {e}")
        return False

def receive_object(self, hand: str = "right"):
    #Gesto de receber objeto
    try:
        self.open_hand(hand)
        self.move_arm(hand, 0.0, 0.0, -45.0, 90.0)
        return True
    except Exception as e:
        print(f"Erro ao receber objeto: {e}")
        return False

# =======================================================
# ================== CONTROLE DE CABEÇA AVANÇADO
# =======================================================

def nod_yes(self, intensity: float = 1.0):
    """Balança a cabeça afirmativamente"""
    try:
        self.animation_player.run("animations/Stand/Gestures/Yes_1")
        return True
    except Exception as e:
        print(f"Erro ao balançar cabeça: {e}")
        return False

def shake_no(self, intensity: float = 1.0):
    """Balança a cabeça negativamente"""
    try:
        self.animation_player.run("animations/Stand/Gestures/No_1")
        return True
    except Exception as e:
        print(f"Erro ao negar com cabeça: {e}")
        return False

def look_around(self):
    """Olha ao redor"""
    try:
        # Yaw é rotação da cabeça para esquerda/direita
        self.motion_proxy.angleInterpolationWithSpeed("HeadYaw", math.radians(-45), 0.2)
        time.sleep(1)
        self.motion_proxy.angleInterpolationWithSpeed("HeadYaw", math.radians(45), 0.2)
        time.sleep(1)
        self.motion_proxy.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.2)
        return True
    except Exception as e:
        print(f"Erro ao olhar ao redor: {e}")
        return False


def tilt_head(self, direction: str, angle: float = 20.0):
    """Inclina a cabeça"""
    try:
        if direction == "left":
            self.move_head("roll", angle, 1.0)
        elif direction == "right":
            self.move_head("roll", -angle, 1.0)
        return True
    except Exception as e:
        print(f"Erro ao inclinar cabeça: {e}")
        return False

# =======================================================
# ================== EXPRESSÕES E EMOÇÕES
# =======================================================

def express_emotion(self, emotion: str):
    """Expressa uma emoção através de animação"""
    emotions = {
        "happy": "animations/Stand/Emotions/Positive/Happy_1",
        "excited": "animations/Stand/Emotions/Positive/Excited_1",
        "proud": "animations/Stand/Emotions/Positive/Proud_1",
        "sad": "animations/Stand/Emotions/Negative/Sad_1",
        "angry": "animations/Stand/Emotions/Negative/Angry_1",
        "fear": "animations/Stand/Emotions/Negative/Fear_1",
        "surprise": "animations/Stand/Emotions/Neutral/Surprise_1",
        "thinking": "animations/Stand/Waiting/Think_1"
    }
    
    try:
        animation = emotions.get(emotion.lower())
        if animation:
            self.animation_player.run(animation)
            self.emotion_state = emotion
            return True
        else:
            print(f"Emoção '{emotion}' não reconhecida")
            return False
    except Exception as e:
        print(f"Erro ao expressar emoção: {e}")
        return False

def celebrate(self):
    """Gesto de celebração"""
    return self.express_emotion("excited")

def bow(self):
    """Faz uma reverência"""
    try:
        self.animation_player.run("animations/Stand/Gestures/BowShort_1")
        return True
    except Exception as e:
        print(f"Erro ao fazer reverência: {e}")
        return False

def show_muscle(self):
    """Mostra os músculos"""
    try:
        self.animation_player.run("animations/Stand/Gestures/Strong_1")
        return True
    except Exception as e:
        print(f"Erro ao mostrar músculos: {e}")
        return False
    
# =======================================================
# ================== COMPORTAMENTOS COMPLEXOS
# =======================================================

def greet_person(self, name: str = ""):
    """Cumprimenta uma pessoa"""
    try:
        self.wave_hand("right")
        if name:
            self.say(f"Hi, {name}! How are you?")
        else:
            self.say("Hi! How I can help you?")
        self.eye_color("green")
        return True
    except Exception as e:
        print(f"Erro ao cumprimentar: {e}")
        return False

def goodbye(self, name: str = ""):
    """Se despede"""
    try:
        if name:
            self.say(f"Bye, {name}! Was a plesure!")
        else:
            self.say("Bye! See you later!")
        self.wave_hand("both")
        self.eye_color("blue")
        return True
    except Exception as e:
        print(f"Erro ao se despedir: {e}")
        return False

def introduce_self(self):
    """Se apresenta"""
    try:
        self.bow()
        self.express_emotion("happy")
        return True
    except Exception as e:
        print(f"Erro na apresentação: {e}")
        return False

def tell_joke(self):
    """Conta uma piada"""
    jokes = [
        "Por que os robôs nunca ficam nervosos? Porque eles têm nerves of steel!",
        "O que um robô faz quando está com fome? Ele processa dados!",
        "Por que o robô foi ao médico? Porque tinha um virus!",
        "Como se chama um robô que demora para fazer as coisas? Um robô-lento!"
    ]
    
    try:
        joke = random.choice(jokes)
        self.say(joke)
        time.sleep(2)
        self.express_emotion("happy")
        return True
    except Exception as e:
        print(f"Erro ao contar piada: {e}")
        return False

def meditation_mode(self, duration: float = 60.0):
    """Modo meditação"""
    try:
        self.sit_down()
        self.eye_color("blue")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            self.blink_eyes(1, 2.0)
            time.sleep(10)
        
        self.say("Meditação concluída. Como se sente?")
        self.stand_up()
        return True
    except Exception as e:
        print(f"Erro no modo meditação: {e}")
        return False

def patrol_mode(self, duration: float = 300.0):
    """Modo patrulhamento"""
    try:
        self.say("Iniciando patrulhamento")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Anda para frente
            if not self.is_obstacle_ahead():
                self.walk_forward(0.5)
            else:
                self.turn_right(90)
            
            # Olha ao redor
            self.look_around()
            
            # Verifica se há pessoas
            if self.is_person_in_room():
                self.say("Pessoa detectada!")
                self.greet_person()
                break
            
            time.sleep(2)
        
        self.say("Patrulhamento concluído")
        return True
    except Exception as e:
        print(f"Erro no patrulhamento: {e}")
        return False


# =======================================================
# ================== CONTROLE AVANÇADO DE NAVEGAÇÃO
# =======================================================

def explore_room(self, duration: float = 300.0):
    """Explora o ambiente"""
    try:
        self.say("I will explore this room!")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Verifica obstáculos
            if self.is_obstacle_ahead():
                self.say("Obstáculo detectado, mudando direção")
                self.turn_right(45)
            else:
                self.walk_forward(0.3)
            
            # Olha ao redor ocasionalmente
            if random.random() < 0.3:
                self.look_around()
            
            # Detecta pessoas
            if self.is_person_in_room():
                self.greet_person()
                break
            
            time.sleep(1)
        
        self.say("Exploration completed!")
        return True
    except Exception as e:
        print(f"Erro na exploração: {e}")
        return False

def go_to_coordinate(self, x: float, y: float, avoid_obstacles: bool = True):
    """Vai para coordenada específica evitando obstáculos"""
    try:
        if avoid_obstacles:
            # Navegação com evitamento de obstáculos
            current_x, current_y = 0, 0  # Simplificado
            
            while abs(current_x - x) > 0.1 or abs(current_y - y) > 0.1:
                if self.is_obstacle_ahead():
                    self.turn_right(30)
                    self.walk_forward(0.2)
                    self.turn_left(30)
                else:
                    direction_x = x - current_x
                    direction_y = y - current_y
                    
                    if abs(direction_x) > abs(direction_y):
                        self.walk_forward(0.2) if direction_x > 0 else self.walk_backward(0.2)
                    else:
                        self.strafe_right(0.2) if direction_y > 0 else self.strafe_left(0.2)
                
                time.sleep(0.5)
        else:
            self.walk_to(x, y, 0)
        
        self.say("Destino alcançado!")
        return True
    except Exception as e:
        print(f"Erro ao navegar: {e}")
        return False
