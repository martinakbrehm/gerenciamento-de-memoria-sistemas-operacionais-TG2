import numpy as np
import random

class GeradorSequencia:
    
    def __init__(self, perfil:[], acessos_esperados: int):
        self.__perfil = perfil # Exemplo: [(64, 16), (64, 8), (64, 4), (64, 2)]
        self.__acessos_esperados = acessos_esperados
        self.__acessos_realizados = 0
        self.__total_alocacoes = 0
        self.__paginas_ordenadas = []
        self.__paginas_embaralhadas = []
        
    @property
    def acessos_realizados(self):
        return self.__acessos_realizados
    
    @acessos_realizados.setter
    def acessos_realizados(self, acessos_realizados):
        self.__acessos_realizados = acessos_realizados
        
    @property
    def paginas_ordenadas(self):
        return self.__paginas_ordenadas
    
    @paginas_ordenadas.setter
    def paginas_ordenadas(self, paginas_ordenadas):
        self.__paginas_ordenadas = paginas_ordenadas
        
    @property
    def paginas_embaralhadas(self):
        return self.__paginas_embaralhadas
    
    @paginas_embaralhadas.setter
    def paginas_embaralhadas(self, paginas_embaralhadas):
        self.__paginas_embaralhadas = paginas_embaralhadas
        

    def gera_sequencia_normal(self):
        for i in range (len(self.__perfil)):
            self.__total_alocacoes += self.__perfil[i][0] * self.__perfil[i][1]
        print('Alocações básicas: ', self.__total_alocacoes)
        multiplicador = int(self.__acessos_esperados / self.__total_alocacoes) +1
        self.__acessos_realizados = multiplicador * self.__total_alocacoes
        
        pagina = 0
        for i in range (len(self.__perfil)):
            quantidade_paginas = self.__perfil[i][0]
            quantidade_alocacoes = self.__perfil[i][1] * multiplicador
            for k in range(quantidade_paginas):
                for j in range(quantidade_alocacoes):
                    self.__paginas_ordenadas.append(pagina)
                pagina += 1
        
        paginas_ordenadas_array = np.array(self.__paginas_ordenadas)
        #print(paginas_ordenadas_array)
        #print()
        return self.__paginas_ordenadas

                
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
    
    @quantidade_page_fault.setter
    def quantidade_page_fault(self, quantidade_page_fault):
        self.__quantidade_page_fault = quantidade_page_fault
            
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
    
    @quantidade_page_fault.setter
    def quantidade_page_fault(self, quantidade_page_fault):
        self.__quantidade_page_fault = quantidade_page_fault
            
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
                self.__quadros_memoria.pop(0)
                self.__quadros_memoria.append(dado)
                self.__pagina_referenciada[dado] = 0
            else:
                self.__quadros_memoria.pop(0)
                self.__quadros_memoria.append(pagina)
                return
            contador += 1
        self.__quadros_memoria.pop(0)
        self.__quadros_memoria.append(pagina)
        
class TesteNRU:
    def __init__(self, quantidade_quadros: int):
        self.__quantidade_page_fault = 0
        self.__quantidade_quadros = quantidade_quadros
        self.__quadros_memoria = []
        for i in range(self.__quantidade_quadros):
            self.__quadros_memoria.append(None)
        self.__pagina_referenciada = {}
        self.__pagina_modificada = {}
        self.__contador_incrementaM = 0
        self.__contador_zera_todosR = 0
            
    @property
    def quantidade_page_fault(self):
        return self.__quantidade_page_fault
    
    @quantidade_page_fault.setter
    def quantidade_page_fault(self, quantidade_page_fault):
        self.__quantidade_page_fault = quantidade_page_fault
            
    def insere_pagina(self, pagina):
        '''
        Neste ponto faremos a simulação de escrita em memória (seta 1 bit M das páginas presentes em quadros)
        o zeramento periódico do todos os bits R.
        '''
        self.__contador_incrementaM += 1
        if self.__contador_incrementaM > 3000:
            indice = random.randint(1, len(self.__quadros_memoria)) - 1
            pagina_sorteada = self.__quadros_memoria[indice]
            self.__pagina_modificada[pagina_sorteada] = 1
            self.__contador_incrementaM = 0
            
        self.__contador_zera_todosR += 1
        if self.__contador_zera_todosR > 100000:
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
              

objeto = GeradorSequencia([(16, 16), (16, 8), (16, 4), (16, 2)], 400000)
normal = objeto.gera_sequencia_normal()
embaralhada = objeto.gera_sequencia_embaralhada()
print("Total de páginas: ", objeto.acessos_realizados)

qtidade_quadros = 40
fifo = TesteFIFO(qtidade_quadros)
relogio = TesteSegundaChance(qtidade_quadros)
nru = TesteNRU(qtidade_quadros)
for i in range(len(embaralhada)):
    fifo.insere_pagina(embaralhada[i])
    relogio.insere_pagina(embaralhada[i])
    nru.insere_pagina(embaralhada[i])
print('Quantidade de page faults (FIFO): ', fifo.quantidade_page_fault)
print('Quantidade de page faults (Relógio): ', relogio.quantidade_page_fault)
print('Quantidade de page faults (NRU): ', nru.quantidade_page_fault)

