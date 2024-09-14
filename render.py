from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import glm
import config
from utils import update_projection
from classCarro import Carro
from objetos import Icone

def init():
    global carro, police
    # Define a cor de fundo da janela (branco)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    update_projection()
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_MULTISAMPLE)                            # habilita anti-aliasing
    glEnable(GL_TEXTURE_2D)                             # habilita o uso de texturas 2D
    glEnable(GL_BLEND);                           # habilita a funcionalidade de mistura (necessário para objetos transparentes)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # define como a mistura entre objetos transparência deve ser realizada
    carro = Carro()
    police = Icone()


def desenharCaminho():
    if config.caminhoFinal:
        glColor(0.43, 0.72, 1)  # Cor do caminho
        glBegin(GL_QUADS)  # Usando quadriláteros para garantir o preenchimento

        pontos = list(config.caminhoFinal.items())

        for i in range(len(pontos) - 1):
            x1, y1 = pontos[i][1]
            x2, y2 = pontos[i+1][1]

            # Calcular a direção do caminho
            dx, dy = x2 - x1, y2 - y1
            length = np.hypot(dx, dy)
            dx, dy = dx / length, dy / length

            # Calcular os deslocamentos para criar o retângulo
            offset_x, offset_y = -dy * config.larguraPista / 2, dx * config.larguraPista / 2

            # Definir os quatro vértices do quadrilátero principal
            vertices = [
                (x1 + offset_x, y1 + offset_y),
                (x1 - offset_x, y1 - offset_y),
                (x2 - offset_x, y2 - offset_y),
                (x2 + offset_x, y2 + offset_y),
            ]

            # Desenhar o quadrilátero principal
            for vertex in vertices:
                glVertex2f(vertex[0], vertex[1])

            # Desenhar vértices extras nas interseções para evitar lacunas
            if i > 0:
                x0, y0 = pontos[i-1][1]
                dx_prev, dy_prev = x1 - x0, y1 - y0
                length_prev = np.hypot(dx_prev, dy_prev)
                dx_prev, dy_prev = dx_prev / length_prev, dy_prev / length_prev
                offset_x_prev, offset_y_prev = -dy_prev * config.larguraPista / 2, dx_prev * config.larguraPista / 2

                # Vértices intermediários para preencher a área na interseção
                glVertex2f(x1 + offset_x_prev, y1 + offset_y_prev)
                glVertex2f(x1 + offset_x, y1 + offset_y)
                glVertex2f(x1 - offset_x, y1 - offset_y)
                glVertex2f(x1 - offset_x_prev, y1 - offset_y_prev)
        
        glEnd()


def desenharElementos():
    for caracte in config.naturalElementos:
        cor = caracte[0]
        pontos = caracte[1]
        glColor3f(cor[0], cor[1], cor[2])
        for geometry in pontos['geometry']:
            if geometry.geom_type == 'Polygon':
                borda = geometry.exterior
                coordenadas = list(borda.coords)
                glBegin(GL_POLYGON)
                for coord in coordenadas:
                    glVertex2f(coord[0], coord[1])
                glEnd()
            elif geometry.geom_type == 'MultiPolygon':
                for poly in geometry.geoms:
                    borda = poly.exterior
                    coordenadas = list(borda.coords)
                    glBegin(GL_POLYGON)
                    for coord in coordenadas:
                        glVertex2f(coord[0], coord[1])
                    glEnd()

def desenharPredios():
    glColor3f(0.3, 0.3, 0.3)

    for geometry in config.predios['geometry']:
        if geometry.geom_type == 'Polygon':
            desenharPredio3d(geometry)
        elif geometry.geom_type == 'MultiPolygon':
            for poly in geometry.geoms:
                desenharPredio3d(poly)

def desenharPredio3d(polygon, altura=0.0002):
    # Desenha a base do prédio
    coordenadas = list(polygon.exterior.coords)
    glBegin(GL_POLYGON)
    for coord in coordenadas:
        glVertex3f(coord[0], coord[1], 0)
    glEnd()

    # Desenha as paredes do prédio
    glBegin(GL_QUADS)
    for i in range(len(coordenadas) - 1):
        x1, y1 = coordenadas[i]
        x2, y2 = coordenadas[i+1]
        
        # Parede
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y2, 0)
        glVertex3f(x2, y2, altura)
        glVertex3f(x1, y1, altura)
    glEnd()

    # Desenha o topo do prédio
    glBegin(GL_POLYGON)
    for coord in coordenadas:
        glVertex3f(coord[0], coord[1], altura)
    glEnd()

def drawMap():
    glColor3f(0.5, 0.5, 0.5)
    
    # Primeira parte: Desenho das estradas
    glBegin(GL_QUADS)
    for u, v, data in config.mapa.edges(keys=False, data=True):
        x1, y1 = config.mapa.nodes[u]['x'], config.mapa.nodes[u]['y']
        x2, y2 = config.mapa.nodes[v]['x'], config.mapa.nodes[v]['y']

        # Calcular direção e tamanho do segmento
        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy)
        dx, dy = dx / length, dy / length

        # Calcular o deslocamento perpendicular para a largura da estrada
        offset_x, offset_y = -dy * config.larguraPista / 2, dx * config.larguraPista / 2

        # Calcular vértices do quadrilátero
        v1 = (x1 + offset_x, y1 + offset_y)
        v2 = (x1 - offset_x, y1 - offset_y)
        v3 = (x2 - offset_x, y2 - offset_y)
        v4 = (x2 + offset_x, y2 + offset_y)
        
        # Desenhar o quadrilátero
        glVertex2f(*v1)
        glVertex2f(*v2)
        glVertex2f(*v3)
        glVertex2f(*v4)
    glEnd()
    
    # Segunda parte: Conexão das quinas com tratamento aprimorado
    glBegin(GL_TRIANGLES)
    for node in config.mapa.nodes():
        neighbors = list(config.mapa.neighbors(node))
        if len(neighbors) < 2:
            continue  # Precisa de pelo menos duas estradas para formar uma quina

        x_center, y_center = config.mapa.nodes[node]['x'], config.mapa.nodes[node]['y']
        
        # Ordenar vizinhos em sentido horário
        angles = []
        for neighbor in neighbors:
            nx, ny = config.mapa.nodes[neighbor]['x'], config.mapa.nodes[neighbor]['y']
            angle = np.arctan2(ny - y_center, nx - x_center)
            angles.append((angle, neighbor))
        angles.sort()

        for i in range(len(angles)):
            _, neighbor1 = angles[i]
            _, neighbor2 = angles[(i + 1) % len(angles)]
            x1, y1 = config.mapa.nodes[neighbor1]['x'], config.mapa.nodes[neighbor1]['y']
            x2, y2 = config.mapa.nodes[neighbor2]['x'], config.mapa.nodes[neighbor2]['y']

            # Calcular os vetores de direção
            dx1, dy1 = x1 - x_center, y1 - y_center
            dx2, dy2 = x2 - x_center, y2 - y_center
            length1 = np.hypot(dx1, dy1)
            length2 = np.hypot(dx2, dy2)
            dx1, dy1 = dx1 / length1, dy1 / length1
            dx2, dy2 = dx2 / length2, dy2 / length2

            # Calcular os deslocamentos para a largura da estrada
            offset_x1, offset_y1 = -dy1 * config.larguraPista / 2, dx1 * config.larguraPista / 2
            offset_x2, offset_y2 = -dy2 * config.larguraPista / 2, dx2 * config.larguraPista / 2

            # Desenhar triângulo na quina
            glVertex2f(x_center + offset_x1, y_center + offset_y1)
            glVertex2f(x_center + offset_x2, y_center + offset_y2)
            glVertex2f(x_center, y_center)

            # Desenhar vértices intermediários para garantir preenchimento correto na quina
            glVertex2f(x_center + offset_x1, y_center + offset_y1)
            glVertex2f(x_center + offset_x2, y_center + offset_y2)
            glVertex2f(x_center, y_center)
    glEnd()




def drawPoints():
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for point in config.points:
        glVertex2f(point[0], point[1])
    glEnd()






def display():
    global novaMatrizDeVizinhos, caminhoFinal
    glClear(GL_COLOR_BUFFER_BIT)
    
    drawMap()
    desenharPredios()

    desenharElementos()

    drawPoints()
    desenharCaminho()

    glPushMatrix()
    
    glTranslatef(config.longitude,config.latitude,0)
    police.desenha()
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf(np.asarray(glm.transpose(config.M))) # função que aplica uma matriz qualquer no objeto
    carro.desenha()
    glPopMatrix()
    glutSwapBuffers()