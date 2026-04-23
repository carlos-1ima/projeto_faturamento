import os
import pandas as pd
import xml.etree.ElementTree as ET

from src.parsers.tinus_csv import ler_tinus_csv
from src.parsers.recife_csv import ler_recife_csv
from src.parsers.nfe_xml import ler_nfe_xml
from src.xml_parser import ler_xml


def detectar_tipo_csv(caminho):
    try:
        with open(caminho, encoding="latin1") as f:
            header = f.readline().lower()

        if "vl. do serv" in header:
            return "tinus"
        elif "valor dos serv" in header:
            return "recife"
        else:
            return "desconhecido"

    except Exception as e:
        print(f"Erro ao detectar tipo CSV: {caminho} -> {e}")
        return "desconhecido"


def processar_csv(caminho):
    tipo = detectar_tipo_csv(caminho)

    if tipo == "tinus":
        return ler_tinus_csv(caminho)

    elif tipo == "recife":
        return ler_recife_csv(caminho)

    else:
        print(f"CSV ignorado (tipo desconhecido): {caminho}")
        return None


def eh_nfe(caminho):
    try:
        tree = ET.parse(caminho)
        root = tree.getroot()

        tag = root.tag.lower()
        children_tags = [child.tag.lower() for child in list(root)]

        if "nfeproc" in tag or "nfe" in tag:
            return True

        if any("nfe" in t for t in children_tags):
            return True

        return False

    except Exception as e:
        print(f"Erro ao identificar tipo XML: {caminho} -> {e}")
        return False


def processar_xml(caminho):
    try:
        if eh_nfe(caminho):
            print(f"Detectado como NFe: {caminho}")

            resultado = ler_nfe_xml(caminho)

            if resultado:
                return pd.DataFrame([resultado])

        else:
            print(f"Detectado como NFS-e: {caminho}")

            dados = ler_xml(caminho)

            if dados:
                return pd.DataFrame(dados)

    except Exception as e:
        print(f"Erro ao processar XML: {caminho} -> {e}")

    return None


def padronizar_colunas(df):
    if "Tipo" not in df.columns:
        df["Tipo"] = "SERVICO"
    else:
        df["Tipo"] = df["Tipo"].fillna("SERVICO")

    if "CFOP" not in df.columns:
        df["CFOP"] = ""

    if "Status" not in df.columns:
        df["Status"] = ""

    return df


def ler_arquivos(pasta):
    df_total = pd.DataFrame()

    for root, dirs, files in os.walk(pasta):
        for arquivo in files:
            caminho = os.path.join(root, arquivo)

            if not os.path.isfile(caminho):
                continue

            print(f"Processando: {caminho}")

            try:
                if arquivo.lower().endswith(".csv"):
                    df = processar_csv(caminho)

                elif arquivo.lower().endswith(".xml"):
                    df = processar_xml(caminho)

                else:
                    continue

                if df is not None and not df.empty:
                    df_total = pd.concat([df_total, df], ignore_index=True)

            except Exception as e:
                print(f"Erro ao processar arquivo: {caminho} -> {e}")

    if df_total.empty:
        return df_total

    df_total = padronizar_colunas(df_total)

    return df_total