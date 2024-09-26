from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import glm
import config
from utils import update_projection
from classCarro import Carro
from objetos import Icone
from elementosClass import elemento
from timergl import iniciarLuz,atuaalizarPontoDeLuz
import math
from PIL import Image
def init():
    global carro, police, predio , alerta, semaforo, sensor,grama,park, water
    glClearColor(0.5, 0.5, 0.5, 1.0)
    update_projection()
    iniciarLuz()
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_MULTISAMPLE)                           
    glEnable(GL_TEXTURE_2D)                            
    glEnable(GL_BLEND);                           
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)   
    carro = Carro()
    police = Icone(config.posIcones,'imgs//policeIcone.png',(0,0,0))
    alerta = Icone(config.posIconesAlertas,'imgs//alerta.png',(1,0.77,0.18))
    semaforo = Icone(config.posIconesSemaforo,'imgs//Semaforo.png',(1,1,0))
    sensor = Icone(config.posIconesSensor,'imgs//speed limit60.png',(0,0,0))
    predio = carregaTextura('imgs//texture2.jpg')

    grama = elemento(config.gramaCoord,'imgs//gramaText.jfif')
    park = elemento(config.parkCoord,'imgs//gramaText.jfif')
    water = elemento(config.waterCoord,'imgs//waterText.jfif')

def carregaTextura(filename):
    
    img = Image.open(filename)                  
    img = img.transpose(Image.FLIP_TOP_BOTTOM)  
    imgData = img.convert("RGBA").tobytes()     

    
    texId = glGenTextures(1)                                                                                
    glBindTexture(GL_TEXTURE_2D, texId)                                                                     
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)                                        
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)                                        
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)                                              
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,  img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)  
    glBindTexture(GL_TEXTURE_2D, 0)                                                                         

    return texId

def desenharCaminho():
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)  
    if config.caminhoFinal:
        glColor(0.43, 0.72, 1) 
        glBegin(GL_QUADS)  
        pontos = list(config.caminhoFinal.items())
        
        for i in range(len(pontos) - 1):
            
            ponto1 = glm.vec2(pontos[i][1])
            ponto2 = glm.vec2(pontos[i + 1][1])


            direcao = ponto2 - ponto1
            direcao = glm.normalize(direcao)


            perpendicular = glm.vec2(-direcao.y, direcao.x) * (config.larguraPista / 2)


            vertices = [
                ponto1 + perpendicular,
                ponto1 - perpendicular,
                ponto2 - perpendicular,
                ponto2 + perpendicular,
            ]


            for vertex in vertices:
                glVertex2f(vertex.x, vertex.y)


            if i > 0:
                ponto_prev = glm.vec2(pontos[i - 1][1])
                direcao_prev = ponto1 - ponto_prev
                direcao_prev = glm.normalize(direcao_prev)
                perpendicular_prev = glm.vec2(-direcao_prev.y, direcao_prev.x) * (config.larguraPista / 2)


                glVertex2f(ponto1.x + perpendicular_prev.x, ponto1.y + perpendicular_prev.y)
                glVertex2f(ponto1.x + perpendicular.x, ponto1.y + perpendicular.y)
                glVertex2f(ponto1.x - perpendicular.x, ponto1.y - perpendicular.y)
                glVertex2f(ponto1.x - perpendicular_prev.x, ponto1.y - perpendicular_prev.y)
        
        glEnd()
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0) 
def desenharElementos():
    texturaGrama = carregaTextura("imgs//gramaText.jfif")
    glBindTexture(GL_TEXTURE_2D, texturaGrama) 
    glEnable(GL_TEXTURE_2D) 

    for caracte in config.naturalElementos:
        cor = caracte[0]
        pontos = caracte[1]
        glColor3f(cor[0], cor[1], cor[2])  
        for geometry in pontos['geometry']:
            if geometry.geom_type == 'Polygon':
                borda = geometry.exterior
                coordenadas = list(borda.coords)
                glBegin(GL_POLYGON)
                for i, coord in enumerate(coordenadas):
                    
                    glTexCoord2f(i % 2, i // 2)
                    glVertex2f(coord[0], coord[1])
                glEnd()
            elif geometry.geom_type == 'MultiPolygon':
                for poly in geometry.geoms:
                    borda = poly.exterior
                    coordenadas = list(borda.coords)
                    glBegin(GL_POLYGON)
                    for i, coord in enumerate(coordenadas):
                        glTexCoord2f(i % 2, i // 2)
                        glVertex2f(coord[0], coord[1])
                    glEnd()

    glDisable(GL_TEXTURE_2D)  
    glBindTexture(GL_TEXTURE_2D, 0) 

def desenharPredios():
    glColor3f(0.3, 0.3, 0.3)

    for geometry in config.predios['geometry']:
        if geometry.geom_type == 'Polygon':
            desenharPredio3d(geometry)
        elif geometry.geom_type == 'MultiPolygon':
            for poly in geometry.geoms:
                desenharPredio3d(poly)

def desenharPredio3d(polygon, altura=0.0001):
    
    coordenadas = list(polygon.exterior.coords)
    glBegin(GL_POLYGON)
    for coord in coordenadas:
        glVertex3f(coord[0], coord[1], 0)
    glEnd()

    
    glBindTexture(GL_TEXTURE_2D, predio)
    glBegin(GL_QUADS)
    for i in range(len(coordenadas) - 1):
        x1, y1 = coordenadas[i]
        x2, y2 = coordenadas[i+1]
        
    
        glTexCoord2f(1,0)
        glVertex3f(x1, y1, 0)
        glTexCoord2f(0,0)
        glVertex3f(x2, y2, 0)
        glTexCoord2f(0,1)
        glVertex3f(x2, y2, altura)
        glTexCoord2f(1,1)
        glVertex3f(x1, y1, altura)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)    
    
    glBegin(GL_POLYGON)
    for coord in coordenadas:
        glVertex3f(coord[0], coord[1], altura)
    glEnd()


def drawMap():
    glColor3f(0.3, 0.3, 0.3)
    
    
    glBegin(GL_QUADS)
    for u, v, data in config.mapa.edges(keys=False, data=True):
    
        ponto1 = glm.vec2(config.mapa.nodes[u]['x'], config.mapa.nodes[u]['y'])
        ponto2 = glm.vec2(config.mapa.nodes[v]['x'], config.mapa.nodes[v]['y'])

    
        direcao = ponto2 - ponto1
        direcao = glm.normalize(direcao)

    
        perpendicular = glm.vec2(-direcao.y, direcao.x) * (config.larguraPista / 2)


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
    glColor3f(1.0, 0.0, 0.0)  
    num_segments = 100  
    radius = 0.00007  

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


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawMap()
    glPushMatrix()
   
    glEnable(GL_DEPTH_TEST)
    desenharPredios()
    glDisable(GL_DEPTH_TEST)

    glPopMatrix()    

    desenharCaminho()

    glPushMatrix()
    park.desenha()
    water.desenha()
    grama.desenha()
    glPopMatrix()
    drawPoints()

    glPushMatrix()
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0) 
    glEnable(GL_DEPTH_TEST)
    police.desenha()
    alerta.desenha()
    sensor.desenha()
    semaforo.desenha()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0) 
    glPopMatrix()

    glPushMatrix()
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0) 
    glMultMatrixf(np.asarray(glm.transpose(config.M))) # função que aplica uma matriz qualquer no objeto
    carro.desenha()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0) 
    glPopMatrix()

    atuaalizarPontoDeLuz()
    glutSwapBuffers()