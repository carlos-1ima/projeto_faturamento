📊 Sistema de Consolidação de Faturamento

Este projeto tem como objetivo processar e consolidar dados de faturamento de empresas, integrando informações provenientes de **Notas Fiscais de Serviço (NFS-e)** e **Notas Fiscais de Produto (NFe)**.

O sistema realiza a leitura de múltiplos formatos de arquivos, aplica regras fiscais e gera relatórios automatizados em Excel.

---

## ⚙️ Como executar o projeto

1. Clone o repositório
2. Crie as seguintes pastas na raiz do projeto:
   - 'entrada'
   - 'saida'
3. Adicione os arquivos XML (NFe/NFS-e) ou CSV na pasta 'entrada'
4. Execute o script principal
5. O relatório será gerado na pasta 'saida'

## 🚀 Funcionalidades

- 📥 Importação de arquivos:
  - CSV (múltiplos formatos)
  - XML de NFS-e (serviços)
  - XML de NFe (comércio)

- 🔍 Processamento de dados:
  - Padronização de CNPJ e competência
  - Identificação de tipo de receita (SERVIÇO / COMÉRCIO)
  - Filtro de notas por CFOP de venda
  - Validação de status da nota

- 📊 Consolidação:
  - Receita mensal consolidada (serviço + comércio)
  - Relatório anual por tipo:
    - SERVIÇO
    - COMÉRCIO
    - TOTAL

- 📄 Geração de Excel:
  - Uma aba por competência (mensal)
  - Aba anual consolidada
  - Filtros automáticos
  - Layout organizado
  - Nome do arquivo com timestamp

---

## 🧠 Regras de Negócio

- Apenas notas de comércio com **CFOP de venda** são consideradas
- Notas inválidas são descartadas
- Receita mensal é sempre consolidada (independente do tipo)
- Relatório anual mantém separação por tipo

---
