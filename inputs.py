from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glm
import config
from utils import update_projection
from timergl import iniciar_movimento


def tecladoSpecial(key, x, y):
    # global frente, tras, esquerda, direita
    # Se alguma tecla for pressionada, faz a variável correspondente ficar verdadeira
    if   key == GLUT_KEY_UP:    config.frente   = True
    elif key == GLUT_KEY_DOWN:  config.tras     = True
    elif key == GLUT_KEY_LEFT:  config.esquerda = True
    elif key == GLUT_KEY_RIGHT: config.direita  = True

def tecladoUpSpecial(key, x, y):
    # global frente, tras, esquerda, direita
    # Se alguma tecla for solta, faz a variável correspondente ficar falsa
    if   key == GLUT_KEY_UP:    config.frente   = False
    elif key == GLUT_KEY_DOWN:  config.tras     = False
    elif key == GLUT_KEY_LEFT:  config.esquerda = False
    elif key == GLUT_KEY_RIGHT: config.direita  = False

def keyboard(key, x, y):
    global qtdZoom
    if key == b'+':
        config.qtdZoom /= 1.1  # Aumenta a escala
    elif key == b'-':
        config.qtdZoom *= 1.1  # Diminui a escala
    elif key == b'm':  # Alterna entre modos de visualização
        if config.current_mode == "perspective":
            config.current_mode = "ortho"
        else:
            config.current_mode = "perspective"
    elif key == b's':  # Alterna entre modos devisualização
        config.velocDir = 0.0003
    update_projection()
    glutPostRedisplay()