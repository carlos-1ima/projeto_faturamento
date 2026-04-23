import pandas as pd
import os


def padronizar_competencia(comp):
    if pd.isna(comp):
        return None

    comp = str(comp)

    # caso venha 2026/02 → vira 02/2026
    if len(comp) == 7 and comp[:4].isdigit():
        ano, mes = comp.split("/")
        return f"{mes}/{ano}"

    return comp


def gerar_excel(faturamento, relatorio_anual, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    # evita erro se arquivo estiver aberto
    if os.path.exists(caminho_saida):
        try:
            os.remove(caminho_saida)
        except PermissionError:
            print("Feche o arquivo Excel antes de rodar.")
            return

    # =========================
    # PADRONIZAÇÃO GERAL
    # =========================
    faturamento = faturamento.copy()

    faturamento["Competencia"] = faturamento["Competencia"].apply(padronizar_competencia)

    faturamento["CNPJ"] = (
        faturamento["CNPJ"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )

    faturamento["Empresa"] = (
        faturamento["Empresa"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # =========================
    # CONSOLIDA MENSAL (SOMA SERVIÇO + COMÉRCIO)
    # =========================
    faturamento_mensal = faturamento.groupby(
        ["CNPJ", "Competencia"],
        as_index=False
    ).agg({
        "Empresa": "first",
        "Valor": "sum",
        "PIS": "sum",
        "COFINS": "sum",
        "IRPJ": "sum",
        "CSLL": "sum"
    })

    with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:

        # =========================
        # ABAS MENSAIS
        # =========================
        competencias = sorted(faturamento_mensal["Competencia"].dropna().unique())

        for comp in competencias:
            df_mes = faturamento_mensal[
                faturamento_mensal["Competencia"] == comp
            ]

            nome_aba = comp.replace("/", "-")

            df_mes.to_excel(
                writer,
                sheet_name=nome_aba,
                index=False,
                startrow=2
            )

            ws = writer.book[nome_aba]

            # título
            ws["A1"] = "Relatório de Faturamento"
            ws["A2"] = f"Competência: {comp}"

            # filtro
            ws.auto_filter.ref = ws.dimensions

        # =========================
        # ABA ANUAL
        # =========================
        relatorio_anual.to_excel(
            writer,
            sheet_name="ANUAL",
            index=False,
            startrow=2
        )

        ws = writer.book["ANUAL"]
        ws["A1"] = "Relatório Anual de Faturamento"
        ws["A2"] = "Separado por Tipo (Serviço / Comércio / Total)"
        ws.auto_filter.ref = ws.dimensions