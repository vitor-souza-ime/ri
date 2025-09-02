# RobotInterface

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Descrição

O **RobotInterface** é um framework modular desenvolvido para interação multimodal com o robô humanoide NAO da Aldebaran Robotics. Ele integra capacidades de visão computacional, reconhecimento de voz, controle de movimento e expressões emocionais em uma arquitetura unificada, facilitando o desenvolvimento de aplicações interativas com o robô.

O framework permite que pesquisadores e desenvolvedores criem comportamentos complexos de forma simplificada, promovendo maior reutilização de código e redução da complexidade de programação.

Mais informações estão disponíveis no repositório: [RobotInterface](https://github.com/vitor-souza-ime/ri)

---

## Funcionalidades

- **Visão Computacional**: detecção e classificação de objetos em tempo real usando o modelo CLIP (Contrastive Language-Image Pre-training).
- **Reconhecimento de Voz**: processamento de comandos de voz e interpretação de linguagem natural.
- **Controle de Movimento**: execução de movimentos e gestos do NAO.
- **Expressões Emocionais**: controle de LEDs, olhos e movimentos faciais para expressar emoções.
- **Arquitetura Modular**: cada funcionalidade é implementada em módulos independentes, permitindo fácil integração e manutenção.

---

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/vitor-souza-ime/ri.git
````

2. Entre na pasta do projeto:

```bash
cd ri
```

3. Instale as dependências (exemplo com pip):

```bash
pip install -r requirements.txt
```

> Observação: o NAO V6 utiliza Python 2.7, então pode ser necessário configurar processamento remoto (*brain transfer*) para certas funcionalidades avançadas.

---

## Exemplo de Uso

```python
from RobotInterface import RobotInterface

ip = "172.15.1.80"
port = 9559
model = "NAOV6"

nao = RobotInterface(ip, port, model)

# Exemplo: mover o braço
nao.move_arm("left", 45)

# Exemplo: detectar objeto
objeto = nao.detect_object("bola")
print(objeto)
```

---

## Contribuição

Contribuições são bem-vindas! Para contribuir, siga os passos:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova funcionalidade'`).
4. Envie para o repositório remoto (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

---

## Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.


Se você quiser, posso criar **uma versão do README.md mais visual**, com badges de status, imagens do NAO e instruções de execução mais detalhadas para cada módulo do framework. Quer que eu faça isso?
```
