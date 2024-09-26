from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from utils import vericarCarroEstrada, calcMatrix, update_projection
import glm
import config
import time
def iniciarLuz():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    luzPosicao = [0.0, 0.0, 1.0, 1.0] 
    luzDifusa = [1.0, 1.0, 1.0, 1.0]  
    luzAmbiente = [1, 1, 1, 1.0]  
    direcaoLuz = [1.0, 0.0, 0.0]  
    glLightfv(GL_LIGHT0, GL_POSITION, luzPosicao)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luzDifusa)
    glLightfv(GL_LIGHT0, GL_AMBIENT, luzAmbiente)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direcaoLuz)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)

    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 30.0)     # Atenuação linear
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 30)


    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 15.0)  
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 2.0)
    

def atuaalizarPontoDeLuz():
    luzPosicao = [config.pos.x, config.pos.y, 0.0005, 1]
    direcaoLuz = [config.dir.x, config.dir.y, -0.3]      
    glLightfv(GL_LIGHT0, GL_POSITION, luzPosicao)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direcaoLuz)
   
def timer(v):
    glutTimerFunc(int(1000/config.FPS), timer, 0)  

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
                
                rotation_axis = glm.cross(config.dir, direcao)
                rotation_angle = min(config.velocAng, angle_difference)

                
                config.dir = glm.rotate(config.dir, glm.radians(rotation_angle), rotation_axis)
                config.lat = glm.vec3(-config.dir.y, config.dir.x, 0) 

                calcMatrix()
                atuaalizarPontoDeLuz()
                update_projection()

                glutPostRedisplay()
                return  


            if distancia < config.velocDir:
                config.pos = destino
                config.index_caminho += 1
                if config.index_caminho >= len(config.caminho_atual):
                    time.sleep(2)
                    config.current_mode = "ortho"
                    config.velocDir = 0.0000001
                    config.movimento_ativo = False
                    
                    calcMatrix()
                    update_projection()
                    atuaalizarPontoDeLuz()
            else:
                config.pos += config.velocDir * direcao

            config.dir = direcao
            config.lat = glm.vec3(-direcao.y, direcao.x, 0)

            if not vericarCarroEstrada():
                config.pos = previous_pos
                config.dir = previous_dir
                config.lat = previous_lat
        else:
            time.sleep(2)
            config.current_mode = "ortho"
            config.movimento_ativo = False
            config.velocDir = 0.0000001
            
            calcMatrix()
            update_projection()
            atuaalizarPontoDeLuz()

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
