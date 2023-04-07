
import numpy as np
from FuncMSPdimensionamento import perdas, perdas_multiplas
import pandas as pd
from dados import f as default


def fitness(x):
    f = default.copy()
    f.demanda = f.demanda * 7
    pot_nominal = (x[0]*0.1100 + x[1]*2.400)/1000 # manda a potência nominal em kW
    perdas_ativas = perdas(pot_nominal)
    if perdas_ativas >= 0.202:
        return 100000000000
    vida_util = 20
    # Defiições do painel fotovoltaico utilizado
    n_PV = 0.173
    n_conv = 0.9
    custo_PV = 1183.94
    custo_OM_fixo_PV = custo_PV * 0.01
    RC_PV = 0
    vida_util_PV = 20
    area_painel = 1.66
    numero_paineis = x[0]

    # Definições para ajuste  de velocidade do vento
    H0 = 2
    H = 15
    Fator_rugosidade = 0.23
    vento_corrigido = f.vento * (H / H0) ** Fator_rugosidade

    # Definições do aerogerador utilizado
    Pot_max_GE = 2400
    Vc = 3.5
    Vf = 25
    Vr = 9.5
    custo_GE = 12394.36
    custo_OM_fixo_GE = custo_GE * 0.03
    RC_GE = 0
    vida_util_GE = 25
    salvage_GE = 772.92
    numero_aerogeradores = x[1]


    # Definições rede elétrica
    rede_disponivel = x[2]
    custo_REDE = 0.713370  # kWh
    custo_rede = custo_REDE / 1000  # kW
    custo_OM_fixo_rede = 0
    vida_util_rede = 1
    compra_total_vida_util = 0
    venda_total_vida_util = 0
    RC_rede = custo_rede
    tempo_avaliacao = 8760

    # Geração fotovoltaica
    Pot_PV = f.radiacao * n_PV * n_conv * area_painel * numero_paineis

    # Para LPSP
    LPS = 0

    # Geração eólica
    Pot_GE = np.zeros(len(vento_corrigido))
    index = set(f.index[vento_corrigido >= Vc].tolist()) & set(f.index[vento_corrigido <= Vr].tolist())
    Pot_GE[list(index)] = Pot_max_GE * ((vento_corrigido[list(index)] - Vc) / (Vr - Vc)) * numero_aerogeradores
    index = set(f.index[vento_corrigido >= Vr].tolist()) & set(f.index[vento_corrigido <= Vf].tolist())
    Pot_GE[list(index)] = Pot_max_GE * numero_aerogeradores

    perdas_energia = 0
    # estado de carga
    balanco = Pot_GE + Pot_PV - f.demanda / n_conv
    venda_total_vida_util = sum(balanco[balanco>0])
    compra_total_vida_util = sum(balanco[balanco<0])

    perdas_energia = sum(perdas_multiplas((balanco)/1000000))
    perdas_totais = perdas_energia - 0.202 * tempo_avaliacao
    # calculo dos indicadores
    ir = 0.06
    K_PV = 0
    K_GE = 0
    K_rede = 0

    for i in range(vida_util):
        K_rede = K_rede + 1 / (1 + ir) ** (i * vida_util_rede)
    PWA = (((1 + ir) ** vida_util) - 1) / (ir * (1 + ir) ** vida_util)

    NPC_PV = numero_paineis * (custo_PV + RC_PV * K_PV + custo_OM_fixo_PV * PWA)
    NPC_GE = numero_aerogeradores * (custo_GE + RC_GE * K_GE + custo_OM_fixo_GE * PWA - salvage_GE)
    NPC_REDE_COMPRA = compra_total_vida_util  * (custo_rede + RC_rede * K_rede + custo_OM_fixo_rede * PWA)
    NPC_REDE_VENDA = venda_total_vida_util  * (custo_rede + RC_rede * K_rede + custo_OM_fixo_rede * PWA)
    NPC_REDE_PERDAS = perdas_totais * 1000000  * (custo_rede + RC_rede * K_rede + custo_OM_fixo_rede * PWA)

    LCC = NPC_PV + NPC_GE - NPC_REDE_COMPRA - NPC_REDE_VENDA + NPC_REDE_PERDAS

    # restrições
    c0 = []
    c = []
    SOC_erro = 0
    #c0.append(LPSP != 0)
    if compra_total_vida_util/1000000 > rede_disponivel:
        c.append(1)
    if venda_total_vida_util/1000000 > 0.3 * sum(f.demanda):
        c.append(1)

    #for i in range(len(SOC)):
    #   if SOC[i] > SOC_max or SOC[i] < SOC_min:
    #        SOC_erro = SOC_erro + 1
    #c0.append(SOC_erro)
    #for i in range(len(c0)):
    #    if c0[i] > 0:
    #        c.append(1)
    #    else:
    #        c.append(0)
    penalidade = 100000000000
    # func = NPC+penalidade*sum(c)
    #print("passei aqui")
    return LCC + penalidade * sum(c)


def fitness2(x):
    f = default.copy()
    f.demanda = f.demanda * 15
    pot_nominal = (x[0]*250 + x[1]*2400)/1000000 # manda a potência nominal em MW
    perdas_ativas = perdas(pot_nominal)
    print("A potêcia nominal é de", pot_nominal, "MW", "As perdas são de", perdas_ativas, "MW")
    if perdas_ativas >= 0.202:
        return 100000000000
    vida_util = 20
    # Defiições do painel fotovoltaico utilizado
    n_PV = 0.173
    n_conv = 0.9
    custo_PV = 1183.94
    custo_OM_fixo_PV = custo_PV * 0.01
    RC_PV = 0
    vida_util_PV = 20
    area_painel = 1.66
    numero_paineis = x[0]

    # Definições para ajuste  de velocidade do vento
    H0 = 2
    H = 15
    Fator_rugosidade = 0.23
    vento_corrigido = f.vento * (H / H0) ** Fator_rugosidade

    # Definições do aerogerador utilizado
    Pot_max_GE = 2400
    Vc = 3.5
    Vf = 25
    Vr = 9.5
    custo_GE = 12394.36
    custo_OM_fixo_GE = custo_GE * 0.03
    RC_GE = 0
    vida_util_GE = 25
    salvage_GE = 772.92
    numero_aerogeradores = x[1]


    # Definições rede elétrica
    #rede_disponivel = x[2]
    custo_REDE = 0.713370  # kWh
    custo_rede = custo_REDE / 1000  # kW
    custo_OM_fixo_rede = 0
    vida_util_rede = 1
    compra_total_vida_util = 0
    venda_total_vida_util = 0
    RC_rede = custo_rede
    tempo_avaliacao = 8760

    # Geração fotovoltaica
    Pot_PV = f.radiacao * n_PV * n_conv * area_painel * numero_paineis

    # Para LPSP
    LPS = 0

    # Geração eólica
    Pot_GE = np.zeros(len(vento_corrigido))
    index = set(f.index[vento_corrigido >= Vc].tolist()) & set(f.index[vento_corrigido <= Vr].tolist())
    Pot_GE[list(index)] = Pot_max_GE * ((vento_corrigido[list(index)] - Vc) / (Vr - Vc)) * numero_aerogeradores
    index = set(f.index[vento_corrigido >= Vr].tolist()) & set(f.index[vento_corrigido <= Vf].tolist())
    Pot_GE[list(index)] = Pot_max_GE * numero_aerogeradores

    perdas_energia = 0
    # estado de carga
    balanco = Pot_GE + Pot_PV - f.demanda / n_conv
    #print(balanco)
    venda_total_vida_util = sum(balanco[balanco>0])
    compra_total_vida_util = sum(balanco[balanco<0])
    print("a venda total foi de", venda_total_vida_util, "A compra total na vida util foi", compra_total_vida_util, "a soma da demanda é", sum(f.demanda))

    perdas_energia = sum(perdas_multiplas((balanco)/1000000))
    perdas_totais = perdas_energia - 0.202 * tempo_avaliacao
    print("As perdas de energia são de", perdas_energia, "MWh", "As perdas totais são de ", perdas_totais, "MWh")

    # calculo dos indicadores
    ir = 0.06
    K_PV = 0
    K_GE = 0
    K_rede = 0

    for i in range(vida_util):
        K_rede = K_rede + 1 / (1 + ir) ** (i * vida_util_rede)
    PWA = (((1 + ir) ** vida_util) - 1) / (ir * (1 + ir) ** vida_util)

    NPC_PV = numero_paineis * (custo_PV + RC_PV * K_PV + custo_OM_fixo_PV * PWA)
    NPC_GE = numero_aerogeradores * (custo_GE + RC_GE * K_GE + custo_OM_fixo_GE * PWA - salvage_GE)
    NPC_REDE_COMPRA = compra_total_vida_util  * (custo_rede + RC_rede * K_rede + custo_OM_fixo_rede * PWA)
    NPC_REDE_VENDA = venda_total_vida_util  * (custo_rede + RC_rede * K_rede + custo_OM_fixo_rede * PWA)
    NPC_REDE_PERDAS = perdas_totais * 1000000  * (custo_rede + RC_rede * K_rede + custo_OM_fixo_rede * PWA)
    print("Os NPC são", NPC_PV, NPC_GE, NPC_REDE_COMPRA, NPC_REDE_VENDA, NPC_REDE_PERDAS)
    LCC = NPC_PV + NPC_GE - NPC_REDE_COMPRA - NPC_REDE_VENDA + NPC_REDE_PERDAS

    # restrições

    c = 0
    SOC_erro = 0
    #c0.append(LPSP != 0)
    #if - compra_total_vida_util/1000000 > rede_disponivel:
    #    c = c + 1
    if venda_total_vida_util > 0.3 * sum(f.demanda):
        c = c + 1
    if abs(venda_total_vida_util + compra_total_vida_util) > 0.1 * sum(f.demanda):
        c = c + 1


    #for i in range(len(SOC)):
    #   if SOC[i] > SOC_max or SOC[i] < SOC_min:
    #        SOC_erro = SOC_erro + 1
    #c0.append(SOC_erro)
    #for i in range(len(c0)):
    #    if c0[i] > 0:
    #        c.append(1)
    #    else:
    #        c.append(0)
    penalidade = 100000000000
    # func = NPC+penalidade*sum(c)
    #print("passei aqui")
    return LCC + penalidade * c