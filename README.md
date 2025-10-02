# Visão Geral
Projeto de criação de um RPG em python

[Brainstorm do projeto no canva](https://www.canva.com/design/DAGzPbYH7wQ/J6XXYxe3BEQWRxS2OEKW9g/edit?utm_content=DAGzPbYH7wQ&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

- Gênero: RPG Clássico
- Tema: Fantasia
- Loop de Gameplay: explorar o mapa -> lutar com inimigos -> coletar itens -> evoluir o personagem
- Ambientação: [Floresta corrompida](./pre-production/images/ambiente_1.png)
- Sistema de luta de acordo com as classes:
	- Guerreiro: Espada
	- Arqueiro: Arco
- Itens coletáveis: 
	- Moeda (drop) (sem utilidade inicialmente)
	- Minério (drop) (para construção de espadas)
	- Fibra de seda (drop) (para a construção de um arco)
	- Acessório (drop) (buff de defesa para jogador)
	- Couro especial (drop) (para a construção de uma armadura)
- Evolução do personagem:
	- 5 Níveis
	- Itens melhores são craftáveis com os drops
- Esboço de elementos visuais:
	- [Inventário](./pre-production/images/Inventario_1.png)
	- Craft
	- HUD

# Instalação e Execução

Para rodar o jogo, é altamente recomendado usar um ambiente virtual para gerenciar as dependências corretamente.

### Passo 1: Clonar e Configurar

Execute os comandos abaixo na ordem:

1.  Clone o repositório e depois abra-o:
    ```bash
    git clone https://github.com/ManoelCosta0/GamePy.git
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
python src/main.py
```
# Controles

- [ESC] Pause
- [I] Inventário
- [TAB] Abrir logbox
- [W], [S], [A], [D] movimentação do personagem

# GitFlow

Para melhor organização do projeto, será utilizado o seguinte GitFlow:

![Diagrama do Fluxo de Trabalho GitFlow](./pre-production/docs/GitFlow_v3.jpg)

## Main
- A main será branch principal em que o código mais estável e devidamente versionado estará. A partir dela serão criadas as branchs develop e documents.

## Develop 
- A develop é a branch base de desenvolvimento e integração das features.

## Documents
- A documents é a branch em que tudo que não faz parte da codificação diretamente estará, como padrões de uso e esboços do projeto.

## Feature
- São criadas para o desenvolvimento das tarefas do projeto.
- Padrão lexico: feature/[nome_da_feature]

# Padrões de Uso do GitHub

Para melhor organização e estética do GitHub, será utilizado o seguinte padrão de uso:

## Commit
- Os commit serão feitos seguindo os modelos abaixo:
	- :sparkles: feat: título da feature
	- :books: docs: título do documento ou descriçaõ da atualização realizada no documento
	- :recycle: refactor: descrição da refatoração
	- :bug: fix: bug corrigido

## Versionamento

- O incremento de versões do projeto na main segue o seguinte padrão: (Para o exemplo v0.0.1)
	- O primeiro número indica que o sistema tem mudanças que o torna incompatível com versões anteriores.
	- O segundo número indica que o sistema tem mudanças compatíveis com versões anteriores, dentro do primeiro número.
	- O terceiro número indica que o sistema tem mudanças menores, como correções de bugs e funcionalidades que não prejudicam a compatibilidade com versões anteriores.
