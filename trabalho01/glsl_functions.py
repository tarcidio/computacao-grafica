from OpenGL.GL import *

# Cria programa glsl na GPU
def create_program_glsl():
    # GLSL para Vertex Shader
    vertex_code = """
            attribute vec3 position;
            uniform mat4 mat_pre_transl;
            uniform mat4 mat_rot_x;
            uniform mat4 mat_rot_y;
            uniform mat4 mat_rot_z; 
            uniform mat4 mat_scale;  
            uniform mat4 mat_transl; 

            attribute vec2 texture_coord;
            varying vec2 out_texture;

            void main(){
                gl_Position = mat_transl * mat_scale * mat_rot_x * mat_rot_y * mat_rot_z * mat_pre_transl * vec4(position,1.0);
                out_texture = vec2(texture_coord);
            }
            """

    # GLSL para Fragment Shader
    fragment_code = """
            uniform vec4 color;
            varying vec2 out_texture;
            uniform sampler2D samplerTexture;
            
            void main(){
                vec4 texture = texture2D(samplerTexture, out_texture);
                gl_FragColor = texture;
            }
            """
    
    # Requisitando slot para GPU
    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # Associando os códigos aos espaços
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    # Compilando shader de vértice
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Vertex Shader")

    # Compilando shader de fragmento
    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Fragment Shader")

    # Associadno programas compilados ao programa principal
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    # Linkagem do programa
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
        
    # Tornando programa o atual
    glUseProgram(program)

    return program

#Ativando texturas 2D
def on_texture():
    glEnable(GL_TEXTURE_2D)

# Ativando 3D
def on_3d():
    glEnable(GL_DEPTH_TEST)

# Define número máximo de texturas e ativa seus ids
def define_num_textures(num_textures):
    #Gerando ids
    glGenTextures(num_textures)

# Solicita espaço e armazena as coordenadas de vértices e textura na GPU
def create_data_space(vertices, textures, program):
    #Solicita dois buffers para GPU
    buffer = glGenBuffers(2)

    # Enviando dados de vértice
    #Tornando o buffer o buffer padrão de dados
    glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
    #Subindo os dados de vértice para o buffer na GPU
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    #Encontrando informações de stride e offset dos vértices
    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)
    #Capturando posição do atributo "position" e habilitando
    loc_vertices = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc_vertices)
    #Linkando dados ao atributo "position"
    glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

    # Enviando dados de textura
    #Tornando o buffer o buffer padrão de dados
    glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
    #Subindo os dados de textura para o buffer na GPU
    glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
    #Encontrando informações de stride e offset das texturas
    stride = textures.strides[0]
    offset = ctypes.c_void_p(0)
    #Capturando posição do atributo "texture_coord" e habilitando
    loc_texture_coord = glGetAttribLocation(program, "texture_coord")
    glEnableVertexAttribArray(loc_texture_coord)
    #Linkando dados ao atributo "texture_coord"
    glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

# Captura localizações das matrizes de transformação no programa glsl
def get_locs_mat(program):
    # Capturando posição dos uniform "mat_rot_x, mat_rot_y, mat_rot_z, mat_scale, mat_transl e mat_pre_transl"
    loc_mat_pre_transl = glGetUniformLocation(program, "mat_pre_transl")
    loc_mat_rot_x = glGetUniformLocation(program, "mat_rot_x")
    loc_mat_rot_y = glGetUniformLocation(program, "mat_rot_y")
    loc_mat_rot_z = glGetUniformLocation(program, "mat_rot_z")
    loc_mat_scale = glGetUniformLocation(program, "mat_scale")
    loc_mat_transl = glGetUniformLocation(program, "mat_transl")
    return [loc_mat_pre_transl,
            loc_mat_rot_x,
            loc_mat_rot_y,
            loc_mat_rot_z,
            loc_mat_scale,
            loc_mat_transl]

# Inicializa o loop principal por parte do sistema glsl
def init_main_loop_glsl():
    # Limpa buffer de cor e Z-buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Define cor como sendo RGB(1.0,1.0,1.0)
    glClearColor(1.0, 1.0, 1.0, 1.0)