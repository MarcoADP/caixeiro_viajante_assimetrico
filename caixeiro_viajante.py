import numpy as np
import timeit

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

    return matriz


def copia_matrix(solucao):
    copia = np.zeros(solucao.shape)
    for i in range(solucao.shape[0]):
        for j in range(solucao.shape[1]):
            copia[i][j] = solucao[i][j]
    return copia


def copia_lista(lista):
    copia = []
    for i in range(len(lista)):
        copia.insert(i, lista[i])
    return copia


def mesma_rota(u, v, origem, solucao):
    solucao, soma = calcular_solucao(copia_matrix(solucao), origem, [], 0)
    u_rota = False
    v_rota = False
    for x, y in solucao:
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


def clark_wright(grafo, vertices, origem):
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


def calcular_solucao(solucao, origem, caminho, soma):
    for destino in range(len(solucao[origem])):
        if solucao[origem][destino] != np.inf:
            caminho.insert(len(caminho), (origem, destino))
            soma = soma + solucao[origem][destino]
            solucao[origem][destino] = np.inf
            return calcular_solucao(solucao, destino, caminho, soma)
    return caminho, soma

#////////////////////// 3OPT /////////////////////////////


def verifica_adjacencia(matriz_adjacencia, i, j):
     if matriz_adjacencia[i][j] != None:  # Verifica se existe adjacência entre dois vértices
        return True
     return False


def tam_caminho(percurso):
     return len(percurso)  #Retorna o tamanho do caminho


def calc_distancia(matriz_adjacencia, percurso):
    soma = 0
    if tam_caminho(percurso)>1:
        for i in range(tam_caminho(percurso) - 1):
            if verifica_adjacencia(matriz_adjacencia, percurso[i], percurso[i+1]):
                soma += matriz_adjacencia[percurso[i]][percurso[i + 1]] #Faz a soma do caminho
    return soma


def distancia(matriz_adjacencia, a, b):
    if verifica_adjacencia(matriz_adjacencia, a, b):
        return matriz_adjacencia[a][b]  #retorna a distância entre dois pontos


def tresopt(matriz_adjacencia, caminho):
    print("Caminho inicial gerado pelo Clark-Wright: ", caminho)
    print("Contagem inicial: ", calc_distancia(matriz_adjacencia, caminho))

    for i in range(len(caminho)-1):
        for j in range(i+2, len(caminho)-1):
            for k in range(j+2, len(caminho)-1):

                opcao = 0
                forma_atual = distancia(matriz_adjacencia, caminho[i], caminho[i+1])+ distancia(matriz_adjacencia, caminho[j], caminho[j+1])+ distancia(matriz_adjacencia, caminho[k], caminho[k+1])

                if forma_atual > distancia(matriz_adjacencia, caminho[i],caminho[i + 1]) + distancia(matriz_adjacencia, caminho[j],caminho[k]) + distancia(matriz_adjacencia, caminho[j + 1],caminho[k + 1]):
                    forma_atual = distancia(matriz_adjacencia, caminho[i],caminho[i + 1]) + distancia(matriz_adjacencia, caminho[j],caminho[k]) + distancia(matriz_adjacencia, caminho[j + 1],caminho[k + 1])
                    opcao = 1

                if forma_atual > distancia(matriz_adjacencia, caminho[i],caminho[j]) + distancia(matriz_adjacencia, caminho[i + 1],caminho[j + 1]) + distancia(matriz_adjacencia, caminho[k],caminho[k + 1]):
                    forma_atual = distancia(matriz_adjacencia, caminho[i],caminho[j]) + distancia(matriz_adjacencia, caminho[i + 1],caminho[j + 1]) + distancia(matriz_adjacencia, caminho[k],caminho[k + 1])
                    opcao = 2

                if forma_atual > distancia(matriz_adjacencia, caminho[i],caminho[j]) + distancia(matriz_adjacencia, caminho[i + 1],caminho[k]) + distancia(matriz_adjacencia, caminho[j + 1],caminho[k + 1]):
                    forma_atual = distancia(matriz_adjacencia, caminho[i],caminho[j]) + distancia(matriz_adjacencia, caminho[i + 1],caminho[k]) + distancia(matriz_adjacencia, caminho[j + 1],caminho[k + 1])
                    opcao = 3

                if forma_atual > distancia(matriz_adjacencia, caminho[i],caminho[j + 1]) + distancia(matriz_adjacencia, caminho[k],caminho[i + 1]) + distancia(matriz_adjacencia, caminho[j],caminho[k + 1]):
                    forma_atual = distancia(matriz_adjacencia, caminho[i],caminho[j + 1]) + distancia(matriz_adjacencia, caminho[k],caminho[i + 1]) + distancia(matriz_adjacencia, caminho[j],caminho[k + 1])
                    opcao = 4

                if forma_atual > distancia(matriz_adjacencia, caminho[i],caminho[j + 1]) + distancia(matriz_adjacencia, caminho[k],caminho[j]) + distancia(matriz_adjacencia, caminho[i + 1],caminho[k + 1]):
                    forma_atual = distancia(matriz_adjacencia, caminho[i], caminho[j + 1]) + distancia(matriz_adjacencia, caminho[k],caminho[j]) + distancia(matriz_adjacencia, caminho[i + 1],caminho[k + 1])
                    opcao = 5

                if forma_atual > distancia(matriz_adjacencia, caminho[i],caminho[k]) + distancia(matriz_adjacencia, caminho[j + 1], caminho[i + 1]) + distancia(matriz_adjacencia, caminho[j],caminho[k + 1]):
                    forma_atual = distancia(matriz_adjacencia, caminho[i],caminho[k]) + distancia(matriz_adjacencia, caminho[k],caminho[i + 1]) + distancia(matriz_adjacencia, caminho[j],caminho[k + 1])
                    opcao = 6
                if forma_atual > distancia(matriz_adjacencia, caminho[i],caminho[k]) + distancia(matriz_adjacencia, caminho[j + 1],caminho[j]) + distancia(matriz_adjacencia, caminho[i + 1],caminho[k + 1]):
                    forma_atual = distancia(matriz_adjacencia, caminho[i],caminho[k]) + distancia(matriz_adjacencia, caminho[j + 1],caminho[j]) + distancia(matriz_adjacencia, caminho[i + 1],caminho[k + 1])
                    opcao = 7

                caminho_aux = copia_lista(caminho)
                if opcao == 1:
                    caminho[j+1:k+1] = reversed(caminho[j+1:k+1])

                if opcao == 2:
                    caminho[i + 1:j + 1] = reversed(caminho[i + 1:j + 1])

                if opcao == 3:
                    caminho[i + 1:j + 1], caminho[j + 1:k + 1] = reversed(caminho[i + 1:j + 1]), reversed(caminho[j + 1:k + 1])

                if opcao == 4:
                    caminho = caminho[:i + 1] + caminho[j + 1:k + 1] + caminho[i + 1:j + 1] + caminho[k + 1:]

                if opcao == 5:
                    aux = caminho[:i + 1] + caminho[j + 1:k + 1]
                    aux += reversed(caminho[i + 1:j + 1])
                    aux += caminho[k + 1:]
                    caminho = aux

                if opcao == 6 :
                    aux = caminho[:i + 1]
                    aux += reversed(caminho[j + 1:k + 1])
                    aux += caminho[i + 1:j + 1]
                    aux += caminho[k + 1:]
                    caminho = aux

                if opcao == 7:
                    aux = caminho[:i + 1]
                    aux += reversed(caminho[j + 1:k + 1])
                    aux += reversed(caminho[i + 1:j + 1])
                    aux += caminho[k + 1:]
                    caminho = aux

                if calc_distancia(matriz_adjacencia, caminho) > calc_distancia(matriz_adjacencia, caminho_aux):
                    caminho = caminho_aux

                #print("Contagem parcial:", calc_distancia(matriz_adjacencia, caminho))

    print(' ')
    print("Caminho final gerado pelo 3-OPT:", caminho)
    print("Contagem final:", calc_distancia(matriz_adjacencia, caminho))


def get_entrada_tresopt(caminho):
    caminho_3opt = []
    for x,y in caminho:
        caminho_3opt.insert(len(caminho_3opt), x)
    caminho_3opt.insert(len(caminho_3opt), y)
    return caminho_3opt


#///////// Main /////////


def main(file='teste', origem=0):
    np.set_printoptions(suppress=True)
    start = timeit.default_timer()
    informacoes = ler_arquivo(file)
    instancia = get_informacao(informacoes, 'NAME')
    vertices = int(get_informacao(informacoes, 'DIMENSION'))
    matriz_adjacencia = get_grafo(informacoes, vertices)
    # print(matriz_adjacencia)

    solucao = clark_wright(matriz_adjacencia, vertices, origem)
    # print(type(solucao))
    caminho, soma = calcular_solucao(copia_matrix(solucao), origem, [], 0)

    print('')
    print('Caminho gerado pelo Clark-Wright:', caminho)
    print('Contagem: ', soma)
    stop = timeit.default_timer()
    print('Time de execução Clark-Wright: ', stop - start)
    print('')

    caminho_3opt = get_entrada_tresopt(caminho)
                    #[0, 11, 13, 2, 12, 10, 9, 1, 16, 8, 7, 15, 4, 3, 14, 6, 5]
    #caminho_3opt = [0, 11, 13, 2, 12, 10, 9, 1, 16, 8, 7, 15, 4, 3, 14, 6, 5, 0]
    start = timeit.default_timer()
    tresopt(matriz_adjacencia, caminho_3opt)
    stop = timeit.default_timer()
    print('Time de execução 3-OPT: ', stop - start)


main(file='kro124p')
