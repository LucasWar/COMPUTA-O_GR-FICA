from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import config
import os
class Carro:
    def __init__(self, textura_file = 'C://Users//Lucas//Desktop//trabalhoFinalCG//carro.png'):
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
        
        glBindTexture(GL_TEXTURE_2D, self.texCarro) # ativando a textura do carro
        glBegin(GL_QUADS)                           # desenhando um quadrado
        glTexCoord2f(0,0)                           # coordenada da textura do canto inferior esquerdo
        glVertex2f(-config.tamCarro,-config.tamCarro)                           # vértice inferior esquerdo
        glTexCoord2f(1,0)                           # coordenada da textura do canto inferior direito
        glVertex2f( config.tamCarro,-config.tamCarro)                           # vértice inferior direito
        glTexCoord2f(1,1)                           # coordenada da textura do canto superior direito
        glVertex2f( config.tamCarro, config.tamCarro)                           # vértice superior direito
        glTexCoord2f(0,1)                           # coordenada da textura do canto superior esquerdo
        glVertex2f(-config.tamCarro, config.tamCarro)                           # vértice superior esquerdo
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)             # desativando a textura do carro
        glPopMatrix()