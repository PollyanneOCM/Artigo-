#Modulo de Funcionamento da Bateria
#Artigo:SBSE

import numpy as np

#Função para calcular o balanço energético da bateria
def ener_bess(n_steps, soc_min, soc_max, soc_int, wind_pwr, sol_pwr, load):
    soc= np.zeros(n_steps)
    local_loss=0
    lpsp=0
    soc[0] = soc_int
    for i in range(time): 
        if soc[i] >= soc_min and soc[i] <= soc_max:
            soc[i+1] = soc[i] + (wind_pwr[i]+sol_pwr[i]-load[i])
            if soc[i+1] > soc_max:
                soc[i+1] = soc_max
            elif soc[i+1] < soc_min:
                soc[i+1] = soc_min
                local_loss = local_loss + (load[i] - ((soc[i]-soc_min)+wind_pwr[i]+sol_pwr[i]))
        lpsl=lpsp+local_loss
    lpsl=lpsp/sum(load)
    return soc, lpsl