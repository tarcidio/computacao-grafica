# Importa bibliotecas
import glfw_functions
import glsl_functions
from obj_wave_class import obj_wave, define_coord_vertices_texture

if __name__ == "__main__":
    # Cria janela glfw
    window = glfw_functions.init_window("Trabalho 01")
    # Cria programa glsl
    program = glsl_functions.create_program_glsl()

    # Ativando texturas 2D
    glsl_functions.on_texture()
    # Ativando 3D
    glsl_functions.on_3d()
    # Libera 10 id para texturas
    glsl_functions.define_num_textures(10)

    # Carregando modelos
    # Os nomes devem ser iguais a da pasta
    names_obj = ['gato', 'dog', 'pug', 'tigre', 'lobo']
    path_wave = 'objetos_wavefront'
    id_obj = 0
    objs_wave = []
    for name_obj in names_obj:
        path_obj = f'{path_wave}\{name_obj}\{name_obj}.obj'
        path_jpg = f'{path_wave}\{name_obj}\{name_obj}.jpg'
        id_obj = id_obj + 1
        objs_wave.append(obj_wave(id_obj, path_obj, path_jpg))
    # Captura coordenadas de vértices e texturas dos modelos
    vertices, textures = define_coord_vertices_texture(objs_wave)
    # Solicita espaço e armazena os vértices na GPU
    glsl_functions.create_data_space(vertices, textures, program)

    # Captura localizações de matrizes de transformação na GPU
    locs = glsl_functions.get_locs_mat(program)

    # Define eventos de teclado e mouse 
    glfw_functions.setup_keyboard_event_handlers(window, objs_wave[0], objs_wave)

    # Exibe janela
    glfw_functions.show_window(window)

    # Loop principal
    while not glfw_functions.verify_window(window):
        # Inicializa loop
        glfw_functions.init_main_loop_glfw(window)
        glsl_functions.init_main_loop_glsl()
        
        # Percorre por todos os objetos
        for obj in objs_wave:
            # Se ele estiver ativado (apenas para otimização, refaz a checagem)
            if obj.get_on():
                # Desenha o objeto
                obj.draw(locs)

    # Finaliza sistema glfw
    glfw_functions.finish_glfw()