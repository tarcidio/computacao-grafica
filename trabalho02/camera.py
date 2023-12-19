import glm
import numpy as np
from OpenGL.GL import *

def create_camera():
    # Posicao inicial da camera
    cameraPos   = glm.vec3(0.0,  1.0,  2.0)
    # Vetor responsável para apontar para frente
    cameraFront = glm.normalize(glm.vec3(0.0,  -0.25, -1.0))
    # Vetor auxiliar que aponta para cima em relação a camera
    cameraUp    = glm.vec3(0.0,  1.0,  0.0)

    return [cameraPos, cameraFront, cameraUp]

# Matriz view: posição e orientação da câmera no espaço 3D. Posiciona a cena em relação à câmera.
def view(cameraPos, cameraFront, cameraUp):
    # Parãmetros: posição da câmera, direção do target e câmera up. Câmera direita é calculado internamente pela função da biblioteca glm
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp)
    mat_view = np.array(mat_view)
    return mat_view

# Matriz Projection: transforma o volume de visualização 3D em um espaço 2D, levando em consideração fatores como a distância dos objetos à câmera
def projection(WIDTH_WINDOW, HEIGHT_WINDOW):
    # Neste caso, definimos parâmetros estáticos, mas poderiam ser dinâmicos
    fov = glm.radians(45.0)
    aspect = WIDTH_WINDOW/HEIGHT_WINDOW
    near = 0.1
    far = 100.0
    mat_projection = glm.perspective(fov, aspect, near, far)
    mat_projection = np.array(mat_projection)    
    return mat_projection

def send_data(program, cam, width, heigh):
    # Unpacking
    cameraPos = cam[0]
    cameraFront = cam[1]
    cameraUp = cam[2]

    # Capturando qualificadores view e projection
    loc_view = glGetUniformLocation(program, "view")
    loc_projection = glGetUniformLocation(program, "projection")

    # Atualiza matriz view e projection
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, view(cameraPos, cameraFront, cameraUp))
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, projection(width, heigh))  
    
     # Atualizando a posicao da câmera/observador na GPU para cálculo da reflexão especular
    loc_view_pos = glGetUniformLocation(program, "viewPos")
    glUniform3f(loc_view_pos, cameraPos[0], cameraPos[1], cameraPos[2])