import numpy as np
import random
import gc

class GeradorSequencia:
    
    def __init__(self, perfil:[], acessos_esperados: int):
        self.__perfil = perfil # Exemplo: [(64 páginas dif, 16 de amplitude), (64, 8), (64, 4), (64, 2)]
        self.__acessos_esperados = acessos_esperados
        self.__acessos_realizados = 0
        self.__total_alocacoes = 0
        self.__paginas_ordenadas = []
        self.__paginas_embaralhadas = []
        
    @property
    def acessos_realizados(self):
        return self.__acessos_realizados
     
    @property
    def paginas_ordenadas(self):
        return self.__paginas_ordenadas
        
    @property
    def paginas_embaralhadas(self):
        return self.__paginas_embaralhadas      

    def gera_sequencia_normal(self):
        for i in range (len(self.__perfil)):
            self.__total_alocacoes += self.__perfil[i][0] * self.__perfil[i][1]
        #print('Alocações básicas: ', self.__total_alocacoes)
        multiplicador = int(self.__acessos_esperados / self.__total_alocacoes)
        self.__acessos_realizados = multiplicador * self.__total_alocacoes
        
        pagina = 0
        for i in range (len(self.__perfil)):
            quantidade_paginas = self.__perfil[i][0]
            quantidade_alocacoes = self.__perfil[i][1] * multiplicador
            for k in range(quantidade_paginas):
                for j in range(quantidade_alocacoes):
                    self.__paginas_ordenadas.append(pagina)
                pagina += 1
      
    def gera_sequencia_embaralhada(self):
        paginas_ordenadas_array = np.array(self.__paginas_ordenadas)
        np.random.shuffle(paginas_ordenadas_array)
        #print(paginas_ordenadas_array)
        #print()
        
        self.__paginas_embaralhadas = paginas_ordenadas_array.tolist()
        #print(self.__paginas_embaralhadas)
        return self.__paginas_embaralhadas

class TesteFIFO:
    def __init__(self, quantidade_quadros: int):
        self.__quantidade_page_fault = 0
        self.__quantidade_quadros = quantidade_quadros
        self.__quadros_memoria = []
        for i in range(self.__quantidade_quadros):
            self.__quadros_memoria.append(None)
            
    @property
    def quantidade_page_fault(self):
        return self.__quantidade_page_fault
           
    def insere_pagina(self, pagina):
        if pagina in self.__quadros_memoria:
            return
        for i in range(self.__quantidade_quadros):
            if self.__quadros_memoria[i] == None:
                self.__quadros_memoria[i] = pagina
                return
        self.__quantidade_page_fault += 1
        self.__quadros_memoria.pop(0)
        self.__quadros_memoria.append(pagina)

        
class TesteSegundaChance:
    def __init__(self, quantidade_quadros: int):
        self.__quantidade_page_fault = 0
        self.__quantidade_quadros = quantidade_quadros
        self.__quadros_memoria = []
        for i in range(self.__quantidade_quadros):
            self.__quadros_memoria.append(None)
        self.__pagina_referenciada = {}
            
    @property
    def quantidade_page_fault(self):
        return self.__quantidade_page_fault
            
    def insere_pagina(self, pagina):
        self.__pagina_referenciada[pagina] = 1
        if pagina in self.__quadros_memoria:
            return
        for i in range(self.__quantidade_quadros):
            if self.__quadros_memoria[i] == None:
                self.__quadros_memoria[i] = pagina
                return
        self.__quantidade_page_fault += 1
        contador = 0
        while contador < self.__quantidade_quadros:
            dado = self.__quadros_memoria[contador]
            if self.__pagina_referenciada[dado] == 1:
                self.__quadros_memoria.pop(contador)
                self.__quadros_memoria.append(dado)
                self.__pagina_referenciada[dado] = 0
            else:
                self.__quadros_memoria.pop(contador)
                self.__quadros_memoria.append(pagina)
                self.__pagina_referenciada[dado] = 0
                return
            contador += 1
        self.__quadros_memoria.pop(0)
        self.__quadros_memoria.append(pagina)
        
class TesteNRU:
    def __init__(self, quantidade_quadros: int, refreshM, refreshR):
        self.__quantidade_page_fault = 0
        self.__quantidade_quadros = quantidade_quadros
        self.__quadros_memoria = []
        for i in range(self.__quantidade_quadros):
            self.__quadros_memoria.append(None)
        self.__pagina_referenciada = {}
        self.__pagina_modificada = {}
        self.__contador_incrementaM = 0
        self.__contador_zera_todosR = 0
        self.__refreshM = refreshM
        self.__refreshR = refreshR
            
    @property
    def quantidade_page_fault(self):
        return self.__quantidade_page_fault

    def insere_pagina(self, pagina):
        '''
        Neste ponto faz a simulação de escrita em memória (seta 1 bit M das páginas presentes em quadros)
        o zeramento periódico de todos os bits R.
        '''
        self.__contador_incrementaM += 1
        if self.__contador_incrementaM > self.__refreshM:
            indice = random.randint(1, len(self.__quadros_memoria)) - 1
            pagina_sorteada = self.__quadros_memoria[indice]
            self.__pagina_modificada[pagina_sorteada] = 1
            self.__contador_incrementaM = 0
            
        self.__contador_zera_todosR += 1
        if self.__contador_zera_todosR > self.__refreshR:
            for paginas in self.__quadros_memoria:
                self.__pagina_referenciada[paginas] = 0
            self.__contador_zera_todosR = 0     

        self.__pagina_referenciada[pagina] = 1
        self.__pagina_modificada[pagina] = 0
        if pagina in self.__quadros_memoria:
            return
        for i in range(self.__quantidade_quadros):
            if self.__quadros_memoria[i] == None:
                self.__quadros_memoria[i] = pagina
                return
        self.__quantidade_page_fault += 1 
        classe0 = []
        classe1 = []
        classe2 = []
        classe3 = []
        contador = 0
        while contador < self.__quantidade_quadros:
            dado = self.__quadros_memoria[contador]
            if self.__pagina_referenciada[dado] == 0 and self.__pagina_modificada[dado] == 0:
                classe0.append(dado)
            else:
                if self.__pagina_referenciada[dado] == 0 and self.__pagina_modificada[dado] == 1:
                    classe1.append(dado)
                else:
                    if self.__pagina_referenciada[dado] == 1 and self.__pagina_modificada[dado] == 0:
                        classe2.append(dado)
                    else:
                        if self.__pagina_referenciada[dado] == 1 and self.__pagina_modificada[dado] == 1:
                            classe3.append(dado)
            contador += 1
        if len(classe0) > 0:
            indice = random.randint(1, len(classe0)) - 1
            pagina_sorteada = classe0[indice]
        else:
            if len(classe1) > 0:
                indice = random.randint(1, len(classe1)) - 1
                pagina_sorteada = classe1[indice]
            else:
                if len(classe2) > 0:
                    indice = random.randint(1, len(classe2)) - 1
                    pagina_sorteada = classe2[indice]
                else:
                    if len(classe3) > 0:
                        indice = random.randint(1, len(classe3)) - 1
                        pagina_sorteada = classe3[indice]
        self.__quadros_memoria.remove(pagina_sorteada)
        self.__quadros_memoria.append(pagina)
        self.__pagina_referenciada[pagina_sorteada] = 0
        self.__pagina_modificada[pagina_sorteada] = 0
        self.__pagina_referenciada[pagina] = 1
        self.__pagina_modificada[pagina] = 0


class TesteLRU:
    def __init__(self, quantidade_quadros: int):
        self.__quantidade_page_fault = 0
        self.__quantidade_quadros = quantidade_quadros
        self.__quadros_memoria = []
        for i in range(self.__quantidade_quadros):
            self.__quadros_memoria.append(None)
            
    @property
    def quantidade_page_fault(self):
        return self.__quantidade_page_fault
            
    def insere_pagina(self, pagina):
        if pagina in self.__quadros_memoria:
            self.__quadros_memoria.remove(pagina)
            self.__quadros_memoria.insert(0, pagina)
            return
        for i in range(self.__quantidade_quadros):
            if self.__quadros_memoria[i] == None:
                self.__quadros_memoria[i] = pagina
                return
        self.__quantidade_page_fault += 1
        self.__quadros_memoria.pop()
        self.__quadros_memoria.insert(0, pagina)    

'''
objeto = GeradorSequencia([(25, 16), (25, 8), (25, 4), (25, 2)], 1000500)
objeto.gera_sequencia_normal()
embaralhada = objeto.gera_sequencia_embaralhada()
print("Total de páginas: ", objeto.acessos_realizados)
qtidade_quadros = 60
fifo = TesteFIFO(qtidade_quadros)
relogio = TesteSegundaChance(qtidade_quadros)
nru = TesteNRU(qtidade_quadros, 1000,10000)
lru = TesteLRU(qtidade_quadros)
for i in range(len(embaralhada)):
     fifo.insere_pagina(embaralhada[i])
     relogio.insere_pagina(embaralhada[i])
     nru.insere_pagina(embaralhada[i])
     lru.insere_pagina(embaralhada[i])
print('Quantidade de page faults (FIFO): ', fifo.quantidade_page_fault)
print('Quantidade de page faults (Relógio): ', relogio.quantidade_page_fault)
print('Quantidade de page faults (NRU): ', nru.quantidade_page_fault)
print('Quantidade de page faults (LRU): ', lru.quantidade_page_fault)
'''

'''
# Teste 1: oferta 1.000.000 de páginas (perfil abaixo) para 4 algoritmos e analisa page faults.
for cont in range(1, 201):
    objeto = GeradorSequencia([(25, 16), (25, 8), (25, 4), (25, 2)], 1000500)
    objeto.gera_sequencia_normal()
    embaralhada = objeto.gera_sequencia_embaralhada()
    qtidade_quadros = 60
    fifo = TesteFIFO(qtidade_quadros)
    relogio = TesteSegundaChance(qtidade_quadros)
    nru = TesteNRU(qtidade_quadros, 1000,10000)
    lru = TesteLRU(qtidade_quadros)
    for i in range(len(embaralhada)):
         fifo.insere_pagina(embaralhada[i])
         relogio.insere_pagina(embaralhada[i])
         nru.insere_pagina(embaralhada[i])
         lru.insere_pagina(embaralhada[i])
    print(cont, objeto.acessos_realizados, fifo.quantidade_page_fault, relogio.quantidade_page_fault, nru.quantidade_page_fault, lru.quantidade_page_fault)
    del fifo
    del relogio
    del nru
    del lru
    gc.collect()

# Teste 2a: oferta 1.000.000 de páginas (perfil abaixo) para 4 algoritmos e analisa page faults.
# Repete oferta 1.000.000 de páginas (alterando quantidade de páginas para 10x, e quantidade de quadros para 10x)
# para 4 algoritmos e analisa page faults. Ou seja, 
for cont in range(1, 201):
    objeto = GeradorSequencia([(250, 16), (250, 8), (250, 4), (250, 2)], 1005000)
    objeto.gera_sequencia_normal()
    embaralhada = objeto.gera_sequencia_embaralhada()
    qtidade_quadros = 600
    fifo = TesteFIFO(qtidade_quadros)
    #relogio = TesteSegundaChance(qtidade_quadros)
    #nru = TesteNRU(qtidade_quadros, 1000,10000)
    #lru = TesteLRU(qtidade_quadros)
    for i in range(len(embaralhada)):
         fifo.insere_pagina(embaralhada[i])
         #relogio.insere_pagina(embaralhada[i])
         #nru.insere_pagina(embaralhada[i])
         #lru.insere_pagina(embaralhada[i])
    #print(cont, objeto.acessos_realizados, fifo.quantidade_page_fault, relogio.quantidade_page_fault, nru.quantidade_page_fault, lru.quantidade_page_fault)
    print(cont, objeto.acessos_realizados, qtidade_quadros, fifo.quantidade_page_fault)
    del fifo
    #del relogio
    #del nru
    #del lru
    gc.collect()
'''
'''
# Teste 2b: oferta 1.000.000 de páginas (perfil abaixo) para 4 algoritmos e analisa page faults.
# Repete oferta 1.000.000 de páginas (alterando quantidade de páginas para 10x, e quantidade de quadros para 10x)
# para 4 algoritmos e analisa page faults. Ou seja, 
for cont in range(1, 201):
    objeto = GeradorSequencia([(25, 16), (25, 8), (25, 4), (25, 2)], 1005000)
    objeto.gera_sequencia_normal()
    embaralhada = objeto.gera_sequencia_embaralhada()
    qtidade_quadros = 60
    fifo = TesteFIFO(qtidade_quadros)
    #relogio = TesteSegundaChance(qtidade_quadros)
    #nru = TesteNRU(qtidade_quadros, 1000,10000)
    #lru = TesteLRU(qtidade_quadros)
    for i in range(len(embaralhada)):
         fifo.insere_pagina(embaralhada[i])
         #relogio.insere_pagina(embaralhada[i])
         #nru.insere_pagina(embaralhada[i])
         #lru.insere_pagina(embaralhada[i])
    #print(cont, objeto.acessos_realizados, fifo.quantidade_page_fault, relogio.quantidade_page_fault, nru.quantidade_page_fault, lru.quantidade_page_fault)
    print(cont, objeto.acessos_realizados, qtidade_quadros, fifo.quantidade_page_fault)
    del fifo
    #del relogio
    #del nru
    #del lru
    gc.collect()
'''
# Teste 3a: oferta 1.000.000 de páginas (perfil abaixo) para 4 algoritmos e analisa page faults. Só que para este
# teste haverá uma relação entre quadros e páginas variando de 10% a 100%.
objeto = GeradorSequencia([(25, 16), (25, 8), (25, 4), (25, 2)], 1000500)
objeto.gera_sequencia_normal()
embaralhada = objeto.gera_sequencia_embaralhada()
for cont in range(1, 11):
    #qtidade_quadros = 60
    qtidade_quadros = 10 * cont
    fifo = TesteFIFO(qtidade_quadros)
    relogio = TesteSegundaChance(qtidade_quadros)
    nru = TesteNRU(qtidade_quadros, 1000,10000)
    lru = TesteLRU(qtidade_quadros)
    for i in range(len(embaralhada)):
         fifo.insere_pagina(embaralhada[i])
         relogio.insere_pagina(embaralhada[i])
         nru.insere_pagina(embaralhada[i])
         lru.insere_pagina(embaralhada[i])
    print(cont, qtidade_quadros, objeto.acessos_realizados, fifo.quantidade_page_fault, relogio.quantidade_page_fault, nru.quantidade_page_fault, lru.quantidade_page_fault)
    del fifo
    del relogio
    del nru
    del lru
'''
# Teste 3b: oferta 1.000.000 de páginas (perfil abaixo) para 4 algoritmos e analisa page faults. Só que para este
# teste haverá uma relação entre quadros e páginas variando de 10% a 100%.
objeto = GeradorSequencia([(250, 16), (250, 8), (250, 4), (250, 2)], 1000500)
objeto.gera_sequencia_normal()
embaralhada = objeto.gera_sequencia_embaralhada()
for cont in range(1, 11):
    #qtidade_quadros = 60
    qtidade_quadros = 100 * cont
    fifo = TesteFIFO(qtidade_quadros)
    relogio = TesteSegundaChance(qtidade_quadros)
    nru = TesteNRU(qtidade_quadros, 1000,10000)
    lru = TesteLRU(qtidade_quadros)
    for i in range(len(embaralhada)):
         fifo.insere_pagina(embaralhada[i])
         relogio.insere_pagina(embaralhada[i])
         nru.insere_pagina(embaralhada[i])
         lru.insere_pagina(embaralhada[i])
    print(cont, qtidade_quadros, objeto.acessos_realizados, fifo.quantidade_page_fault, relogio.quantidade_page_fault, nru.quantidade_page_fault, lru.quantidade_page_fault)
    del fifo
    del relogio
    del nru
    del lru
    gc.collect()
'''




