import pygame
import sys
import random
from configuracoes import *


def escalar_proporcional(imagem, altura_desejada):
    """Redimensiona a imagem mantendo a proporção original para não ficar esticada."""
    largura_original, altura_original = imagem.get_size()
    proporcao = largura_original / altura_original
    nova_largura = int(altura_desejada * proporcao)
    return pygame.transform.smoothscale(imagem, (nova_largura, altura_desejada))


def exibir_intro(tela):
    # 1. Carregando os Fundos
    bg_normal = pygame.image.load("assets/salanormal.png")
    bg_normal = pygame.transform.scale(bg_normal, (LARGURA_TELA, ALTURA_TELA))

    bg_escuro = pygame.image.load("assets/salacorrompida.png")
    bg_escuro = pygame.transform.scale(bg_escuro, (LARGURA_TELA, ALTURA_TELA))

    # 2. Carregando e arrumando a PROPORÇÃO dos Retratos
    altura_retrato = 300  # Altura ideal para encaixar certinho em cima da caixa de texto

    retrato_heroi_normal = pygame.image.load("assets/normalprincipal.png")
    retrato_heroi_normal = escalar_proporcional(retrato_heroi_normal, altura_retrato)

    retrato_heroi_susto = pygame.image.load("assets/principalsurpreso.png")
    retrato_heroi_susto = escalar_proporcional(retrato_heroi_susto, altura_retrato)

    retrato_professora = pygame.image.load("assets/professora.png")
    retrato_professora = escalar_proporcional(retrato_professora, altura_retrato)

    fonte_nome = pygame.font.SysFont("Arial", 28, bold=True)
    fonte_fala = pygame.font.SysFont("Arial", 24)
    fonte_dica = pygame.font.SysFont("Arial", 18, italic=True)

    # 3. Roteiro da Cena
    # AQUI ESTÁ A MUDANÇA: Diminuí os números para empurrar tudo para a esquerda!
    pos_esq = -100  # Antes era 50
    pos_dir = 350  # Antes era 450

    dialogos = [
        # 1º Mostra só o Max normal ouvindo
        ("Professora", "Bom dia, classe! Por favor, guardem os materiais.", retrato_heroi_normal, pos_esq),

        # 2º Some o Max, mostra só a Professora falando
        ("Professora", "Hoje teremos uma PROVA SURPRESA de MATEMÁTICA!", retrato_professora, pos_dir),

        # 3º Some a professora, mostra só o Max assustado
        ("James", "Ah não... eu não estudei para isso!", retrato_heroi_susto, pos_esq),

        # 4º Some o Max, professora dá o ultimato
        ("Professora", "A nota de vocês depende disso. Preparem-se!", retrato_professora, pos_dir)
    ]

    indice_atual = 0
    rodando_intro = True

    # --- LOOP DO DIÁLOGO ---
    while rodando_intro:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_RETURN:
                    indice_atual += 1
                    if indice_atual >= len(dialogos):
                        rodando_intro = False

        # Desenha o fundo normal claro da escola
        tela.blit(bg_normal, (0, 0))

        if indice_atual < len(dialogos):
            nome_falando, texto_fala, imagem_atual, pos_x = dialogos[indice_atual]

            # Desenha APENAS a imagem de quem está participando daquela frase!
            tela.blit(imagem_atual, (pos_x, 90))

            # Retângulo da caixa preta por cima
            caixa_rect = pygame.Rect(50, 450, 700, 120)
            pygame.draw.rect(tela, PRETO, caixa_rect)
            pygame.draw.rect(tela, BRANCO, caixa_rect, 3)

            # Textos
            cor_nome = AZUL_MENU if nome_falando == "James" else VERMELHO_DANO
            txt_nome = fonte_nome.render(nome_falando, True, cor_nome)
            txt_fala = fonte_fala.render(texto_fala, True, BRANCO)
            txt_dica = fonte_dica.render("(Aperte ESPAÇO)", True, CINZA)

            tela.blit(txt_nome, (70, 460))
            tela.blit(txt_fala, (70, 500))
            tela.blit(txt_dica, (600, 540))

        pygame.display.flip()

    # --- TRANSIÇÃO: O MUNDO ESCURECE E TREME ---
    relogio = pygame.time.Clock()
    frames_tremor = 40

    for _ in range(frames_tremor):
        deslocamento_x = random.randint(-15, 15)
        deslocamento_y = random.randint(-15, 15)

        tela.fill(PRETO)

        # Desenha SÓ o fundo escuro tremendo!
        tela.blit(bg_escuro, (deslocamento_x, deslocamento_y))

        pygame.display.flip()
        relogio.tick(FPS)