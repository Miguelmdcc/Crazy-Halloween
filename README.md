# Crazy Halloween 🎃

Um jogo de plataforma 2D temático de Halloween desenvolvido em **Pygame Zero** para avaliação técnica de instrutores de programação. O projeto atende a todos os requisitos PEP 8, utiliza identificadores em inglês e possui mecânicas completas de movimentação, física, animações e efeitos sonoros.

---

## 🎮 Mecânicas e Recursos

* **Menu Principal Interativo:** Opções para iniciar a aventura, alternar áudio/música (ON/OFF) e sair do jogo.
* **3 Níveis Progressivos:** Design de fases com plataformas, obstáculos, buracos e progressão orgânica de dificuldade.
* **Física e Controles:** Sistema de gravidade, pulo, colisão com plataformas (tiles) e movimentação suave.
* **Inimigos e Patrulha (AI):**
  * **Slime & Morcego:** Patrulham o território e podem ser esmagados pulando sobre eles.
  * **Fantasma:** Inimigo imortal que flutua e causa dano ao contato.
* **Sistema de Vidas e Dano:**
  * O jogador possui 2 vidas e sofre *knockback* (empurrão) com sprite de dano ao colidir com inimigos.
  * Queda em buracos reseta o nível imediatamente.
* **Animações de Sprites:** Animação cíclica contínua para estados *idle*, *walk*, *jump*, *cheer* e *hit*.
* **Áudio Dinâmico:** Músicas de fundo específicas para cada etapa/nível e efeitos sonoros para moedas, pulo, dano e cliques.

---

## 🛠️ Tecnologias e Dependências

* **Python 3.10+**
* **Pygame Zero (`pgzero`)**
* **Módulos Nativos:** `math`, `random` e `Rect` (da biblioteca Pygame/Pgzero builtins).

---

## 📁 Estrutura do Projeto

```text
Crazy-Halloween/
├── main.py          # Loop principal do jogo, gerenciamento de estados, eventos e telas
├── levels.py        # Configuração das matrizes dos mapas e instanciação dos objetos
├── zombie.py        # Classe do jogador (Zombie) com física e controle de animações
├── enemy.py         # Classe genérica de inimigos (Slime, Bat, Ghost) com patrulha e animações
├── images/          # Sprites de personagens, tilesets, HUD e telas de fundo
├── music/           # Músicas de fundo (.ogg / .mp3)
└── sounds/          # Efeitos sonoros do jogo (.wav / .ogg)
```

---

## 🚀 Como Executar

    Certifique-se de ter o Python instalado na versão 3.10 ou superior.

    Instale o Pygame Zero via terminal:
    Bash

    pip install pgzero

    Execute o jogo a partir do diretório raiz do projeto:
    Bash

    pgzrun main.py

---

## 🎹 Controles do Jogo

    Seta Esquerda / Direita: Movimenta o personagem.

    Seta Para Cima: Pula.

    Mouse (Botão Esquerdo): Interação com os botões do menu