from OpenGL.GL import *

# Cria programa glsl na GPU
def create_program_glsl():
    # GLSL para Vertex Shader
    vertex_code = """
            //POSIÇÃO VERTICES, TEXTURA E NORMAL
            attribute vec3 position;
            attribute vec2 texture_coord;
            attribute vec3 normals;

            //VALORES REPASSADOS PARA O SHADER FRAGMENT
            varying vec2 out_texture;
            varying vec3 out_fragPos;
            varying vec3 out_normal;
            
            //MATRIZES DE TRANSFORMACAO 
            uniform mat4 mat_pre_transl;
            uniform mat4 mat_rot_x;
            uniform mat4 mat_rot_y;
            uniform mat4 mat_rot_z; 
            uniform mat4 mat_scale;  
            uniform mat4 mat_transl;
            uniform mat4 view;
            uniform mat4 projection;   

            void main(){
                mat4 model = mat_transl * mat_scale * mat_rot_x * mat_rot_y * mat_rot_z * mat_pre_transl;
                gl_Position = projection * view * model * vec4(position,1.0);
                out_texture = vec2(texture_coord);
                out_fragPos = vec3(model * vec4(position, 1.0));
                out_normal = vec3(model *vec4(normals, 1.0));
            }
            """

    # GLSL para Fragment Shader
    fragment_code = """
        // POSICAO DA FONTE DE LUZ E COR DA LUZ
        uniform vec3 lightPos; // define coordenadas de posicao da luz
        uniform vec3 lightColor;
        
        // ILUMINACAO AMBIENTE E DIFUSA
        uniform float ka; // coeficiente de reflexao ambiente
        uniform float kd; // coeficiente de reflexao difusa
        
        // ILUMINACAO ESPECULAR
        uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
        uniform float ks; // coeficiente de reflexao especular
        uniform float ns; // expoente de reflexao especular

        // VARIAVEIS VINDOS DO SHADER VERTEX
        varying vec2 out_texture; // recebido do vertex shader
        varying vec3 out_normal; // recebido do vertex shader
        varying vec3 out_fragPos; // recebido do vertex shader

        // PARAMETRO DE TEXTURA
        uniform sampler2D samplerTexture;   

        // PARAMETRO DE GEOMETRIA
        uniform bool geometric;
        uniform vec4 color;
        
        void main(){
            // REFLEXAO AMBIENTE
            vec3 ambient = ka * lightColor;             
        
            // REFLEXAO DIFUSA
            vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
            vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz
            float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
            vec3 diffuse = kd * diff * lightColor; // iluminacao difusa
            
            // REFLEXAO ESPECULAR
            vec3 viewDir = normalize(viewPos - out_fragPos); // direcao do observador/camera
            vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direcao da reflexao
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
            vec3 specular = ks * spec * lightColor;             
            
            // MODELO DE PHONG
            vec4 texture;
            if(geometric)
                texture = color;
            else
                texture = texture2D(samplerTexture, out_texture);
            vec4 result = vec4((ambient + diffuse + specular),1.0) * texture; // aplica iluminacao
            gl_FragColor = result;
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
def create_data_space(vertices, textures, normals, program):
    #Solicita dois buffers para GPU
    buffer = glGenBuffers(3)

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

    # Enviando dados das normais
    #Tornando o buffer o buffer padrão de dados
    glBindBuffer(GL_ARRAY_BUFFER, buffer[2])
    #Subindo os dados das normais para o buffer na GPU
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    #Encontrando informações de stride e offset das normais
    stride = normals.strides[0]
    offset = ctypes.c_void_p(0)
    #Capturando posição do atributo "normals" e habilitando
    loc_normals_coord = glGetAttribLocation(program, "normals")
    glEnableVertexAttribArray(loc_normals_coord)
    #Linkando dados ao atributo "normals"
    glVertexAttribPointer(loc_normals_coord, 3, GL_FLOAT, False, stride, offset)

# Inicializa o loop principal por parte do sistema glsl
def init_main_loop_glsl():
    # Limpa buffer de cor e Z-buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Define cor como sendo RGB(1.0,1.0,1.0)
    glClearColor(1.0, 1.0, 1.0, 1.0)

# Verifica se deve ser exibido a malha]
def check_polygonal(polygonal):
    if polygonal[0]:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# Atualiza cor da luz ambiente
def update_color(program, color_amb):
    # Capturando intensidade da luz
    loc_lightColor = glGetUniformLocation(program, "lightColor")

    # Envia dados da intensidade da luz ambiente
    glUniform3f(loc_lightColor, color_amb[0], color_amb[1], color_amb[2]) 