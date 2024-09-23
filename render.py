from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import glm
import config
from utils import update_projection
from classCarro import Carro
from objetos import Icone
import math
def init():
    global carro, police
    # Define a cor de fundo da janela (branco)
    glClearColor(0.7, 0.7, 0.7, 1.0)
    update_projection()
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_MULTISAMPLE)                            # habilita anti-aliasing
    glEnable(GL_TEXTURE_2D)                             # habilita o uso de texturas 2D
    glEnable(GL_BLEND);                           # habilita a funcionalidade de mistura (necessário para objetos transparentes)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # define como a mistura entre objetos transparência deve ser realizada
    carro = Carro()
    police = Icone(config.posIcones)


def desenharCaminho():
    if config.caminhoFinal:
        glColor(0.43, 0.72, 1)  # Cor do caminho
        glBegin(GL_QUADS)  # Usando quadriláteros para garantir o preenchimento
        pontos = list(config.caminhoFinal.items())
        
        for i in range(len(pontos) - 1):
            # Pontos do caminho atual e o próximo ponto
            ponto1 = glm.vec2(pontos[i][1])
            ponto2 = glm.vec2(pontos[i + 1][1])

            # Calcular a direção do caminho
            direcao = ponto2 - ponto1
            direcao = glm.normalize(direcao)

            # Calcular os deslocamentos para criar o retângulo
            perpendicular = glm.vec2(-direcao.y, direcao.x) * (config.larguraPista / 2)

            # Definir os quatro vértices do quadrilátero principal
            vertices = [
                ponto1 + perpendicular,
                ponto1 - perpendicular,
                ponto2 - perpendicular,
                ponto2 + perpendicular,
            ]

            # Desenhar o quadrilátero principal
            for vertex in vertices:
                glVertex2f(vertex.x, vertex.y)

            # Desenhar vértices extras nas interseções para evitar lacunas
            if i > 0:
                ponto_prev = glm.vec2(pontos[i - 1][1])
                direcao_prev = ponto1 - ponto_prev
                direcao_prev = glm.normalize(direcao_prev)
                perpendicular_prev = glm.vec2(-direcao_prev.y, direcao_prev.x) * (config.larguraPista / 2)

                # Vértices intermediários para preencher a área na interseção
                glVertex2f(ponto1.x + perpendicular_prev.x, ponto1.y + perpendicular_prev.y)
                glVertex2f(ponto1.x + perpendicular.x, ponto1.y + perpendicular.y)
                glVertex2f(ponto1.x - perpendicular.x, ponto1.y - perpendicular.y)
                glVertex2f(ponto1.x - perpendicular_prev.x, ponto1.y - perpendicular_prev.y)
        
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
        # Usando glm para facilitar o cálculo dos pontos
        ponto1 = glm.vec2(config.mapa.nodes[u]['x'], config.mapa.nodes[u]['y'])
        ponto2 = glm.vec2(config.mapa.nodes[v]['x'], config.mapa.nodes[v]['y'])

        # Calcular direção e normalizar
        direcao = ponto2 - ponto1
        direcao = glm.normalize(direcao)

        # Calcular o deslocamento perpendicular para a largura da estrada
        perpendicular = glm.vec2(-direcao.y, direcao.x) * (config.larguraPista / 2)

        # Calcular vértices do quadrilátero
        vertices = [
            ponto1 + perpendicular,
            ponto1 - perpendicular,
            ponto2 - perpendicular,
            ponto2 + perpendicular,
        ]
        
        # Desenhar o quadrilátero
        for vertex in vertices:
            glVertex2f(vertex.x, vertex.y)
    glEnd()
    
    # Segunda parte: Conexão das quinas com tratamento aprimorado
    glBegin(GL_TRIANGLES)
    for node in config.mapa.nodes():
        neighbors = list(config.mapa.neighbors(node))
        if len(neighbors) < 2:
            continue  # Precisa de pelo menos duas estradas para formar uma quina

        ponto_central = glm.vec2(config.mapa.nodes[node]['x'], config.mapa.nodes[node]['y'])
        
        # Ordenar vizinhos em sentido horário
        angles = []
        for neighbor in neighbors:
            ponto_vizinho = glm.vec2(config.mapa.nodes[neighbor]['x'], config.mapa.nodes[neighbor]['y'])
            angle = np.arctan2(ponto_vizinho.y - ponto_central.y, ponto_vizinho.x - ponto_central.x)
            angles.append((angle, neighbor))
        angles.sort()

        for i in range(len(angles)):
            _, vizinho1 = angles[i]
            _, vizinho2 = angles[(i + 1) % len(angles)]
            ponto_vizinho1 = glm.vec2(config.mapa.nodes[vizinho1]['x'], config.mapa.nodes[vizinho1]['y'])
            ponto_vizinho2 = glm.vec2(config.mapa.nodes[vizinho2]['x'], config.mapa.nodes[vizinho2]['y'])

            # Calcular os vetores de direção
            direcao1 = glm.normalize(ponto_vizinho1 - ponto_central)
            direcao2 = glm.normalize(ponto_vizinho2 - ponto_central)

            # Calcular os deslocamentos para a largura da estrada
            perpendicular1 = glm.vec2(-direcao1.y, direcao1.x) * (config.larguraPista / 2)
            perpendicular2 = glm.vec2(-direcao2.y, direcao2.x) * (config.larguraPista / 2)

            # Desenhar triângulo na quina
            glVertex2f(ponto_central.x + perpendicular1.x, ponto_central.y + perpendicular1.y)
            glVertex2f(ponto_central.x + perpendicular2.x, ponto_central.y + perpendicular2.y)
            glVertex2f(ponto_central.x, ponto_central.y)

            # Desenhar vértices intermediários para garantir preenchimento correto na quina
            glVertex2f(ponto_central.x + perpendicular1.x, ponto_central.y + perpendicular1.y)
            glVertex2f(ponto_central.x + perpendicular2.x, ponto_central.y + perpendicular2.y)
            glVertex2f(ponto_central.x, ponto_central.y)
    glEnd()




def drawPoints():
    glColor3f(1.0, 0.0, 0.0)  # Cor vermelha
    num_segments = 100  # Número de segmentos do círculo
    radius = 0.00007  # Raio do círculo

    for point in config.points:
        glBegin(GL_POLYGON)
        for i in range(num_segments):
            theta = 2.0 * math.pi * i / num_segments  # Ângulo atual
            x = radius * math.cos(theta)  # Coordenada x do ponto no círculo
            y = radius * math.sin(theta)  # Coordenada y do ponto no círculo
            glVertex2f(point[0] + x, point[1] + y)  # Adiciona o ponto ajustado
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
    police.desenha()
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf(np.asarray(glm.transpose(config.M))) # função que aplica uma matriz qualquer no objeto
    carro.desenha()
    
    glPopMatrix()
    glutSwapBuffers()