from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import config
import os
class Carro:
    def __init__(self, textura_file = 'imgs//carro.png'):
        self.texCarro = self.carregaTextura(textura_file)

    
    def carregaTextura(self, filename):
    
        img = Image.open(filename)                  # abrindo o arquivo da textura
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # espelhando verticalmente a textura (normalmente, a coordenada y das imagens cresce de cima para baixo)
        imgData = img.convert("RGBA").tobytes()     # convertendo a imagem carregada em bytes que serão lidos pelo OpenGL

    
        texId = glGenTextures(1)                                                                                # criando um objeto textura
        glBindTexture(GL_TEXTURE_2D, texId)                                                                     # tornando o objeto textura recém criado ativo
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)                                        # suavização quando um texel ocupa vários pixels
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)                                        # suavização quanto vários texels ocupam um único pixel
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)                                              # definindo que a cor da textura substituirá a cor do polígono
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,  img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)  # enviando os dados lidos pelo módulo PIL para a OpenGL
        glBindTexture(GL_TEXTURE_2D, 0)                                                                         # tornando o objeto textura inativo por enquanto

    
        return texId
    
    
    def desenha(self):
        glPushMatrix()
        glColor(1,1,1)
    
        glBegin(GL_TRIANGLES)
        
    
        glVertex3f(-config.tamCarro , -config.tamCarro, 0.0)
        
    
        glVertex3f(config.tamCarro , -config.tamCarro , 0.0)
        
    
        glVertex3f(0.0, config.tamCarro, 0.0)
        
        glEnd()

    

        glColor(0,0,1)
        glBegin(GL_TRIANGLES)
        
    
        glVertex3f(-config.tamCarro, -config.tamCarro, 0.00001)
        
    
        glVertex3f(config.tamCarro, -config.tamCarro, 0.00001)
        
    
        glVertex3f(0.0, config.tamCarro, 0.00001)
        
        glEnd()

    
        glColor(1,1,1)
        glBegin(GL_QUADS)
        
    
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