from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import config
import os
class Carro:
    def __init__(self, textura_file = 'imgs//carro.png'):
        self.texCarro = self.carregaTextura(textura_file)

    # Função responsável por carregar uma textura a partir do nome do arquivo
    def carregaTextura(self, filename):
        # carregamento da textura feita pelo módulo PIL
        img = Image.open(filename)                  # abrindo o arquivo da textura
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # espelhando verticalmente a textura (normalmente, a coordenada y das imagens cresce de cima para baixo)
        imgData = img.convert("RGBA").tobytes()     # convertendo a imagem carregada em bytes que serão lidos pelo OpenGL

        # criando o objeto textura dentro da máquina OpenGL
        texId = glGenTextures(1)                                                                                # criando um objeto textura
        glBindTexture(GL_TEXTURE_2D, texId)                                                                     # tornando o objeto textura recém criado ativo
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)                                        # suavização quando um texel ocupa vários pixels
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)                                        # suavização quanto vários texels ocupam um único pixel
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)                                              # definindo que a cor da textura substituirá a cor do polígono
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,  img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)  # enviando os dados lidos pelo módulo PIL para a OpenGL
        glBindTexture(GL_TEXTURE_2D, 0)                                                                         # tornando o objeto textura inativo por enquanto

        # retornando o identificador da textura recém-criada
        return texId
    
    # Função que desenha o carro (um quadrado de lado 2 centrado na origem com textura de carro)
    def desenha(self):
        glPushMatrix()
        glColor(1,1,1)
        # Desenha a base do triângulo (plano inferior)
        glBegin(GL_TRIANGLES)
        
        # Vértice inferior esquerdo
        glVertex3f(-config.tamCarro , -config.tamCarro, 0.0)
        
        # Vértice inferior direito
        glVertex3f(config.tamCarro , -config.tamCarro , 0.0)
        
        # Vértice superior (apontando para frente)
        glVertex3f(0.0, config.tamCarro, 0.0)
        
        glEnd()

        # Desenha a parte superior do triângulo (plano superior ligeiramente elevado)

        glColor(0,0,1)
        glBegin(GL_TRIANGLES)
        
        # Vértice inferior esquerdo elevado
        glVertex3f(-config.tamCarro, -config.tamCarro, 0.00001)
        
        # Vértice inferior direito elevado
        glVertex3f(config.tamCarro, -config.tamCarro, 0.00001)
        
        # Vértice superior elevado
        glVertex3f(0.0, config.tamCarro, 0.00001)
        
        glEnd()

        # Desenha as laterais para dar volume
        glColor(1,1,1)
        glBegin(GL_QUADS)
        
        # Lado esquerdo
        glVertex3f(-config.tamCarro, -config.tamCarro, 0.0)
        glVertex3f(0.0, config.tamCarro, 0.0)
        glVertex3f(0.0, config.tamCarro, 0.00001)
        glVertex3f(-config.tamCarro, -config.tamCarro, 0.00001)
        
        # Lado direito
        glVertex3f(config.tamCarro, -config.tamCarro, 0.0)
        glVertex3f(0.0, config.tamCarro, 0.0)
        glVertex3f(0.0, config.tamCarro, 0.00001)
        glVertex3f(config.tamCarro, -config.tamCarro, 0.00001)
        
        # Lado inferior
        glVertex3f(-config.tamCarro, -config.tamCarro, 0.0)
        glVertex3f(config.tamCarro, -config.tamCarro, 0.0)
        glVertex3f(config.tamCarro, -config.tamCarro, 0.00001)
        glVertex3f(-config.tamCarro, -config.tamCarro, 0.00001)
        
        glEnd()

        glPopMatrix()