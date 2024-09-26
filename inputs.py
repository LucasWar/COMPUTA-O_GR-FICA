from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glm
import config
from utils import update_projection
from timergl import iniciar_movimento


def tecladoSpecial(key, x, y):
    if   key == GLUT_KEY_UP:    config.frente   = True
    elif key == GLUT_KEY_DOWN:  config.tras     = True
    elif key == GLUT_KEY_LEFT:  config.esquerda = True
    elif key == GLUT_KEY_RIGHT: config.direita  = True

def tecladoUpSpecial(key, x, y):
    if   key == GLUT_KEY_UP:    config.frente   = False
    elif key == GLUT_KEY_DOWN:  config.tras     = False
    elif key == GLUT_KEY_LEFT:  config.esquerda = False
    elif key == GLUT_KEY_RIGHT: config.direita  = False

def keyboard(key, x, y):
    global qtdZoom
    if key == b'+' and config.current_mode == 'ortho':
        config.qtdZoom /= 1.1  # Aumenta a escala
    elif key == b'-' and config.current_mode == 'ortho':
        config.qtdZoom *= 1.1  # Diminui a escala
    elif key == b's':  
        config.velocDir = 0.00009
    update_projection()
    glutPostRedisplay()