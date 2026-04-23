import pandas as pd


def ler_recife_csv(caminho):
    df_total = pd.DataFrame()

    try:
        df = pd.read_csv(caminho, sep=";", encoding="latin1")

        # normalizar nomes das colunas
        df.columns = [col.strip() for col in df.columns]

        # garantir tipo correto
        df["Tipo de Registro"] = df["Tipo de Registro"].astype(str)

        # filtrar registros válidos
        df = df[df["Tipo de Registro"] == "2"]

        for _, row in df.iterrows():
            try:
                valor = str(row["Valor dos Serviços"])
                valor = float(valor.replace(".", "").replace(",", "."))

                data = str(row["Data NFE"])
                competencia = data[3:10]  # MM/AAAA

                cnpj = row.get("CPF/CNPJ do Prestador", "")
                empresa = row.get("Razão Social do Prestador", "")

                df_total = pd.concat([
                    df_total,
                    pd.DataFrame([{
                        "CNPJ": cnpj,
                        "Empresa": empresa,
                        "Competencia": competencia,
                        "Valor": valor
                    }])
                ], ignore_index=True)

            except:
                continue

    except Exception as e:
        print(f"Erro Recife CSV: {caminho} -> {e}")

    return df_total