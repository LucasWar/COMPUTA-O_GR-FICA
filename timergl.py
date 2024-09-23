from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from utils import vericarCarroEstrada, calcMatrix, update_projection
import glm
import config

def timer(v):
    glutTimerFunc(int(1000/config.FPS), timer, 0)  # a cada frame é necessário chamar essa função para 'agendar' a sua próxima execução

    previous_pos = config.pos
    previous_dir = config.dir
    previous_lat = config.lat

    if config.movimento_ativo:
        if config.index_caminho < len(config.caminho_atual):
            destino = glm.vec3(config.caminho_atual[config.index_caminho][0], config.caminho_atual[config.index_caminho][1], 0)
            direcao = glm.normalize(destino - config.pos)
            distancia = glm.length(destino - config.pos)

            angle_difference = glm.degrees(glm.acos(glm.dot(glm.normalize(config.dir), glm.normalize(direcao))))
        
            if angle_difference >= config.velocAng:
                # Calculate the rotation axis (perpendicular to the plane of movement)
                rotation_axis = glm.cross(config.dir, direcao)
                rotation_angle = min(config.velocAng, angle_difference)  # Rotate by the smaller of the angular velocity or the angle difference

                # Apply the rotation to the current direction
                config.dir = glm.rotate(config.dir, glm.radians(rotation_angle), rotation_axis)
                config.lat = glm.vec3(-config.dir.y, config.dir.x, 0)  # Update the "up" direction

                # Recalculate the direction to ensure we continue rotating towards the destination
                calcMatrix()
                update_projection()

                glutPostRedisplay()
                return  # Skip the position update this frame if the car is still aligning


            if distancia < config.velocDir:
                config.pos = destino
                config.index_caminho += 1
                if config.index_caminho >= len(config.caminho_atual):
                    config.velocDir = 0.0000001
                    config.movimento_ativo = False
            else:
                config.pos += config.velocDir * direcao

            config.dir = direcao
            config.lat = glm.vec3(-direcao.y, direcao.x, 0)  # Direção "up" ajustada para a direção do movimento

            if not vericarCarroEstrada():
                config.pos = previous_pos
                config.dir = previous_dir
                config.lat = previous_lat
        else:
            print("AQUI")
            config.movimento_ativo = False
            config.velocDir = 0.0000001

    else:
        if config.frente:
            config.pos = config.pos + config.velocDir * config.dir
        if config.tras:
            config.pos = config.pos - config.velocDir * config.dir
        if config.esquerda:
            config.dir = glm.rotate(config.velocAng) * config.dir
            config.lat = glm.rotate(config.velocAng) * config.lat
        if config.direita:
            config.dir = glm.rotate(-config.velocAng) * config.dir
            config.lat = glm.rotate(-config.velocAng) * config.lat
    
        if not vericarCarroEstrada():
            config.pos = previous_pos
            config.dir = previous_dir
            config.lat = previous_lat

    if config.frente or config.tras or config.esquerda or config.direita or config.movimento_ativo:
        calcMatrix()
        update_projection()
    glutPostRedisplay()

def iniciar_movimento():
    if config.caminhoFinal:
        config.index_caminho = 0
        config.movimento_ativo = True
        if config.caminho_atual:
            config.pos = glm.vec3(config.caminho_atual[0][0], config.caminho_atual[0][1], 0)
            calcMatrix()
