from OpenGL.GL import *
from PIL import Image

class elemento:
    def __init__(self, elemento, caminho_textura):
        self.elemento = elemento
        self.textura = self.carregarTextura(caminho_textura)

    def carregarTextura(self, filename):
        # Carregamento da textura com PIL
        img = Image.open(filename)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        imgData = img.convert("RGBA").tobytes()

        texId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)
        glBindTexture(GL_TEXTURE_2D, 0)

        return texId

    def desenha(self):
        glBindTexture(GL_TEXTURE_2D, self.textura)  # Ativa a textura
        glEnable(GL_TEXTURE_2D)  # Habilita o mapeamento de textura

        pontos = self.elemento

        for geometry in pontos['geometry']:
            if geometry.geom_type == 'Polygon':
                borda = geometry.exterior
                coordenadas = list(borda.coords)
                glBegin(GL_POLYGON)
                for i, coord in enumerate(coordenadas):
                    # Aplica as coordenadas da textura baseadas no índice
                    glTexCoord2f(i % 2, i // 2)
                    glVertex2f(coord[0], coord[1])
                glEnd()
            elif geometry.geom_type == 'MultiPolygon':
                for poly in geometry.geoms:
                    borda = poly.exterior
                    coordenadas = list(borda.coords)
                    glBegin(GL_POLYGON)
                    for i, coord in enumerate(coordenadas):
                        glTexCoord2f(i % 2, i // 2)
                        glVertex2f(coord[0], coord[1])
                    glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)  # Desativa a textura