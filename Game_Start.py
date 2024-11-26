import pygame as pg
import sys
from classes.Carta import Carta
from classes.Jogador import Jogador
from classes.Tabuleiro import Tabuleiro
import funcoes_interface

def inicio_jogo():
    global tela_atual
    tela_atual = "comeco_jogo"

def start(bot_dificil, tela, largura, altura, tocando):
    pg.init()
    pg.mixer.init()
    musica_atual = None
    
    tabuleiro = Tabuleiro()
    global tela_atual
    tela_atual = "pre_jogo"
    
    if tocando and tela_atual != "endgame":
        pg.mixer.music.load("musics//gameplay_musica.mp3")
        pg.mixer.music.set_volume(0.25)
        pg.mixer.music.play(-1)
    
    # Dimensões e recursos
    imagem_menu = pg.image.load("images//FFXV.jpg")
    imagem_menu = pg.transform.scale(imagem_menu, (largura, altura))
    imagem_tabuleiro = pg.image.load("images//tabuleiro.png")
    imagem_tabuleiro = pg.transform.scale(imagem_tabuleiro, (largura, altura))
    imagem_vitoria = pg.image.load("images//WIN.png")
    imagem_vitoria = pg.transform.scale(imagem_vitoria, (500, 200))
    imagem_empate = pg.image.load("images//DRAW.png")
    imagem_empate = pg.transform.scale(imagem_empate, (500, 200))
    imagem_derrota = pg.image.load("images//LOSE.png")
    imagem_derrota = pg.transform.scale(imagem_derrota, (500, 200))

    rodando = True
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    cinza_claro = (170, 170, 170)
    cinza_escuro = (100, 100, 100)
    fonte = pg.font.SysFont('couriernew', 20, True, True)
    
    luva = pg.image.load("images//luva.png")
    luva = pg.transform.scale(luva, (60,60))

    fps = 60
    clock = pg.time.Clock()
    
    # Posição inicial e final da carta
    posicao_inicial_carta = [-100, -100]
    posicao_inicial_carta1_j1 = [0.055*largura, 0.25*altura]
    posicao_inicial_carta2_j1 = [0.055*largura, 0.25*altura+140]
    posicao_inicial_carta3_j1 = [0.055*largura, 0.25*altura+280]
    posicao_inicial_carta4_j1 = [0.16*largura, 0.25*altura]
    posicao_inicial_carta5_j1 = [0.16*largura, 0.25*altura+140]

    posicao_inicial_carta1_j2 = [0.74*largura, 0.25*altura]
    posicao_inicial_carta2_j2 = [0.74*largura, 0.25*altura+140]
    posicao_inicial_carta3_j2 = [0.845*largura, 0.25*altura]
    posicao_inicial_carta4_j2 = [0.845*largura, 0.25*altura+140]
    posicao_inicial_carta5_j2 = [0.845*largura, 0.25*altura+280]
    posicao_inicial_imagem_vencedor = [-400, 200]

    # Criando jogadores
    jogador1 = Jogador("j1")
    jogador2 = Jogador("j2")
    jogador1.carregar_cartas()
    jogador2.carregar_cartas()

    # Preparar as cartas de ambos os jogadores
    j1_cartas = []
    j1_cartas_grande = []
    j2_cartas = []
    tamanho_carta = 100
    mover_carta1_j1_posicao = []
    mover_carta2_j1_posicao = []
    mover_carta3_j1_posicao = []
    mover_carta4_j1_posicao = []
    mover_carta5_j1_posicao = []

    mover_carta1_j2_posicao = []
    mover_carta2_j2_posicao = []
    mover_carta3_j2_posicao = []
    mover_carta4_j2_posicao = []
    mover_carta5_j2_posicao = []

    for i in range(5):
        linha1j1 = []
        linha2j1 = []
        linha3j1 = []
        linha4j1 = []
        linha5j1 = []
        
        linha1j2 = []
        linha2j2 = []
        linha3j2 = []
        linha4j2 = []
        linha5j2 = []
        for j in range(5):
            linha1j1.append(False)
            linha2j1.append(False)
            linha3j1.append(False)
            linha4j1.append(False)
            linha5j1.append(False)
            
            linha1j2.append(False)
            linha2j2.append(False)
            linha3j2.append(False)
            linha4j2.append(False)
            linha5j2.append(False)
            
        mover_carta1_j1_posicao.append(linha1j1)
        mover_carta2_j1_posicao.append(linha2j1)
        mover_carta3_j1_posicao.append(linha3j1)
        mover_carta4_j1_posicao.append(linha4j1)
        mover_carta5_j1_posicao.append(linha5j1)

        mover_carta1_j2_posicao.append(linha1j2)
        mover_carta2_j2_posicao.append(linha2j2)
        mover_carta3_j2_posicao.append(linha3j2)
        mover_carta4_j2_posicao.append(linha4j2)
        mover_carta5_j2_posicao.append(linha5j2)

    carta1_j1_selecionada = False
    carta2_j1_selecionada = False
    carta3_j1_selecionada = False
    carta4_j1_selecionada = False
    carta5_j1_selecionada = False
    
    carta1_j2_selecionada = False
    carta2_j2_selecionada = False
    carta3_j2_selecionada = False
    carta4_j2_selecionada = False
    carta5_j2_selecionada = False
    
    
    vez = "jogador"
    
    for i in range(5):
        # Carregar e redimensionar as cartas de cada jogador
        j1_cartas.append(pg.image.load(jogador1.get_cartas()[i].get_imagem()))
        j2_cartas.append(pg.image.load(jogador2.get_cartas()[i].get_imagem()))
        
        j1_cartas[i] = pg.transform.scale(j1_cartas[i], (tamanho_carta, tamanho_carta))
        j1_cartas_grande.append(pg.transform.scale(j1_cartas[i], (150, 150)))
        
        j2_cartas[i] = pg.transform.scale(j2_cartas[i], (tamanho_carta, tamanho_carta))

    while rodando:
        tela.blit(imagem_tabuleiro, (0, 0))
        clique = False
        mouse_pos = pg.mouse.get_pos()
        
        # Verificar eventos de saída
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                rodando = False
            if evento.type == pg.MOUSEBUTTONDOWN:
                clique = True
            if evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE and tela_atual == "endgame":
                pg.mixer.music.stop()
                pg.quit()
                sys.exit()
                
        
        if tela_atual == "pre_jogo":            
            fundo_carta = pg.image.load("images//fundo_carta.jpeg")
            fundo_carta = pg.transform.scale(fundo_carta, (150, 150))
            
            # Exibir cartas e mover pela tela
            if posicao_inicial_carta < [largura * 0.04, altura * 0.42]:
                posicao_inicial_carta = funcoes_interface.mover_carta_e_imagem(posicao_inicial_carta, [largura * 0.04, altura * 0.42], 15)
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[0], posicao_inicial_carta, 150, jogador1.get_cartas()[0].get_up(), jogador1.get_cartas()[0].get_down(), jogador1.get_cartas()[0].get_left(), jogador1.get_cartas()[0].get_right())
                
            elif posicao_inicial_carta < [largura * 0.25, altura * 0.42]:
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[0], [largura * 0.04, altura * 0.42], 150, jogador1.get_cartas()[0].get_up(), jogador1.get_cartas()[0].get_down(), jogador1.get_cartas()[0].get_left(), jogador1.get_cartas()[0].get_right())
                posicao_inicial_carta = funcoes_interface.mover_carta_e_imagem(posicao_inicial_carta, [largura * 0.25, altura * 0.42], 15)
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[1], posicao_inicial_carta, 150, jogador1.get_cartas()[1].get_up(), jogador1.get_cartas()[1].get_down(), jogador1.get_cartas()[1].get_left(), jogador1.get_cartas()[1].get_right())
                
            elif posicao_inicial_carta < [largura * 0.45, altura * 0.42]:
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[0], [largura * 0.04, altura * 0.42], 150, jogador1.get_cartas()[0].get_up(), jogador1.get_cartas()[0].get_down(), jogador1.get_cartas()[0].get_left(), jogador1.get_cartas()[0].get_right())
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[1], [largura * 0.25, altura * 0.42], 150, jogador1.get_cartas()[1].get_up(), jogador1.get_cartas()[1].get_down(), jogador1.get_cartas()[1].get_left(), jogador1.get_cartas()[1].get_right())
                posicao_inicial_carta = funcoes_interface.mover_carta_e_imagem(posicao_inicial_carta, [largura * 0.45, altura * 0.42], 15)
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[2], posicao_inicial_carta, 150, jogador1.get_cartas()[2].get_up(), jogador1.get_cartas()[2].get_down(), jogador1.get_cartas()[2].get_left(), jogador1.get_cartas()[2].get_right())

            elif posicao_inicial_carta < [largura * 0.65, altura * 0.42]:
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[0], [largura * 0.04, altura * 0.42], 150, jogador1.get_cartas()[0].get_up(), jogador1.get_cartas()[0].get_down(), jogador1.get_cartas()[0].get_left(), jogador1.get_cartas()[0].get_right())
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[1], [largura * 0.25, altura * 0.42], 150, jogador1.get_cartas()[1].get_up(), jogador1.get_cartas()[1].get_down(), jogador1.get_cartas()[1].get_left(), jogador1.get_cartas()[1].get_right())
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[2], [largura * 0.45, altura * 0.42], 150, jogador1.get_cartas()[2].get_up(), jogador1.get_cartas()[2].get_down(), jogador1.get_cartas()[2].get_left(), jogador1.get_cartas()[2].get_right())
                posicao_inicial_carta = funcoes_interface.mover_carta_e_imagem(posicao_inicial_carta, [largura * 0.65, altura * 0.42], 15)
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[3], posicao_inicial_carta, 150, jogador1.get_cartas()[3].get_up(), jogador1.get_cartas()[3].get_down(), jogador1.get_cartas()[3].get_left(), jogador1.get_cartas()[3].get_right())
                
            elif posicao_inicial_carta <= [largura * 0.85, altura * 0.42]:
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[0], [largura * 0.04, altura * 0.42], 150, jogador1.get_cartas()[0].get_up(), jogador1.get_cartas()[0].get_down(), jogador1.get_cartas()[0].get_left(), jogador1.get_cartas()[0].get_right())
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[1], [largura * 0.25, altura * 0.42], 150, jogador1.get_cartas()[1].get_up(), jogador1.get_cartas()[1].get_down(), jogador1.get_cartas()[1].get_left(), jogador1.get_cartas()[1].get_right())
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[2], [largura * 0.45, altura * 0.42], 150, jogador1.get_cartas()[2].get_up(), jogador1.get_cartas()[2].get_down(), jogador1.get_cartas()[2].get_left(), jogador1.get_cartas()[2].get_right())
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[3], [largura * 0.65, altura * 0.42], 150, jogador1.get_cartas()[3].get_up(), jogador1.get_cartas()[3].get_down(), jogador1.get_cartas()[3].get_left(), jogador1.get_cartas()[3].get_right())
                posicao_inicial_carta = funcoes_interface.mover_carta_e_imagem(posicao_inicial_carta, [largura * 0.85, altura * 0.42], 15)
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas_grande[4], posicao_inicial_carta, 150, jogador1.get_cartas()[4].get_up(), jogador1.get_cartas()[4].get_down(), jogador1.get_cartas()[4].get_left(), jogador1.get_cartas()[4].get_right())

            if posicao_inicial_carta == [largura * 0.85, altura * 0.42]:
                    funcoes_interface.desenhar_botao(tela, "iniciar jogo", largura//2.2, altura//1.2, 150, 50, cinza_claro, cinza_escuro, mouse_pos, clique, inicio_jogo)
                    funcoes_interface.desenhar_texto(tela, "SUA MÃO", largura//2.5, altura//5, 60, preto)
                    
        elif tela_atual == "comeco_jogo":
            fundo_carta = pg.image.load("images//fundo_carta.jpeg")
            fundo_carta = pg.transform.scale(fundo_carta, (tamanho_carta, tamanho_carta))

            # Desenhar cartas do jogador 1
            funcoes_interface.desenhar_texto(tela, "Jogador 1", 0.04*largura, 0.08*altura, 35, preto)
            if(jogador1.get_cartas()[0].get_posicao() == None):
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas[0], (0.055*largura, 0.25*altura), tamanho_carta, jogador1.get_cartas()[0].get_up(), jogador1.get_cartas()[0].get_down(), jogador1.get_cartas()[0].get_left(), jogador1.get_cartas()[0].get_right())
            if(jogador1.get_cartas()[1].get_posicao() == None):
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas[1], (0.055*largura, 0.25*altura+140), tamanho_carta, jogador1.get_cartas()[1].get_up(), jogador1.get_cartas()[1].get_down(), jogador1.get_cartas()[1].get_left(), jogador1.get_cartas()[1].get_right())
            if(jogador1.get_cartas()[2].get_posicao() == None):
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas[2], (0.055*largura, 0.25*altura+280), tamanho_carta, jogador1.get_cartas()[2].get_up(), jogador1.get_cartas()[2].get_down(), jogador1.get_cartas()[2].get_left(), jogador1.get_cartas()[2].get_right())
            if(jogador1.get_cartas()[3].get_posicao() == None):
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas[3], (0.16*largura, 0.25*altura), tamanho_carta, jogador1.get_cartas()[3].get_up(), jogador1.get_cartas()[3].get_down(), jogador1.get_cartas()[3].get_left(), jogador1.get_cartas()[3].get_right())
            if(jogador1.get_cartas()[4].get_posicao() == None):
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j1_cartas[4], (0.16*largura, 0.25*altura+140), tamanho_carta, jogador1.get_cartas()[4].get_up(), jogador1.get_cartas()[4].get_down(), jogador1.get_cartas()[4].get_left(), jogador1.get_cartas()[4].get_right())
            funcoes_interface.desenhar_texto(tela, f"{tabuleiro.qtd_carta_jogador(jogador1)}", 0.12*largura, 0.85*altura, 60, preto)

            # Desenhar cartas do jogador 2
            funcoes_interface.desenhar_texto(tela, "Jogador 2", 0.8*largura, 0.08*altura, 35, preto)
            if jogador2.get_cartas()[0].get_posicao() == None:
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j2_cartas[0], (0.74*largura, 0.25*altura), tamanho_carta, jogador2.get_cartas()[0].get_up(), jogador2.get_cartas()[0].get_down(), jogador2.get_cartas()[0].get_left(), jogador2.get_cartas()[0].get_right())
            if jogador2.get_cartas()[1].get_posicao() == None:                
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j2_cartas[1], (0.74*largura, 0.25*altura+140), tamanho_carta, jogador2.get_cartas()[1].get_up(), jogador2.get_cartas()[1].get_down(), jogador2.get_cartas()[1].get_left(), jogador2.get_cartas()[1].get_right())
            if jogador2.get_cartas()[2].get_posicao() == None:
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j2_cartas[2], (0.845*largura, 0.25*altura), tamanho_carta, jogador2.get_cartas()[2].get_up(), jogador2.get_cartas()[2].get_down(), jogador2.get_cartas()[2].get_left(), jogador2.get_cartas()[2].get_right())
            if jogador2.get_cartas()[3].get_posicao() == None:
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j2_cartas[3], (0.845*largura, 0.25*altura+140), tamanho_carta, jogador2.get_cartas()[3].get_up(), jogador2.get_cartas()[3].get_down(), jogador2.get_cartas()[3].get_left(), jogador2.get_cartas()[3].get_right())
            if jogador2.get_cartas()[4].get_posicao() == None:
                funcoes_interface.desenhar_carta_com_fundo(tela, fundo_carta, j2_cartas[4], (0.845*largura, 0.25*altura+280), tamanho_carta, jogador2.get_cartas()[4].get_up(), jogador2.get_cartas()[4].get_down(), jogador2.get_cartas()[4].get_left(), jogador2.get_cartas()[4].get_right())
            funcoes_interface.desenhar_texto(tela, f"{tabuleiro.qtd_carta_jogador(jogador2)}", 0.85*largura, 0.85*altura, 60, preto)
            
            posicoes_tabuleiro = [
            [largura*0.274, altura*0.185, largura*0.274*0.556, altura*0.187*1.11],
            [largura*0.425, altura*0.185, largura*0.274*0.556, altura*0.187*1.11],
            [largura*0.57, altura*0.185, largura*0.274*0.556, altura*0.187*1.11],
            [largura*0.274, altura*0.392, largura*0.274*0.556, altura*0.187*1.11],
            [largura*0.425, altura*0.392, largura*0.274*0.556, altura*0.187*1.11],
            [largura*0.57, altura*0.392, largura*0.274*0.556, altura*0.187*1.11],
            [largura*0.274, altura*0.595, largura*0.274*0.556, altura*0.187*1.11],
            [largura*0.425, altura*0.595, largura*0.274*0.556, altura*0.187*1.11],
            [largura*0.57, altura*0.595, largura*0.274*0.556, altura*0.187*1.11]
            ]
            
            posicao_carta1_j1 = 0.055*largura < mouse_pos[0] < 0.055*largura + tamanho_carta and 0.25*altura < mouse_pos[1] < 0.25*altura + tamanho_carta
            posicao_carta2_j1 = 0.055*largura < mouse_pos[0] < 0.055*largura + tamanho_carta and 0.25*altura+140 < mouse_pos[1] < 0.25*altura +140+ tamanho_carta
            posicao_carta3_j1 = 0.055*largura < mouse_pos[0] < 0.055*largura + tamanho_carta and 0.25*altura+280 < mouse_pos[1] < 0.25*altura+280+ tamanho_carta
            posicao_carta4_j1 = 0.16*largura < mouse_pos[0] < 0.16*largura + tamanho_carta and 0.25*altura < mouse_pos[1] < 0.25*altura+ tamanho_carta
            posicao_carta5_j1 = 0.16 *largura < mouse_pos[0] < 0.16*largura + tamanho_carta and 0.25*altura+140 < mouse_pos[1] < 0.25*altura+140+tamanho_carta

            posicao_carta1_j2 = 0.74*largura < mouse_pos[0] < 0.74*largura + tamanho_carta and 0.25*altura < mouse_pos[1] < 0.25*altura + tamanho_carta
            posicao_carta2_j2 = 0.74*largura < mouse_pos[0] < 0.74*largura + tamanho_carta and 0.25*altura+140 < mouse_pos[1] < 0.25*altura +140+ tamanho_carta
            posicao_carta3_j2 = 0.845*largura < mouse_pos[0] < 0.845*largura + tamanho_carta and 0.25*altura < mouse_pos[1] < 0.25*altura+ tamanho_carta
            posicao_carta4_j2 = 0.845*largura < mouse_pos[0] < 0.845*largura + tamanho_carta and 0.25*altura+140 < mouse_pos[1] < 0.25*altura+140+ tamanho_carta
            posicao_carta5_j2 = 0.845*largura < mouse_pos[0] < 0.845*largura + tamanho_carta and 0.25*altura+280 < mouse_pos[1] < 0.25*altura+280+tamanho_carta

            if vez == "jogador":
                carta1_j1_selecionada, carta2_j1_selecionada, carta3_j1_selecionada, carta4_j1_selecionada, carta5_j1_selecionada = funcoes_interface.selecionar_carta(posicao_carta1_j1, posicao_carta2_j1, posicao_carta3_j1, posicao_carta4_j1, posicao_carta5_j1, clique, jogador1, carta1_j1_selecionada, carta2_j1_selecionada, carta3_j1_selecionada, carta4_j1_selecionada, carta5_j1_selecionada)
                
                if carta1_j1_selecionada and clique and jogador1.get_cartas()[0].get_posicao() == None:
                    if posicoes_tabuleiro[0][0] < mouse_pos[0] < posicoes_tabuleiro[0][0]+posicoes_tabuleiro[0][2] and posicoes_tabuleiro[0][1] < mouse_pos[1] < posicoes_tabuleiro[0][1]+posicoes_tabuleiro[0][3]:
                        mover_carta1_j1_posicao[0][0] = True
                    if posicoes_tabuleiro[1][0] < mouse_pos[0] < posicoes_tabuleiro[1][0]+posicoes_tabuleiro[1][2] and posicoes_tabuleiro[1][1] < mouse_pos[1] < posicoes_tabuleiro[1][1]+posicoes_tabuleiro[1][3]:
                        mover_carta1_j1_posicao[0][1]  = True
                    if posicoes_tabuleiro[2][0] < mouse_pos[0] < posicoes_tabuleiro[2][0]+posicoes_tabuleiro[2][2] and posicoes_tabuleiro[2][1] < mouse_pos[1] < posicoes_tabuleiro[2][1]+posicoes_tabuleiro[2][3]:
                        mover_carta1_j1_posicao[0][2]  = True
                    if posicoes_tabuleiro[3][0] < mouse_pos[0] < posicoes_tabuleiro[3][0]+posicoes_tabuleiro[3][2] and posicoes_tabuleiro[3][1] < mouse_pos[1] < posicoes_tabuleiro[3][1]+posicoes_tabuleiro[3][3]:
                        mover_carta1_j1_posicao[1][0]  = True                
                    if posicoes_tabuleiro[4][0] < mouse_pos[0] < posicoes_tabuleiro[4][0]+posicoes_tabuleiro[4][2] and posicoes_tabuleiro[4][1] < mouse_pos[1] < posicoes_tabuleiro[4][1]+posicoes_tabuleiro[4][3]:
                        mover_carta1_j1_posicao[1][1]  = True
                    if posicoes_tabuleiro[5][0] < mouse_pos[0] < posicoes_tabuleiro[5][0]+posicoes_tabuleiro[5][2] and posicoes_tabuleiro[5][1] < mouse_pos[1] < posicoes_tabuleiro[5][1]+posicoes_tabuleiro[5][3]:
                        mover_carta1_j1_posicao[1][2]  = True
                    if posicoes_tabuleiro[6][0] < mouse_pos[0] < posicoes_tabuleiro[6][0]+posicoes_tabuleiro[6][2] and posicoes_tabuleiro[6][1] < mouse_pos[1] < posicoes_tabuleiro[6][1]+posicoes_tabuleiro[6][3]:
                        mover_carta1_j1_posicao[2][0]  = True
                    if posicoes_tabuleiro[7][0] < mouse_pos[0] < posicoes_tabuleiro[7][0]+posicoes_tabuleiro[7][2] and posicoes_tabuleiro[7][1] < mouse_pos[1] < posicoes_tabuleiro[7][1]+posicoes_tabuleiro[7][3]:
                        mover_carta1_j1_posicao[2][1]  = True
                    if posicoes_tabuleiro[8][0] < mouse_pos[0] < posicoes_tabuleiro[8][0]+posicoes_tabuleiro[8][2] and posicoes_tabuleiro[8][1] < mouse_pos[1] < posicoes_tabuleiro[8][1]+posicoes_tabuleiro[8][3]:
                        mover_carta1_j1_posicao[2][2]  = True
                
                if carta2_j1_selecionada and clique and jogador1.get_cartas()[1].get_posicao() == None:
                    if posicoes_tabuleiro[0][0] < mouse_pos[0] < posicoes_tabuleiro[0][0]+posicoes_tabuleiro[0][2] and posicoes_tabuleiro[0][1] < mouse_pos[1] < posicoes_tabuleiro[0][1]+posicoes_tabuleiro[0][3]:
                        mover_carta2_j1_posicao[0][0] = True
                    if posicoes_tabuleiro[1][0] < mouse_pos[0] < posicoes_tabuleiro[1][0]+posicoes_tabuleiro[1][2] and posicoes_tabuleiro[1][1] < mouse_pos[1] < posicoes_tabuleiro[1][1]+posicoes_tabuleiro[1][3]:
                        mover_carta2_j1_posicao[0][1]  = True
                    if posicoes_tabuleiro[2][0] < mouse_pos[0] < posicoes_tabuleiro[2][0]+posicoes_tabuleiro[2][2] and posicoes_tabuleiro[2][1] < mouse_pos[1] < posicoes_tabuleiro[2][1]+posicoes_tabuleiro[2][3]:
                        mover_carta2_j1_posicao[0][2]  = True
                    if posicoes_tabuleiro[3][0] < mouse_pos[0] < posicoes_tabuleiro[3][0]+posicoes_tabuleiro[3][2] and posicoes_tabuleiro[3][1] < mouse_pos[1] < posicoes_tabuleiro[3][1]+posicoes_tabuleiro[3][3]:
                        mover_carta2_j1_posicao[1][0]  = True
                    if posicoes_tabuleiro[4][0] < mouse_pos[0] < posicoes_tabuleiro[4][0]+posicoes_tabuleiro[4][2] and posicoes_tabuleiro[4][1] < mouse_pos[1] < posicoes_tabuleiro[4][1]+posicoes_tabuleiro[4][3]:
                        mover_carta2_j1_posicao[1][1]  = True
                    if posicoes_tabuleiro[5][0] < mouse_pos[0] < posicoes_tabuleiro[5][0]+posicoes_tabuleiro[5][2] and posicoes_tabuleiro[5][1] < mouse_pos[1] < posicoes_tabuleiro[5][1]+posicoes_tabuleiro[5][3]:
                        mover_carta2_j1_posicao[1][2]  = True
                    if posicoes_tabuleiro[6][0] < mouse_pos[0] < posicoes_tabuleiro[6][0]+posicoes_tabuleiro[6][2] and posicoes_tabuleiro[6][1] < mouse_pos[1] < posicoes_tabuleiro[6][1]+posicoes_tabuleiro[6][3]:
                        mover_carta2_j1_posicao[2][0]  = True
                    if posicoes_tabuleiro[7][0] < mouse_pos[0] < posicoes_tabuleiro[7][0]+posicoes_tabuleiro[7][2] and posicoes_tabuleiro[7][1] < mouse_pos[1] < posicoes_tabuleiro[7][1]+posicoes_tabuleiro[7][3]:
                        mover_carta2_j1_posicao[2][1]  = True
                    if posicoes_tabuleiro[8][0] < mouse_pos[0] < posicoes_tabuleiro[8][0]+posicoes_tabuleiro[8][2] and posicoes_tabuleiro[8][1] < mouse_pos[1] < posicoes_tabuleiro[8][1]+posicoes_tabuleiro[8][3]:
                        mover_carta2_j1_posicao[2][2]  = True
                        
                if carta3_j1_selecionada and clique and jogador1.get_cartas()[2].get_posicao() == None:
                    if posicoes_tabuleiro[0][0] < mouse_pos[0] < posicoes_tabuleiro[0][0]+posicoes_tabuleiro[0][2] and posicoes_tabuleiro[0][1] < mouse_pos[1] < posicoes_tabuleiro[0][1]+posicoes_tabuleiro[0][3]:
                        mover_carta3_j1_posicao[0][0] = True
                    if posicoes_tabuleiro[1][0] < mouse_pos[0] < posicoes_tabuleiro[1][0]+posicoes_tabuleiro[1][2] and posicoes_tabuleiro[1][1] < mouse_pos[1] < posicoes_tabuleiro[1][1]+posicoes_tabuleiro[1][3]:
                        mover_carta3_j1_posicao[0][1]  = True
                    if posicoes_tabuleiro[2][0] < mouse_pos[0] < posicoes_tabuleiro[2][0]+posicoes_tabuleiro[2][2] and posicoes_tabuleiro[2][1] < mouse_pos[1] < posicoes_tabuleiro[2][1]+posicoes_tabuleiro[2][3]:
                        mover_carta3_j1_posicao[0][2]  = True
                    if posicoes_tabuleiro[3][0] < mouse_pos[0] < posicoes_tabuleiro[3][0]+posicoes_tabuleiro[3][2] and posicoes_tabuleiro[3][1] < mouse_pos[1] < posicoes_tabuleiro[3][1]+posicoes_tabuleiro[3][3]:
                        mover_carta3_j1_posicao[1][0]  = True
                    if posicoes_tabuleiro[4][0] < mouse_pos[0] < posicoes_tabuleiro[4][0]+posicoes_tabuleiro[4][2] and posicoes_tabuleiro[4][1] < mouse_pos[1] < posicoes_tabuleiro[4][1]+posicoes_tabuleiro[4][3]:
                        mover_carta3_j1_posicao[1][1]  = True
                    if posicoes_tabuleiro[5][0] < mouse_pos[0] < posicoes_tabuleiro[5][0]+posicoes_tabuleiro[5][2] and posicoes_tabuleiro[5][1] < mouse_pos[1] < posicoes_tabuleiro[5][1]+posicoes_tabuleiro[5][3]:
                        mover_carta3_j1_posicao[1][2]  = True
                    if posicoes_tabuleiro[6][0] < mouse_pos[0] < posicoes_tabuleiro[6][0]+posicoes_tabuleiro[6][2] and posicoes_tabuleiro[6][1] < mouse_pos[1] < posicoes_tabuleiro[6][1]+posicoes_tabuleiro[6][3]:
                        mover_carta3_j1_posicao[2][0]  = True
                    if posicoes_tabuleiro[7][0] < mouse_pos[0] < posicoes_tabuleiro[7][0]+posicoes_tabuleiro[7][2] and posicoes_tabuleiro[7][1] < mouse_pos[1] < posicoes_tabuleiro[7][1]+posicoes_tabuleiro[7][3]:
                        mover_carta3_j1_posicao[2][1]  = True
                    if posicoes_tabuleiro[8][0] < mouse_pos[0] < posicoes_tabuleiro[8][0]+posicoes_tabuleiro[8][2] and posicoes_tabuleiro[8][1] < mouse_pos[1] < posicoes_tabuleiro[8][1]+posicoes_tabuleiro[8][3]:
                        mover_carta3_j1_posicao[2][2]  = True


                if carta4_j1_selecionada and clique and jogador1.get_cartas()[3].get_posicao() == None:
                    if posicoes_tabuleiro[0][0] < mouse_pos[0] < posicoes_tabuleiro[0][0]+posicoes_tabuleiro[0][2] and posicoes_tabuleiro[0][1] < mouse_pos[1] < posicoes_tabuleiro[0][1]+posicoes_tabuleiro[0][3]:
                        mover_carta4_j1_posicao[0][0] = True
                    if posicoes_tabuleiro[1][0] < mouse_pos[0] < posicoes_tabuleiro[1][0]+posicoes_tabuleiro[1][2] and posicoes_tabuleiro[1][1] < mouse_pos[1] < posicoes_tabuleiro[1][1]+posicoes_tabuleiro[1][3]:
                        mover_carta4_j1_posicao[0][1]  = True
                    if posicoes_tabuleiro[2][0] < mouse_pos[0] < posicoes_tabuleiro[2][0]+posicoes_tabuleiro[2][2] and posicoes_tabuleiro[2][1] < mouse_pos[1] < posicoes_tabuleiro[2][1]+posicoes_tabuleiro[2][3]:
                        mover_carta4_j1_posicao[0][2]  = True
                    if posicoes_tabuleiro[3][0] < mouse_pos[0] < posicoes_tabuleiro[3][0]+posicoes_tabuleiro[3][2] and posicoes_tabuleiro[3][1] < mouse_pos[1] < posicoes_tabuleiro[3][1]+posicoes_tabuleiro[3][3]:
                        mover_carta4_j1_posicao[1][0]  = True
                    if posicoes_tabuleiro[4][0] < mouse_pos[0] < posicoes_tabuleiro[4][0]+posicoes_tabuleiro[4][2] and posicoes_tabuleiro[4][1] < mouse_pos[1] < posicoes_tabuleiro[4][1]+posicoes_tabuleiro[4][3]:
                        mover_carta4_j1_posicao[1][1]  = True
                    if posicoes_tabuleiro[5][0] < mouse_pos[0] < posicoes_tabuleiro[5][0]+posicoes_tabuleiro[5][2] and posicoes_tabuleiro[5][1] < mouse_pos[1] < posicoes_tabuleiro[5][1]+posicoes_tabuleiro[5][3]:
                       mover_carta4_j1_posicao[1][2]  = True
                    if posicoes_tabuleiro[6][0] < mouse_pos[0] < posicoes_tabuleiro[6][0]+posicoes_tabuleiro[6][2] and posicoes_tabuleiro[6][1] < mouse_pos[1] < posicoes_tabuleiro[6][1]+posicoes_tabuleiro[6][3]:
                        mover_carta4_j1_posicao[2][0]  = True            
                    if posicoes_tabuleiro[7][0] < mouse_pos[0] < posicoes_tabuleiro[7][0]+posicoes_tabuleiro[7][2] and posicoes_tabuleiro[7][1] < mouse_pos[1] < posicoes_tabuleiro[7][1]+posicoes_tabuleiro[7][3]:
                        mover_carta4_j1_posicao[2][1]  = True
                    if posicoes_tabuleiro[8][0] < mouse_pos[0] < posicoes_tabuleiro[8][0]+posicoes_tabuleiro[8][2] and posicoes_tabuleiro[8][1] < mouse_pos[1] < posicoes_tabuleiro[8][1]+posicoes_tabuleiro[8][3]:
                        mover_carta4_j1_posicao[2][2]  = True

                if carta5_j1_selecionada and clique and jogador1.get_cartas()[4].get_posicao() == None:
                    if posicoes_tabuleiro[0][0] < mouse_pos[0] < posicoes_tabuleiro[0][0]+posicoes_tabuleiro[0][2] and posicoes_tabuleiro[0][1] < mouse_pos[1] < posicoes_tabuleiro[0][1]+posicoes_tabuleiro[0][3]:
                        mover_carta5_j1_posicao[0][0] = True
                    if posicoes_tabuleiro[1][0] < mouse_pos[0] < posicoes_tabuleiro[1][0]+posicoes_tabuleiro[1][2] and posicoes_tabuleiro[1][1] < mouse_pos[1] < posicoes_tabuleiro[1][1]+posicoes_tabuleiro[1][3]:
                        mover_carta5_j1_posicao[0][1]  = True
                    if posicoes_tabuleiro[2][0] < mouse_pos[0] < posicoes_tabuleiro[2][0]+posicoes_tabuleiro[2][2] and posicoes_tabuleiro[2][1] < mouse_pos[1] < posicoes_tabuleiro[2][1]+posicoes_tabuleiro[2][3]:
                        mover_carta5_j1_posicao[0][2]  = True
                    if posicoes_tabuleiro[3][0] < mouse_pos[0] < posicoes_tabuleiro[3][0]+posicoes_tabuleiro[3][2] and posicoes_tabuleiro[3][1] < mouse_pos[1] < posicoes_tabuleiro[3][1]+posicoes_tabuleiro[3][3]:
                        mover_carta5_j1_posicao[1][0]  = True
                    if posicoes_tabuleiro[4][0] < mouse_pos[0] < posicoes_tabuleiro[4][0]+posicoes_tabuleiro[4][2] and posicoes_tabuleiro[4][1] < mouse_pos[1] < posicoes_tabuleiro[4][1]+posicoes_tabuleiro[4][3]:
                        mover_carta5_j1_posicao[1][1]  = True
                    if posicoes_tabuleiro[5][0] < mouse_pos[0] < posicoes_tabuleiro[5][0]+posicoes_tabuleiro[5][2] and posicoes_tabuleiro[5][1] < mouse_pos[1] < posicoes_tabuleiro[5][1]+posicoes_tabuleiro[5][3]:
                        mover_carta5_j1_posicao[1][2]  = True
                    if posicoes_tabuleiro[6][0] < mouse_pos[0] < posicoes_tabuleiro[6][0]+posicoes_tabuleiro[6][2] and posicoes_tabuleiro[6][1] < mouse_pos[1] < posicoes_tabuleiro[6][1]+posicoes_tabuleiro[6][3]:
                        mover_carta5_j1_posicao[2][0]  = True
                    if posicoes_tabuleiro[7][0] < mouse_pos[0] < posicoes_tabuleiro[7][0]+posicoes_tabuleiro[7][2] and posicoes_tabuleiro[7][1] < mouse_pos[1] < posicoes_tabuleiro[7][1]+posicoes_tabuleiro[7][3]:
                        mover_carta5_j1_posicao[2][1]  = True
                    if posicoes_tabuleiro[8][0] < mouse_pos[0] < posicoes_tabuleiro[8][0]+posicoes_tabuleiro[8][2] and posicoes_tabuleiro[8][1] < mouse_pos[1] < posicoes_tabuleiro[8][1]+posicoes_tabuleiro[8][3]:
                        mover_carta5_j1_posicao[2][2]  = True
            if vez == "bot":
                carta1_j2_selecionada,carta2_j2_selecionada,carta3_j2_selecionada,carta4_j2_selecionada,carta5_j2_selecionada,lin_tab,col_tab = funcoes_interface.selecionar_carta_bot(jogador2, tabuleiro, carta1_j2_selecionada, carta2_j2_selecionada, carta3_j2_selecionada, carta4_j2_selecionada, carta5_j2_selecionada, bot_dificil)
                if carta1_j2_selecionada and jogador2.get_cartas()[0].get_posicao() == None:
                    if lin_tab == 0 and col_tab == 0:
                        mover_carta1_j2_posicao[0][0] = True
                    if lin_tab == 0 and col_tab == 1:
                        mover_carta1_j2_posicao[0][1]  = True
                    if lin_tab == 0 and col_tab == 2:
                        mover_carta1_j2_posicao[0][2]  = True
                    if lin_tab == 1 and col_tab == 0:
                        mover_carta1_j2_posicao[1][0]  = True
                    if lin_tab == 1 and col_tab == 1:
                        mover_carta1_j2_posicao[1][1]  = True
                    if lin_tab == 1 and col_tab == 2:
                        mover_carta1_j2_posicao[1][2]  = True
                    if lin_tab == 2 and col_tab == 0:
                        mover_carta1_j2_posicao[2][0]  = True
                    if lin_tab == 2 and col_tab == 1:
                        mover_carta1_j2_posicao[2][1]  = True
                    if lin_tab == 2 and col_tab == 2:
                        mover_carta1_j2_posicao[2][2]  = True
                
                if carta2_j2_selecionada and jogador2.get_cartas()[1].get_posicao() == None:
                    if lin_tab == 0 and col_tab == 0:
                        mover_carta2_j2_posicao[0][0] = True
                    if lin_tab == 0 and col_tab == 1:
                        mover_carta2_j2_posicao[0][1]  = True
                    if lin_tab == 0 and col_tab == 2:
                        mover_carta2_j2_posicao[0][2]  = True
                    if lin_tab == 1 and col_tab == 0:
                        mover_carta2_j2_posicao[1][0]  = True
                    if lin_tab == 1 and col_tab == 1:
                        mover_carta2_j2_posicao[1][1]  = True
                    if lin_tab == 1 and col_tab == 2:
                        mover_carta2_j2_posicao[1][2]  = True
                    if lin_tab == 2 and col_tab == 0:
                        mover_carta2_j2_posicao[2][0]  = True
                    if lin_tab == 2 and col_tab == 1:
                        mover_carta2_j2_posicao[2][1]  = True
                    if lin_tab == 2 and col_tab == 2:
                        mover_carta2_j2_posicao[2][2]  = True
                        
                if carta3_j2_selecionada and jogador2.get_cartas()[2].get_posicao() == None:
                    if lin_tab == 0 and col_tab == 0:
                        mover_carta3_j2_posicao[0][0] = True
                    if lin_tab == 0 and col_tab == 1:
                        mover_carta3_j2_posicao[0][1]  = True
                    if lin_tab == 0 and col_tab == 2:
                        mover_carta3_j2_posicao[0][2]  = True
                    if lin_tab == 1 and col_tab == 0:
                        mover_carta3_j2_posicao[1][0]  = True
                    if lin_tab == 1 and col_tab == 1:
                        mover_carta3_j2_posicao[1][1]  = True
                    if lin_tab == 1 and col_tab == 2:
                        mover_carta3_j2_posicao[1][2]  = True
                    if lin_tab == 2 and col_tab == 0:
                        mover_carta3_j2_posicao[2][0]  = True
                    if lin_tab == 2 and col_tab == 1:
                        mover_carta3_j2_posicao[2][1]  = True
                    if lin_tab == 2 and col_tab == 2:
                        mover_carta3_j2_posicao[2][2]  = True

                if carta4_j2_selecionada and jogador2.get_cartas()[3].get_posicao() == None:
                    if lin_tab == 0 and col_tab == 0:
                        mover_carta4_j2_posicao[0][0] = True
                    if lin_tab == 0 and col_tab == 1:
                        mover_carta4_j2_posicao[0][1]  = True
                    if lin_tab == 0 and col_tab == 2:
                        mover_carta4_j2_posicao[0][2]  = True
                    if lin_tab == 1 and col_tab == 0:
                        mover_carta4_j2_posicao[1][0]  = True
                    if lin_tab == 1 and col_tab == 1:
                        mover_carta4_j2_posicao[1][1]  = True
                    if lin_tab == 1 and col_tab == 2:
                        mover_carta4_j2_posicao[1][2]  = True
                    if lin_tab == 2 and col_tab == 0:
                        mover_carta4_j2_posicao[2][0]  = True
                    if lin_tab == 2 and col_tab == 1:
                        mover_carta4_j2_posicao[2][1]  = True
                    if lin_tab == 2 and col_tab == 2:
                        mover_carta4_j2_posicao[2][2]  = True

                if carta5_j2_selecionada and jogador2.get_cartas()[4].get_posicao() == None:
                    if lin_tab == 0 and col_tab == 0:
                        mover_carta5_j2_posicao[0][0] = True
                    if lin_tab == 0 and col_tab == 1:
                        mover_carta5_j2_posicao[0][1]  = True
                    if lin_tab == 0 and col_tab == 2:
                        mover_carta5_j2_posicao[0][2]  = True
                    if lin_tab == 1 and col_tab == 0:
                        mover_carta5_j2_posicao[1][0]  = True
                    if lin_tab == 1 and col_tab == 1:
                        mover_carta5_j2_posicao[1][1]  = True
                    if lin_tab == 1 and col_tab == 2:
                        mover_carta5_j2_posicao[1][2]  = True
                    if lin_tab == 2 and col_tab == 0:
                        mover_carta5_j2_posicao[2][0]  = True
                    if lin_tab == 2 and col_tab == 1:
                        mover_carta5_j2_posicao[2][1]  = True
                    if lin_tab == 2 and col_tab == 2:
                        mover_carta5_j2_posicao[2][2]  = True
            
            vez = funcoes_interface.desenhar_carta_no_tabuleiro(posicao_inicial_carta1_j1, posicao_inicial_carta2_j1, posicao_inicial_carta3_j1, posicao_inicial_carta4_j1, posicao_inicial_carta5_j1, mover_carta1_j1_posicao, mover_carta2_j1_posicao, mover_carta3_j1_posicao, mover_carta4_j1_posicao, mover_carta5_j1_posicao, tela, fundo_carta, j1_cartas, posicoes_tabuleiro, jogador1, tabuleiro, tamanho_carta, vez)  
            vez = funcoes_interface.desenhar_carta_no_tabuleiro(posicao_inicial_carta1_j2, posicao_inicial_carta2_j2, posicao_inicial_carta3_j2, posicao_inicial_carta4_j2, posicao_inicial_carta5_j2, mover_carta1_j2_posicao, mover_carta2_j2_posicao, mover_carta3_j2_posicao, mover_carta4_j2_posicao, mover_carta5_j2_posicao, tela, fundo_carta, j2_cartas, posicoes_tabuleiro, jogador2, tabuleiro, tamanho_carta, vez)

            funcoes_interface.mostrar_infos(tela, luva, carta1_j1_selecionada, carta2_j1_selecionada, carta3_j1_selecionada, carta4_j1_selecionada, carta5_j1_selecionada, posicao_inicial_carta1_j1, posicao_inicial_carta2_j1,  posicao_inicial_carta3_j1,  posicao_inicial_carta4_j1,  posicao_inicial_carta5_j1, jogador1, fonte, largura, altura)            

            if tabuleiro.tabuleiro_completo():
                tela_atual = "endgame"
        
        if tela_atual == "endgame":
            vencedor = tabuleiro.ganhador(jogador1, jogador2)
            nova_musica = None
            loop = 0

            if vencedor == "Jogador 1 é o vencedor!":
                nova_musica = "musics//vitoria.mp3"
                loop = -1
            elif vencedor in ["Jogador 2 é o vencedor!", "Empate!"]:
                nova_musica = "musics//game-over.mp3"
                loop = 0

            if nova_musica and musica_atual != nova_musica and tocando:
                pg.mixer.music.stop()
                pg.mixer.music.load(nova_musica)
                pg.mixer.music.play(loop)
                pg.mixer.music.set_volume(0.15)
                musica_atual = nova_musica
            tela.fill(preto)
            if vencedor == "Jogador 1 é o vencedor!":
                posicao_inicial_imagem_vencedor = funcoes_interface.mover_imagem(tela, imagem_vitoria, [400, 200], posicao_inicial_imagem_vencedor)
            elif vencedor == "Jogador 2 é o vencedor!":
                posicao_inicial_imagem_vencedor = funcoes_interface.mover_imagem(tela, imagem_derrota, [400, 200], posicao_inicial_imagem_vencedor)
            else:
                posicao_inicial_imagem_vencedor = funcoes_interface.mover_imagem(tela, imagem_empate, [400, 200], posicao_inicial_imagem_vencedor)

            if posicao_inicial_imagem_vencedor == [400, 200]:
                funcoes_interface.desenhar_texto_com_fundo(tela, "x", 0.475*largura, 0.56*altura, 50, 50, preto, branco,40)
                funcoes_interface.desenhar_texto_com_fundo(tela, f"{tabuleiro.qtd_carta_jogador(jogador1)}", 0.448*largura, 0.56*altura, 50, 50, preto, branco, 40)
                funcoes_interface.desenhar_texto_com_fundo(tela, f"{tabuleiro.qtd_carta_jogador(jogador2)}", 0.51*largura, 0.56*altura, 50, 50, preto, branco, 40)
                funcoes_interface.desenhar_texto(tela, f'"ESC" para sair!', 0.4*largura, 0.85*altura, 30, branco)

        pg.display.update()
        clock.tick(fps)

    pg.mixer.music.stop()
    pg.quit()
    sys.exit()