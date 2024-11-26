import pygame as pg
import random

preto = (0, 0, 0)
branco = (255, 255, 255)
cinza_claro = (170, 170, 170)
cinza_escuro = (100, 100, 100)

def jogada_bot_facil(bot, tabuleiro):
    lin_tab = random.randint(0,2)
    col_tab = random.randint(0,2)
    carta = random.randint(0,4)
    
    while bot.get_cartas()[carta].get_posicao() != None:
        if bot.get_cartas()[carta].get_posicao() != None:
            carta = random.randint(0,4)
            
    while tabuleiro.espaco_vazio(lin_tab, col_tab) != True:
        if tabuleiro.espaco_vazio(lin_tab, col_tab) != True:
            lin_tab = random.randint(0,2)
            col_tab = random.randint(0,2)
    
    return bot.get_cartas()[carta], lin_tab, col_tab

def jogada_bot_dificil(bot, tabuleiro):
    carta_no_tab = []
    pos_carta = random.randint(0,4)
    
    for i in range(3):
        for j in range(3):
            if tabuleiro.espaco_vazio(i, j) == False and tabuleiro.get_carta_posicao(i, j).get_dono() == "j1":
                carta_no_tab.append(tabuleiro.get_carta_posicao(i, j))
                
    carta_mais_poderosa = carta_no_tab[0]
    for carta in carta_no_tab:
        if carta.get_pontuacao_total() > carta_mais_poderosa.get_pontuacao_total():
            carta_mais_poderosa = carta
    
    linha, coluna, lado_mais_fraco, pos_lado_mais_fraco = carta_mais_poderosa.ponto_fraco(tabuleiro)
    carta_retornada = None
    if pos_lado_mais_fraco == "UP":
        for carta in bot.get_cartas():
            if carta.get_down() > lado_mais_fraco:
                carta_retornada = carta
    elif pos_lado_mais_fraco == "LEFT":
        for carta in bot.get_cartas():
            if carta.get_right() > lado_mais_fraco:
                carta_retornada = carta
    elif pos_lado_mais_fraco == "RIGHT":
        for carta in bot.get_cartas():
            if carta.get_left() > lado_mais_fraco:
                carta_retornada = carta
    elif pos_lado_mais_fraco == "DOWN":
        for carta in bot.get_cartas():
            if carta.get_up() > lado_mais_fraco:
                carta_retornada = carta
    elif carta_retornada == None:
        return jogada_bot_facil(bot, tabuleiro)
    
    return bot.get_cartas()[pos_carta], linha, coluna
    
def desenhar_botao(tela, texto, x, y, largura, altura, cor_clara, cor_escura, mouse_pos, clique, acao=None):
    preto = (0, 0, 0)
    fonte = pg.font.SysFont('couriernew', 20, True, True)


    if x + largura > mouse_pos[0] > x and y + altura > mouse_pos[1] > y:
        pg.draw.rect(tela, cor_clara, (x, y, largura, altura))  # Mudar cor quando o mouse está sobre o botão
        if clique and acao is not None:
            acao()
    else:
        pg.draw.rect(tela, cor_escura, (x, y, largura, altura))  # Cor padrão do botão

    # Texto do botão
    texto_surface = fonte.render(texto, True, preto)
    tela.blit(texto_surface, (x + (largura - texto_surface.get_width()) // 2, y + (altura - texto_surface.get_height()) // 2))

def mover_carta_tabuleiro(tela, fundo_carta, carta, tabuleiro_posicao, jogador, tamanho_carta, posicao_inicial_carta, up, down, left, right):
    if posicao_inicial_carta > [tabuleiro_posicao[0]+50, tabuleiro_posicao[1]+30]:
        posicao_inicial_carta = [tabuleiro_posicao[0]+50, tabuleiro_posicao[1]+30]
    posicao_inicial_carta = mover_carta_e_imagem(posicao_inicial_carta, [tabuleiro_posicao[0]+50, tabuleiro_posicao[1]+30], 100)
    desenhar_carta_com_fundo(tela, fundo_carta, carta, posicao_inicial_carta, tamanho_carta, up, down, left, right)
    return posicao_inicial_carta

def mover_imagem(tela, imagem, posicao, posicao_inicial):
    if posicao_inicial > [posicao[0], posicao[1]]:
        posicao_inicial = [posicao[0], posicao[1]]
    posicao_inicial = mover_carta_e_imagem(posicao_inicial, [posicao[0], posicao[1]], 10)
    tela.blit(imagem, posicao_inicial)
    return posicao_inicial
    

def desenhar_texto_com_fundo(tela, texto, x, y, largura, altura, cor_primaria, cor_secundaria, tamanho):
    fonte = pg.font.SysFont('couriernew', tamanho, True, True)
    pg.draw.rect(tela, cor_primaria, (x, y, largura, altura))  # Cor padrão do botão

    texto_surface = fonte.render(texto, True, cor_secundaria)
    tela.blit(texto_surface, (x + (largura - texto_surface.get_width()) // 2, y + (altura - texto_surface.get_height()) // 2))
    
def desenhar_texto(tela, texto, x, y, tamanho, cor):
    fonte = pg.font.SysFont('couriernew', tamanho, True, True)
    #pg.draw.rect(tela, cor, (x, y, largura, altura))

    texto_surface = fonte.render(texto, True, cor)
    tela.blit(texto_surface, (x, y))
    
# Função para mover a carta de uma posição inicial até a final
def mover_carta_e_imagem(posicao_atual, posicao_final, velocidade):
    dist_x = posicao_final[0] - posicao_atual[0]
    dist_y = posicao_final[1] - posicao_atual[1]

    if dist_x != 0:
        posicao_atual[0] += velocidade if dist_x > 0 else -velocidade
    if dist_y != 0:
        posicao_atual[1] += velocidade if dist_y > 0 else -velocidade

    if abs(dist_x) < velocidade:
        posicao_atual[0] = posicao_final[0]
    if abs(dist_y) < velocidade:
        posicao_atual[1] = posicao_final[1]

    return posicao_atual

def desenhar_carta_com_fundo(tela, imagem_fundo, imagem_carta, posicao, tamanho_carta, up, down, left, right):
    x, y = posicao  # Extrai as coordenadas da posição

    # Definir as posições relativas para os valores, mantendo-os dentro da carta
    pos_up = (x + tamanho_carta // 2 - 10, y + tamanho_carta // 8 - 10)
    pos_down = (x + tamanho_carta // 2 - 10, y + tamanho_carta - tamanho_carta // 6 - 10)
    pos_left = (x + tamanho_carta // 8 - 10, y + tamanho_carta // 2 - 15)
    pos_right = (x + tamanho_carta - tamanho_carta // 6 - 5, y + tamanho_carta // 2 - 15)

    # Carregar a fonte
    fonte = pg.font.SysFont('couriernew', 25, True, True)

    # Desenhar o fundo e a carta na tela
    tela.blit(imagem_fundo, posicao)  # Desenha o fundo primeiro
    tela.blit(imagem_carta, posicao)  # Desenha a carta por cima do fundo

    if int(up) == 10:
        texto_up = fonte.render('A', True, (255, 255, 255))
    else:
        texto_up = fonte.render(str(up), True, (255, 255, 255))
    
    if int(down) == 10:
        texto_down = fonte.render(str('A'), True, (255, 255, 255))
    else:
        texto_down = fonte.render(str(down), True, (255, 255, 255))
    
    if int(left) == 10:
        texto_left = fonte.render(str('A'), True, (255, 255, 255))
    else:
        texto_left = fonte.render(str(left), True, (255, 255, 255))
        
    if int(right) == 10:
        texto_right = fonte.render(str('A'), True, (255, 255, 255))
    else:
        texto_right = fonte.render(str(right), True, (255, 255, 255))  # Texto para direita

    # Desenhar os textos nas posições corretas
    tela.blit(texto_up, pos_up)
    tela.blit(texto_down, pos_down)
    tela.blit(texto_left, pos_left)
    tela.blit(texto_right, pos_right)

def mostrar_infos(tela, luva, carta1_j1_selecionada, carta2_j1_selecionada, carta3_j1_selecionada, carta4_j1_selecionada, carta5_j1_selecionada, posicao_inicial_carta1_j1, posicao_inicial_carta2_j1,  posicao_inicial_carta3_j1,  posicao_inicial_carta4_j1,  posicao_inicial_carta5_j1, jogador1, fonte, largura, altura):
    
    if carta1_j1_selecionada and posicao_inicial_carta1_j1 == [0.055*largura, 0.25*altura]:
        tela.blit(luva, [0.13*largura, 0.26*altura])
        pg.draw.rect(tela, cinza_escuro, (0.42*largura, 0.85*altura, 250, 100))
        desenhar_texto(tela, "info", 0.42*largura+10, 0.85*altura+10, 10, branco)
        tela.blit(fonte.render(f"nome: {jogador1.get_cartas()[0].get_nome()}", True, (branco)), (0.42*largura+20, 0.85*altura+40))
        tela.blit(fonte.render(f"elemento: {jogador1.get_cartas()[0].get_elemento()}", True, (branco)), (0.42*largura+20, 0.85*altura+70))
    if carta2_j1_selecionada and posicao_inicial_carta2_j1 == [0.055*largura, 0.25*altura+140]:
        pg.draw.rect(tela, cinza_escuro, (0.42*largura, 0.85*altura, 250, 100))
        desenhar_texto(tela, "info", 0.42*largura+10, 0.85*altura+10, 10, branco)
        tela.blit(fonte.render(f"nome: {jogador1.get_cartas()[1].get_nome()}", True, (branco)), (0.42*largura+20, 0.85*altura+40))
        tela.blit(fonte.render(f"elemento: {jogador1.get_cartas()[1].get_elemento()}", True, (branco)), (0.42*largura+20, 0.85*altura+70))
        tela.blit(luva, [0.13*largura, 0.26*altura+140])
    if carta3_j1_selecionada and posicao_inicial_carta3_j1 == [0.055*largura, 0.25*altura+280]:
        pg.draw.rect(tela, cinza_escuro, (0.42*largura, 0.85*altura, 250, 100))
        desenhar_texto(tela, "info", 0.42*largura+10, 0.85*altura+10, 10, branco)
        tela.blit(fonte.render(f"nome: {jogador1.get_cartas()[2].get_nome()}", True, (branco)), (0.42*largura+20, 0.85*altura+40))
        tela.blit(fonte.render(f"elemento: {jogador1.get_cartas()[2].get_elemento()}", True, (branco)), (0.42*largura+20, 0.85*altura+70))
        tela.blit(luva, [0.13*largura, 0.26*altura+280])
    if carta4_j1_selecionada and posicao_inicial_carta4_j1 == [0.16*largura, 0.25*altura]:
        pg.draw.rect(tela, cinza_escuro, (0.42*largura, 0.85*altura, 250, 100))
        desenhar_texto(tela, "info", 0.42*largura+10, 0.85*altura+10, 10, branco)
        tela.blit(fonte.render(f"nome: {jogador1.get_cartas()[3].get_nome()}", True, (branco)), (0.42*largura+20, 0.85*altura+40))
        tela.blit(fonte.render(f"elemento: {jogador1.get_cartas()[3].get_elemento()}", True, (branco)), (0.42*largura+20, 0.85*altura+70))
        tela.blit(luva, [0.235*largura, 0.26*altura])
    if carta5_j1_selecionada and posicao_inicial_carta5_j1 == [0.16*largura, 0.25*altura+140]:
        pg.draw.rect(tela, cinza_escuro, (0.42*largura, 0.85*altura, 250, 100))
        desenhar_texto(tela, "info", 0.42*largura+10, 0.85*altura+10, 10, branco)
        tela.blit(fonte.render(f"nome: {jogador1.get_cartas()[4].get_nome()}", True, (branco)), (0.42*largura+20, 0.85*altura+40))
        tela.blit(fonte.render(f"elemento: {jogador1.get_cartas()[4].get_elemento()}", True, (branco)), (0.42*largura+20, 0.85*altura+70))
        tela.blit(luva, [0.235*largura, 0.26*altura+140])


def selecionar_carta(posicao_carta1_j1, posicao_carta2_j1, posicao_carta3_j1, posicao_carta4_j1, posicao_carta5_j1, clique, jogador1, carta1_selecionada, carta2_selecionada, carta3_selecionada, carta4_selecionada, carta5_selecionada):
    if posicao_carta1_j1 and clique:
        carta1_selecionada = True
        if carta2_selecionada:
            carta2_selecionada = False
        if carta3_selecionada:
            carta3_selecionada = False
        if carta4_selecionada:
            carta4_selecionada = False
        if carta5_selecionada:
            carta5_selecionada = False
    if posicao_carta2_j1 and clique:
        carta2_selecionada = True
        if carta1_selecionada:
            carta1_selecionada = False
        if carta3_selecionada:
            carta3_selecionada = False
        if carta4_selecionada:
            carta4_selecionada = False
        if carta5_selecionada:
            carta5_selecionada = False
    if posicao_carta3_j1 and clique:
        carta3_selecionada = True                
        if carta2_selecionada:
            carta2_selecionada = False
        if carta1_selecionada:
            carta1_selecionada = False
        if carta4_selecionada:
            carta4_selecionada = False
        if carta5_selecionada:
            carta5_selecionada = False
    if posicao_carta4_j1 and clique:
        carta4_selecionada = True
        if carta2_selecionada:
            carta2_selecionada = False
        if carta3_selecionada:
            carta3_selecionada = False
        if carta1_selecionada:
            carta1_selecionada = False
        if carta5_selecionada:
            carta5_selecionada = False
    if posicao_carta5_j1 and clique:
        carta5_selecionada = True
        if carta2_selecionada:
            carta2_selecionada = False
        if carta3_selecionada:
            carta3_selecionada = False
        if carta4_selecionada:
            carta4_selecionada = False
        if carta1_selecionada:
            carta1_selecionada = False
    return carta1_selecionada, carta2_selecionada, carta3_selecionada, carta4_selecionada, carta5_selecionada

def selecionar_carta_bot(bot, tabuleiro, carta1_selecionada, carta2_selecionada, carta3_selecionada, carta4_selecionada, carta5_selecionada, bot_dificil):
    if bot_dificil:
        carta, lin_tab, col_tab = jogada_bot_dificil(bot, tabuleiro)
    elif bot_dificil == False:
        carta,lin_tab,col_tab = jogada_bot_facil(bot, tabuleiro)
    
    if carta == bot.get_cartas()[0]:
        carta1_selecionada = True
        if carta2_selecionada:
            carta2_selecionada = False
        if carta3_selecionada:
            carta3_selecionada = False
        if carta4_selecionada:
            carta4_selecionada = False
        if carta5_selecionada:
            carta5_selecionada = False
    if carta == bot.get_cartas()[1]:
        carta2_selecionada = True
        if carta1_selecionada:
            carta1_selecionada = False
        if carta3_selecionada:
            carta3_selecionada = False
        if carta4_selecionada:
            carta4_selecionada = False
        if carta5_selecionada:
            carta5_selecionada = False
    if carta == bot.get_cartas()[2]:
        carta3_selecionada = True                
        if carta2_selecionada:
            carta2_selecionada = False
        if carta1_selecionada:
            carta1_selecionada = False
        if carta4_selecionada:
            carta4_selecionada = False
        if carta5_selecionada:
            carta5_selecionada = False
    if carta == bot.get_cartas()[3]:
        carta4_selecionada = True
        if carta2_selecionada:
            carta2_selecionada = False
        if carta3_selecionada:
            carta3_selecionada = False
        if carta1_selecionada:
            carta1_selecionada = False
        if carta5_selecionada:
            carta5_selecionada = False
    if carta == bot.get_cartas()[4]:
        carta5_selecionada = True
        if carta2_selecionada:
            carta2_selecionada = False
        if carta3_selecionada:
            carta3_selecionada = False
        if carta4_selecionada:
            carta4_selecionada = False
        if carta1_selecionada:
            carta1_selecionada = False

    return carta1_selecionada, carta2_selecionada, carta3_selecionada, carta4_selecionada, carta5_selecionada, lin_tab, col_tab

def desenhar_carta_no_tabuleiro(posicao_inicial_carta1, posicao_inicial_carta2, posicao_inicial_carta3, posicao_inicial_carta4, posicao_inicial_carta5, mover_carta1_posicao, mover_carta2_posicao, mover_carta3_posicao, mover_carta4_posicao, mover_carta5_posicao, tela, fundo_carta, cartas, posicoes_tabuleiro, jogador, tabuleiro, tamanho_carta, vez):
    if mover_carta1_posicao[0][0]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[0], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(0, 0, jogador.get_cartas()[0], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[0][0]+50, posicoes_tabuleiro[0][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta1_posicao[0][1]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[1], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(0, 1, jogador.get_cartas()[0], jogador)                
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[1][0]+50, posicoes_tabuleiro[1][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta1_posicao[0][2]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[2], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(0, 2, jogador.get_cartas()[0], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[2][0]+50, posicoes_tabuleiro[2][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta1_posicao[1][0]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[3], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(1, 0, jogador.get_cartas()[0], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[3][0]+50, posicoes_tabuleiro[3][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta1_posicao[1][1]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[4], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(1, 1, jogador.get_cartas()[0], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[4][0]+50, posicoes_tabuleiro[4][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta1_posicao[1][2]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[5], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(1, 2, jogador.get_cartas()[0], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[5][0]+50, posicoes_tabuleiro[5][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta1_posicao[2][0]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[6], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(2, 0, jogador.get_cartas()[0], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[6][0]+50, posicoes_tabuleiro[6][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta1_posicao[2][1]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[7], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(2, 1, jogador.get_cartas()[0], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[7][0]+50, posicoes_tabuleiro[7][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta1_posicao[2][2]:
        posicao_inicial_carta1=mover_carta_tabuleiro(tela, fundo_carta, cartas[0], posicoes_tabuleiro[8], jogador, tamanho_carta, posicao_inicial_carta1, jogador.get_cartas()[0].get_up(), jogador.get_cartas()[0].get_down(), jogador.get_cartas()[0].get_left(), jogador.get_cartas()[0].get_right())
        tabuleiro.jogar_carta(2, 2, jogador.get_cartas()[0], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[0].get_dono()}", posicao_inicial_carta1[0], posicao_inicial_carta1[1], 20, branco)
        if posicao_inicial_carta1 == [posicoes_tabuleiro[8][0]+50, posicoes_tabuleiro[8][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[0]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
            
    if mover_carta2_posicao[0][0]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[0], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(0, 0, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[0][0]+50, posicoes_tabuleiro[0][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta2_posicao[0][1]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[1], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(0, 1, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[1][0]+50, posicoes_tabuleiro[1][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta2_posicao[0][2]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[2], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(0, 2, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[2][0]+50, posicoes_tabuleiro[2][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta2_posicao[1][0]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[3], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(1, 0, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[3][0]+50, posicoes_tabuleiro[3][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta2_posicao[1][1]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[4], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(1, 1, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[4][0]+50, posicoes_tabuleiro[4][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta2_posicao[1][2]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[5], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(1, 2, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[5][0]+50, posicoes_tabuleiro[5][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta2_posicao[2][0]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[6], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(2, 0, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[6][0]+50, posicoes_tabuleiro[6][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta2_posicao[2][1]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[7], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(2, 1, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[7][0]+50, posicoes_tabuleiro[7][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta2_posicao[2][2]:
        posicao_inicial_carta2=mover_carta_tabuleiro(tela, fundo_carta, cartas[1], posicoes_tabuleiro[8], jogador, tamanho_carta, posicao_inicial_carta2, jogador.get_cartas()[1].get_up(), jogador.get_cartas()[1].get_down(), jogador.get_cartas()[1].get_left(), jogador.get_cartas()[1].get_right())
        tabuleiro.jogar_carta(2, 2, jogador.get_cartas()[1], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[1].get_dono()}", posicao_inicial_carta2[0], posicao_inicial_carta2[1], 20, branco)
        if posicao_inicial_carta2 == [posicoes_tabuleiro[8][0]+50, posicoes_tabuleiro[8][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[1]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"

    if mover_carta3_posicao[0][0]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[0], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(0, 0, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[0][0]+50, posicoes_tabuleiro[0][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta3_posicao[0][1]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[1], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(0, 1, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[1][0]+50, posicoes_tabuleiro[1][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta3_posicao[0][2]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[2], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(0, 2, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[2][0]+50, posicoes_tabuleiro[2][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta3_posicao[1][0]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[3], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(1, 0, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[3][0]+50, posicoes_tabuleiro[3][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta3_posicao[1][1]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[4], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(1, 1, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[4][0]+50, posicoes_tabuleiro[4][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta3_posicao[1][2]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[5], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(1, 2, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[5][0]+50, posicoes_tabuleiro[5][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta3_posicao[2][0]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[6], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(2, 0, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[6][0]+50, posicoes_tabuleiro[6][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta3_posicao[2][1]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[7], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(2, 1, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[7][0]+50, posicoes_tabuleiro[7][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta3_posicao[2][2]:
        posicao_inicial_carta3=mover_carta_tabuleiro(tela, fundo_carta, cartas[2], posicoes_tabuleiro[8], jogador, tamanho_carta, posicao_inicial_carta3, jogador.get_cartas()[2].get_up(), jogador.get_cartas()[2].get_down(), jogador.get_cartas()[2].get_left(), jogador.get_cartas()[2].get_right())
        tabuleiro.jogar_carta(2, 2, jogador.get_cartas()[2], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[2].get_dono()}", posicao_inicial_carta3[0], posicao_inicial_carta3[1], 20, branco)
        if posicao_inicial_carta3 == [posicoes_tabuleiro[8][0]+50, posicoes_tabuleiro[8][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[2]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
            
    if mover_carta4_posicao[0][0]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[0], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(0, 0, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[0][0]+50, posicoes_tabuleiro[0][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta4_posicao[0][1]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[1], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(0, 1, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[1][0]+50, posicoes_tabuleiro[1][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta4_posicao[0][2]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[2], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(0, 2, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[2][0]+50, posicoes_tabuleiro[2][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta4_posicao[1][0]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[3], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(1, 0, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[3][0]+50, posicoes_tabuleiro[3][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta4_posicao[1][1]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[4], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(1, 1, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[4][0]+50, posicoes_tabuleiro[4][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta4_posicao[1][2]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[5], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(1, 2, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[5][0]+50, posicoes_tabuleiro[5][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta4_posicao[2][0]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[6], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(2, 0, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[6][0]+50, posicoes_tabuleiro[6][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta4_posicao[2][1]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[7], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(2, 1, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[7][0]+50, posicoes_tabuleiro[7][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"            
    if mover_carta4_posicao[2][2]:
        posicao_inicial_carta4=mover_carta_tabuleiro(tela, fundo_carta, cartas[3], posicoes_tabuleiro[8], jogador, tamanho_carta, posicao_inicial_carta4, jogador.get_cartas()[3].get_up(), jogador.get_cartas()[3].get_down(), jogador.get_cartas()[3].get_left(), jogador.get_cartas()[3].get_right())
        tabuleiro.jogar_carta(2, 2, jogador.get_cartas()[3], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[3].get_dono()}", posicao_inicial_carta4[0], posicao_inicial_carta4[1], 20, branco)
        if posicao_inicial_carta4 == [posicoes_tabuleiro[8][0]+50, posicoes_tabuleiro[8][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[3]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
                
    if mover_carta5_posicao[0][0]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[0], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(0, 0, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[0][0]+50, posicoes_tabuleiro[0][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta5_posicao[0][1]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[1], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(0, 1, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[1][0]+50, posicoes_tabuleiro[1][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta5_posicao[0][2]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[2], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(0, 2, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[2][0]+50, posicoes_tabuleiro[2][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta5_posicao[1][0]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[3], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(1, 0, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[3][0]+50, posicoes_tabuleiro[3][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta5_posicao[1][1]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[4], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(1, 1, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[4][0]+50, posicoes_tabuleiro[4][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta5_posicao[1][2]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[5], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(1, 2, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[5][0]+50, posicoes_tabuleiro[5][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta5_posicao[2][0]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[6], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(2, 0, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[6][0]+50, posicoes_tabuleiro[6][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta5_posicao[2][1]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[7], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(2, 1, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[7][0]+50, posicoes_tabuleiro[7][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    if mover_carta5_posicao[2][2]:
        posicao_inicial_carta5=mover_carta_tabuleiro(tela, fundo_carta, cartas[4], posicoes_tabuleiro[8], jogador, tamanho_carta, posicao_inicial_carta5, jogador.get_cartas()[4].get_up(), jogador.get_cartas()[4].get_down(), jogador.get_cartas()[4].get_left(), jogador.get_cartas()[4].get_right())
        tabuleiro.jogar_carta(2, 2, jogador.get_cartas()[4], jogador)
        desenhar_texto(tela, f"{jogador.get_cartas()[4].get_dono()}", posicao_inicial_carta5[0], posicao_inicial_carta5[1], 20, branco)
        if posicao_inicial_carta5 == [posicoes_tabuleiro[8][0]+50, posicoes_tabuleiro[8][1]+30] and tabuleiro.get_ultima_carta() == jogador.get_cartas()[4]:
            if vez == "bot" and jogador.nome == "j2":
                vez = "jogador"
            elif vez == "jogador" and jogador.nome == "j1":
                vez = "bot"
    return vez 