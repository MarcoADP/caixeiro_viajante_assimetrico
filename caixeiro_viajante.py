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


def esta_solucao(x, lista):
    return x in lista


def copia_matrix(solucao):
    copia = np.zeros(solucao.shape)
    for i in range(solucao.shape[0]):
        for j in range(solucao.shape[1]):
            copia[i][j] = solucao[i][j]
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


def extremo_inicial_roteiro(vertice, origem, solucao):
    return solucao[origem][vertice] != np.inf


def extremo_final_roteiro(vertice, origem, solucao):
    return solucao[vertice][origem] != np.inf


def clark_wright(grafo, vertices, origem):
    economias_dict = {}

    #Passo 1 - Construir a solução passando sempre na origem
    # solucao_inicial = []
    # for i in range(0, vertices):
    #     if i != origem:
    #         solucao_inicial.insert(len(solucao_inicial), (origem, i))
    #         solucao_inicial.insert(len(solucao_inicial), (i, origem))
    #
    # soma_solucao_inicial = 0
    # for x in solucao_inicial:
    #     soma_solucao_inicial = soma_solucao_inicial + grafo[x]
    #
    # return soma_solucao_inicial

    #Passo 2 - Calculando a economia para cada par de vértices (exceto se for dele para ele mesmo ou envolver a origem)
    for i in range(vertices):
        for j in range(vertices):
            if i == origem or j == origem or i == j:
                continue
            economias_dict[(i, j)] = grafo[i][origem] + grafo[origem][j] - grafo[i][j]
            #input("Press Enter to continue...")

    #[o, i] + [i, o] + [o, j] + [j,o] (caminho passando sempre pela origem)
    #[o, i] + [i, j] + [j, o] (caminho em que i vai direto para o j)
    #[i, o] + [o, j] - [i,j] (calculo da diferenca entre os dois caminhos)

    #Passo 3 - Ordenando as economias
    economias_lista = sorted(economias_dict.items(), key=lambda kv: kv[1])
    economias_lista.reverse()

    vertices_solucao = []
    solucao = np.full((vertices, vertices), np.inf)
    #Passo 4 - Inserindo as economias possíveis
    for (u, v), valor in economias_lista:
        # print(vertices_solucao)
        # print((u, v))
        u_solucao = esta_solucao(u , vertices_solucao)
        v_solucao = esta_solucao(v, vertices_solucao)

        #Verificar se nem u e nem v estão em roteiro
        if not u_solucao and not v_solucao:    #ambos 0 e 0
            # print(str((u, v)) + " estão em nenhum roteiro")
            #TODO Criar aresta 0-u-v-0
            solucao[origem][u] = grafo[origem][u]
            solucao[u][v] = grafo[u][v]
            solucao[v][origem] = grafo[v][origem]
            vertices_solucao.insert(0, u)
            vertices_solucao.insert(0, v)

        #Algum dos dois ou os dois estão em roteiro
        else:

            #Verificar se u ou v estão em roteiro (xor)
            if u_solucao ^ v_solucao: # operacao booleana de xor # 0 e 1 ou 1 e 0
                # print(str((u, v)) + " estão em um roteiro (um deles)")

                #Verificar se u ou v (quem estiver no roteiro) está no extremo do roteiro
                #Rever essa parte
                if u_solucao:
                    if extremo_inicial_roteiro(u, origem, solucao):
                        # print(str(u) + " está no extremo do roteiro0")
                        #TODO Agregar (i, j) no roteiro
                        solucao[origem][u] = np.inf
                        #solucao[u][origem] = np.inf
                        solucao[origem][v] = grafo[origem][v]
                        solucao[v][u] = grafo[v][u]
                        vertices_solucao.insert(0, v)

                elif v_solucao:
                    if extremo_final_roteiro(v, origem, solucao):
                        # print(str(v) + " está no extremo do roteiro1")
                        #TODO Agregar (i, j) no roteiro
                        #solucao[origem][v] = np.inf
                        solucao[v][origem] = np.inf
                        solucao[u][origem] = grafo[u][origem]
                        solucao[v][u] = grafo[v][u]
                        vertices_solucao.insert(0, u)


            #Os dois estão em roteiro
            else:
                # print(str((u, v)) + " estão em roteiros")
                #Verificar se os roteiros são diferentes
                if not mesma_rota(u, v, origem, solucao):
                    # print(str((u, v)) + " estão em roteiros diferentes")
                    # Verificar se u E v estão no extremo do roteiro
                    if extremo_final_roteiro(u, origem, solucao) and extremo_inicial_roteiro(v, origem, solucao):
                        # print(str((u, v)) + " estão no extremo do roteiro")
                        solucao[u][origem] = np.inf
                        solucao[origem][v] = np.inf
                        solucao[u][v] = grafo[u][v]
                        # print('ENTROU AQUI!!!!!!!!!!!!!!!!!!!')
                        #TODO Unir os dois roteiros

        # print(solucao)
        # print(vertices_solucao)
        # print('')
        # input("Press Enter to continue...")
        # print('')

    return solucao

def clark_wright2(grafo, vertices, origem):
    economias_dict = {}

    solucao = np.full((vertices, vertices), np.inf)
    #Passo 1 - Construir a solução passando sempre na origem
    # solucao_inicial = []
    for i in range(0, vertices):
        if i != origem:
            solucao[origem][i] = grafo[origem][i]
            solucao[i][origem] = grafo[i][origem]
            # solucao_inicial.insert(len(solucao_inicial), (origem, i))
            # solucao_inicial.insert(len(solucao_inicial), (i, origem))



    #Passo 2 - Calculando a economia para cada par de vértices (exceto se for dele para ele mesmo ou envolver a origem)
    for i in range(vertices):
        for j in range(vertices):
            if i == origem or j == origem or i == j:
                continue
            economias_dict[(i, j)] = grafo[i][origem] + grafo[origem][j] - grafo[i][j]
            #input("Press Enter to continue...")

    #[o, i] + [i, o] + [o, j] + [j,o] (caminho passando sempre pela origem)
    #[o, i] + [i, j] + [j, o] (caminho em que i vai direto para o j)
    #[i, o] + [o, j] - [i,j] (calculo da diferenca entre os dois caminhos)

    #Passo 3 - Ordenando as economias
    economias_lista = sorted(economias_dict.items(), key=lambda kv: kv[1])
    economias_lista.reverse()

    #Passo 4 - Inserindo as economias possíveis
    a = 0
    t = len(economias_lista)
    for (u, v), valor in economias_lista:
        a = a + 1
        #print(str(a) + '/' + str(t))
        # print(u, v)
        if not mesma_rota(u, v, origem, copia_matrix(solucao)) and (solucao[u][origem] != np.inf and solucao[origem][v] != np.inf):
            #print('ROTA DIFERENTE')
            solucao[u][origem] = np.inf
            solucao[origem][v] = np.inf
            solucao[u][v] = grafo[u][v]
        # elif (solucao[u][origem] != np.inf and solucao[origem][v] != np.inf):
        #     print('EXTREMOS!')
        #     solucao[u][origem] = np.inf
        #     solucao[origem][v] = np.inf
        #     solucao[u][v] = grafo[u][v]
        # else:
        #     print('SEM IF!!!')
        #print(solucao)
        #print('')

    return solucao


def calcular_solucao(solucao, origem, caminho, soma):
    for destino in range(len(solucao[origem])):
        if solucao[origem][destino] != np.inf:
            caminho.insert(len(caminho), (origem, destino))
            soma = soma + solucao[origem][destino]
            solucao[origem][destino] = np.inf
            return calcular_solucao(solucao, destino, caminho, soma)
    return caminho, soma


def main(file='teste', origem=0):
    np.set_printoptions(suppress=True)
    start = timeit.default_timer()
    informacoes = ler_arquivo(file)
    instancia = get_informacao(informacoes, 'NAME')
    vertices = int(get_informacao(informacoes, 'DIMENSION'))
    matriz_adjacencia = get_grafo(informacoes, vertices)
    # print(matriz_adjacencia)
    solucao = clark_wright(matriz_adjacencia, vertices, origem)
    caminho, soma = calcular_solucao(copia_matrix(solucao), origem, [], 0)
    print(caminho)
    print(soma)

    solucao = clark_wright2(matriz_adjacencia, vertices, origem)
    # print(type(solucao))
    caminho, soma = calcular_solucao(copia_matrix(solucao), origem, [], 0)
    print(caminho)
    print(soma)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    return soma

#main(file='br17')