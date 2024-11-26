import pygame as pg
import sys
import Game_Start
import funcoes_interface

def iniciar_jogo():
    global tela_atual
    tela_atual = "start"

def regras():
    global tela_atual
    tela_atual = "regras"
    
def opcoes():
    global tela_atual
    tela_atual = "opcoes"  

def mutar():
    global tocando
    if tocando:
        tocando = False
        pg.mixer_music.pause()
    else:
        tocando = True
        pg.mixer_music.unpause()
    
def sair():
    pg.quit()
    sys.exit()

def voltar_menu():
    global tela_atual
    tela_atual = "menu"

def voltar_opcoes():
    global tela_atual
    tela_atual = "opcoes"

def mudar_dificuldade():
    global bot_dificil
    if bot_dificil:
        bot_dificil = False
    else:
        bot_dificil = True

pg.init()
pg.mixer.init()

global altura, largura
altura = 720
largura = 1280
imagem_menu = pg.image.load("images//Menu_Image.png")
imagem_menu = pg.transform.scale(imagem_menu, (largura, altura))
imagem_tabuleiro = pg.image.load("images//tabuleiro.png")
imagem_tabuleiro = pg.transform.scale(imagem_tabuleiro, (largura, altura))
global tela
tela = pg.display.set_mode((largura, altura))
rodando = True
preto = (0, 0, 0)
cinza_claro = (170, 170, 170)
cinza_escuro = (100, 100, 100)
fonte = pg.font.SysFont('couriernew', 20, True, True)
posicao_inicial_carta = [-100, -100]
posicao_final_carta = [80, 130]
velocidade_carta = 5  # Velocidade de animação da carta
tela_atual = "menu"
fps = 60
clock = pg.time.Clock()
pg.mixer.music.load("musics//menu_musica.mp3")
global tocando, bot_dificil
tocando = True
bot_dificil = False
pg.mixer.music.play(-1)

while rodando:

    tela.blit(imagem_menu, (0, 0))
    clique = False
    mouse_pos = pg.mouse.get_pos()

    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            rodando = False
        if evento.type == pg.MOUSEBUTTONDOWN:
            clique = True

    if tela_atual == "menu":
        funcoes_interface.desenhar_botao(tela, "Iniciar Jogo", largura // 2.4, altura // 1.85, 200, 60, cinza_claro, cinza_escuro, mouse_pos, clique, iniciar_jogo)
        funcoes_interface.desenhar_botao(tela, "opções", largura // 2.4, altura // 1.5, 200, 60, cinza_claro, cinza_escuro, mouse_pos, clique, opcoes)
        funcoes_interface.desenhar_botao(tela, "Sair", largura // 2.4, altura // 1.25, 200, 60, cinza_claro, cinza_escuro, mouse_pos, clique, sair)

    elif tela_atual == "opcoes":
        funcoes_interface.desenhar_botao(tela, "<- Voltar", 25, 25, 125, 40, cinza_claro, cinza_escuro, mouse_pos, clique, voltar_menu)
        if tocando:
            funcoes_interface.desenhar_botao(tela, "musica: on", largura // 2.45, altura // 1.85, 250, 60, cinza_claro, cinza_escuro, mouse_pos, clique, mutar)
        elif tocando == False:
            funcoes_interface.desenhar_botao(tela, "musica: off", largura // 2.45, altura // 1.85, 250, 60, cinza_claro, cinza_escuro, mouse_pos, clique, mutar)

        if bot_dificil == False:
            funcoes_interface.desenhar_botao(tela, "dificuldade: fácil", largura // 2.45, altura // 1.5, 250, 60, cinza_claro, cinza_escuro, mouse_pos, clique, mudar_dificuldade)
        
        elif bot_dificil:
            funcoes_interface.desenhar_botao(tela, "dificuldade: difícil", largura // 2.45, altura // 1.5, 250, 60, cinza_claro, cinza_escuro, mouse_pos, clique, mudar_dificuldade)
        funcoes_interface.desenhar_botao(tela, "Ver Regras", largura // 2.45, altura // 1.25, 250, 60, cinza_claro, cinza_escuro, mouse_pos, clique, regras)


    elif tela_atual == "regras":
        funcoes_interface.desenhar_texto_com_fundo(tela, "=== REGRAS DO JOGO ===", largura // 6.5, altura // 1.8, 880, 50, cinza_escuro, preto, 20)
        funcoes_interface.desenhar_texto_com_fundo(tela, "1. Cada jogador começa com 5 cartas.", largura // 6.5, altura // 1.6, 880, 50, cinza_escuro, preto, 20)
        funcoes_interface.desenhar_texto_com_fundo(tela, "2. Os jogadores se alternam para jogar suas cartas em um tabuleiro 3x3.", largura // 6.5, altura // 1.6 + 50, 880, 50, cinza_escuro, preto, 20)
        funcoes_interface.desenhar_texto_com_fundo(tela, "3. O jogador que capturar mais cartas ganha.", largura // 6.5, altura // 1.6 + 100, 880, 50, cinza_escuro, preto, 20)
        funcoes_interface.desenhar_texto_com_fundo(tela, "4. As cartas têm valores em 4 lados e podem capturar cartas do oponente.", largura // 6.5, altura // 1.6 + 150, 880, 50, cinza_escuro, preto, 20)
        funcoes_interface.desenhar_texto_com_fundo(tela, "5. O jogo termina quando todas as cartas são jogadas.", largura // 6.5, altura // 1.6 + 200, 880, 50, cinza_escuro, preto, 20)
    
        funcoes_interface.desenhar_botao(tela, "<- Voltar", 25, 25, 125, 40, cinza_claro, cinza_escuro, mouse_pos, clique, voltar_menu)


    elif tela_atual == "start":
        pg.mixer.music.stop()
        Game_Start.start(bot_dificil, tela, largura, altura, tocando)

    pg.display.update()
    clock.tick(fps)
sys.exit()
pg.quit()