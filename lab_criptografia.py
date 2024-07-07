from funcoes_criptografia import * 


####################################################### Função principal ####################################################### 

def main():
    mensagem = """NO MEIO DO CAMINHO TINHA UMA PEDRA. TINHA UMA PEDRA NO MEIO DO
CAMINHO. TINHA UMA PEDRA. NO MEIO DO CAMINHO TINHA UMA PEDRA.
NUNCA ME ESQUECEREI DESSE ACONTECIMENTO NA VIDA DE MINHAS RETINAS
TAO FATIGADAS. NUNCA ME ESQUECEREI QUE NO MEIO DO CAMINHO TINHA
UMA PEDRA. TINHA UMA PEDRA. TINHA UMA PEDRA NO MEIO DO CAMINHO. NO
MEIO DO CAMINHO TINHA UMA PEDRA. POEMA DE CARLOS DRUMMOND DE
ANDRADE."""
    
    ordem_chaves = 10**5

    # Mensagem sem Tabs e \n
    mensagem = " ".join(mensagem.split("\n"))
    

    ## Preparação do Algoritmo - obtenção das chaves pública e privada
    primos = crivo_eratostenes(ordem_chaves)
    p, q = escolher_primos(ordem_chaves, primos)
    print(f"Primos escolhidos: p={p}, q={q}")
    n = p*q
    e = expoente_publico(p, q)


    ## Execução do algoritmo de codificação
    mensagem_pre_codificada = pre_codificacao(mensagem)
    print(f"Mensagem pré-codificada: {mensagem_pre_codificada}")
    chave_publica = {'n':n, 'e':e}
    print(f"Chave pública: {chave_publica}")
    msg_codificada = codificacao(mensagem_pre_codificada, chave_publica)
    print(f"Mensagem codificada: {msg_codificada}")

    # Execução do algoritmo de decodificação de forma errada
    # r, s = escolher_primos(ordem_chaves, primos) # primos utilizados para decodificar de forma errônea
    # d_errado = expoente_privado(r, s, e)
    # chave_privada_errada = {'n':n, 'd':d_errado}
    # print(f"Chave privada errada: {chave_privada_errada}")

    # msg_decodificada_errada = decodificacao(msg_codificada, chave_privada_errada)
    # print(f"Mensagem decodificada com primos errados: {msg_decodificada_errada}")


    # Execução do algoritmo de decodificação de forma correta
    d = expoente_privado(p, q, e)
    chave_privada = {'n':n, 'd':d}
    print(f"Chave privada: {chave_privada}")
    msg_decodificada = decodificacao(msg_codificada, chave_privada)
    print(f"Mensagem decodificada com primos corretos: {msg_decodificada}")


main()

