#Atividade de aplicaçao de metaheuristicas para resolver o problema da localização ótima de geradores na rede de distribuição
#Disciplina: Métodos de Otimização
#Aluno: Gabriel Loureiro Medeiros
#PSO

import numpy
import pandas
import msp

#Atualiza o arquivo de dados com a posição dos geradores
def tabela_gerador(tabela_dados, father_and_son, P_gen):
    tabela_dados_aux=tabela_dados.copy()
    for ii in range(len(father_and_son)):
        tabela_dados_aux.loc[father_and_son[ii]-1,['pl']]=tabela_dados_aux.loc[father_and_son[ii]-1,['pl']]-P_gen[ii]
    return tabela_dados_aux 

#Define o exame inicial randomicamente
def exame_inicial(N_bus,N_gen,N_pop):
    populacao=numpy.empty(shape=(N_pop,N_gen),dtype=numpy.int64) #aloca
    for ii in range(N_pop):
        populacao[ii]=numpy.random.randint(low=1, high= N_bus-1, size=N_gen)#cria um array randomico sem repetição que vai até o número de barras
    return populacao

#Avalia o custo da posicao avaliada
def funcao_custo(V0,tol,kmax,tabela_dados,posicao, P_gen):
    custo = msp.msp(V0,tol,kmax,tabela_gerador(tabela_dados,posicao, P_gen))
    return custo

#Verifica se o vertice está dentro dos limites permitidos
def verifica_limites(particula,N_bus):
    for i in range(len(particula)):
        if particula[i] > N_bus-1:
            particula[i] = 1
            continue
        elif particula[i] < 1:
            particula[i] = N_bus-1
    return particula

#Input dos Dados
N_bus = 13
N_mov = 10
N_gen = 3
P_gen = numpy.array([0.040, 0.060, 0.080])
V0 = 4.16
tol = 1e-6
kmax = 10
K_run=10
N_pop=40

w = 0.5                   
c1 = 2.0                  
c2 = 2.0                  

D = N_gen                     
max_iter = 100             
x_min = 1
x_max = N_bus-1
iterMax = 20

p_val = numpy.zeros(N_pop)

p_best_val = numpy.zeros(N_pop)        
g_best_val = numpy.zeros(1)          

p_best = numpy.zeros((N_pop,D),dtype=int)      
g_best = numpy.zeros(D,dtype=int)     

populacao = exame_inicial(N_bus,N_gen,N_pop)

#Leitura do arquivo texto dos dados com pandas
tabela_dados = pandas.read_csv('dados13bus.txt',sep = "\t", skiprows = 1, header = None, names=["bus_from","bus_to","pl","ql","resistance","reatance","miles"],dtype={"bus_from":int,"bus_to":int,"pl":float,"ql":float,"resistance":float,"reatance":float,"miles":float})
tabela_dados.resistance=tabela_dados.resistance*tabela_dados.miles
tabela_dados.reatance=tabela_dados.reatance*tabela_dados.miles
tabela_dados.drop('miles',axis=1,inplace=True)
tabela_dados.pl = tabela_dados.pl/1000
tabela_dados.ql = tabela_dados.ql/1000


##main


for ii in range(N_pop):
    p_best_val[ii] = funcao_custo(V0,tol,kmax,tabela_dados,populacao[ii], P_gen)
    p_best [ii] = populacao[ii]

ind = numpy.argmin(p_best_val)                      
g_best_val = numpy.copy(p_best_val[ind]) 
g_best = numpy.copy(p_best[ind,:])  

v = numpy.zeros((N_pop,D))  

x=populacao
for iter in range(iterMax):
    rp = numpy.random.rand(D,N_pop)         
    rg = numpy.random.rand(D,N_pop)           
    
    y=g_best.reshape(1,len(g_best))
    z=p_best.reshape(N_gen,len(p_best))

    v_global = numpy.multiply(((x-y)),rg.transpose())*c2*(-1.0)    
    v_local = numpy.multiply((z.T- x),rp.T)*c1          
    
    v = w*v + (v_local + v_global)       

    for ii in range(N_pop):
        for jj in range(N_gen):
            if v[ii,jj] > x_max - x[ii,jj]:
                v[ii,jj] = x_max - x[ii,jj]
                continue
            elif v[ii,jj] < x_min - x[ii,jj]:
                v[ii,jj] = x_min - x[ii,jj]
    x = x + v

    x=numpy.round(x).astype(int)

    for ii in range(N_pop):
        p_val[ii] = funcao_custo(V0,tol,kmax,tabela_dados,x[ii], P_gen)
        if p_val[ii] < p_best_val[ii]:
            p_best_val[ii] = p_val[ii]
            p_best [ii] = x[ii]

    ind = numpy.argmin(p_best_val)                      
    g_best_val = numpy.copy(p_best_val[ind]) 
    g_best = numpy.copy(p_best[ind,:])  


print(g_best_val)
print(g_best)