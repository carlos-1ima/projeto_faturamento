import pandas as pd
import os

pasta = "entrada"
df_total = pd.DataFrame()

def processar_linha(linha):
    partes = linha.split(";")
    
    try:
        competencia = partes[2]
        situacao = partes[4].strip().upper()
        valor = partes[12]
        
        if situacao != "NORMAL":
            return None
        
        valor = valor.replace(".", "").replace(",", ".")
        valor = float(valor)
        
        return {
            "Competencia": competencia,
            "Valor": valor
        }
    except:
        return None

for arquivo in os.listdir(pasta):
    if arquivo.endswith(".csv"):
        caminho = os.path.join(pasta, arquivo)
        
        print(f"\n📂 Processando: {arquivo}")
        
        with open(caminho, encoding="latin1") as f:
            linhas = f.readlines()
        
        # Ignorar cabeçalho
        dados = linhas[1:]
        
        registros = []
        
        for linha in dados:
            resultado = processar_linha(linha)
            if resultado:
                registros.append(resultado)
        
        df = pd.DataFrame(registros)
        
        print("Linhas processadas:", len(df))
        print(df)
        
        df_total = pd.concat([df_total, df], ignore_index=True)

# Resultado final
faturamento_mes = df_total.groupby("Competencia")["Valor"].sum()

print("\n📊 Faturamento por mês:\n")

for mes, valor in faturamento_mes.items():
    valor_formatado = "R$ {:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    print(f"{mes}: {valor_formatado}")