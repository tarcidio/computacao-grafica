import glfw

# get_dim_pos: retorna tamanho da tela e posição da tela
# Entrada: porcentagem largura e altura da tela que deve ser ocupada
# Saída: tamanho da largura e altura da tela, além da posição x e y da tela
def get_dim_pos(per_width, per_height): 
    # Obtendo configurações do monitor
    monitores = glfw.get_monitors()
    monitor = monitores[0]
    video_mode = glfw.get_video_mode(monitor)
    WIDTH_WINDOW, HEIGHT_WINDOW = video_mode.size
    # Definindo proporção que se quer do monitor
    WIDTH_WINDOW : int = int(per_width*WIDTH_WINDOW)
    HEIGHT_WINDOW : int = int(per_height*HEIGHT_WINDOW)
    POSX_WINDOW : int = (video_mode.size[0] - WIDTH_WINDOW) // 2
    POSY_WINDOW : int = (video_mode.size[1] - HEIGHT_WINDOW) // 2
    return WIDTH_WINDOW, HEIGHT_WINDOW, POSX_WINDOW, POSY_WINDOW

# init_window: inicializa e retorna janela glfw
# Entrada: título da janela, além da porcentagem largura e altura da tela que deve ser ocupada
# Saída: janela glfw
def init_window(title, per_width = 0.6, per_height = 0.6):
    # Inicializando sistema glfw
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    # Pega tamanho da tela e posição da tela
    WIDTH_WINDOW, HEIGHT_WINDOW, POSX_WINDOW, POSY_WINDOW = get_dim_pos(per_width, per_height)
    # Criando janela
    window = glfw.create_window(WIDTH_WINDOW, HEIGHT_WINDOW, title, None, None)
    # Posicionando janela
    glfw.set_window_pos(window, POSX_WINDOW, POSY_WINDOW)
    glfw.make_context_current(window)
    return window

# Define sistema de resposta a eventos de teclado e mouse
def setup_keyboard_event_handlers(window, initial_obj_wave, objs_wave):
    # Obs: objs_wave vai mudar porque lista é um tipo mutável no python que é passado sempre como referencia
    # Define um objeto principal para uso na capturação de eventos
    main_obj = initial_obj_wave
    # Controladores de teclas para evitar erro
    press_keys = [True, True]

    def keyboard_event(window, key, scancode, action, mods):
        nonlocal main_obj, press_keys

        # Ativando objetos
        # Determinando id_obj
        id_obj = key

        # Ativa o objeto chamado
        if id_obj >= 48 and id_obj <= 57:
            id_obj = id_obj - 48
            # Ativa e desativa objeto
            for obj in objs_wave:
                obj.set_on(id_obj)
                if obj.get_on():
                    main_obj = obj # Apenas por otimização, captura o objeto ativo
        
        # Ações do objeto
        if key == 262: main_obj.rotate('-', 'y')    #Tecla LEFT: rotacionar para esquerda
        if key == 263: main_obj.rotate('+','y')     #Tecla RIGHT: rotacionar para direita
        
        if key == 264: main_obj.rotate('-','x')     #Tecla DOWN: rotacionar para baixo
        if key == 265: main_obj.rotate('+','x')     #Tecla UP: rotacionar para cima

        if key == 333: main_obj.rotate('-','z')     #Tecla -: rotacionar no sentido antihorario
        if key == 334: main_obj.rotate('+','z')     #Tecla +: rotacionar no sentido horario

        if key == 88: main_obj.distort('-')         #Tecla X: diminuir escala
        if key == 90: main_obj.distort('+')         #Tecla Z: aumentar escala

        if key == 87: main_obj.move('+','y')        #Tecla W: mover para cima
        if key == 83: main_obj.move('-','y')        #Tecla S: mover para baixo
        if key == 65: main_obj.move('-','x')        #Tecla A: mover para esquerda
        if key == 68: main_obj.move('+','x')        #Tecla D: mover para direita

        if key == 80:                               #Tecla P: altera visualização de textura
            if press_keys[0]:
                main_obj.turn_texture()
                press_keys[0] = False
            else:
                press_keys[0] = True

        if key == 86:                               #Tecla V: altera modo de magnificação
            if press_keys[1]:
                main_obj.turn_mag()
                press_keys[1] = False
            else:
                press_keys[1] = True

    # Seta função de ação de eventos de teclado
    glfw.set_key_callback(window, keyboard_event)

# Exibe a janela
def show_window(window):
    glfw.show_window(window)

# Verifica se a janela precisa se fechada
def verify_window(window):
    return glfw.window_should_close(window)

# Encerra sistema glfw
def finish_glfw():
    # Encerra
    glfw.terminate()

# Inicializa o loop main no sistema glfw
def init_main_loop_glfw(window):
    # Gerencia troca de dados entre janela e OpenGL
    glfw.swap_buffers(window)
    # Lê eventos
    glfw.poll_events()