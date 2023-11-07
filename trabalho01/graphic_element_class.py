from OpenGL.GL import *
import math
import numpy as np

# graphic_element: classe para criação de elementos que se movimentam no cenário
# Esta classe é genérica, sendo utilizada principalmente para objetos criados pelo próprio programador
class graphic_element:
    def __init__(   self, 
                    inicial_vert = 0, num_vert = 0, 
                    pos_x = 0, pos_y = 0, pos_z = 0,
                    angle_x = 0, angle_y = 0, angle_z = 0,
                    scale = 1,
                    linear_speed = 0.05, angular_speed = 0.139, scale_speed = 0.2,
                    limit_sup = 1,
                    limit_inf = -1):
        # Atributos de identificação
        # Inicialmente estes atributos são inicializados com valores falsos, mas são alterados em seguida
        self._inicial_vert = inicial_vert   # Vértice inicial da onde deve partir a diretiva geométrica
        self._num_vert = num_vert           # Quantidade de vértices que o polígono tem
        # Mapa de eixo
        self.map_eixo = {}
        self.map_eixo['x'] = 0
        self.map_eixo['y'] = 1
        self.map_eixo['z'] = 2
        # Atributos de posição
        self._pos = [pos_x, pos_y, pos_z]   # Posição "central"
        self._linear_speed = linear_speed   # Velocidade do objeto para qualquer eixo
        self._limit_sup = limit_sup         # Limite superior dos dois eixos
        self._limit_inf = limit_inf         # Limite inferior dos dois eixos
        # Atributos de rotação
        self._angle = [angle_x, angle_y, angle_z]
        self._angular_speed = angular_speed
        self._cos = [math.cos(angle_x), math.cos(angle_y), math.cos(angle_z)]
        self._sin = [math.sin(angle_x), math.sin(angle_y), math.sin(angle_z)]
        # Atributos de escala
        self._scale = scale
        self._scale_speed = scale_speed
        # Indica quando o objeto está ativado ou não para ser desenhado
        self._on = False
        # Indica ativação ou não da textura do objeto
        self._polygonal_mode = GL_FILL

    # Ativa e desativa a textura do objeto
    def turn_texture(self):
        if self._polygonal_mode == GL_LINE:
            self._polygonal_mode = GL_FILL
        else:
            self._polygonal_mode = GL_LINE

    # Altera valores de idenficação para desenho
    # Entrada: 
        # Vértice inicial da onde deve partir a diretiva geométrica
        # Número de vértices do objeto
    def set_identification(self, inicial_vert, num_vert):
        self._inicial_vert = inicial_vert
        self._num_vert = num_vert
    
    # Calcula a validade da nova escala do objeto com base no limite de borda
    def _verify_limit(self,
                    new_value,
                    old_value,
                    pos = [False, False, False],
                    angle = [False, False, False],
                    scale = False):
        return new_value
    
    # Retorna estado de ativação do objeto
    def get_on(self):
        return self._on

    # Seta true para ativação do objeto
    def set_on(self):
        self._on = True
    
    # Seta off para ativação do objeto
    def set_off(self):
        self._on = False
    
    # Movimenta o objeto
    # Entrada: operação de somar ou subtrair, além do eixo da movimentação
    def move(self, operation, eixo):
        # A combinação da escolha 'somar','subtrair' e eixo gera todas as movimentações
        if self._on: # Se o objeto estiver ativo
            new_pos = old_pos = self._pos[self.map_eixo[eixo]]
            # Calcula a nova posição
            if operation == '+':
                new_pos += self._linear_speed
            elif operation == '-':
                new_pos -= self._linear_speed
            # Verifica se ela é válida e atribui
            pos_flag = [False, False, False]
            pos_flag[self.map_eixo[eixo]] = True
            if self._verify_limit(new_pos, old_pos, pos = pos_flag):
                self._pos[self.map_eixo[eixo]] = new_pos

    # Rotaciona o objeto
    # Entrada: operação de somar ou subtrair, além do eixo da rotação
    def rotate(self, operation, eixo):
        # A combinação da escolha 'somar','subtrair' e eixo gera todas as rotações
        if self._on:
            new_angle = old_angle = self._angle[self.map_eixo[eixo]]
            # Calcula o novo ângulo
            if operation == '+':
                new_angle += self._angular_speed
            elif operation == '-':
                new_angle -= self._angular_speed
            angle_flag = [False, False, False]
            angle_flag[self.map_eixo[eixo]] = True
            if self._verify_limit(new_angle, old_angle, angle = angle_flag):
                self._angle[self.map_eixo[eixo]] = new_angle
                self._cos[self.map_eixo[eixo]] = math.cos(new_angle)
                self._sin[self.map_eixo[eixo]] = math.sin(new_angle)

    # Escala o objeto
    # Entrada: operação de somar ou subtrair
    def distort(self, operation):
        if self._on:
            # Calcula a nova escala
            new_scale = old_scale = self._scale
            if operation == '+':
                new_scale += self._scale_speed
            elif operation == '-':
                new_scale -= self._scale_speed
            # Verifica se ela é válida e atribui
            if self._verify_limit(new_scale, old_scale, scale = True):
                self._scale = new_scale
    
    # Retorna a matriz de translação do objeto
    def _mat_translation(self):
        return np.array([   1.0, 0.0, 0.0, self._pos[0], 
                            0.0, 1.0, 0.0, self._pos[1], 
                            0.0, 0.0, 1.0, self._pos[2], 
                            0.0, 0.0, 0.0,        1.0], np.float32)
    
    # Retorna a matriz de escala do objeto
    def _mat_scale(self):
        return np.array([     self._scale,           0.0,           0.0, 0.0, 
                                      0.0,   self._scale,           0.0, 0.0, 
                                      0.0,           0.0,   self._scale, 0.0, 
                                      0.0,           0.0,           0.0, 1.0], np.float32)
    
    # Retorna a matriz de rotação no eixo z do objeto
    def _rotation_z(self):  
        return np.array([   self._cos[2], -self._sin[2], 0.0, 0.0, 
                            self._sin[2],  self._cos[2], 0.0, 0.0, 
                                     0.0,           0.0, 1.0, 0.0, 
                                     0.0,           0.0, 0.0, 1.0], np.float32)
    
    # Retorna a matriz de rotação no eixo x do objeto
    def _rotation_x(self): 
        return np.array([   1.0,          0.0,           0.0, 0.0, 
                            0.0, self._cos[0], -self._sin[0], 0.0, 
                            0.0, self._sin[0],  self._cos[0], 0.0, 
                            0.0,          0.0,           0.0, 1.0], np.float32)
    
    # Retorna a matriz de rotação no eixo y do objeto
    def _rotation_y(self):
        return np.array([    self._cos[1],  0.0, self._sin[1], 0.0, 
                                      0.0,  1.0,          0.0, 0.0, 
                            -self._sin[1],  0.0, self._cos[1], 0.0, 
                                      0.0,  0.0,          0.0, 1.0], np.float32)
    # Desenha o objeto na tela
    # Entrada: localizações dos qualificadores uniformes no shader relativos as matrizes de transformação geométrica
    def draw(self, locs, gl_Draw = GL_TRUE):
        if self._on:
            # Separando localizacões de matrizes
            loc_mat_pre_transl = locs[0]
            loc_mat_rot_x = locs[1]
            loc_mat_rot_y = locs[2]
            loc_mat_rot_z = locs[3]
            loc_mat_scale = locs[4]
            loc_mat_transl = locs[5]
            # Define se será mostrado a textura ou não
            glPolygonMode(GL_FRONT_AND_BACK, self._polygonal_mode)
            # Envia as matrizes de transformação
            glUniformMatrix4fv(loc_mat_pre_transl, 1, gl_Draw, np.identity(4)) 
            glUniformMatrix4fv(loc_mat_rot_x, 1, gl_Draw, self._rotation_x()) 
            glUniformMatrix4fv(loc_mat_rot_y, 1, gl_Draw, self._rotation_y()) 
            glUniformMatrix4fv(loc_mat_rot_z, 1, gl_Draw, self._rotation_z()) 
            glUniformMatrix4fv(loc_mat_scale, 1, gl_Draw, self._mat_scale()) 
            glUniformMatrix4fv(loc_mat_transl, 1, gl_Draw, self._mat_translation()) 
            # Desenha o objeto com primitiva GL_TRIANGLES
            glDrawArrays(GL_TRIANGLES, self._inicial_vert, self._num_vert)