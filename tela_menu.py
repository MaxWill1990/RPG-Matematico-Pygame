import pygame
import sys
from configuracoes import *


def exibir_menu(tela):
    try:
        fundo = pygame.image.load("assets/menugame.png")
        fundo = pygame.transform.scale(fundo, (LARGURA_TELA, ALTURA_TELA))
    except:
        fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        fundo.fill(PRETO)

    # Adicionando um desenho na tela inicial
    try:
        desenho = pygame.image.load("assets/personagem.png")
        desenho = pygame.transform.scale(desenho, (150, 150))
    except:
        desenho = None

    fonte_titulo = pygame.font.SysFont("Arial", 70, bold=True)
    fonte_opcao = pygame.font.SysFont("Arial", 45, bold=True)

    opcoes = ["NOVO JOGO", "SAIR"]
    indice_selecionado = 0

    relogio = pygame.time.Clock()

    # ESSA LINHA SEGURA O MENU ABERTO:
    while True:
        tela.blit(fundo, (0, 0))

        pelicula_escura = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        pelicula_escura.fill(PRETO)
        pelicula_escura.set_alpha(128)
        tela.blit(pelicula_escura, (0, 0))

        texto_titulo = "A PROVA FINAL"
        txt_titulo = fonte_titulo.render(texto_titulo, True, AMARELO_DESTAQUE)
        sombra_titulo = fonte_titulo.render(texto_titulo, True, PRETO)

        tela.blit(sombra_titulo, (LARGURA_TELA // 2 - sombra_titulo.get_width() // 2 + 4, 104))
        tela.blit(txt_titulo, (LARGURA_TELA // 2 - txt_titulo.get_width() // 2, 100))

        for i, opcao in enumerate(opcoes):
            if i == indice_selecionado:
                cor = VERDE_HP
                texto_exibicao = f"> {opcao} <"
            else:
                cor = BRANCO
                texto_exibicao = opcao

            txt_op = fonte_opcao.render(texto_exibicao, True, cor)
            sombra_op = fonte_opcao.render(texto_exibicao, True, PRETO)

            pos_y = 350 + (i * 80)

            tela.blit(sombra_op, (LARGURA_TELA // 2 - sombra_op.get_width() // 2 + 3, pos_y + 3))
            tela.blit(txt_op, (LARGURA_TELA // 2 - txt_op.get_width() // 2, pos_y))

        # Desenha o personagem, se disponível
        if desenho:
            tela.blit(desenho, (LARGURA_TELA // 2 - desenho.get_width() // 2, ALTURA_TELA // 2 - desenho.get_height() // 2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    indice_selecionado = (indice_selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    indice_selecionado = (indice_selecionado + 1) % len(opcoes)
                elif evento.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    if indice_selecionado == 0:
                        return "novo_jogo"
                    else:
                        return "sair"

        relogio.tick(FPS)