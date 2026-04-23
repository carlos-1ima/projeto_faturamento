import os

from datetime import datetime
from src.leitura import ler_arquivos
from src.processamento import filtrar_notas, gerar_relatorio_anual
from src.impostos import adicionar_impostos
from src.excel import gerar_excel


def main():
    entrada = "entrada"
    saida = "saida"

    os.makedirs(saida, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    arquivo_saida = f"saida/faturamento_{timestamp}.xlsx"

    # 1. leitura
    df = ler_arquivos(entrada)

    if df.empty:
        print("Nenhum dado encontrado.")
        return

    # DEBUG 1 - verificar tipos carregados
    print("\nTipos encontrados:")
    print(df["Tipo"].value_counts())

    print("\nPrévia dos dados:")
    print(df[["CNPJ", "Empresa", "Competencia", "Valor", "Tipo"]].head(10))

    # 2. filtro fiscal
    df = filtrar_notas(df)

    if df.empty:
        print("Nenhuma nota válida após filtros.")
        return

    # DEBUG 2 - após filtro
    print("\nApós filtro:")
    print(df["Tipo"].value_counts())

    # 3. impostos
    faturamento = adicionar_impostos(df)

    # 4. relatório anual
    relatorio_anual = gerar_relatorio_anual(faturamento)

    print("\nRelatório Anual:\n")
    print(relatorio_anual)

    # 5. gerar excel
    try:
        gerar_excel(faturamento, relatorio_anual, arquivo_saida)
        print(f"\nArquivo gerado em: {arquivo_saida}")

    except PermissionError:
        print("Erro: feche o arquivo Excel antes de rodar novamente.")


if __name__ == "__main__":
    main()