import xml.etree.ElementTree as ET


def detectar_tipo_xml(root):
    xml_str = ET.tostring(root, encoding="unicode").lower()

    if "abrasf" in xml_str or "nfse" in xml_str:
        return "nacional"
    else:
        return "municipal"


# XML Nacional
def parse_xml_nacional(root):
    dados = []

    for inf in root.iter():
        tag = str(inf.tag).lower()

        if "infnfse" in tag:
            try:
                valor = None
                data = None
                cnpj = None
                empresa = None

                for elem in inf.iter():
                    tag_elem = str(elem.tag).lower()

                    if "valorservicos" in tag_elem:
                        valor = float(elem.text)

                    elif "dataemissao" in tag_elem:
                        data = elem.text[:7].replace("-", "/")

                    elif "cnpj" in tag_elem and cnpj is None:
                        cnpj = elem.text

                    elif "razaosocial" in tag_elem and empresa is None:
                        empresa = elem.text

                if valor and data:
                    dados.append({
                        "CNPJ": cnpj,
                        "Empresa": empresa,
                        "Competencia": data,
                        "Valor": valor
                    })

            except:
                continue

    return dados


# XML Municipal
def parse_xml_municipal(root):
    dados = []

    for elem in root.iter():
        tag = str(elem.tag).lower()

        if "valor" in tag:
            try:
                valor = float(elem.text)
                dados.append({
                    "CNPJ": None,
                    "Empresa": "NÃO IDENTIFICADA",
                    "Competencia": "00/0000",
                    "Valor": valor
                })
            except:
                continue

    return dados


# Função principal para ler XML
def ler_xml(caminho):
    try:
        tree = ET.parse(caminho)
        root = tree.getroot()

        tipo = detectar_tipo_xml(root)

        if tipo == "nacional":
            return parse_xml_nacional(root)
        else:
            return parse_xml_municipal(root)

    except Exception as e:
        print(f"Erro ao ler XML {caminho}: {e}")
        return []