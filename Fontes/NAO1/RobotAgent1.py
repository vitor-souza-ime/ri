import qi
import cv2
import numpy as np

class RobotAgent:
    def __init__(self, ip: str, port: int, model: str):
        self.app = qi.Application(["RobotAgentApp", f"--qi-url=tcp://{ip}:{port}"])
        self.app.start()
        self.session = self.app.session
        self.tts = self.session.service("ALTextToSpeech")
        self.video = self.session.service("ALVideoDevice")

    def say(self, text: str):
        self.tts.say(text)

    def show_camera(self, camera_name: str = "top"):
        """
        Captura e mostra a imagem da câmera superior ou inferior.
        :param camera_name: 'top' para câmera superior, 'bottom' para inferior
        """
        if camera_name == "top":
            camera_index = 0  # NAO: 0 = top, 1 = bottom
        elif camera_name == "bottom":
            camera_index = 1
        else:
            print("Escolha 'top' ou 'bottom'")
            return

        # Parâmetros de captura
        resolution = 2  # 0=160x120, 1=320x240, 2=640x480
        color_space = 11  # kRGBColorSpace (BGR pode causar problemas)
        fps = 30

        name_id = None
        try:
            # Assinar a câmera
            name_id = self.video.subscribeCamera("python_client", camera_index, resolution, color_space, fps)
            print(f"Subscribed to camera with ID: {name_id}")
            
            # Aguardar um pouco para a câmera se estabilizar
            import time
            time.sleep(0.5)
            
            # Capturar imagem
            image = self.video.getImageRemote(name_id)
            
            if image is None or len(image) < 7:
                print("Erro: Imagem não capturada ou dados incompletos")
                return

            # Extrair informações da imagem
            width = image[0]
            height = image[1]
            channels = image[2]  # número de canais
            
            print(f"Dimensões da imagem: {width}x{height}, canais: {channels}")
            
            # Verificar se os dados da imagem existem
            if len(image[6]) == 0:
                print("Erro: Dados da imagem estão vazios")
                return
            
            # Converter para NumPy array
            array = np.frombuffer(image[6], dtype=np.uint8)
            
            # Verificar se o tamanho dos dados está correto
            expected_size = width * height * channels
            if len(array) != expected_size:
                print(f"Erro: Tamanho dos dados ({len(array)}) não coincide com esperado ({expected_size})")
                return
            
            # Reshape a imagem
            array = array.reshape((height, width, channels))
            
            # Se for RGB, converter para BGR para o OpenCV
            if color_space == 11:  # RGB
                array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
            
            # Mostrar imagem
            cv2.imshow(f"Camera {camera_name}", array)
            print("Pressione qualquer tecla para fechar a janela...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"Erro durante captura: {e}")
            
        finally:
            # Sempre desinscrever da câmera
            if name_id is not None:
                try:
                    self.video.unsubscribe(name_id)
                    print("Camera unsubscribed successfully")
                except:
                    print("Erro ao desinscrever da câmera")

    def show_camera_stream(self, camera_name: str = "top", duration: int = 10):
        """
        Mostra stream contínuo da câmera por um período determinado.
        :param camera_name: 'top' para câmera superior, 'bottom' para inferior
        :param duration: duração em segundos
        """
        if camera_name == "top":
            camera_index = 0
        elif camera_name == "bottom":
            camera_index = 1
        else:
            print("Escolha 'top' ou 'bottom'")
            return

        # Parâmetros de captura
        resolution = 1      # Usar resolução menor para stream
        color_space = 11    # RGB
        fps = 15            # FPS menor para stream

        name_id = None
        try:
            name_id = self.video.subscribeCamera("python_stream", camera_index, resolution, color_space, fps)
            print(f"Iniciando stream da câmera {camera_name}. Pressione 'q' para sair.")
            
            import time
            start_time = time.time()
            
            while time.time() - start_time < duration:
                image = self.video.getImageRemote(name_id)
                
                if image is not None and len(image) > 6:
                    width = image[0]
                    height = image[1]
                    channels = image[2]
                    
                    if len(image[6]) > 0:
                        array = np.frombuffer(image[6], dtype=np.uint8)
                        array = array.reshape((height, width, channels))
                        
                        # Converter RGB para BGR
                        if color_space == 11:
                            array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
                        
                        cv2.imshow(f"Stream - Camera {camera_name}", array)
                        
                        # Sair se 'q' for pressionado
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                
                time.sleep(0.1)  # Pequena pausa
                
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

    def test_camera_info(self):
        """
        Testa informações básicas das câmeras disponíveis.
        """
        try:
            # Listar câmeras disponíveis
            camera_names = self.video.getCameraNames()
            print(f"Câmeras disponíveis: {camera_names}")
            
            # Testar parâmetros suportados
            for i in range(2):  # NAO normalmente tem 2 câmeras
                try:
                    name_id = self.video.subscribeCamera(f"test_{i}", i, 1, 11, 15)
                    image = self.video.getImageRemote(name_id)
                    if image:
                        print(f"Câmera {i}: {image[0]}x{image[1]}, canais: {image[2]}")
                    self.video.unsubscribe(name_id)
                except Exception as e:
                    print(f"Erro testando câmera {i}: {e}")
                    
        except Exception as e:
            print(f"Erro obtendo informações das câmeras: {e}")