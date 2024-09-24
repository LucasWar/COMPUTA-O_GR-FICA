from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import config
import glm
class Icone:
    def __init__(self,posIcones, iconeLoad,cor):
        self.icone = self.carregaTextura(iconeLoad)
        self.angulo_rotacao = 0
        self.posIcones = posIcones
        self.cor = cor 
    def carregaTextura(self, filename):
        # Carregamento da textura feita pelo módulo PIL
        img = Image.open(filename)                  # Abrindo o arquivo da textura
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # Espelhando verticalmente a textura (y cresce de cima para baixo)
        imgData = img.convert("RGBA").tobytes()     # Convertendo a imagem em bytes lidos pelo OpenGL

        # Criando o objeto textura na OpenGL
        texId = glGenTextures(1)                                                                                # Criando uma textura
        glBindTexture(GL_TEXTURE_2D, texId)                                                                     # Ativando a textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)                                        # Suavização
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)                                              # Cor da textura substitui a cor do polígono
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,  img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)  # Enviando dados da imagem para a OpenGL

        glBindTexture(GL_TEXTURE_2D, 0)                                                                         # Desativando temporariamente a textura

        # Retornando o identificador da textura recém-criada
        return texId


    def desenha(self):
        #todos esses +- 0.00000001 funciona para combater o z-fighting.
        for posIcone in self.posIcones:
            largura = config.larguraIcone - 0.000000001  # Largura do retângulo
            altura = config.alturaIcone  - 0.000000001  # Altura do retângulo
            profundidade = config.profundidadeIcone - 0.000000001 # Profundidade do retângulo

            glPushMatrix()
            glTranslatef(posIcone.x,posIcone.y,0)
            # Rotacionar em torno do eixo X para que as faces fiquem posicionadas corretamente
            glRotatef(90, 1, 0, 0)

            self.angulo_rotacao += 0.03  # Incremento do ângulo de rotação (ajuste para aumentar/diminuir a velocidade)

            # Aplicando a rotação no eixo Y

            if(glm.distance(config.pos,posIcone) <= 0.0009):
                glRotatef(self.angulo_rotacao, 0, 1, 0) 
            
            #desenhando o quadrado interno, caso não tenha esse quadrado acabara gerando um quadrado transparente somente com as texturas
            #dando para ver as texturas de trás e ficando com as texturas desconectadas
            glColor(self.cor)
            glBegin(GL_QUADS)
            glVertex3f(-largura, -altura,  profundidade - 0.00000001)  # Inferior esquerdo
            glVertex3f( largura, -altura,  profundidade - 0.00000001)  # Inferior direito
            glVertex3f( largura,  altura,  profundidade - 0.00000001)  # Superior direito
            glVertex3f(-largura,  altura,  profundidade - 0.00000001)  # Superior esquerdo

            glVertex3f(-largura, -altura, -profundidade + 0.00000001)  # Inferior esquerdo
            glVertex3f( largura, -altura, -profundidade + 0.00000001)  # Inferior direito
            glVertex3f( largura,  altura, -profundidade + 0.00000001)  # Superior direito
            glVertex3f(-largura,  altura, -profundidade + 0.00000001)  # Superior esquerdo

            glVertex3f(-largura, -altura, -profundidade + 0.00000001)  # Inferior esquerdo
            glVertex3f(-largura, -altura,  profundidade - 0.00000001)  # Inferior direito
            glVertex3f(-largura,  altura,  profundidade - 0.00000001)  # Superior direito
            glVertex3f(-largura,  altura, -profundidade + 0.00000001)  # Superior esquerdo

            glVertex3f( largura, -altura, -profundidade + 0.00000001)  # Inferior esquerdo
            glVertex3f( largura, -altura,  profundidade - 0.00000001)  # Inferior direito
            glVertex3f( largura,  altura,  profundidade - 0.00000001)  # Superior direito
            glVertex3f( largura,  altura, -profundidade + 0.00000001)  # Superior esquerdo

            glVertex3f(-largura, altura,  profundidade - 0.00000001)  # Inferior esquerdo
            glVertex3f( largura, altura,  profundidade - 0.00000001)  # Inferior direito
            glVertex3f( largura, altura, -profundidade + 0.00000001)  # Superior direito
            glVertex3f(-largura, altura, -profundidade + 0.00000001)  # Superior esquerdo

            glVertex3f(-largura, -altura,  profundidade - 0.00000001)  # Inferior esquerdo
            glVertex3f( largura, -altura,  profundidade - 0.00000001)  # Inferior direito
            glVertex3f( largura, -altura, -profundidade + 0.00000001)  # Superior direito
            glVertex3f(-largura, -altura, -profundidade + 0.00000001)
            glEnd()
            largura = config.larguraIcone+ 0.00000001  # Largura do retângulo
            altura = config.alturaIcone+ 0.00000001    # Altura do retângulo
            profundidade = config.profundidadeIcone+ 0.00000001
            
            glBindTexture(GL_TEXTURE_2D, self.icone)  # Ativando a textura
            
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(-largura, -altura,  profundidade + 0.0000005)  # Inferior esquerdo
            glTexCoord2f(1, 0); glVertex3f( largura, -altura,  profundidade + 0.0000005)  # Inferior direito
            glTexCoord2f(1, 1); glVertex3f( largura,  altura,  profundidade + 0.0000005)  # Superior direito
            glTexCoord2f(0, 1); glVertex3f(-largura,  altura,  profundidade + 0.0000005)  # Superior esquerdo

            glTexCoord2f(0, 0); glVertex3f(-largura, -altura, -profundidade - 0.0000005)  # Inferior esquerdo
            glTexCoord2f(1, 0); glVertex3f( largura, -altura, -profundidade - 0.0000005)  # Inferior direito
            glTexCoord2f(1, 1); glVertex3f( largura,  altura, -profundidade - 0.0000005)  # Superior direito
            glTexCoord2f(0, 1); glVertex3f(-largura,  altura, -profundidade - 0.0000005)  # Superior esquerdo

            glTexCoord2f(0, 0); glVertex3f(-largura, -altura, -profundidade - 0.0000005)  # Inferior esquerdo
            glTexCoord2f(1, 0); glVertex3f(-largura, -altura,  profundidade + 0.0000005)  # Inferior direito
            glTexCoord2f(1, 1); glVertex3f(-largura,  altura,  profundidade + 0.0000005)  # Superior direito
            glTexCoord2f(0, 1); glVertex3f(-largura,  altura, -profundidade - 0.0000005)  # Superior esquerdo

            glTexCoord2f(0, 0);glVertex3f( largura, -altura, -profundidade - 0.0000005)  # Inferior esquerdo
            glTexCoord2f(1, 0);glVertex3f( largura, -altura,  profundidade + 0.0000005)  # Inferior direito
            glTexCoord2f(1, 1);glVertex3f( largura,  altura,  profundidade + 0.0000005)  # Superior direito
            glTexCoord2f(0, 1);glVertex3f( largura,  altura, -profundidade - 0.0000005)  # Superior esquerdo

            glTexCoord2f(0, 0);glVertex3f(-largura, altura,  profundidade + 0.0000005)  # Inferior esquerdo
            glTexCoord2f(1, 0);glVertex3f( largura, altura,  profundidade + 0.0000005)  # Inferior direito
            glTexCoord2f(1, 1);glVertex3f( largura, altura, -profundidade - 0.0000005)  # Superior direito
            glTexCoord2f(0, 1);glVertex3f(-largura, altura, -profundidade - 0.0000005)  # Superior esquerdo

            glTexCoord2f(0, 0);glVertex3f(-largura, -altura,  profundidade + 0.0000005)  # Inferior esquerdo
            glTexCoord2f(1, 0);glVertex3f( largura, -altura,  profundidade + 0.0000005)  # Inferior direito
            glTexCoord2f(1, 1);glVertex3f( largura, -altura, -profundidade - 0.0000005)  # Superior direito
            glTexCoord2f(0, 1);glVertex3f(-largura, -altura, -profundidade - 0.0000005)  # Superior esquerdo

            glEnd()
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()

