from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import random
import config
import glm

def update_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width = (config.x_max - config.x_min)
    height = (config.y_max - config.y_min)
    aspect_ratio = 800 / 600

    if config.current_mode == "perspective":
        fov = 60.0 
        near = 0.001 
        far = 1000.0  # Plano distante
        gluPerspective(fov, aspect_ratio, near, far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera_distance = 0.001  # Distância da câmera atrás do carro
        camera_height = 0.0008  # Altura da câmera acima do carro
        camera_position = config.pos - config.dir * camera_distance + glm.vec3(0, 0, camera_height)
        look_at_point = config.pos + config.dir * 0.001  # Ponto para onde a câmera está olhando
        up_vector = glm.vec3(0, 0, 1)  # Vetor "up" da câmera
        gluLookAt(camera_position.x, camera_position.y, camera_position.z,
                  look_at_point.x, look_at_point.y, look_at_point.z,
                  up_vector.x, up_vector.y, up_vector.z)
        
    elif config.current_mode == "ortho":
        width = (config.x_max - config.x_min) * config.qtdZoom
        height = (config.y_max - config.y_min) * config.qtdZoom
        glOrtho(-width / 2, width / 2, -height / 2, height / 2, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(config.camera_x, config.camera_y, 1,  # Posicionar a câmera no eixo Z
                  config.camera_x, config.camera_y, 0,  # Olhar para o centro do config.mapa
                  0, 1, 0)  # Vetor de "up"
                  
def telaParaMapa(x, y):
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    map_width = (config.x_max - config.x_min) * config.qtdZoom
    map_height = (config.y_max - config.y_min) * config.qtdZoom
    mapX = config.camera_x + (x / width - 0.5) * map_width
    mapY = config.camera_y - (y / height - 0.5) * map_height
    return mapX, mapY

def buscaVizinhosDoPonto(mapX, mapY, tolerance=0.000001):
    
    edges_and_vertices = []

    for u, v, data in config.mapa.edges(keys=False, data=True):
        x1, y1 = config.mapa.nodes[u]['x'], config.mapa.nodes[u]['y']
        x2, y2 = config.mapa.nodes[v]['x'], config.mapa.nodes[v]['y']

        # Verificar se o ponto (mapX, mapY) está na linha entre (x1, y1) e (x2, y2)
        if verificarSeguimento((x1, y1), (x2, y2), (mapX, mapY), tolerance):
            if (x1, y1) not in edges_and_vertices:
                edges_and_vertices.append((x1, y1))
            if (x2, y2) not in edges_and_vertices:
                edges_and_vertices.append((x2, y2))
    return edges_and_vertices

def verificarSeguimento(A, B, P, tolerance):
    A = np.array(A)
    B = np.array(B)
    P = np.array(P)
    AB = B - A
    AP = P - A
    BP = P - B

    # Projeção do ponto P no segmento AB
    AB_length_squared = np.dot(AB, AB)
    if AB_length_squared == 0:
        distance = np.linalg.norm(AP)
    else:
        t = np.dot(AP, AB) / AB_length_squared
        t = max(0, min(1, t))
        projection = A + t * AB
        distance = np.linalg.norm(projection - P)

    return distance <= tolerance


def buscarPontoMaisProximo(mapX, mapY):

    min_dist = float('inf')
    nearest_point = None

    for u, v, data in config.mapa.edges(keys=False, data=True):
        x1, y1 = config.mapa.nodes[u]['x'], config.mapa.nodes[u]['y']
        x2, y2 = config.mapa.nodes[v]['x'], config.mapa.nodes[v]['y']

        # Calcular o ponto mais próximo na linha (x1, y1) - (x2, y2)
        A = np.array([x1, y1])
        B = np.array([x2, y2])
        P = np.array([mapX, mapY])
        AP = P - A
        AB = B - A
        AB_norm = AB / np.linalg.norm(AB)
        proj = np.dot(AP, AB_norm)
        proj = np.clip(proj, 0, np.linalg.norm(AB))
        closest_point = A + proj * AB_norm
        dist = np.linalg.norm(P - closest_point)

        if dist < min_dist:
            min_dist = dist
            nearest_point = closest_point

    return nearest_point

def vericarCarroEstrada():
    car_pos = glm.vec2(config.pos.x, config.pos.y) 
    for u, v, data in config.mapa.edges(keys=False, data=True):
        ponto1 = glm.vec2(config.mapa.nodes[u]['x'], config.mapa.nodes[u]['y'])
        ponto2 = glm.vec2(config.mapa.nodes[v]['x'], config.mapa.nodes[v]['y'])

        direcao = ponto2 - ponto1
        length = glm.length(direcao)
        direcao = glm.normalize(direcao)

        perpendicular = glm.vec2(-direcao.y, direcao.x) * (config.larguraPista / 2)

        vertices = [
            ponto1 + perpendicular,  
            ponto1 - perpendicular,  
            ponto2 - perpendicular,  
            ponto2 + perpendicular,  
        ]

        if verificarPontoPoligno(car_pos.x,car_pos.y,vertices):
            return True

    return False


def verificarPontoPoligno(x, y, vertices):
    num_vertices = len(vertices)
    inside = False

    p1x, p1y = vertices[0].x, vertices[0].y
    for i in range(num_vertices + 1):
        p2x, p2y = vertices[i % num_vertices].x, vertices[i % num_vertices].y
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def calcMatrix():
    # global pos, dir, lat, M
    config.M[0] = glm.vec4(config.lat,0)   # 1ª coluna é igual ao vetor i (vetor que aponta pra lateral direita do carro)
    config.M[1] = glm.vec4(config.dir,0)   # 2ª coluna é igual ao vetor j (vetor que aponta pra frente do carro)
    config.M[2] = glm.vec4(0,0,1,0) # 3ª coluna é igual ao vetor k (vetor que aponta para o topo do carro (direção do eixo z))
    config.M[3] = glm.vec4(config.pos,1)   # 4ª coluna é igual ao ponto O (posição do carro)


def attModeview(mode):
    config.current_mode = mode
    update_projection()
    glutPostRedisplay()


def gerarCordenadasIcones(mapa, n=5):
    # Obtem os nós e as coordenadas do mapa
    nodes = mapa.nodes(data=True, default=None)
    coords = np.array([(data['x'], data['y']) for node, data in nodes])

    cordenadasFinais = []

    # Pega 'n' coordenadas aleatórias
    coordenadas_aleatorias = random.sample(list(coords), n)

    for x,y in coordenadas_aleatorias:
        cordenadasFinais.append(glm.vec3(x,y,0))

    return cordenadasFinais