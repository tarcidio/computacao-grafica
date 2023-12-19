import glfw
import math
import glm

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
    return window, WIDTH_WINDOW, HEIGHT_WINDOW

# Define sistema de resposta a eventos de teclado e mouse
def setup_keyboard_event_handlers(window, color_amb, polygonal, cam, sun, objs_wave, objs_geometric, sky_radius, WIDTH_WINDOW, HEIGHT_WINDOW):
    # Variável que controla malha
    press_keys_polygonal = True

    def key_event(window,key,scancode,action,mods):
        nonlocal cam
        nonlocal color_amb
        nonlocal sun
        nonlocal sky_radius
        nonlocal polygonal, press_keys_polygonal
        nonlocal objs_wave, objs_geometric

        # Altera coeficiente de iluminação ambiente
        if key == 79 or key == 73: # Tecla O ou Tecla I
            operation = '+' if key == 79 else '-'
            for obj in objs_wave:
                obj.ka_change(operation)
            for obj in objs_geometric:
                obj.ka_change(operation)

        # Alterando intensidade da luz ambiente
        speed_amb = 0.01
        # Aumentando
        if key == 82 and color_amb[0] < 1.0: color_amb[0] += speed_amb    # Tecla R
        if key == 84 and color_amb[1] < 1.0: color_amb[1] += speed_amb    # Tecla T
        if key == 89 and color_amb[2] < 1.0: color_amb[2] += speed_amb    # Tecla Y
        # Diminuindo
        if key == 70 and color_amb[0] > 0.0: color_amb[0] -= speed_amb    # Tecla F
        if key == 71 and color_amb[1] > 0.0: color_amb[1] -= speed_amb    # Tecla G
        if key == 72 and color_amb[2] > 0.0: color_amb[2] -= speed_amb    # Tecla H
        
        # Movimentando o sol
        if key == 262: sun.move('+','x')     #Tecla LEFT: move para esuqerda
        if key == 263: sun.move('-','x')     #Tecla RIGHT: move para direita
        
        if key == 264: sun.move('-','y')     #Tecla DOWN: desce
        if key == 265: sun.move('+','y')     #Tecla UP: sobe

        # Ativa e desativa malhas
        if key == 80 and action == 1:        #Tecla P: altera visualização de textura
            polygonal[0] = 1 - polygonal[0]                 

        # Componentes da câmera
        # Velocidade da camera
        cameraSpeed = 0.1 # 0.01
        old_cameraPos = glm.vec3(cam[0])  # Cria uma cópia independente
        new_cameraPos = glm.vec3(cam[0])  # Cria uma cópia independente

        # Ir para frente
        if key == 87 and (action==1 or action==2): # Tecla W
            new_cameraPos += cameraSpeed * cam[1]
        # Ir para trás
        if key == 83 and (action==1 or action==2): # Tecla S
            new_cameraPos -= cameraSpeed * cam[1]
        # Ir para esquerda
        if key == 65 and (action==1 or action==2): # Tecla A
            new_cameraPos -= glm.normalize(glm.cross(cam[1], cam[2])) * cameraSpeed
        # Ir para direita    
        if key == 68 and (action==1 or action==2): # Tecla D
            new_cameraPos += glm.normalize(glm.cross(cam[1], cam[2])) * cameraSpeed
        
        # Chega se a nova posicao continua valido
        security_border_sphere = 2 
        in_sphere = new_cameraPos[0]**2 + new_cameraPos[1]**2 + new_cameraPos[2]**2 < sky_radius**2 - security_border_sphere
        on_top_plan = new_cameraPos[1] > 0
        cam[0] = new_cameraPos if in_sphere and on_top_plan else old_cameraPos

    # Variáveis auxiliar para captura de cursor
    # Flag para definir se eh a primeira vez que o mouse aparece na tela
    firstMouse = True
    # yaw: rotação no eixo y
    yaw = -90.0 
    # pitch: rotação no eixo x
    pitch = 0.0
    # Valores iniciais da última posição do mouse
    lastX =  WIDTH_WINDOW/2
    lastY =  HEIGHT_WINDOW/2

    def mouse_event(window, xpos, ypos):
        nonlocal firstMouse, cam, yaw, pitch, lastX, lastY
        # Tratando caso de primeira aparição do mouse
        if firstMouse:
            lastX = xpos
            lastY = ypos
            firstMouse = False

        # Calculos da variação
        xoffset = xpos - lastX
        yoffset = lastY - ypos
        # Atualizando valor da última posição
        lastX = xpos
        lastY = ypos
        # Calculando yam e pitch aproximadamente
        sensitivity = 0.3 
        xoffset *= sensitivity
        yoffset *= sensitivity
        yaw += xoffset
        pitch += yoffset

        # Evitando que rotação extremas
        if pitch >= 90.0: pitch = 90.0
        if pitch <= -90.0: pitch = -90.0

        # Fórmulas matemáticas para calcular o novo cameraFront
        front = glm.vec3()
        front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        front.y = math.sin(glm.radians(pitch))
        front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        cam[1] = glm.normalize(front)

    # Define função de evento para teclado
    glfw.set_key_callback(window,key_event)
    # Define função de evento para cursor
    glfw.set_cursor_pos_callback(window, mouse_event)

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


