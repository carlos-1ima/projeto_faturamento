import pandas as pd


def ler_tinus_csv(caminho):
    df_total = pd.DataFrame()

    try:
        try:
            df = pd.read_csv(
                caminho,
                sep=";",
                encoding="latin1"
            )
        except:
            # fallback seguro
            df = pd.read_csv(
                caminho,
                sep=";",
                encoding="latin1",
                engine="python",
                quoting=3,
                on_bad_lines="skip"
            )

        for _, row in df.iterrows():
            try:
                situacao = str(row.get("Situação Nota", "")).upper()
                if situacao != "NORMAL":
                    continue

                valor = str(row.get("Vl. do Serv.", "0"))
                valor = float(valor.replace(".", "").replace(",", "."))

                competencia = row.get("Competencia", "")
                cnpj = row.get("CPF/CNPJ Prestador", "")
                empresa = row.get("Razão Social Prestador", "")

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
        print(f"Erro TINUS CSV: {caminho} -> {e}")

    return df_total