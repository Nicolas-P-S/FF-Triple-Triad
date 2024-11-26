class Carta:
    def __init__(self, id, nome, lados, elemento, imagem):
        self.id = id
        self.nome = nome
        self.elemento = elemento
        self.lados = lados  # lados[0]: UP, lados[1]: LEFT, lados[2]: DOWN, lados[3]: RIGHT
        self.imagem = imagem
        self.dono = None
        self.posicao = None

    def ponto_fraco(self, tabuleiro):
        linha, coluna = self.get_posicao()
        lado_mais_fraco = 10 # VALOR MAXIMO PARA COMPARACAO
        linha_retornada, coluna_retornada = 0, 0
        posicao_lado_mais_fraco = None
        
        for i in range(4):
            if self.get_lados()[i] <= lado_mais_fraco:
                if i == 0 and tabuleiro.espaco_vazio(linha-1, coluna): # UP
                    lado_mais_fraco = self.get_lados()[i]
                    linha_retornada = linha-1
                    coluna_retornada = coluna
                    posicao_lado_mais_fraco = "UP"
                elif i == 1 and tabuleiro.espaco_vazio(linha, coluna-1): # LEFT
                    lado_mais_fraco = self.get_lados()[i]
                    linha_retornada = linha
                    coluna_retornada = coluna-1
                    posicao_lado_mais_fraco = "LEFT"
                elif i == 2 and tabuleiro.espaco_vazio(linha+1, coluna): # DOWN
                    lado_mais_fraco = self.get_lados()[i]
                    linha_retornada = linha+1
                    coluna_retornada = coluna
                    posicao_lado_mais_fraco = "DOWN"
                elif i == 3 and tabuleiro.espaco_vazio(linha, coluna+1): # RIGHT
                    lado_mais_fraco = self.get_lados()[i]
                    linha_retornada = linha
                    coluna_retornada = coluna+1
                    posicao_lado_mais_fraco = "RIGHT"

        return linha_retornada, coluna_retornada, lado_mais_fraco, posicao_lado_mais_fraco
                
    def get_pontuacao_total(self):
        return self.lados[0] + self.lados[1] + self.lados[2] + self.lados[3]

    def get_elemento(self):
        return self.elemento

    def get_dono(self):
        return self.dono

    def get_no_tabuleiro(self):
        return self.no_tabuleiro
    
    def set_no_tabuleiro(self, valor):
        self.no_tabuleiro = valor
    
    def get_posicao(self):
        return self.posicao
    
    def set_posicao(self, posicao):
        self.posicao = posicao

    def diminuir_superior(self, valor):
        self.lados[0] = max(0, self.lados[0] - valor)

    def diminuir_inferior(self, valor):
        self.lados[2] = max(0, self.lados[2] - valor)

    def diminuir_esquerdo(self, valor):
        self.lados[1] = max(0, self.lados[1] - valor)

    def diminuir_direito(self, valor):
        self.lados[3] = max(0, self.lados[3] - valor)
    
    def get_nome(self):
        return self.nome
    
    def get_id(self):
        return self.id
    
    def get_imagem(self):
        return self.imagem
    
    def get_lados(self):
        return self.lados
    
    def get_up(self):
        return self.lados[0]
    
    def get_down(self):
        return self.lados[2]
    
    def get_left(self):
        return self.lados[1]
    
    def get_right(self):
        return self.lados[3]