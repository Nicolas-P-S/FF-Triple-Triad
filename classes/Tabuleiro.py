class Tabuleiro:
    def __init__(self):
        self.grid = [[None for _ in range(3)] for _ in range(3)]
        self.ultima_carta = None

    def qtd_carta_jogador(self, jogador):
        cont = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != None:
                    if self.grid[i][j].get_dono() == jogador.nome:
                        cont += 1
        return cont + jogador.qtd_cartas_na_mao()
            
    def get_ultima_carta(self):
        return self.ultima_carta

    def set_ultima_carta(self, carta):
        self.ultima_carta = carta

    def ganhador(self, jogador1, jogador2):
        cont_j1 = 0
        cont_j2 = 0

        for i in range(3):
            for j in range(3):
                if self.grid[i][j] is not None:  # Verificar se há uma carta
                    if self.grid[i][j].dono == "j1":
                        cont_j1 += 1
                    elif self.grid[i][j].dono == "j2":
                        cont_j2 += 1
        cont_j1 = cont_j1 + jogador1.qtd_cartas_na_mao()
        cont_j2 = cont_j2 + jogador2.qtd_cartas_na_mao()

        if cont_j1 > cont_j2:
            return "Jogador 1 é o vencedor!"
        elif cont_j2 > cont_j1:
            return "Jogador 2 é o vencedor!"
        else:
            return "Empate!"

    def get_carta_posicao(self, linha, coluna):
        return self.grid[linha][coluna]

    def espaco_vazio(self, linha, coluna):
        if linha >= 0 and linha <= 2 and coluna >= 0 and coluna <=2:
            return self.grid[linha][coluna] is None
        return None

    def aplicar_descension(self):
        for linha in self.grid:
            for carta in linha:
                if carta:
                    carta.diminuir_superior(1)
                    carta.diminuir_inferior(1)
                    carta.diminuir_esquerdo(1)
                    carta.diminuir_direito(1)

    def jogar_carta(self, linha, coluna, carta, jogador):
        if self.espaco_vazio(linha, coluna):
            carta.set_no_tabuleiro(True)
            carta.set_posicao((linha, coluna))
            carta.dono = jogador.nome
            self.grid[linha][coluna] = carta
            self.verificar_captura(linha, coluna, carta, jogador)
            self.aplicar_descension()
            self.set_ultima_carta(carta)

    def verificar_captura(self, linha, coluna, carta, jogador):
        direcoes = [
            {"dx": -1, "dy": 0, "meu_lado": 0, "lado_oposto": 2},
            {"dx": 1, "dy": 0, "meu_lado": 2, "lado_oposto": 0},
            {"dx": 0, "dy": -1, "meu_lado": 1, "lado_oposto": 3},
            {"dx": 0, "dy": 1, "meu_lado": 3, "lado_oposto": 1}
        ]

        for direcao in direcoes:
            nova_linha = linha + direcao["dx"]
            nova_coluna = coluna + direcao["dy"]
            if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
                carta_adversaria = self.grid[nova_linha][nova_coluna]
                if carta_adversaria and carta_adversaria.dono != jogador.nome:
                    if carta.lados[direcao["meu_lado"]] > carta_adversaria.lados[direcao["lado_oposto"]]:
                        print(f"{carta.nome} capturou {carta_adversaria.nome}!")
                        carta_adversaria.dono = jogador.nome

    def mostrar_tabuleiro(self):
        for linha in self.grid:
            print(' | '.join([f"{carta.nome} ({carta.dono})" if carta else 'Vazio' for carta in linha]))

    def tabuleiro_completo(self):
        return all(all(carta is not None for carta in linha) for linha in self.grid)