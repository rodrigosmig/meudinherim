def getMetaPercent(meta, saldo):
    if(saldo >= meta):
        return 100.00
    elif(saldo <= meta and saldo > 0):
        progresso = (saldo / meta) * 100
        return round(progresso, 2)

    return 0.0

