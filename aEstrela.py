import osmnx as ox
import math 
import numpy as np
from queue import PriorityQueue
from collections import defaultdict


# latitude = -4.9261
# longitude = -37.9743
# dist = 3000

import math
from queue import PriorityQueue

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def estrela(xp, yp, xf, yf, matrizDeVizinhos):
    # print("xp da estrela aqui",xp)
    caminho = {}
    g_score = {}
    f_score = {}

    for chave in matrizDeVizinhos:
        f_score[chave] = float("inf")
    g_score[(xp, yp)] = 0
    f_score[(xp, yp)] = g_score[(xp, yp)] + distance(xp, yp, xf, yf)
    fila = PriorityQueue()
    item = (f_score[(xp, yp)], distance(xp, yp, xf, yf), (xp, yp))
    fila.put(item)

    while not fila.empty():
        no = fila.get()[2]
        # print("AQUI ESTA O NO ",no)
        if no[0] == xf and no[1] == yf:
            break
        for noVizinho in matrizDeVizinhos[no]:
            # print("NO DENtro DO FOR 0 ",noVizinho[0])
            novo_g_score = g_score[no] + distance(no[0], no[1], noVizinho[0], noVizinho[1])
            novo_f_score = novo_g_score + distance(noVizinho[0], noVizinho[1], xf, yf)
            
            if novo_f_score < f_score.get(noVizinho, float("inf")):
                f_score[noVizinho] = novo_f_score
                g_score[noVizinho] = novo_g_score
                item = (novo_f_score, distance(noVizinho[0], noVizinho[1], xf, yf), noVizinho)
                fila.put(item)
                caminho[noVizinho] = no
    

    caminhoFinal = {}
    noAnalisado = (xf, yf)
    while noAnalisado != (xp, yp):
        caminhoFinal[caminho[noAnalisado]] = noAnalisado
        noAnalisado = caminho[noAnalisado]
    
    caminhoFinal[(xp, yp)] = caminhoFinal.get((xp, yp), None)  # Adiciona o nó inicial
    return caminhoFinal
        


# G = ox.graph_from_point((latitude, longitude), dist=dist, network_type='all')
# # # Obtenha os nós (vértices) do gráfico
# nodes = list(G.nodes())
# # [(-37.9671849, -37.9569376), (-37.9569376, -37.9644062), (-37.9569376, -37.9671849), (-37.9644062, -37.9569376)]
# # # Inicialize um dicionário para armazenar os vizinhos de cada nó
# vizinhos_dict = defaultdict(list)

# # # Preencha o dicionário com os vizinhos de cada nó
# for node in nodes:
#     # Obtenha as coordenadas de latitude e longitude do nó
#     coords_node = (G.nodes[node]['x'], G.nodes[node]['y'])
#     # Obtenha os vizinhos do nó
#     vizinhos = list(G.neighbors(node))
#     # Preencha o dicionário com as coordenadas dos vizinhos
#     for vizinho in vizinhos:
#         coords_vizinho = (G.nodes[vizinho]['x'], G.nodes[vizinho]['y'])
#         vizinhos_dict[coords_node].append(coords_vizinho)

# teste = estrela(-37.9876647, -4.9390912,-37.986896, -4.9422771,vizinhos_dict)
# print(teste)