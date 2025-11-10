# Visão Geral
Projeto de criação de um RPG em python

- Gênero: RPG Clássico
- Tema: Fantasia

# Instalação e Execução

Para rodar o jogo, é altamente recomendado usar um ambiente virtual para gerenciar as dependências corretamente.

### Passo 1: Clonar e Configurar

Execute os comandos abaixo na ordem:

1.  Clone o repositório e depois abra-o:
    ```bash
    git clone https://github.com/ManoelCosta0/GamePy.git
    ```
    ```bash
    cd GamePy
    ```

2.  **Configuração Rápida (Recomendado):**
    * **Windows:** Execute `setup.bat`
    * **Linux/macOS:** Execute `./setup.sh` (Pode ser necessário rodar `chmod +x setup.sh` antes)

**OU**

2.  **Configuração Manual:**
    * Crie e ative o ambiente virtual:
        * `python -m venv venv`
        * *Windows:* `venv\Scripts\activate.bat`
        * *Linux/macOS:* `source venv/bin/activate`
    * Instale as dependências:
        * `pip install -r requirements.txt`

### Passo 2: Executar o Jogo

Com o ambiente virtual ativado, rode:

```bash
python -m src.main
```
# Controles

- [ESC] Pause
- [I] Inventário
- [E] Interagir com objetos e estruturas
- [W], [S], [A], [D] movimentação do personagem
- 🖱️ Botão esquerdo: golpe com a espada (se equipada)

 # Funcionalidades
 **Atenção! O que está a seguir é uma descrição das funcionalidades do jogo. Para uma experiência mais completa sugiro jogar antes de ler.**
 
 ## Classes
 Ao iniciar um novo jogo, é possível escolher entre duas classes, sendo elas guerreiro e assassino, cada uma com suas características individuais:
 - Guerreiro: Tem um dano maior e mais vida, porém menos velocidade de caminhar de ataque. Arma inicial: Espada Velha
 - Assassino: Tem maior velocidade de ataque e de caminhar, porém menos vida e menos dano. Arma inicial: Adaga Velha
  
## Progressão
1. Logo no começo do jogo, ao selecionar a classe, o jogador nasce ao lado de uma fogueira.
    1. Ao interagir com uma fogueira apagada (tecla "E") é possível acende-la e alterar o local de nascimento do jogador
	2. Cada fogueira disposta no mapa tem um nível mínimo para ser acesa
    3. Para saber o nível necessário de uma fogueira ative a opção "Logbox" nas configurações
       
3. A cada inimigo derrotado uma determinada quantidade de experiência será ganha
   
4. Ao chegar no limite de exp (experiência) do nível o jogador evolui para o próximo nível
    1. A cada nível a vida máxima do jogador aumenta em 20%
       
5. Alguns inimigos dão itens (drops) ao jogador ao serem derrotados. Esses iten podem ser: 
   1. Um cristal (drop dos slimes, ainda sem utilidade)
   2. Uma Espada (drop de um dos orcs) (chance de drop: 5%)

# GitFlow
Para melhor organização do projeto, é utilizado o seguinte GitFlow:

## Main
- A main é a branch em que estará a versão mais estável do jogo em sua fase de desenvolvimento atual

## Develop 
- A develop é a branch base para desenvolvimento de novas funcionalidades e também é onde a integração delas acontece.

## Feature
- Branches temporárias para desenvolvimento de funcionalidades novas.
- Seu padrão léxico é: feature/{fase_atual}/{nome_feature} (Ex.: feature/alpha/tela_de_aviso)

# Padrões de Uso do GitHub
Para melhor organização e estética do GitHub, será utilizado o seguinte padrão de uso:

## Commit
- Os commit serão feitos seguindo os modelos abaixo:
	- :sparkles: feat: título da feature
	- :books: docs: título do documento ou descriçaõ da atualização realizada no documento
	- :recycle: refact: descrição da refatoração
	- :bug: fix: bug corrigido

## Versionamento
- O incremento de versões do projeto na main segue o seguinte padrão: (Para o exemplo v0.0.1)
	- O primeiro número indica que o sistema tem mudanças que o torna incompatível com versões anteriores.
	- O segundo número indica que o sistema tem mudanças compatíveis com versões anteriores, dentro do primeiro número.
	- O terceiro número indica que o sistema tem mudanças menores, como correções de bugs e funcionalidades que não prejudicam a compatibilidade com versões anteriores.
