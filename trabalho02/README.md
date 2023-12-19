**Introdução:**

A computação gráfica é uma disciplina da ciência da computação que lida com a geração, manipulação e representação de imagens e objetos visuais por meio de software e hardware. Ela desempenha um papel crucial em várias áreas, incluindo entretenimento, design, engenharia, medicina, educação e muitos outros campos. Neste trabalho, aborda-se algumas de suas bases.

**Objetivos do trabalho:**

Neste trabalho, busca-se sedimentar os seguintes conhecimentos: pipeline gráfico, API OpenGL, sistemas de janelas, primitivas geométricas, transformações geométricas 3D, coordenadas homogêneas, além de malhas e texturas. Para isso, o trabalho importa cinco objetos no formato wavefront (.obj) em um ambiente 3D.

**Descrição dos comandos:**

* Movimentação: as teclas 'a','d','s' e 'w' transladam a câmera para esquerda, direita, cima e baixo respectivamente
* Rotação: as teclas 'LEFT', 'RIGHT', 'UP' e 'DOWN' move o sol para esquerda, direita, cima e baixo respectivamente
* Textura: a tecla 'p' ativa e desativa a textura
* Iluminação ambiente: as tecla 'O' e 'I' aumentam e diminuem, respectivamente, a iluminação ambiente

**Execução:**

Para este trabalho, é necessário que tenha instalado as seguintes bibliotecas: 
* glfw
* OpenGL
* numpy
* PIL
* glm

Para instalar as bibliotecas, pode-se utilizar os respectivos comandos:

```python
pip install glfw
pip install pyopengl
pip install numpy
pip install pillow
pip install glm
```

Para rodar o programa com o código principal no arquivo `.ipynb` (mais recomendado), basta executar a única célula disponível no arquivo `Trabalho02_SmallCode.ipynb`. `Trabalho02_BigCode.ipynb` é apenas uma versão não modularizada de `Trabalho02_SmallCode.ipynb`. Para executar na janela de comando do Windows ou Linux, basta executar 

```python
python3 main.py
```

**Ferramentas:**

Para criação deste projeto foi utilizado as seguintes ferramentas:
* Linguagem Python
* Sistemas de janela GLFW
* API OpenGL
* Bibliotecas: numpy, mathm glm e PIL

---

<sup>Instituto de Ciências Matemáticas e de Computação (ICMC) - Universidade de São Paulo (USP)</sup>
