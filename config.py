import glm
from collections import defaultdict
from loadMap import *
# global latitude
# global longitude

latitude = -4.9261
longitude = -37.9743
distMapa = 1300

elementos = {
    'leisure': 'park',            
    'natural': 'water',           
    'landuse': 'grass'
}

coresElementos = [[0,0,0],[0.2,0.3,0.7],[0,0.7,0.2]]
naturalElementos = []

for (chave, valor), cor in zip(elementos.items(), coresElementos):
    naturalElementos.append([cor, carregarElementosNaturais([chave, valor])])

predios = carregarEdificios()

mapa,x_min, x_max,y_min, y_max, coords = gerarMapa()

current_mode = "ortho"

anguloMinimoCurva = 180

distanciaSegmento = 40

#variavies carro
FPS = 60             # quantidade de frames por segundo que deseja-se atualizar a aplicação
pos = glm.vec3(-37.97284880149743,-4.925185938966515,0) # posição do carro (representando a origem do eixo local)
dir = glm.vec3(0,1,0) # vetor direção do carro (vetor j representando o eixo y local)
lat = glm.vec3(1,0,0) # vetor lateral do carro (vetor i representando o eixo x local)
M = glm.mat4(1)       # matriz de mudança de base
velocDir = 0.0001        # velocidade de deslocamento do carro
velocAng = 3       # velocidade de rotação do carro 
frente   = False      # controle teclado (seta cima)
tras     = False      # controle teclado (seta baixo)
esquerda = False      # controle teclado (seta esquerda) 
direita  = False      # controle teclado (seta direita)
tamCarro = 0.00007
turn_rate = 0.05  # Rate at which the car turns (radians per update)
target_dir = glm.vec2(0, 1)  # Target direction vector


tamIcone = 0.00007

caminho_atual = []
index_caminho = 0
movimento_ativo = False

carro = None
caminhoFinal = {}


qtdZoom = 1.0
larguraPista = 0.00009  # Largura inicial das estradas, ajustar conforme necessário
camera_x, camera_y = -37.9743, -4.9261
mousePres = False
ultCordMouseX = 0
ultCordMouseY = 0
points = []

matrizDeVizinhos = defaultdict(list)
novaMatrizDeVizinhos = defaultdict(list)


nodes = list(mapa.nodes())
for node in nodes:
    coords_node = mapa.nodes[node]['x'], mapa.nodes[node]['y']
    vizinhos = mapa.neighbors(node)
    for vizinho in vizinhos:
        coords_vizinho = mapa.nodes[vizinho]['x'], mapa.nodes[vizinho]['y']
        matrizDeVizinhos[coords_node].append(coords_vizinho)

for chave, valor in matrizDeVizinhos.items():
    novaMatrizDeVizinhos[chave] = valor.copy()



AGUA = False
PREDIOS = False