**🇧🇷 PT/BR**
# Projeto IA Elysium Aimbot


Este é um projeto open source de um aimbot por IA feito para dar tanto uma ajuda para os que estão querendo aprender a como fazer como para quem quer algo que é so baixar, instalar as dependências e jogar.


## Atalhos / Comandos

**PT/BR**

- **F3**: pausar / resumir
- **HOME**: Update config 
- **LEFT and RIGHT click**: turn on aimbot(mouse moviment)


## Installation

Install with pip 

```bash
  pip install -r requirements.txt
```
    
    
## Config.json


- **offset_y**: apontar a mira mais acima ou mais abaixo do centro do box (positivo para cima, negativo para baixo)

- **sensi**: sensibilidade do movimento da mira (só funciona na função de backup na pasta _BACKUP_M_EVENT.py)

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

Install with pip 

```bash
  pip install -r requirements.txt
```
    
## Config.json


- **offset_y**: Adjusts the aim higher or lower relative to the center of the box (positive for up, negative for down).

- **sensi**: Sensitivity of aim movement (only works in the backup function inside the `_BACKUP_M_EVENT.py` folder).

- **fov**: Detection area.

- **fov-min**: Dynamic detection area; it decreases while holding the RIGHT click.

- **confidence**: Confidence level the AI must have to detect the object (0.9 - 0.1).

- **smooth_enable**: Enables or disables smooth movement.

- **smooth_value**: Smoothness of aim movement (0.1 - 0.9).

- **t_factor**: Constant in Bézier curve calculations (mouse movement humanization) (0.1 - 0.001).

