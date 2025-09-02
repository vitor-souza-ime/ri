import qi
import time
import math
import sys
import select
import cv2

# =======================================================
# ================== loop_until_keypress
# =======================================================
def loop_until_keypress(self, message="Pressione Enter para parar..."):
    """
    Mantém o robô em loop até que o usuário pressione Enter.
    """
    print(message)
    while True:
        # Executa ações do robô aqui se quiser
        time.sleep(0.1)  # evita consumir 100% CPU
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            input()  # captura a tecla
            break
    print("Loop encerrado.")

# =======================================================
# ================== wait_ms
# =======================================================
def wait_ms(self, milliseconds: int):
    """Espera por um tempo em milissegundos"""
    time.sleep(milliseconds / 1000)

# =======================================================
# ================== wait_s
# =======================================================
def wait_s(self, seconds: float):
    """Espera por um tempo em segundos"""
    time.sleep(seconds)

# =======================================================
# ================== wait_min 
# =======================================================
def wait_min(self, minutes: float):
    """Espera por um tempo em minutos"""
    time.sleep(minutes * 60)

# =======================================================
# ================== MODO SHUTDOWN E CLEANUP
# =======================================================

def shutdown(self):
    """Desliga o robô de forma segura"""
    try:
        self.say("Desligando sistemas... Até logo!")
        
        # Para todos os rastreamentos
        if self.face_tracking_active:
            self.stop_face_tracking()
        if self.sound_localization_active:
            self.stop_sound_localization()
        
        # Para movimentos
        self.stop_walking()
        
        # Desliga LEDs
        self.off_led("AllLeds")
        
        # Posição de descanso
        self.go_to_posture("Crouch", 1.0)
        
        # Remove rigidez
        self.motion.setStiffnesses("Body", 0.0)
        
        # Para o robô
        self.motion.rest()
        
        print("Robô desligado com segurança")
        return True
    except Exception as e:
        print(f"Erro ao desligar: {e}")
        return False
