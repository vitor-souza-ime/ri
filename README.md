# RobotInterface

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

**RobotInterface** is a modular framework designed for multimodal interaction with the **NAO humanoid robot** developed by Aldebaran Robotics. The framework integrates computer vision, speech recognition, motion control, and emotional expression capabilities into a unified architecture, facilitating the development of interactive robotic applications.

The framework allows researchers and developers to create complex robot behaviors in a simplified way, promoting code reuse and reducing programming complexity.

More information is available in the repository:
[RobotInterface](https://github.com/vitor-souza-ime/ri)

---

## Features

* **Computer Vision**: real-time object detection and classification using the **CLIP (Contrastive Language–Image Pre-training)** model.
* **Speech Recognition**: processing of voice commands and natural language interpretation.
* **Motion Control**: execution of NAO movements and gestures.
* **Emotional Expressions**: control of LEDs, eyes, and facial movements to express emotions.
* **Modular Architecture**: each functionality is implemented as an independent module, allowing easy integration and maintenance.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/vitor-souza-ime/ri.git
```

2. Enter the project directory:

```bash
cd ri
```

3. Install the dependencies (example using pip):

```bash
pip install -r requirements.txt
```

> **Note:** NAO V6 uses **Python 2.7**, so remote processing (*brain transfer*) may be required for some advanced functionalities.

---

## Usage Example

```python
from RobotInterface import RobotInterface

ip = "172.15.1.80"
port = 9559
model = "NAOV6"

nao = RobotInterface(ip, port, model)

# Example: move the arm
nao.move_arm("left", 45)

# Example: detect an object
object_detected = nao.detect_object("ball")
print(object_detected)
```

---

## Contributing

Contributions are welcome! To contribute, follow these steps:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the remote repository (`git push origin feature/new-feature`).
5. Open a Pull Request.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
