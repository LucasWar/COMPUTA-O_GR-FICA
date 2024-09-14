import osmnx as ox
import config
import numpy as np
from scipy.spatial import cKDTree
def gerarEdificios():
    pass

def carregarEdificios():
    return ox.features_from_point((config.latitude, config.longitude),tags={'building': True},dist=config.distMapa)
    
def carregarElementosNaturais(tag):
    return ox.features_from_point(((config.latitude,config.longitude)),dist=config.distMapa,tags={tag[0]:tag[1]})

def gerarMapa():
    mapa = ox.graph_from_point((config.latitude,config.longitude), dist=config.distMapa, network_type='all')
    # Obtem os limites das coordenadas x e y
    nodes = mapa.nodes(data=True, default=None)
    x_vals = [data['x'] for node, data in nodes]
    y_vals = [data['y'] for node, data in nodes]
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)


    # Cria a árvore KD para busca de vizinhos mais próximos
    coords = np.array([(data['x'], data['y']) for node, data in nodes])
    kdtree = cKDTree(coords)

    return mapa,x_min, x_max,y_min, y_max, coords