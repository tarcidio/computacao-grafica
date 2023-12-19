from graphic_element_class import graphic_element
from OpenGL.GL import *
import math
import numpy as np
from PIL import Image

# obj_wave: classe para criação de objetos com textura importados
    # Esta classe é específica para objetos importados de wavefront
    # É filha da classe graphic_element
class obj_wave(graphic_element):
    def __init__(   self, 
                    id_texture, path_obj, path_jpg,
                    inicial_vert = 0, num_vert = 0,
                    pos_x = 0, pos_y = 0, pos_z = 0,
                    angle_x = 0, angle_y = 0, angle_z = 0,
                    scale = 1,
                    linear_speed = 0.05, angular_speed = 0.139, scale_speed = 0.2,
                    limit_sup = 1,
                    limit_inf = -1,
                    ka_speed = 0.1, ka = 1, kd = 1, ks = 1, ns = 0.10,
                    light_source = False,
                    geometric = False,
                    R = 1.0, G = 1.0, B = 1.0,
                    mag = GL_LINEAR,
                ):
        # Inicializa atributos da mãe
        super().__init__(   inicial_vert = inicial_vert, 
                            num_vert = num_vert,
                            pos_x = pos_x, pos_y = pos_y, pos_z = pos_z,
                            angle_x = angle_x, angle_y = angle_y, angle_z = angle_z,
                            scale = scale,
                            linear_speed = linear_speed, angular_speed = angular_speed, scale_speed = scale_speed,
                            limit_sup = limit_sup,
                            limit_inf = limit_inf,
                            ka_speed = ka_speed, ka = ka, kd = kd, ks = ks, ns = ns,
                            light_source = light_source,
                            geometric = geometric,
                            R = R, G = G, B = B
                        )
        # Atributos de identificação
        self._id_texture = id_texture   # id que identifica qual textura se está trabalhando
        self._path_obj = path_obj       # Caminho do arquivo .obj com malhas
        self._path_jpg = path_jpg       # Caminho do arquivo .jpg com texturas
        # Gerando modelos
        # Carregando os valores das coordenadas de maior e menor valor de cada eixo
        # Carregando valores médios de cada coordenada
        self._model, self._min_coord, self._max_coord, self._average_coord = self._load_model_from_file()
        # Encontra a maior diferença entre as coordenadas do objeto
        self._max_dif = self.find_max_dif()
        # Corrigindo escala para limita entre [-1,1]
        self._correct_scale = 1/(2*self._max_dif)
        self._scale = self._scale * self._correct_scale
        self._scale_speed *= self._correct_scale
        # Variável de magnificação que define se será linear ou nearest
        self._mag = mag
        # Carrega textura
        self._load_texture_from_file()
    
    # Alterna entre os modos de magnificação
    def turn_mag(self):
        if self._mag == GL_NEAREST:
            self._mag = GL_LINEAR
            self._load_texture_from_file()
        else:
            self._mag = GL_NEAREST
            self._load_texture_from_file()

    # Encontra a maior diferença entre as coordenadas do objeto
    def find_max_dif(self):
        max_dif = -1
        for i in range(0,3):
            max_dif = max(max_dif, abs(self._min_coord[i] - self._max_coord[i]))
        return max_dif

    # Calcula a posição final de uma coordenada fornecida
    def _calc_mat_pos_final(self, coord):
        pos_final = np.dot(self._mat_pre_translation().reshape(4,4), coord)
        pos_final = np.dot(self._rotation_z().reshape(4,4), pos_final)
        pos_final = np.dot(self._rotation_y().reshape(4,4), pos_final)
        pos_final = np.dot(self._rotation_x().reshape(4,4), pos_final)
        pos_final = np.dot(self._mat_scale().reshape(4,4), pos_final)
        return np.dot(self._mat_translation().reshape(4,4), pos_final)
    
    # Verifica se com a mudança de um atributo para o novo valor faz com que o objeto saida tela
    # Entrada: novo e antigo valor e flags indicando qual atributo está sendo alterado
    def _verify_limit(self,
                    new_value,
                    old_value,
                    pos = [False, False, False],
                    angle = [False, False, False],
                    scale = False): 
        
        # Atribui o novo valor ao atributo do objeto temporariamente
        if scale: self._scale = new_value         
        for i in range(0,3):
            if pos[i]: self._pos[i] = new_value
            if angle[i]: 
                self._cos[i] = math.cos(new_value)
                self._sin[i] = math.sin(new_value)
        # Calcula a posição máxima e minima
        pos_max_final = self._calc_mat_pos_final(np.array(self._max_coord + [1]).reshape(4,1))
        pos_min_final = self._calc_mat_pos_final(np.array(self._min_coord + [1]).reshape(4,1))
        # Retorna o valor antigo ao atributo do objeto
        if scale: self._scale = old_value   
        for i in range(0,3):
            if pos[i]: self._pos[i] = old_value
            if angle[i]: 
                self._cos[i] = math.cos(new_value)
                self._sin[i] = math.sin(new_value)
        # print(f'Valor max final: {pos_max_final}')
        # print(f'Valor min final: {pos_min_final}')
        # Verifica se a posição do máxima e mínima são aceitáveis
        for i in range(0,3):
            if (   pos_max_final[i] > self._limit_sup
                or pos_max_final[i] < self._limit_inf
                or pos_min_final[i] > self._limit_sup
                or pos_min_final[i] < self._limit_inf):
                # Se não for, retorna falso
                # print(f'Valor max final: {pos_max_final}')
                # print(f'Valor min final: {pos_min_final}')
                return False
        # Se fo, retorna true
        return True

    # Overriding: alterando a forma como o objeto deve se manter ativo
    def set_on(self, id):
        if id == self._id_texture:
            self._on = True
        else:
            self._on = False

    # Função: carrega o arquivo Wavefront
    # Entrada: nome do arquivo
    # Saida: estrutura que armazena o elemento (vertices, textura e faces)
    def _load_model_from_file(self):
        # Arrays que armazenaram informações de coordenadas ou vetores
        vertices = []       # Posições dos vértices
        texture_coords = [] # Coordenada dos vértices de textura
        normals = []        # Coordenada que define os vetores normais
        relations = []      # Modelo que conecta, a partir da funções dadas no .obj, 
                        # vértices do objeto, vértices dde textura e os vetores normais
        # Soma das coordenadas para média com intenção de centralizar posição
        sum_coord = [0, 0, 0]
        num_vertices = 0
        # Menor valor de cada eixo
        min_coord = [0x3f3f3f3f,0x3f3f3f3f,0x3f3f3f3f]
        # Maior valor de cada eixo
        max_coord = [-0x3f3f3f3f,-0x3f3f3f3f,-0x3f3f3f3f]

        # Não é utilizado, mas refere-se ao material do .obj
        material = None

        # Abre o arquivo obj (wavefront) para leitura
        for line in open(self._path_obj, "r"): ## para cada linha do arquivo .obj
            # Se for comentário, ignore esta linha e use a próxima
            if line.startswith('#'): continue

            # Quebra a linha por espaço
            values = line.split()
            # Se não há informações na linha, ignore esta linha e use a próxima
            if not values: continue

            # Recupera as informações
            ### Armazena coordenadas dos vertices do elemento no vetor vertices
            if values[0] == 'v':
                vertices.append(values[1:4])
                # Se alguma coordenada é maior que todas as outras
                for i in range(1,4):
                    if float(values[i]) > float(max_coord[i - 1]):
                        max_coord[i - 1] = float(values[i])
                    if float(values[i]) < float(min_coord[i - 1]):
                        min_coord[i - 1] = float(values[i])
                    sum_coord[i - 1] += float(values[i])
                # Somando coordenadas para fazer média
                num_vertices = num_vertices + 1
            ### Armazena vetor normais no vetor normals
            elif values[0] == 'vn':
                normals.append(values[1:4])
            ### Armazena coordenadas das texturas no vetor texture_coords
            elif values[0] == 'vt':
                texture_coords.append(values[1:3])
            ### Define o material 
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            ### Armazena informações sobre a construção das faces
            elif values[0] == 'f':
                 # Declara vetores intermediários
                relation_vert = []
                relation_texture = []
                relation_normal = []
                # Para cada uma das triplas da linha que define a função
                for bloco in values[1:]:
                    # Separa o elemento em vetor de elementos separando os números que são separados por /
                    positions = bloco.split('/')
                    # Adiciona o primeiro número no vetor relation_vert (que representa o número da linha que encontra-se um vértice)
                    relation_vert.append(int(positions[0]))
                    try:
                        # Adiciona o terceiro número no vetor relation_normal (que representa o número da linha que encontra-se a normal para aquele vértice)
                        relation_normal.append(int(positions[2]))
                    except:
                        print(f"Modelo {self._path_obj} não possui normal para esta coordenada")
                    # Se o vetor com elementos separados por / for maior ou igual que dois
                    # Se o segundo número do elemento for maior do que zero
                    if len(positions) >= 2 and len(positions[1]) > 0:
                        # Adicione o segundo número no vetor relation_texture (que representa o número da linha que encontra-se um vértice de textura da figura)
                        relation_texture.append(int(positions[1]))
                    else:
                        # Se não for maior ou igual a dois ou não for maior que zero, coloque zero na textura
                        relation_texture.append(0)
                # Após conseguir, provavelmente, os três valores para vértice, os três valores para textura, os três valores para normal e o tipo de material, insira no vetor relations
                relations.append((relation_vert, relation_texture, relation_normal, material))

        # Armazena cada uma das partes do modelo
        model = {}
        model['vertices'] = vertices
        model['texture'] = texture_coords
        model['relations'] = relations
        model['normals'] = normals

        return model, min_coord, max_coord, sum_coord/np.full(3,num_vertices)
    
    # Função: associa id com a textura
    # Entradas: o id que queremos associar e o caminho do arquivo .jpg
    # Saida: não possui, apenas associa
    def _load_texture_from_file(self):
        #Definindo o id
        glBindTexture(GL_TEXTURE_2D, self._id_texture)
        #Alterando configurações paramétricas de textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self._mag)
        #Abre imagem
        img = Image.open(self._path_jpg)
        #Captura as dimensões
        img_width = img.size[0]
        img_height = img.size[1]
        #Transforma imagem para um sequência de bytes em formato raw de arquivo
        image_data = img.tobytes("raw", "RGB", 0, -1)
        #Carregando os dados da imagem
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    # Função: retorna uma lista para coordenadas dos vertices do objeto, outra para as da textura e outra para as das normais
    # Obs: como as listas de vértices só tem funcionalidade no momento em que são enviados para a GPU,
    # não há necessidade de manter dentro da classe
    def get_vertices_textures_normals(self):
        vertices_list = []    
        textures_coord_list = []
        normals_list = []
        # Para cada um das relations (num_line(v), num_line(vt), num_line(vn) material)
        for relation in self._model['relations']:
            # Para cada um dos números que representa a linha do vértice
            for vertice_id in relation[0]: # Pega o valor a coordenada do vértice
                vertices_list.append( self._model['vertices'][vertice_id-1] )
            # Para cada um dos números que representa a linha da coordenada da textura
            for texture_id in relation[1]:  # Pega o valor a coordenada da textura
                textures_coord_list.append( self._model['texture'][texture_id-1] )
            # Para cada um dos números que representa a linha da coordenada da normal
            for normal_id in relation[2]:
                normals_list.append( self._model['normals'][normal_id-1] )
        return vertices_list, textures_coord_list, normals_list
    
    # Retorna matriz de translação inicial para garantir que o objeto inicialize em (0,0,0)
    def _mat_pre_translation(self):
        return np.array([   1.0, 0.0, 0.0, - self._average_coord[0], 
                            0.0, 1.0, 0.0, - self._average_coord[1], 
                            0.0, 0.0, 1.0, - self._average_coord[2], 
                            0.0, 0.0, 0.0,                     1.0], np.float32)
    
    # Overriding: altera a maneira de desenhar levando em conta a textura e a translação inicial
    def draw(self, program, gl_Draw = GL_TRUE):
        if self._on:
            # Capturando qualificadores de matrizes de transformação
            loc_mat_rot_x = glGetUniformLocation(program, "mat_rot_x")
            loc_mat_rot_y = glGetUniformLocation(program, "mat_rot_y")
            loc_mat_rot_z = glGetUniformLocation(program, "mat_rot_z")
            loc_mat_scale = glGetUniformLocation(program, "mat_scale")
            loc_mat_transl = glGetUniformLocation(program, "mat_transl")
            loc_mat_pre_transl = glGetUniformLocation(program, "mat_pre_transl")

            # Capturado qualificadores de iluminação
            loc_ka = glGetUniformLocation(program, "ka")
            loc_kd = glGetUniformLocation(program, "kd") 
            loc_ks = glGetUniformLocation(program, "ks")
            loc_ns = glGetUniformLocation(program, "ns")
            loc_light_pos = glGetUniformLocation(program, "lightPos")

            # Capturando qualificador de geometria e enviando informação
            loc_geometric = glGetUniformLocation(program, "geometric")
            glUniform1f(loc_geometric, self._geometric)

            # Define se será utilizado texturas ou não (desativado)
            # glPolygonMode(GL_FRONT_AND_BACK, self._polygonal_mode)

            # Exporta matrizes
            glUniformMatrix4fv(loc_mat_pre_transl, 1, gl_Draw, self._mat_pre_translation())
            glUniformMatrix4fv(loc_mat_rot_x, 1, gl_Draw, self._rotation_x()) 
            glUniformMatrix4fv(loc_mat_rot_y, 1, gl_Draw, self._rotation_y()) 
            glUniformMatrix4fv(loc_mat_rot_z, 1, gl_Draw, self._rotation_z()) 
            glUniformMatrix4fv(loc_mat_scale, 1, gl_Draw, self._mat_scale()) 
            glUniformMatrix4fv(loc_mat_transl, 1, gl_Draw, self._mat_translation())
             # Envia parâmetros de iluminação
            glUniform1f(loc_ka, self._ka) 
            glUniform1f(loc_kd, self._kd)   
            glUniform1f(loc_ks, self._ks)
            glUniform1f(loc_ns, self._ns)
            # Envia localizacao da luz de iluminação
            if self._light_source:
                glUniform3f(loc_light_pos, self._pos[0], self._pos[1], self._pos[2])
            # Ativa textura com id
            glBindTexture(GL_TEXTURE_2D, self._id_texture)
            # Desenha o elemento
            glDrawArrays(GL_TRIANGLES, self._inicial_vert, self._num_vert)