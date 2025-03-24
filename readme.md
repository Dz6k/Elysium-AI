**🇧🇷 PT/BR**
# Projeto IA Elysium Aimbot


Este é um projeto open source de um aimbot por IA feito para dar tanto uma ajuda para os que estão querendo aprender a como fazer como para quem quer algo que é so baixar, instalar as dependências e jogar.


## Atalhos / Comandos

**PT/BR**

- **F3**: pausar / resumir
- **HOME**: Update config 
- **LEFT and RIGHT click**: turn on aimbot(mouse moviment)


## Instalação

### Instale com pip (FAÇA ISSO SEGUINDO ESTA SEQUÊNCIA!)
#### **OPENGL OBS**: Use a mesma versão do python na lib OpenGL (Eu uso python 3.11.7)
- [OpenGL Dependences](https://github.com/cgohlke/pyopengl-build)
```bash
  pip install private\OpenGL\PyOpenGL_accelerate-3.1.9-cp311-cp311-win_amd64.whl 
  pip install private\OpenGL\PyOpenGL-3.1.9-cp311-cp311-win_amd64.whl
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
  pip install ultralytics
  pip install -r requirements.txt
```
## Dependências externas necessárias

- **CUDA**: [NVIDIA Cuda 12.4.0](https://developer.nvidia.com/cuda-12-4-0-download-archive)

- **cuDNN**: [cuDNN 8.9.6](https://developer.nvidia.com/downloads/compute/cudnn/secure/8.9.6/local_installers/12.x/cudnn-windows-x86_64-8.9.6.50_cuda12-archive.zip/)

### Opcional (para modelos .engine)

- **TensorRT**: [TensorRT 10.3 GA](https://developer.nvidia.com/downloads/compute/machine-learning/tensorrt/10.3.0/zip/TensorRT-10.3.0.26.Windows.win10.cuda-12.5.zip)

    
## Config.json


- **offset_y**: apontar a mira mais acima ou mais abaixo do centro do box (positivo para cima, negativo para baixo)

- **sensi**: sensibilidade do movimento da mira (só funciona na função de backup no modulo _BACKUP_M_EVENT.py)

- **fov**: Área de detecção 

- **fov-min**: Área de detecção dinâmica, ela diminui enquanto aperta RIGHT click

- **confidence**: Nível de confiança que a IA tem que ter na detecção do objeto (0.9 - 0.1)

- **smooth_enable**: Ativa e desativa smooth 

- **smooth_value**: Suavização do movimento da mira (0.1 - 0.9)

- **t_factor**: Constante nos cálculos da curva de benzier (humanização do movimento do mouse) (0.1-0.001)

---------------------------

**EN/US**
# Project AI Elysium Aimbot

This is an open-source AI-powered aimbot project designed both to help those who want to learn how to create one and for those who just want something ready to download, install the dependencies, and play

## Shortcuts / Commands

**EN/US**
- **F3**: Pause / Resume
- **HOME**: Update config
- **LEFT and RIGHT click**: Turn on aimbot (mouse movement)


## Installation

### Install with pip (DO THIS BY FOLLOWING THIS SEQUENCE!)
#### **OPENGL OBS**: Use the same version of python in opengl (i'm using python 3.11.7)
- [OpenGL Dependences](https://github.com/cgohlke/pyopengl-build)
```bash
  pip install private\OpenGL\PyOpenGL_accelerate-3.1.9-cp311-cp311-win_amd64.whl 
  pip install private\OpenGL\PyOpenGL-3.1.9-cp311-cp311-win_amd64.whl
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
  pip install ultralytics
  pip install -r requirements.txt
```
## Required External Dependencies

- **CUDA**: [NVIDIA Cuda 12.4.0](https://developer.nvidia.com/cuda-12-4-0-download-archive)

- **cuDNN**: [cuDNN 8.9.6](https://developer.nvidia.com/downloads/compute/cudnn/secure/8.9.6/local_installers/12.x/cudnn-windows-x86_64-8.9.6.50_cuda12-archive.zip/)

### Optional (for .engine models)

- **TensorRT**: [TensorRT 10.3 GA](https://developer.nvidia.com/downloads/compute/machine-learning/tensorrt/10.3.0/zip/TensorRT-10.3.0.26.Windows.win10.cuda-12.5.zip)


## Config.json


- **offset_y**: Adjusts the aim higher or lower relative to the center of the box (positive for up, negative for down).

- **sensi**: Sensitivity of aim movement (only works in the backup function inside the `_BACKUP_M_EVENT.py` module).

- **fov**: Detection area.

- **fov-min**: Dynamic detection area; it decreases while holding the RIGHT click.

- **confidence**: Confidence level the AI must have to detect the object (0.9 - 0.1).

- **smooth_enable**: Enables or disables smooth movement.

- **smooth_value**: Smoothness of aim movement (0.1 - 0.9).

- **t_factor**: Constant in Bézier curve calculations (mouse movement humanization) (0.1 - 0.001).

