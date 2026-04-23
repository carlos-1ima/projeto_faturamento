import xml.etree.ElementTree as ET


def get_text(root, tag):
    for elem in root.iter():
        if tag in elem.tag:
            return elem.text
    return None


def ler_nfe_xml(caminho):
    try:
        tree = ET.parse(caminho)
        root = tree.getroot()

        # CAMPOS PRINCIPAIS
        cstat = get_text(root, "cStat")
        cfop = get_text(root, "CFOP")
        valor = get_text(root, "vNF")
        data = get_text(root, "dhEmi")
        cnpj = get_text(root, "CNPJ")
        empresa = get_text(root, "xNome")

        # TRATAMENTOS
        valor = float(valor) if valor else 0.0

        if data:
            competencia = data[:7].replace("-", "/")
        else:
            competencia = ""

        # DEBUG (pode remover depois)
        print("NFE LIDA:")
        print({
            "CNPJ": cnpj,
            "Empresa": empresa,
            "Competencia": competencia,
            "Valor": valor,
            "CFOP": cfop,
            "Status": cstat
        })

        return {
            "CNPJ": cnpj,
            "Empresa": empresa,
            "Competencia": competencia,
            "Valor": valor,
            "CFOP": cfop,
            "Status": cstat,
            "Tipo": "COMERCIO"
        }

    except Exception as e:
        print(f"Erro NFe XML: {caminho} -> {e}")
        return None