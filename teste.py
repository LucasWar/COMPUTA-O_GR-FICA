from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
from classCarro import Carro

# Exemplo de uso da classe Carro em um código principal
if __name__ == "__main__":
    from OpenGL.GLUT import *
    import glm

    # Variáveis globais
    FPS = 30              
    pos = glm.vec3(0,0,0) 
    dir = glm.vec3(0,1,0) 
    lat = glm.vec3(1,0,0) 
    M = glm.mat4(1)       
    velocDir = 10         
    velocAng = 0.1        
    frente   = False      
    tras     = False      
    esquerda = False      
    direita  = False      

    mundoAlt = 600        
    mundoLar = 799        
    janelaAlt = 705       
    janelaLar = 1366       

    carro = None

    # Função que calcula a matriz de mudança de base local do carro
    def calcMatrix():
        global pos, dir, lat, M
        M[0] = glm.vec4(lat,0)   
        M[1] = glm.vec4(dir,0)   
        M[2] = glm.vec4(0,0,1,0) 
        M[3] = glm.vec4(pos,1)   

    def eixos():
        glColor3f(0,0,0)
        glBegin(GL_LINES)
        glVertex2f(-900,0) # eixo x
        glVertex2f( 900,0)
        glVertex2f(0,-900) # eixo y
        glVertex2f(0, 900)
        glEnd()
    # Função de inicialização
    def inicio():
        global carro
        glClearColor(0.5,0.5,0.5,1)                         
        glLineWidth(30)                                      
        glEnable(GL_MULTISAMPLE)                            
        glEnable(GL_TEXTURE_2D)                             
        glEnable(GL_BLEND);                                 
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   
        carro = Carro()                          

    # Função que trata o pressionar de uma tecla especial
    def tecladoSpecial(key, x, y):
        global frente, tras, esquerda, direita
        if   key == GLUT_KEY_UP:    frente   = True
        elif key == GLUT_KEY_DOWN:  tras     = True
        elif key == GLUT_KEY_LEFT:  esquerda = True
        elif key == GLUT_KEY_RIGHT: direita  = True

    # Função que trata o soltar de uma tecla especial
    def tecladoUpSpecial(key, x, y):
        global frente, tras, esquerda, direita
        if   key == GLUT_KEY_UP:    frente   = False
        elif key == GLUT_KEY_DOWN:  tras     = False
        elif key == GLUT_KEY_LEFT:  esquerda = False
        elif key == GLUT_KEY_RIGHT: direita  = False

    # Função que será chamada a cada redimensionar da janela
    def reshape(w, h):
        global mundoLar, janelaAlt, janelaLar
        janelaLar = w            
        janelaAlt = h            
        mundoLar  = mundoAlt*w/h 
        glViewport(0,0,w,h)      

    # Função que será chamada a cada 1000/FPS milissegundos
    def timer(v):
        global pos, dir, lat

        glutTimerFunc(int(1000/FPS), timer, 0) 

        if frente:
            pos = pos + velocDir*dir
        if tras:
            pos = pos - velocDir*dir
        if esquerda:
            dir = glm.rotate(velocAng)*dir
            lat = glm.rotate(velocAng)*lat
        if direita:
            dir = glm.rotate(-velocAng)*dir
            lat = glm.rotate(-velocAng)*lat
        
        if frente or tras or esquerda or direita:
            calcMatrix()

        glutPostRedisplay()                    

    # Função que será chamada cada vez que o conteúdo da janela precisar ser redesenhado
    def desenha():
        glClear(GL_COLOR_BUFFER_BIT) 

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, janelaLar / janelaAlt, 1, 1000) 

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(pos[0] - (dir[0] * 40), pos[1] - (dir[1] * 40), 50, pos[0], pos[1], 1, dir[0], dir[1], dir[2])

        glBegin(GL_QUADS)                      
        glVertex2f(-10,-10)                    
        glVertex2f( 10,-10)                    
        glVertex2f( 10, 10)                    
        glVertex2f(-10, 10)                    
        glEnd()
        eixos()
        glPushMatrix()
        glMultMatrixf(np.asarray(glm.transpose(M))) 
        carro.desenha()
        glPopMatrix()

        glutSwapBuffers() 

    # Corpo inicial do código
    glutInit()                                  
    glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_RGB) 
    glutInitWindowSize(janelaLar,janelaAlt)     
    glutInitWindowPosition(0,0)                 
    glutCreateWindow('Mudança de Base')         
    inicio()                                    
    glutTimerFunc(int(1000/FPS), timer, 0)      
    glutSpecialFunc(tecladoSpecial)             
    glutSpecialUpFunc(tecladoUpSpecial)
    glutReshapeFunc(reshape)
    glutDisplayFunc(desenha)                    
    glutMainLoop()
