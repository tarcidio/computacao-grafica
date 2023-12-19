import math
import numpy as np
from graphic_element_class import graphic_element
from obj_wave_class import obj_wave

# Entrada: angulo de longitude, latitude, raio
# Saida: coordenadas na esfera
def F(u,v,r):
    x = r*math.sin(v)*math.cos(u)
    y = r*math.sin(v)*math.sin(u)
    z = r*math.cos(v)
    return (x,y,z)

# Cria uma esfera de raio radius
def create_sphere(radius):
    # Define as constantes
    PI : float = 3.141592
    NUM_SECTORS : int = 30 
    NUM_STACKS : int = 30

    # Quanto de ângulo vai variar de um sector/ stack para outro com base na quantidade informada?
    SECTOR_STEP : float = (PI*2)/NUM_SECTORS # variar de 0 até 2π
    STACK_STEP : float =   (PI)/NUM_STACKS # variar de 0 até π

    # Gerando os vértices de cada um dos polígonos representados por triângulos
    vertices_list_sphere = []
    for i in range(0, NUM_SECTORS): 
        for j in range(0, NUM_STACKS):
            sector_i = i * SECTOR_STEP # angulo setor
            stack_j = j * STACK_STEP # angulo stack
            
            # O próximo sector será (i+1)*SECTOR_STEP exceto se ele for o ultimo
            sector_i_next = 0 # angulo do proximo sector
            if i + 1 == NUM_SECTORS:
                sector_i_next = PI*2
            else: sector_i_next = (i+1)*SECTOR_STEP

            #O próximo stack será (j+1)*SECTOR_STEP exceto se ele for ultimo
            stack_j_next = 0 # angulo do proximo stack
            if j + 1 == NUM_STACKS:
                stack_j_next = PI
            else: stack_j_next = (j+1)*STACK_STEP

            # Calcula vértices do poligono
            p0 = F(sector_i, stack_j, radius)
            p1 = F(sector_i, stack_j_next, radius)
            p2 = F(sector_i_next, stack_j, radius)
            p3 = F(sector_i_next, stack_j_next, radius)

            # Triangulo 1 (primeira parte do poligono)
            vertices_list_sphere.append(p0)
            vertices_list_sphere.append(p2)
            vertices_list_sphere.append(p1)

            # Triangulo 2 (segunda e ultima parte do poligono)
            vertices_list_sphere.append(p3)
            vertices_list_sphere.append(p1)
            vertices_list_sphere.append(p2)

    return vertices_list_sphere

def load_models_obj():
    # Carregando modelos
    path_wave = 'objetos_wavefront'
    # Vetor com os modelos
    objs_wave = []
    objs_geometric = []

    # Valor inicial de coeficiente ambiente
    initial_ka = 1

    # Gato
    id_obj = 0
    name_obj = 'gato'
    path_obj = f'{path_wave}\{name_obj}\{name_obj}.obj'
    path_jpg = f'{path_wave}\{name_obj}\{name_obj}.jpg'
    cat = obj_wave(id_obj, path_obj, path_jpg, pos_y = -0.12, 
                ka = initial_ka, kd = 1, ks = 0, ns = 32, 
                angle_y = np.radians(-90))
    objs_wave.append(cat)

    # Dog
    id_obj = id_obj + 1
    name_obj = 'dog'
    path_obj = f'{path_wave}\{name_obj}\{name_obj}.obj'
    path_jpg = f'{path_wave}\{name_obj}\{name_obj}.jpg'
    dog = obj_wave(id_obj, path_obj, path_jpg, 
                pos_x = 0.5, pos_y = -0.017, 
                ka = initial_ka, kd = 1, ks = 1, ns = 32,
                angle_y = np.radians(-45))
    objs_wave.append(dog)

    # Pug
    id_obj = id_obj + 1
    name_obj = 'pug'
    path_obj = f'{path_wave}\{name_obj}\{name_obj}.obj'
    path_jpg = f'{path_wave}\{name_obj}\{name_obj}.jpg'
    pug = obj_wave(id_obj, path_obj, path_jpg, 
                pos_x = - 0.5, pos_y = -0.017, 
                ka = initial_ka, kd = 1, ks = 1, ns = 32,
                angle_y = np.radians(45))
    objs_wave.append(pug)

    # Tigre
    id_obj = id_obj + 1
    name_obj = 'tigre'
    path_obj = f'{path_wave}\{name_obj}\{name_obj}.obj'
    path_jpg = f'{path_wave}\{name_obj}\{name_obj}.jpg'
    tiger = obj_wave(id_obj, path_obj, path_jpg, 
                    pos_x = -1, pos_y = 0.17, pos_z = 1,
                    ka = initial_ka, kd = 1, ks = 1, ns = 32,
                    scale = 3,
                    angle_y = np.radians(150))
    objs_wave.append(tiger)

    # Lobo
    id_obj = id_obj + 1
    name_obj = 'lobo'
    path_obj = f'{path_wave}\{name_obj}\{name_obj}.obj'
    path_jpg = f'{path_wave}\{name_obj}\{name_obj}.jpg'
    wolf = obj_wave(id_obj, path_obj, path_jpg, 
                    pos_x = 1, pos_y = 0.1, pos_z = 1,
                    ka = initial_ka, kd = 1, ks = 1, ns = 32,
                    scale = 3,
                    angle_y = np.radians(-90))
    objs_wave.append(wolf)

    # Quantidade total de vértices de objeto a serem utilizados neste programa
    total_len_vert_obj = 0
    # Quantidade total de vértices de textura a serem utilizados neste programa
    total_len_vert_text = 0
    # Quantidade total de normais a serem utilizados neste programa
    total_len_normals = 0
    # Vértices de objeto a serem utilizados neste programa
    vertices_obj_total = []
    # Vértices de textura a serem utilizados neste programa
    vertices_text_total = []
    # Normais a serem utilizados neste programa
    normals_total = []
    # Controla os valores que definem a identificação de cada objeto
    identification = []

    # Para cada objeto:
    for obj in objs_wave:
        # Captura os vertices do objeto e de textura
        vertices_list, textures_coord_list, normals_list = obj.get_vertices_textures_normals()
        # Declara a identificação
        identification.append((total_len_vert_obj, len(vertices_list)))
        # Adiciona o tamanho total dos vertices de objeto e de textura
        total_len_vert_obj += len(vertices_list)
        total_len_vert_text += len(textures_coord_list)
        total_len_normals += len(normals_list)
        # Adiciona os vértices de objeto e de textura
        vertices_obj_total += vertices_list
        vertices_text_total += textures_coord_list
        normals_total += normals_list

    # Constrói o "solo" plano
    ground = graphic_element(
        inicial_vert = total_len_vert_obj, num_vert = 6, 
        ka = initial_ka - 0.2, kd = 1, ks = 1, ns = 1000,
        R = 0.0, G = 1.0, B = 0.0
        )
    # Atualiza identificadores
    total_len_vert_obj += 6
    level_ground = -0.25
    size_ground  = 50
    vertices_obj_total += [(-size_ground, level_ground, size_ground), (size_ground, level_ground, size_ground), (size_ground, level_ground, -size_ground), (-size_ground, level_ground, size_ground), (-size_ground, level_ground, -size_ground), (size_ground, level_ground, -size_ground)]
    # Adiciona no vetor
    objs_geometric += [ground]

    # Contrói o "sol" esférico
    vertices_list_sun = create_sphere(1)
    sun = graphic_element(
        inicial_vert = total_len_vert_obj, num_vert = len(vertices_list_sun), 
        ka = initial_ka, kd = 1, ks = 1, ns = 1000,
        light_source = True,
        R = 1.0, G = 1.0, B = 0.0,
        pos_y = 2
        )
    # Atualiza identificadores
    total_len_vert_obj += len(vertices_list_sun)
    vertices_obj_total += vertices_list_sun
    # Adiciona no vetor
    objs_geometric += [sun]

    # Constrói o "céu" esférico
    sky_radius = 7
    vertices_list_sky = create_sphere(sky_radius)
    sky = graphic_element(
        inicial_vert = total_len_vert_obj, num_vert = len(vertices_list_sky), 
        ka = initial_ka, kd = 1, ks = 1, ns = 1000,
        R = 0.0, G = 0.0, B = 1.0
        )
    # Atualiza identificadores
    total_len_vert_obj += len(vertices_list_sky)
    vertices_obj_total += vertices_list_sky
    # Adiciona no vetor
    objs_geometric += [sky]

    #Finaliza a modelagem dos dados de vértices
    vertices = np.zeros(total_len_vert_obj, [("position", np.float32, 3)])
    vertices['position'] = vertices_obj_total

    #Finaliza a modelagem dos dados de texturas
    textures = np.zeros(total_len_vert_text, [("position", np.float32, 2)])
    textures['position'] = vertices_text_total

    #Finaliza a modelagem dos dados das normais
    normals = np.zeros(total_len_normals, [("position", np.float32, 3)])
    normals['position'] = normals_total

    #Setando as identificações de desenho do objeto
    for i, obj in enumerate(objs_wave):
        obj.set_identification(identification[i][0], identification[i][1])

    return vertices, textures, normals, sun, objs_wave, objs_geometric, sky_radius


def draw_objs(program, objs_geometric, objs_wave):
    # Percorre por todos os objetos
    for obj in objs_wave:
        # Se ele estiver ativado (apenas para otimização, refaz a checagem)
        if obj.get_on():
            # Desenha o objeto
            obj.draw(program)

    # Percorre por todos os objetos
    for obj in objs_geometric:
        # Se ele estiver ativado (apenas para otimização, refaz a checagem)
        if obj.get_on():
            # Desenha o objeto
            obj.draw(program)
