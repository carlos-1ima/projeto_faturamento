def adicionar_impostos(faturamento):
    # limpeza de dados inválidos
    faturamento = faturamento[faturamento["Competencia"].notna()]
    faturamento = faturamento[faturamento["Competencia"] != ""]
    
    faturamento["PIS"] = faturamento["Valor"] * 0.0065
    faturamento["COFINS"] = faturamento["Valor"] * 0.03

    def get_trimestre(mes):
        try:
            if not mes or "/" not in mes:
                return None

            mes_num = int(mes.split("/")[0])

            if mes_num <= 3:
                return "1T"
            elif mes_num <= 6:
                return "2T"
            elif mes_num <= 9:
                return "3T"
            else:
                return "4T"
        except:
            return None

    faturamento["Trimestre"] = faturamento["Competencia"].apply(get_trimestre)

    faturamento["Total_Trimestre"] = (
        faturamento
        .groupby(["CNPJ", "Trimestre"])["Valor"]
        .transform("sum")
        .round(2)
    )

    faturamento["IRPJ"] = 0.0
    faturamento["CSLL"] = 0.0

    for (cnpj, trimestre), grupo in faturamento.groupby(["CNPJ", "Trimestre"]):
        
        faturamento_trimestre = grupo["Valor"].sum()
        
        base_irpj = faturamento_trimestre * 0.16
        base_csll = faturamento_trimestre * 0.32
        
        irpj = base_irpj * 0.15
        csll = base_csll * 0.09
        
        if base_irpj > 60000:
            adicional = (base_irpj - 60000) * 0.10
            irpj += adicional
        
        idx = grupo.index[-1]
        
        faturamento.loc[idx, "IRPJ"] = irpj
        faturamento.loc[idx, "CSLL"] = csll

    return faturamento