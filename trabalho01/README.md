**Introdução:**

A computação gráfica é uma disciplina da ciência da computação que lida com a geração, manipulação e representação de imagens e objetos visuais por meio de software e hardware. Ela desempenha um papel crucial em várias áreas, incluindo entretenimento, design, engenharia, medicina, educação e muitos outros campos. Neste trabalho, aborda-se algumas de suas bases.

**Objetivos do trabalho:**

Neste trabalho, busca-se sedimentar os seguintes conhecimentos: pipeline gráfico, API OpenGL, sistemas de janelas, primitivas geométricas, transformações geométricas 3D, coordenadas homogêneas, além de malhas e texturas. Para isso, o trabalho importa cinco objetos no formato wavefront (.obj) e suas respectivas texturas, permitindo que o usuário aplique transformações geométricas a partir do teclado.

**Descrição dos comandos:**

* Invocação: os objetos são apresentados de forma individual e acionados por eventos de teclado. Ao pressionar a tecla 1, o objeto 1 deve ser exibido, a tecla 2 para o objeto 2 e assim por diante. Todos partem da origem (0,0,0) e não ultrapassam o limite da janela. 
* Movimentação: as teclas 'a','d','s' e 'w' transladam o objeto para esquerda, direita, cima e baixo respectivamente
* Rotação: as teclas 'LEFT', 'RIGHT', 'UP' e 'DOWN' rotacionam o objeto. Os dois primeiros em relação ao eixo y e os dois últimos em relação ao eixo x. As teclas '+' e '-' rotacionam o objeto no eixo z.
* Escala: as teclas 'z' e 'x' aumenta e diminui respectivamente a escala do objeto
* Textura: a tecla 'p' ativa e desativa a textura
* Magnificação: a tecla 'v' altera entre as técnicas de magnificação linear e nearest

**Execução:**

Para este trabalho, é necessário que tenha instalado as seguintes bibliotecas: 
* glfw
* OpenGL
* numpy
* PIL

Para instalar as bibliotecas, pode-se utilizar os respectivos comandos:

```python
pip install glfw
pip install pyopengl
pip install numpy
pip install pillow
```

Para rodar o programa com o código principal no arquivo `.ipynb` (mais recomendado), basta executar a única célula disponível. Para executar na janela de comando do windows ou linux, basta executar 

```python
python3 main.py
```

**Ferramentas:**

Para criação deste projeto foi utilizado as seguintes ferramentas:
* Linguagem Python
* Sistemas de janela GLFW
* API OpenGL
* Bibliotecas: numpy, math e PIL

---

<sup>Instituto de Ciências Matemáticas e de Computação (ICMC) - Universidade de São Paulo (USP)</sup>
