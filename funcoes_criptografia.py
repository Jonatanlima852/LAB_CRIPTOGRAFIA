import random

####################################################### Funções principais #######################################################


def escolher_primos(ordem, primos):


    # Primos que satisfazem a ordem mínima
    primos_filtrados = [p for p in primos if (ordem <= p)]
    # escolhe dois primos acima da ordem pedida 
    p1, p2 = random.sample(primos_filtrados, 2)
    
    return p1, p2


def pre_codificacao(msg):
    mapeamento = {
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 
        'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 
        'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'X': 32, 'W': 33, 
        'Y': 34, 'Z': 35, ' ': 36, '.': 37
    }

    msg = msg.upper() # Converte para todas maiúsculas
    codigos = []

    for caractere in msg:
        if caractere in mapeamento:
            codigos.append(mapeamento[caractere])
        else:
            print(f"Na mensagem, há um caractere não mapeado: {caractere}")


    return codigos

def codificacao(mensagem, chave_publica):
    # Passo 1: Quebrar a mensagem em blocos de tamanho até m
    inf = 3
    sup = 9
    blocos = quebrar_em_blocos(mensagem, inf, sup)
    # Passo 2: Codificar cada bloco
    blocos_codificados = [codificar_bloco(bloco, chave_publica) for bloco in blocos]
    return blocos_codificados


def decodificacao(blocos_codificados, chave_privada):
    mensagem_decodificada = ''
    for bloco_codificado in blocos_codificados:
        bloco_decodificado_str = decodificar_bloco(bloco_codificado, chave_privada)
        mensagem_decodificada += bloco_decodificado_str


    # Converte a string decodificada de volta para a mensagem original
    mapeamento_inverso = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 
                          18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 
                          26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'X', 33: 'W', 
                          34: 'Y', 35: 'Z', 36: ' ', 37: '.'}
    mensagem_original = ''


    for i in range(0, len(mensagem_decodificada), 2):
        codigo = int(mensagem_decodificada[i:i+2])
        mensagem_original += mapeamento_inverso[codigo]
    return mensagem_original



####################################################### Funções secundárias #######################################################

def crivo_eratostenes(n):
    # Aumenta n em duas ordens para, ao fim, ter a chaves da ordem requerida apesar do limite inferior
    n = n*10**2
    # Cria uma lista de booleanos representando se o índice é primo ou não
    primos = [True] * (n + 1)
    p = 2
    
    while (p * p <= n):
        # Se primos[p] não foi marcado como False, então é um número primo
        if (primos[p] == True):
            # Atualiza todos os múltiplos de p para False
            for i in range(p * p, n + 1, p):
                primos[i] = False
        p += 1
    
    lista_primos = [p for p in range(2, n + 1) if primos[p]]
    return lista_primos


def expoente_publico(p,q):

    phi_n = (p-1)*(q-1)

    candidatos = [17, 257, 65537] # Primos de Fermat do tipo 2^2^k+1, fornecem segurança e fácil exponenciação
    random.shuffle(candidatos)
    for e in candidatos:
        if gcd(e, phi_n) == 1:
            return e
    # Caso nenhum dos candidatos funcione, escolha um aleatório dentro de um intervalo
    while True:
        e = random.randrange(2, phi_n)
        if gcd(e, phi_n) == 1:
            return e
        

def expoente_privado(p, q, e):
    phi_n = (p-1)*(q-1)
    mdc, x, y = euclides_estendido(e, phi_n)  # Portanto, e*x+phi_n*y = 1 => x e = e^-1 (mod phi_n)
    if mdc != 1:
        raise ValueError("O valor de 'e' não é coprimo com phi_n, escolha outro 'e'.")

    # O valor de x pode ser negativo, então ajustamos para que seja positivo
    d = x % phi_n
    return d


def quebrar_em_blocos(codigos, inf, sup):
    bloco_total = ''.join(map(str, codigos))

    blocos = []
    bloco_atual = []
    m = random.randint(inf, sup) # primeiro valor para n

    for i, numero in enumerate(bloco_total):
        bloco_atual.append(numero)
        if i+1 < len(bloco_total):
            proximo_numero = bloco_total[i+1]
        else: 
            proximo_numero = 1  # Apenas para realizar a comparação final
        

        # Condição do próximo número não ser zero. 
        # Observe que não há caso em que há dois zeros, de forma que o bloco nunca poderá ser maior que n.
        if len(bloco_atual) == m and proximo_numero != '0' : 
            blocos.append(bloco_atual)
            bloco_atual = []
            m = random.randint(inf, sup) # próximo valor para m
        elif len(bloco_atual) == m:
            m = m + 1 # para o zero ser adicionado ao fim no próximo loop
    
    if bloco_atual:
        blocos.append(bloco_atual)  # Adicionar último bloco
    
    return blocos


def codificar_bloco(bloco, chave_publica):
    # Concatena os números do bloco para formar um número grande
    numero = int(''.join(map(str, bloco)))
    # Codifica o número grande usando exponenciação modular
    return pow(numero, chave_publica['e'], chave_publica['n'])


def decodificar_bloco(bloco_codificado, chave_privada):
    # Decodifica o bloco usando exponenciação modular
    numero_decodificado = pow(bloco_codificado, chave_privada['d'], chave_privada['n'])
    # Converte o número decodificado de volta para uma string
    bloco_decodificado_str = str(numero_decodificado)

    return bloco_decodificado_str


####################################################### Funções matemáticas #######################################################


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def euclides_estendido(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = euclides_estendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y  # Retorna mdc entre a e b, e coeficientes x, y que satisfazem ax+by=1


def potencia_modular(a, e, n): 
    # formato: a^e (mod n)
    P = 1
    E = e
    A = a
    while(E != 0):
        if(E % 2 == 0):
            A = (A ** 2) % n
            E = E / 2
        else:
            P = (A * P) % n
            A = (A ** 2) % n
            E = (E - 1) / 2
    return P
