import pygame
import random

# Inicializar o Pygame
pygame.init()

# Configurações da janela
LARGURA = 800
ALTURA = 600
TAMANHO_PERSONAGEM = 50
TAMANHO_PLATAFORMA = (100, 20)
FPS = 60

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Criar a janela do jogo
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Plataforma")

# Classe para o jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA // 2, ALTURA - TAMANHO_PERSONAGEM)
        self.velocidade_y = 0
        self.velocidade_x = 0
        self.pulos_realizados = 0  # Contador de pulos

    def update(self):
        # Gravidade
        self.velocidade_y += 1
        self.rect.y += self.velocidade_y

        # Movimento horizontal
        self.rect.x += self.velocidade_x

        # Limitar o movimento dentro da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

        # Impedir que o personagem caia no chão
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA
            self.velocidade_y = 0
            self.pulos_realizados = 0  # Reseta os pulos ao tocar o chão

    def pular(self):
        if self.pulos_realizados == 0:  # Primeiro pulo
            self.velocidade_y = -15
            self.pulos_realizados += 1
        elif self.pulos_realizados == 1:  # Segundo pulo
            self.velocidade_y = -20
            self.pulos_realizados += 1

# Classe para plataformas
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(TAMANHO_PLATAFORMA)
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Classe para itens coletáveis
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Criar grupos de sprites
todos_sprites = pygame.sprite.Group()
plataformas = pygame.sprite.Group()
itens = pygame.sprite.Group()

# Criar o jogador
jogador = Jogador()
todos_sprites.add(jogador)

# Criar plataformas
for i in range(6):
    plataforma = Plataforma(random.randint(0, LARGURA - TAMANHO_PLATAFORMA[0]), random.randint(0, ALTURA - 50))
    todos_sprites.add(plataforma)
    plataformas.add(plataforma)

# Variáveis de nível e pontuação
pontuacao = 0
nivel = 1
meta_pontuacao = 5  # Pontos necessários para passar de nível

# Função para criar itens coletáveis
def criar_itens(qtd):
    for i in range(qtd):
        item = Item(random.randint(0, LARGURA - 20), random.randint(0, ALTURA - 100))
        todos_sprites.add(item)
        itens.add(item)

# Criar itens iniciais
criar_itens(meta_pontuacao)

# Loop principal do jogo
rodando = True
relogio = pygame.time.Clock()

while rodando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jogador.pular()
            if evento.key == pygame.K_LEFT:
                jogador.velocidade_x = -5
            if evento.key == pygame.K_RIGHT:
                jogador.velocidade_x = 5
        if evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                jogador.velocidade_x = 0

    # Atualizar
    todos_sprites.update()

    # Verificar colisão com plataformas
    colisoes = pygame.sprite.spritecollide(jogador, plataformas, False)
    if colisoes:
        jogador.rect.bottom = colisoes[0].rect.top  # Fixa o jogador na plataforma
        jogador.velocidade_y = 0
        jogador.pulos_realizados = 0  # Reseta os pulos ao tocar uma plataforma

    # Verificar colisão com itens
    itens_coletados = pygame.sprite.spritecollide(jogador, itens, True)
    pontuacao += len(itens_coletados)

    # Verificar se passou de nível
    if pontuacao >= meta_pontuacao:
        nivel += 1
        if nivel > 10:
            rodando = False  # Finaliza o jogo após o nível 10
        else:
            meta_pontuacao += 5  # Aumenta a meta de pontos para o próximo nível
            criar_itens(meta_pontuacao)  # Cria mais itens para o próximo nível

    # Desenhar
    janela.fill(BRANCO)
    todos_sprites.draw(janela)

    # Mostrar pontuação e nível
    fonte = pygame.font.Font(None, 36)
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    texto_nivel = fonte.render(f"Nível: {nivel}", True, PRETO)
    janela.blit(texto_pontuacao, (10, 10))
    janela.blit(texto_nivel, (10, 50))

    pygame.display.flip()
    relogio.tick(FPS)

# Final do jogo
janela.fill(BRANCO)
fonte = pygame.font.Font(None, 72)
texto_final = fonte.render("Parabéns, você ganhou!", True, PRETO)
janela.blit(texto_final, (LARGURA // 2 - 300, ALTURA // 2 - 50))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()

