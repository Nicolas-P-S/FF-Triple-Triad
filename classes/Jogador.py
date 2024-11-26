import random
import csv
from .Carta import Carta

class Jogador:
    def __init__(self, nome):
        self.pontos = 5
        self.nome = nome
        self.cartas = []  # Iniciar lista de cartas vazia

    def qtd_cartas_na_mao(self):
        cont = 0
        for i in range(5):
            if self.cartas[i].get_posicao() == None:
                cont +=1
        return cont
                
    def adicionar_carta(self, carta):
        try:
            self.cartas.append(carta)
            print(f"Carta '{carta.nome}' adicionada a {self.nome}.")
        except Exception as e:
            print(f"Erro ao adicionar a carta: {e}")

    def mostrar_cartas(self):
        if not self.cartas:  # Verificar se a lista está vazia
            print(f"{self.nome} ainda não possui cartas.")
        else:
            print(f"Cartas de {self.nome}:")
            for i, carta in enumerate(self.cartas):
                print(f"\n[{i}] - Nome: {carta.nome} \n Elemento: {carta.elemento} \n UP: {carta.lados[0]}, LEFT: {carta.lados[1]}, DOWN: {carta.lados[2]}, RIGHT: {carta.lados[3]}\n")

    def recolher_lados(self, split1, split2):
        lados = []
        parte1 = split1.split(",")
        parte2 = split2.split(",")

        # Verificando se a parte1 e parte2 têm o número correto de lados
        if len(parte1) < 2 or len(parte2) < 2:
            print("Formato de entrada inválido para os lados.")
            return None

        try:
            # Usando strip() para remover espaços em branco e caracteres indesejados
            up = int(parte1[0].split(":")[1].strip().rstrip('['))
            left = int(parte1[1].split(":")[1].strip())
            down = int(parte2[0].split(":")[1].strip())
            right = int(parte2[1].split(":")[1].strip().rstrip(']'))

            lados.extend([up, left, down, right])  # Adicionando os lados à lista
            return lados
        except ValueError as e:
            print(f"Erro ao converter lados para inteiro: {e}")
            return None

    def carregar_imagem(self, id_carta):
        id_carta = int(id_carta)
        
        if id_carta < 10:
            imagem = (f"images//cards//00{id_carta}.png")
        elif id_carta < 100:
            imagem = (f"images//cards//0{id_carta}.png")
        else:
            imagem = (f"images//cards//{id_carta}.png")
        return imagem

    def carregar_cartas(self):
        try:
            with open('data//cards.csv', 'r', encoding='utf-16le') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)  # Pular o cabeçalho
                cartas_disponiveis = []
                ids_selecionados = set()

                for linha in reader:
                    if len(linha) > 1:
                        lados = self.recolher_lados(linha[2], linha[3])
                        if lados:  # Verifica se lados foi retornado corretamente
                            nova_carta = Carta(linha[0], linha[1], lados, linha[4], self.carregar_imagem(linha[0]))
                            cartas_disponiveis.append(nova_carta)

                if cartas_disponiveis:
                    print(f"Total de cartas carregadas: {len(cartas_disponiveis)}")
                    while len(ids_selecionados) < 5:
                        id_aleatorio = random.randint(0, len(cartas_disponiveis) - 1)
                        if id_aleatorio not in ids_selecionados:
                            ids_selecionados.add(id_aleatorio)
                            carta_selecionada = cartas_disponiveis[id_aleatorio]
                            self.adicionar_carta(carta_selecionada)
                            print(f"Carta '{carta_selecionada.nome}' adicionada.")
                else:
                    print("Nenhuma carta disponível no arquivo.")
        except Exception as e:
            print(f"Não foi possível carregar as cartas: {e}")

    
    def get_cartas(self):
        return self.cartas