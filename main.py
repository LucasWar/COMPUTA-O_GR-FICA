from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from aEstrela import estrela
import config
from utils import *
from inputs import *
from timergl import *
from render import *


global ultCordMouseX, ultCordMouseY

def mouse(button, state, x, y):
    global ultCordMouseX, ultCordMouseY
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            config.mousePres = True
            ultCordMouseX = x
            ultCordMouseY = y
        elif state == GLUT_UP:
            config.mousePres = False
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            mapX, mapY = telaParaMapa(x, y)
            nearest_point = buscarPontoMaisProximo(mapX, mapY)
            mapX, mapY = nearest_point
            config.points.append(nearest_point)
            
            if len(config.points) < 2:
                config.caminhoFinal = {}
                for chave, valor in config.matrizDeVizinhos.items():
                    config.novaMatrizDeVizinhos[chave] = valor.copy()

                vizinhosPonto = buscaVizinhosDoPonto(mapX, mapY)
                config.novaMatrizDeVizinhos[mapX, mapY] = vizinhosPonto
                print("ponto 1 coordenadas x = {} e y = {}".format(mapX, mapY))
                print("Vizinhos {}",vizinhosPonto)
            else:
                vizinhosPonto = buscaVizinhosDoPonto(mapX, mapY)
                config.novaMatrizDeVizinhos[mapX, mapY] = vizinhosPonto
                #Corrigir esse for, erro provavel loop eterno pois deve esta appontando para ele mesmo.
                for vizinho in vizinhosPonto:
                    config.novaMatrizDeVizinhos[vizinho[0],vizinho[1]].append((mapX, mapY))
                config.caminhoFinal = estrela(config.points[0][0],config.points[0][1],config.points[1][0],config.points[1][1],config.novaMatrizDeVizinhos)
                iniciar_movimento()
                print("ponto 1 coordenadas x = {} e y = {}".format(mapX, mapY))
                print("Vizinhos {}",vizinhosPonto)
                config.points = []

            glutPostRedisplay()


def motion(x, y):
    global  ultCordMouseX, ultCordMouseY
    if config.mousePres:
        dx = (x - ultCordMouseX) * 0.0001 * config.qtdZoom
        dy = (y - ultCordMouseY) * 0.0001 * config.qtdZoom
        config.camera_x -= dx
        config.camera_y += dy
        ultCordMouseX = x
        ultCordMouseY = y
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        update_projection()
        glutPostRedisplay()

# def find_nearest_vertices(point):
#     global kdtree
#     nearest_vertices = []
#     for point in config.points:
#         dist, idx = kdtree.query(point)
#         nearest_vertices.append(config.coords[idx])
#     return np.array(nearest_vertices)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b'config.mapa')
    init()
    glutDisplayFunc(display)
    glutTimerFunc(int(1000/config.FPS), timer, 0)      
    glutSpecialFunc(tecladoSpecial)             
    glutSpecialUpFunc(tecladoUpSpecial)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutMainLoop()

if __name__ == "__main__":
    main()