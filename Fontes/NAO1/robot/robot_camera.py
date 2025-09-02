import qi
import time
import cv2
import numpy as np
from PIL import Image
import torch

# =======================================================
# ================== show_camera
# =======================================================
def show_camera(self, camera_name: str = "top"):
    if camera_name == "top":
        camera_index = 0
    elif camera_name == "bottom":
        camera_index = 1
    else:
        print("Escolha 'top' ou 'bottom'")
        return

    resolution = 2  # 640x480
    color_space = 11  # RGB
    fps = 30

    name_id = None
    try:
        name_id = self.video.subscribeCamera("python_client", camera_index, resolution, color_space, fps)
        print(f"Subscribed to camera with ID: {name_id}")
        time.sleep(0.5)
        image = self.video.getImageRemote(name_id)

        if image is None or len(image) < 7:
            print("Erro: Imagem não capturada ou dados incompletos")
            return

        width, height, channels = image[0], image[1], image[2]
        if len(image[6]) == 0:
            print("Erro: Dados da imagem estão vazios")
            return

        array = np.frombuffer(image[6], dtype=np.uint8)
        expected_size = width * height * channels
        if len(array) != expected_size:
            print(f"Erro: Tamanho dos dados ({len(array)}) não coincide com esperado ({expected_size})")
            return

        array = array.reshape((height, width, channels))
        if color_space == 11:
            array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

        cv2.imshow(f"Camera {camera_name}", array)
        print("Pressione qualquer tecla para fechar a janela...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Erro durante captura: {e}")
    finally:
        if name_id is not None:
            try:
                self.video.unsubscribe(name_id)
                print("Camera unsubscribed successfully")
            except:
                print("Erro ao desinscrever da câmera")

# =======================================================
# ================== show_camera_stream
# =======================================================
def show_camera_stream(self, camera_name: str = "top", duration: int = 10):
    if camera_name == "top":
        camera_index = 0
    elif camera_name == "bottom":
        camera_index = 1
    else:
        print("Escolha 'top' ou 'bottom'")
        return

    resolution = 1
    color_space = 11
    fps = 15
    name_id = None

    try:
        name_id = self.video.subscribeCamera("python_stream", camera_index, resolution, color_space, fps)
        print(f"Iniciando stream da câmera {camera_name}. Pressione 'q' para sair.")
        start_time = time.time()

        while time.time() - start_time < duration:
            image = self.video.getImageRemote(name_id)
            if image is not None and len(image) > 6:
                width, height, channels = image[0], image[1], image[2]
                if len(image[6]) > 0:
                    array = np.frombuffer(image[6], dtype=np.uint8).reshape((height, width, channels))
                    if color_space == 11:
                        array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
                    cv2.imshow(f"Stream - Camera {camera_name}", array)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            time.sleep(0.1)
    except Exception as e:
        print(f"Erro durante stream: {e}")
    finally:
        cv2.destroyAllWindows()
        if name_id is not None:
            try:
                self.video.unsubscribe(name_id)
                print("Stream finalizado")
            except:
                print("Erro ao finalizar stream")

# =======================================================
# ================== test_camera_info
# =======================================================
def test_camera_info(self):
    for cam_index in [0, 1]:
        try:
            name_id = self.video.subscribeCamera(f"test_{cam_index}", cam_index, 2, 11, 15)
            image = self.video.getImageRemote(name_id)
            if image is not None:
                width, height, channels = image[0], image[1], image[2]
                array = np.frombuffer(image[6], dtype=np.uint8).reshape((height, width, channels))
                print(f"Câmera {cam_index}: {width}x{height}, canais: {channels}")
                cv2.imshow(f"Câmera {cam_index}", array)
                cv2.waitKey(1000)
                cv2.destroyWindow(f"Câmera {cam_index}")
            self.video.unsubscribe(name_id)
        except Exception as e:
            print(f"Erro testando câmera {cam_index}: {e}")

# =======================================================
# ================== get_camera_frame
# =======================================================
def get_camera_frame(self, camera_name: str = "top"):
    if camera_name == "top":
        camera_index = 0
    elif camera_name == "bottom":
        camera_index = 1
    else:
        print("Escolha 'top' ou 'bottom'")
        return None

    resolution = 1
    color_space = 11
    fps = 15
    name_id = None

    try:
        name_id = self.video.subscribeCamera("clip_frame", camera_index, resolution, color_space, fps)
        time.sleep(0.3)
        image = self.video.getImageRemote(name_id)
        self.video.unsubscribe(name_id)

        if image is None or len(image) < 7:
            return None

        width, height, channels = image[0], image[1], image[2]
        array = np.frombuffer(image[6], dtype=np.uint8).reshape((height, width, channels))
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
# ================== DETECÇÃO DE PESSOA/OBJETO
# =======================================================
def is_person_in_room(self, camera_name: str = "top") -> bool:
    image_array = self.get_camera_frame(camera_name)
    if image_array is None:
        print("Erro ao capturar a imagem")
        return False

    image = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
    image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)
    text_inputs = self.clip_module.tokenize(["a person", "no person"]).to(self.device)

    with torch.no_grad():
        image_features = self.clip_model.encode_image(image_input)
        text_features = self.clip_model.encode_text(text_inputs)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(1)
        return indices.item() == 0

def is_object_in_frame(self, object_name: str, camera_name: str = "top") -> bool:
    image_array = self.get_camera_frame(camera_name)
    if image_array is None:
        print("Erro ao capturar a imagem")
        return False

    image = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
    image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)
    text_inputs = self.clip_module.tokenize([object_name, f"no {object_name}"]).to(self.device)

    with torch.no_grad():
        image_features = self.clip_model.encode_image(image_input)
        text_features = self.clip_model.encode_text(text_inputs)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(1)
        return indices.item() == 0
