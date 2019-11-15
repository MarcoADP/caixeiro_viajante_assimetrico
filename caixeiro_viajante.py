import numpy as np
import timeit
import itertools

#
# LEITURA
#
def ler_arquivo(file):
    f = open('instancias/' + file + '.atsp', 'r')
    return f.read().split('\n')


def get_informacao(informacoes, info):
    result = list(filter(lambda x: info in x, informacoes))
    if not result:
        return
    return result[0].split(':')[1].strip()


def get_grafo(informacoes, vertices):
    matriz = np.zeros((vertices, vertices))
    dados = informacoes[7:]
    i = 0
    j = 0
    for dado in dados:
        dado_separado = dado.split(' ')
        dado_separado = [s for s in dado_separado if s != '']
        for peso in dado_separado:
            if peso == 'EOF':
                break
            if j == vertices:
                i = i + 1
                j = 0
            matriz[i][j] = peso
            j = j + 1

    return matriz.astype(int)


def copia_matrix(solucao):
    copia = np.zeros(solucao.shape)
    for i in range(solucao.shape[0]):
        for j in range(solucao.shape[1]):
            copia[i][j] = solucao[i][j]
    return copia

#
# CLARKE WRIGHT
#
def calcular_caminho(solucao, origem, caminho):
    for destino in range(len(solucao[origem])):
        if solucao[origem][destino] != np.inf:
            caminho.insert(len(caminho), (origem, destino))
            solucao[origem][destino] = np.inf
            return calcular_caminho(solucao, destino, caminho)
    return caminho


def mesma_rota(u, v, origem, solucao):
    caminho = calcular_caminho(copia_matrix(solucao), origem, [])
    u_rota = False
    v_rota = False
    for x, y in caminho:
        if x == 0:
            u_rota = False
            v_rota = False
        if y == u:
            u_rota = True
        if y == v:
            v_rota = True
        if u_rota and v_rota:
            return True
    return False


def clarke_wright(grafo, vertices, origem):
    economias_dict = {}

    solucao = np.full((vertices, vertices), np.inf)
    #Passo 1 - Construir a solução passando sempre na origem
    for i in range(0, vertices):
        if i != origem:
            solucao[origem][i] = grafo[origem][i]
            solucao[i][origem] = grafo[i][origem]

    #Passo 2 - Calculando a economia para cada par de vértices (exceto se for dele para ele mesmo ou envolver a origem)
    for i in range(vertices):
        for j in range(vertices):
            if i == origem or j == origem or i == j:
                continue

            # [o, i] + [i, o] + [o, j] + [j,o] (caminho passando sempre pela origem)
            # [o, i] + [i, j] + [j, o] (caminho em que i vai direto para o j)
            # [i, o] + [o, j] - [i,j] (calculo da diferenca entre os dois caminhos)
            economias_dict[(i, j)] = grafo[i][origem] + grafo[origem][j] - grafo[i][j]

    #Passo 3 - Ordenando as economias
    economias_lista = sorted(economias_dict.items(), key=lambda kv: kv[1])
    economias_lista.reverse()

    #Passo 4 - Inserindo as economias possíveis
    a = 0
    t = len(economias_lista)
    for (u, v), valor in economias_lista:
        a = a + 1
        if (solucao[u][origem] != np.inf and solucao[origem][v] != np.inf) and (not mesma_rota(u, v, origem, copia_matrix(solucao))):
            solucao[u][origem] = np.inf
            solucao[origem][v] = np.inf
            solucao[u][v] = grafo[u][v]

    return solucao

#
# 3-OPT
#
def verifica_troca(grafo, caminho, a, b, c):
    aux = caminho[a]
    caminho[a] = caminho[b]
    caminho[b] = aux

    return 0



def three_opt(grafo, caminho, vertices):
    combinacoes = itertools.combinations(range(vertices), 3)
    while True:
        delta = 0
        for idx, (a, b, c) in enumerate(combinacoes):
            delta = delta + verifica_troca(grafo, caminho, a, b, c)
        if delta >= 0:
            break
        break


def calcular_solucao(solucao, origem, caminho, soma):
    for destino in range(len(solucao[origem])):
        if solucao[origem][destino] != np.inf:
            #caminho.insert(len(caminho), (origem, destino))
            caminho[origem] = destino
            soma = soma + solucao[origem][destino]
            solucao[origem][destino] = np.inf
            return calcular_solucao(solucao, destino, caminho, soma)
    return caminho.astype(int), soma


def mostrar_caminho(caminho, origem):
    for i in range(len(caminho)):
        destino = caminho[origem]
        print((origem, destino), end=' - ')
        origem = destino
    print('')


def main(file='br17', origem=0):
    np.set_printoptions(suppress=True)
    start = timeit.default_timer()
    informacoes = ler_arquivo(file)
    instancia = get_informacao(informacoes, 'NAME')
    vertices = int(get_informacao(informacoes, 'DIMENSION'))
    matriz_adjacencia = get_grafo(informacoes, vertices)
    # print(matriz_adjacencia)

    solucao = clarke_wright(matriz_adjacencia, vertices, origem)
    # print(type(solucao))
    caminho, soma = calcular_solucao(copia_matrix(solucao), origem, np.full(vertices, np.inf), 0)
    mostrar_caminho(caminho, origem)
    three_opt(matriz_adjacencia, caminho, vertices)
    print(soma)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    return soma

main(file='br17')