import pandas as pd

from src.regras.cfop import eh_venda
from src.regras.validacoes import nota_valida


def filtrar_notas(df):
    df = df.copy()

    # --- PADRONIZAÇÃO ---
    df["CFOP"] = df["CFOP"].fillna("").astype(str)
    df["Status"] = df["Status"].fillna("").astype(str)
    df["Tipo"] = df["Tipo"].fillna("SERVICO").astype(str)

    # --- COMÉRCIO ---
    df_comercio = df[df["Tipo"] == "COMERCIO"].copy()

    filtro_cfop = df_comercio["CFOP"].apply(eh_venda).astype(bool)
    filtro_status = df_comercio["Status"].apply(nota_valida).astype(bool)

    df_comercio = df_comercio[filtro_cfop & filtro_status]

    # --- SERVIÇO ---
    df_servico = df[df["Tipo"] == "SERVICO"].copy()

    # --- JUNTA FINAL ---
    df_final = pd.concat([df_servico, df_comercio], ignore_index=True)

    return df_final

def padronizar_competencia(comp):
    if pd.isna(comp):
        return None

    comp = str(comp)

    # caso venha 2026/02
    if len(comp) == 7 and comp[0:4].isdigit():
        ano, mes = comp.split("/")
        return f"{mes}/{ano}"

    return comp

def gerar_relatorio_anual(df):
    df["Competencia"] = df["Competencia"].apply(padronizar_competencia)
    df = df.copy()

    # --- PADRONIZA DADOS ---
    df["CNPJ"] = df["CNPJ"].astype(str).str.replace(r"\D", "", regex=True)

    df["Empresa"] = (
        df["Empresa"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # --- EXTRAI ANO ---
    df["Ano"] = df["Competencia"].str.extract(r"(\d{4})")
    # --- AGRUPAMENTO POR TIPO ---
    relatorio = df.groupby(
        ["CNPJ", "Ano", "Tipo"],
        as_index=False
    ).agg({
        "Empresa": "first",
        "Valor": "sum",
        "PIS": "sum",
        "COFINS": "sum",
        "IRPJ": "sum",
        "CSLL": "sum"
    })

    # --- TOTAL CONSOLIDADO ---
    total = df.groupby(
        ["CNPJ", "Ano"],
        as_index=False
    ).agg({
        "Empresa": "first",
        "Valor": "sum",
        "PIS": "sum",
        "COFINS": "sum",
        "IRPJ": "sum",
        "CSLL": "sum"
    })

    total["Tipo"] = "TOTAL"

    # --- JUNTA TUDO ---
    relatorio_final = pd.concat([relatorio, total], ignore_index=True)

    # --- ORDENAÇÃO ---
    ordem = {"SERVICO": 1, "COMERCIO": 2, "TOTAL": 3}
    relatorio_final["Ordem"] = relatorio_final["Tipo"].map(ordem)

    relatorio_final = relatorio_final.sort_values(
        by=["CNPJ", "Ano", "Ordem"]
    ).drop(columns="Ordem")

    return relatorio_final

