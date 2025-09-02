import qi
import threading

# ================== LEDs ==================
def set_led(self, name: str, color: str, duration: float = 1.0):
    """
    Acende um LED do NAO de forma assíncrona.
    :param name: nome do grupo de LEDs (ex: "FaceLeds", "ChestLeds", "EarLeds")
    :param color: cor em formato "#RRGGBB"
    :param duration: duração em segundos
    """
    def worker():
        try:
            self.leds.fadeRGB(name, color, duration)
        except Exception as e:
            print(f"Erro ao acender LED {name}: {e}")

    threading.Thread(target=worker, daemon=True).start()


def off_led(self, name: str):
    """
    Apaga um LED do NAO de forma assíncrona.
    :param name: nome do grupo de LEDs
    """
    threading.Thread(target=lambda: self.leds.off(name), daemon=True).start()

"""
# =======================================================
# ================== set_led
# =======================================================
def set_led(self, name: str, color: str, duration: float = 1.0):
    
    Acende um LED do NAO.
    :param name: nome do grupo de LEDs (ex: "FaceLeds", "ChestLeds", "EarLeds")
    :param color: cor em formato "#RRGGBB"
    :param duration: duração em segundos
    
    self.leds.fadeRGB(name, color, duration)

# =======================================================
# ================== off_led
# =======================================================
def off_led(self, name: str):
    self.leds.off(name)
    """
# =======================================================
# ================== CONTROLE DE LEDs AVANÇADO
# =======================================================

def eye_color(self, color: str):
    """Define cor dos olhos"""
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "purple": (255, 0, 255),
        "cyan": (0, 255, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "orange": (255, 128, 0)
    }
    
    try:
        r, g, b = colors.get(color.lower(), (255, 255, 255))
        self.leds.fadeRGB("FaceLeds", r, g, b, 1.0)
        return True
    except Exception as e:
        print(f"Erro ao definir cor dos olhos: {e}")
        return False


def chest_color(self, color: str):
    """Define cor do peito"""
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "purple": (255, 0, 255),
        "cyan": (0, 255, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0)
    }
    
    try:
        r, g, b = colors.get(color.lower(), (255, 255, 255))
        self.leds.fadeRGB("ChestLeds", r, g, b, 1.0)
        return True
    except Exception as e:
        print(f"Erro ao definir cor do peito: {e}")
        return False


def ear_color(self, ear: str, color: str):
    """Define cor das orelhas"""
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "purple": (255, 0, 255),
        "cyan": (0, 255, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0)
    }
    
    try:
        r, g, b = colors.get(color.lower(), (255, 255, 255))
        if ear.lower() == "left":
            self.leds.fadeRGB("LeftEarLeds", r, g, b, 1.0)
        elif ear.lower() == "right":
            self.leds.fadeRGB("RightEarLeds", r, g, b, 1.0)
        elif ear.lower() == "both":
            self.leds.fadeRGB("EarLeds", r, g, b, 1.0)
        return True
    except Exception as e:
        print(f"Erro ao definir cor da orelha: {e}")
        return False


def blink_eyes(self, times: int = 3, duration: float = 0.5):
    """Pisca os olhos"""
    try:
        for _ in range(times):
            # Apaga os olhos
            self.leds.fade("FaceLeds", 0.0, 0.2)
            time.sleep(duration / 2)

            # Acende os olhos (branco)
            self.leds.fade("FaceLeds", 1.0, 0.2)
            time.sleep(duration / 2)
        return True
    except Exception as e:
        print(f"Erro ao piscar olhos: {e}")
        return False


def rainbow_eyes(self, duration: float = 5.0):
    """Efeito arco-íris nos olhos"""
    # Cores como tuplas RGB (0.0 a 1.0)
    colors = [
        (1.0, 0.0, 0.0),  # vermelho
        (1.0, 0.5, 0.0),  # laranja
        (1.0, 1.0, 0.0),  # amarelo
        (0.0, 1.0, 0.0),  # verde
        (0.0, 0.0, 1.0),  # azul
        (0.5, 0.0, 1.0),  # violeta
        (1.0, 0.0, 1.0)   # magenta
    ]
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            for r, g, b in colors:
                self.leds.fadeRGB("FaceLeds", r, g, b, 0.3)
                time.sleep(0.3)
        return True
    except Exception as e:
        print(f"Erro no efeito arco-íris: {e}")
        return False

