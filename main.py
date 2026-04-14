import pygame
import sys
import random
from configuracoes import *
from tela_menu import exibir_menu
from cena_intro import exibir_intro
from combate import gerar_pergunta, gerar_pergunta_super


# Função de escala
def escalar_proporcional(imagem, altura_desejada):
    largura_original, altura_original = imagem.get_size()
    proporcao = largura_original / altura_original
    nova_largura = int(altura_desejada * proporcao)
    return pygame.transform.smoothscale(imagem, (nova_largura, altura_desejada))


pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("A Prova Final - Demo")


# --- CARREGANDO EFEITOS SONOROS (SFX) ---
def carregar_som(caminho):
    try:
        return pygame.mixer.Sound(caminho)
    except:
        return None


som_ataque = carregar_som("assets/som_ataque.mp3")
som_dano = carregar_som("assets/som_dano.mp3")
som_combo = carregar_som("assets/som_combo.mp3")
som_vitoria = carregar_som("assets/som_vitoria.mp3")
som_gameover = carregar_som("assets/som_gameover.mp3")

# Fontes
fonte_nome = pygame.font.SysFont("Arial", 22, bold=True)
fonte_hp = pygame.font.SysFont("Arial", 50, bold=True)
fonte_pergunta = pygame.font.SysFont("Arial", 45, bold=True)
fonte_digitacao = pygame.font.SysFont("Arial", 35)
fonte_feedback = pygame.font.SysFont("Arial", 80, bold=True)
fonte_aviso = pygame.font.SysFont("Arial", 30, italic=True)
fonte_timer = pygame.font.SysFont("Arial", 50, bold=True)
fonte_tut_titulo = pygame.font.SysFont("Arial", 50, bold=True)
fonte_tut_texto = pygame.font.SysFont("Arial", 28, bold=True)

COR_JAMES = (0, 191, 255)
COR_INIMIGO = (255, 60, 60)

relogio = pygame.time.Clock()

while True:
    # 🎵 RESET DE ÁUDIO E VOLTA AO MENU
    pygame.mixer.stop()
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/musica_menu.mp3")
    pygame.mixer.music.play(-1)

    escolha = exibir_menu(tela)
    if escolha != "novo_jogo":
        break

    pygame.mixer.music.load("assets/musica_intro.mp3")
    pygame.mixer.music.play(-1)
    exibir_intro(tela)

    fundo = pygame.image.load("assets/cenariodaluta.png")
    fundo = pygame.transform.scale(fundo, (LARGURA_TELA, ALTURA_TELA))

    altura_heroi, altura_inimigo = 320, 290

    # Carregamento de Sprites
    img_heroi_normal = escalar_proporcional(pygame.image.load("assets/heroinormal.png"), altura_heroi)
    img_heroi_ataque = escalar_proporcional(pygame.image.load("assets/heroiataque.png"), altura_heroi)
    img_heroi_dano = escalar_proporcional(pygame.image.load("assets/heroidano.png"), altura_heroi)
    try:
        img_heroi_super = escalar_proporcional(pygame.image.load("assets/heroisuper.png"), altura_heroi)
    except:
        img_heroi_super = img_heroi_ataque

    img_ini_normal = escalar_proporcional(pygame.image.load("assets/inimigonormal.png"), altura_inimigo)
    img_ini_ataque = escalar_proporcional(pygame.image.load("assets/inimigoataque.png"), altura_inimigo)
    img_ini_dano = escalar_proporcional(pygame.image.load("assets/inimigodano.png"), altura_inimigo)
    img_ini_derrota = escalar_proporcional(pygame.image.load("assets/inimigo defauteado.png"), altura_inimigo)

    img_boss_normal = escalar_proporcional(pygame.image.load("assets/bossnormal.png"), altura_inimigo)
    img_boss_ataque = escalar_proporcional(pygame.image.load("assets/bossataque.png"), altura_inimigo)
    img_boss_dano = escalar_proporcional(pygame.image.load("assets/bossdano.png"), altura_inimigo)
    img_boss_derrota = escalar_proporcional(pygame.image.load("assets/bossderrota.png"), altura_inimigo)

    tela_gameover = pygame.transform.scale(pygame.image.load("assets/Derrota.png"), (LARGURA_TELA, ALTURA_TELA))
    tela_vitoria = pygame.transform.scale(pygame.image.load("assets/Victory.png"), (LARGURA_TELA, ALTURA_TELA))

    hp_heroi, hp_inimigo_atual = 150, 150
    fase_boss, estado_jogo = False, "tutorial"
    pergunta_atual, resposta_correta = gerar_pergunta(is_boss=False)
    texto_digitado = ""
    indice_selecionado, tempo_limite_base, tempo_turno_atual, tempo_restante = 0, 10, 10, 10
    tempo_inicio_turno = 0

    opcoes_dificuldade = ["FÁCIL - 10 segundos", "NORMAL - 5 segundos"]
    acertos_seguidos, erros_seguidos, status_combo = 0, 0, ""
    tremor_frames, tempo_feedback, frames_transicao, frames_flash = 0, 0, 0, 0
    msg_feedback = ""
    heroi_atual, inimigo_atual = img_heroi_normal, img_ini_normal
    pos_x_heroi, pos_x_inimigo = -80, 320
    alvo_tremor = "heroi"

    rodando_batalha = True
    while rodando_batalha:
        agora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # 🏠 VOLTAR AO MENU NAS TELAS FINAIS
                if estado_jogo in ["gameover", "vitoria"]:
                    if evento.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                        rodando_batalha = False

                elif estado_jogo == "tutorial":
                    if evento.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                        estado_jogo = "dificuldade"

                elif estado_jogo == "dificuldade":
                    if evento.key == pygame.K_UP:
                        indice_selecionado = (indice_selecionado - 1) % 2
                    elif evento.key == pygame.K_DOWN:
                        indice_selecionado = (indice_selecionado + 1) % 2
                    elif evento.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        tempo_limite_base = 10 if indice_selecionado == 0 else 5
                        tempo_turno_atual, estado_jogo = tempo_limite_base, "lutando"
                        pygame.mixer.music.load("assets/musica_batalha.mp3")
                        pygame.mixer.music.play(-1)
                        tempo_inicio_turno = agora

                elif estado_jogo == "lutando":
                    if evento.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        if texto_digitado == resposta_correta:
                            # ACERTOU!
                            if status_combo == "preparando_heroi":
                                hp_inimigo_atual -= 75
                                heroi_atual, frames_flash = img_heroi_super, 30
                                if som_combo:
                                    som_combo.play()
                            else:
                                hp_inimigo_atual -= 25
                                heroi_atual = img_heroi_ataque
                                if som_ataque:
                                    som_ataque.play()

                            alvo_tremor, tremor_frames, tempo_feedback = "inimigo", 30, 120
                            msg_feedback = "ACERTOU!"
                            inimigo_atual = img_boss_dano if fase_boss else img_ini_dano
                            acertos_seguidos += 1
                            erros_seguidos = 0

                            if hp_inimigo_atual <= 0:
                                hp_inimigo_atual = 0
                                if not fase_boss:
                                    estado_jogo = "transicao_boss"
                                    frames_transicao = 120
                                    inimigo_atual = img_ini_derrota
                                else:
                                    estado_jogo = "espera_vitoria"
                                    frames_transicao = 120
                                    inimigo_atual = img_boss_derrota
                                    pygame.mixer.music.stop()
                                    if som_vitoria:
                                        som_vitoria.play()
                        else:
                            # ERROU!
                            if status_combo == "preparando_inimigo":
                                hp_heroi -= 60
                            else:
                                hp_heroi -= 20

                            if som_dano:
                                som_dano.play()

                            msg_feedback, tremor_frames, tempo_feedback = "ERROU!", 30, 120
                            heroi_atual = img_heroi_dano
                            inimigo_atual = img_boss_ataque if fase_boss else img_ini_ataque
                            alvo_tremor = "heroi"
                            erros_seguidos += 1
                            acertos_seguidos = 0

                            if hp_heroi <= 0:
                                estado_jogo = "gameover"
                                pygame.mixer.music.stop()
                                if som_gameover:
                                    som_gameover.play()

                        if estado_jogo == "lutando":
                            texto_digitado = ""
                            if acertos_seguidos == 3:
                                resultado = gerar_pergunta_super()
                                status_combo = "preparando_heroi"
                                tempo_turno_atual = 12
                                pergunta_atual = resultado[0]
                                resposta_correta = resultado[1]
                            elif erros_seguidos == 3:
                                resultado = gerar_pergunta(fase_boss)
                                status_combo = "preparando_inimigo"
                                tempo_turno_atual = tempo_limite_base
                                pergunta_atual = resultado[0]
                                resposta_correta = resultado[1]
                            else:
                                resultado = gerar_pergunta(fase_boss)
                                status_combo = ""
                                tempo_turno_atual = tempo_limite_base
                                pergunta_atual = resultado[0]
                                resposta_correta = resultado[1]
                            tempo_inicio_turno = agora

                    elif evento.key == pygame.K_BACKSPACE:
                        texto_digitado = texto_digitado[:-1]
                    else:
                        if evento.unicode.isnumeric() or evento.unicode == '-':
                            texto_digitado += evento.unicode

        # --- CRONÔMETRO ---
        if estado_jogo == "lutando" and tempo_feedback <= 0:
            passado = (agora - tempo_inicio_turno) // 1000
            tempo_restante = tempo_turno_atual - passado
            if tempo_restante <= 0:
                hp_heroi -= 20
                if som_dano:
                    som_dano.play()
                msg_feedback = "TEMPO!"
                tremor_frames = 30
                tempo_feedback = 120
                heroi_atual = img_heroi_dano
                alvo_tremor = "heroi"
                inimigo_atual = img_boss_ataque if fase_boss else img_ini_ataque
                erros_seguidos += 1
                acertos_seguidos = 0
                texto_digitado = ""
                tempo_inicio_turno = agora

                resultado = gerar_pergunta(fase_boss)
                pergunta_atual = resultado[0]
                resposta_correta = resultado[1]

                if hp_heroi <= 0:
                    estado_jogo = "gameover"
                    pygame.mixer.music.stop()
                    if som_gameover:
                        som_gameover.play()

        # --- TRANSIÇÕES ---
        if estado_jogo == "transicao_boss":
            frames_transicao -= 1
            if frames_transicao == 60:
                fase_boss = True
                hp_inimigo_atual = 200
                inimigo_atual = img_boss_normal
                heroi_atual = img_heroi_normal
                pygame.mixer.music.load("assets/musica_boss.mp3")
                pygame.mixer.music.play(-1)
            if frames_transicao <= 0:
                estado_jogo = "lutando"
                texto_digitado = ""
                resultado = gerar_pergunta(True)
                pergunta_atual = resultado[0]
                resposta_correta = resultado[1]

        if estado_jogo == "espera_vitoria":
            frames_transicao -= 1
            if frames_transicao <= 0:
                estado_jogo = "vitoria"

        # --- LÓGICA DE TREMOR E RESET DE IMAGEM ---
        offset_hx, offset_hy, offset_ix, offset_iy = 0, 0, 0, 0
        if tremor_frames > 0:
            dx = random.randint(-8, 8)
            dy = random.randint(-8, 8)
            if alvo_tremor == "heroi":
                offset_hx, offset_hy = dx, dy
            else:
                offset_ix, offset_iy = dx, dy
            tremor_frames -= 1

        if tempo_feedback > 0:
            tempo_feedback -= 1
            if tempo_feedback == 0 and hp_inimigo_atual > 0 and hp_heroi > 0:
                heroi_atual = img_heroi_normal
                inimigo_atual = img_boss_normal if fase_boss else img_ini_normal

        # --- DESENHO ---
        if estado_jogo in ["lutando", "tutorial", "dificuldade", "transicao_boss", "espera_vitoria"]:
            tela.blit(fundo, (0, 0))
            tela.blit(heroi_atual, (pos_x_heroi + offset_hx, 640 - altura_heroi + offset_hy))
            tela.blit(inimigo_atual, (pos_x_inimigo + offset_ix, 600 - altura_inimigo + offset_iy))

            # 🌟 CLARÃO DO BOSS (Entre os personagens e o HUD)
            if estado_jogo == "transicao_boss":
                alpha = int(255 * (120 - frames_transicao) / 60) if frames_transicao > 60 else int(
                    255 * frames_transicao / 60)
                brilho = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
                brilho.fill(BRANCO)
                brilho.set_alpha(max(0, min(255, alpha)))
                tela.blit(brilho, (0, 0))

            # HUD de Perguntas
            pygame.draw.rect(tela, PRETO, (50, 20, 700, 120))
            pygame.draw.rect(tela, BRANCO, (50, 20, 700, 120), 3)
            if estado_jogo not in ["transicao_boss", "tutorial", "espera_vitoria"]:
                tela.blit(fonte_pergunta.render(f"Conta: {pergunta_atual}", True, BRANCO), (70, 30))
                tela.blit(fonte_digitacao.render(f"RESPOSTA: {texto_digitado}", True, AMARELO_DESTAQUE), (70, 90))

            # HUD de Status
            tela.blit(fonte_nome.render("JAMES", True, COR_JAMES), (50, 150))
            tela.blit(fonte_hp.render(f"{hp_heroi}/150", True, VERDE_HP), (50, 175))
            tela.blit(fonte_nome.render("BOSS" if fase_boss else "INIMIGO", True, COR_INIMIGO), (550, 150))
            tela.blit(fonte_hp.render(f"{hp_inimigo_atual}/{200 if fase_boss else 150}", True, VERMELHO_DANO),
                      (550, 175))

            if estado_jogo == "tutorial":
                ov = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
                ov.fill((0, 0, 0, 200))
                tela.blit(ov, (0, 0))

                # Textos detalhados e coloridos
                txt_t1 = fonte_tut_titulo.render("SISTEMA DE COMBATE", True, AMARELO_DESTAQUE)
                txt_t2 = fonte_tut_texto.render("Sua arma é o conhecimento! Responda as", True, BRANCO)
                txt_t3 = fonte_tut_texto.render("equações corretamente para atacar.", True, BRANCO)
                txt_t4 = fonte_tut_texto.render("Se você errar ou o tempo acabar,", True, VERMELHO_DANO)
                txt_t5 = fonte_tut_texto.render("o inimigo vai te punir!", True, VERMELHO_DANO)
                txt_t6 = fonte_tut_texto.render("Zere o HP de todos para vencer a prova.", True, VERDE_HP)
                txt_t7 = fonte_aviso.render("(Pressione ENTER para continuar)", True, CINZA)

                # Centralização e posicionamento
                tela.blit(txt_t1, (LARGURA_TELA // 2 - txt_t1.get_width() // 2, 120))
                tela.blit(txt_t2, (LARGURA_TELA // 2 - txt_t2.get_width() // 2, 220))
                tela.blit(txt_t3, (LARGURA_TELA // 2 - txt_t3.get_width() // 2, 260))
                tela.blit(txt_t4, (LARGURA_TELA // 2 - txt_t4.get_width() // 2, 320))
                tela.blit(txt_t5, (LARGURA_TELA // 2 - txt_t5.get_width() // 2, 360))
                tela.blit(txt_t6, (LARGURA_TELA // 2 - txt_t6.get_width() // 2, 420))
                tela.blit(txt_t7, (LARGURA_TELA // 2 - txt_t7.get_width() // 2, 500))

            if estado_jogo == "dificuldade":
                ov = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
                ov.fill((0, 0, 0, 210))
                tela.blit(ov, (0, 0))
                for i, op in enumerate(opcoes_dificuldade):
                    cor = AMARELO_DESTAQUE if i == indice_selecionado else BRANCO
                    tela.blit(fonte_tut_texto.render(op, True, cor), (LARGURA_TELA // 2 - 150, 300 + i * 60))

            if estado_jogo == "lutando":
                c_t = BRANCO if tempo_restante > 2 else VERMELHO_DANO
                tela.blit(fonte_timer.render(str(max(0, tempo_restante)), True, c_t), (680, 45))

                # Exibir feedback de acerto/erro
                if tempo_feedback > 0:
                    cor = VERDE_HP if msg_feedback == "ACERTOU!" else (VERMELHO_DANO if msg_feedback == "ERROU!" else AMARELO_DESTAQUE)
                    txt_feedback = fonte_feedback.render(msg_feedback, True, cor)
                    tela.blit(txt_feedback, (LARGURA_TELA // 2 - txt_feedback.get_width() // 2, ALTURA_TELA // 2 - 50))

        elif estado_jogo == "gameover":
            tela.blit(tela_gameover, (0, 0))
            tela.blit(fonte_aviso.render("Pressione ENTER para voltar ao Menu", True, BRANCO), (230, 520))

        elif estado_jogo == "vitoria":
            tela.blit(tela_vitoria, (0, 0))
            tela.blit(fonte_aviso.render("Pressione ENTER para voltar ao Menu", True, PRETO), (230, 520))

        pygame.display.flip()
        relogio.tick(FPS)

pygame.quit()
sys.exit()