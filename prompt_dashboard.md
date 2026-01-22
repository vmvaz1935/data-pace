## PROMPT — Dashboard Streamlit (Atendimentos × Diagnóstico)

Você é um(a) **Engenheiro(a) de Dados / Analytics Engineer sênior** com foco em **qualidade**, **rastreabilidade** e **UX**. Gere um app **Streamlit** completo e funcional. **Não invente dados**: use apenas os arquivos fornecidos. Se algo estiver faltando, explique e implemente fallback/validação.

### Contexto e arquivos de entrada

Os dados já foram processados e geraram:

- `atendimentos_por_diagnostico.xlsx` com abas:
  - `Base_Avaliacoes_Limpa`
  - `Base_Atendimentos_Limpa`
  - `Vigencia_Diagnosticos`
  - `Atendimentos_Com_Diagnostico`
  - `Resumo_Diagnostico`
  - `Resumo_Diag_Profissional`
  - `Resumo_Diag_Unidade`
  - `Resumo_Diag_Unidade_Prof`
  - `QA`
- `Atendimentos_Com_Diagnostico.csv` (a base principal em CSV)
- `Resumos.xlsx` (resumos consolidados)

Colunas esperadas na aba/base principal `Atendimentos_Com_Diagnostico`:
`atendimento_id | paciente_id | data_atendimento | profissional_atendimento | unidade | diagnostico_vigente | data_avaliacao_origem | profissional_avaliacao_origem`

### Objetivo do dashboard

Criar um dashboard para análise de atendimentos atribuídos ao **diagnóstico vigente**, com filtros, KPIs, gráficos e uma seção explícita de **QA**.

### Requisitos obrigatórios (funcionais)

1. **Carregamento de dados**
   - Ler preferencialmente `atendimentos_por_diagnostico.xlsx` (abas necessárias).
   - Se falhar (arquivo ausente, engine, etc.), fazer fallback para `Atendimentos_Com_Diagnostico.csv` + `Resumos.xlsx` quando possível.
   - Converter datas (`data_atendimento`, `data_avaliacao_origem`) para `datetime`.
   - Tratar `diagnostico_vigente == "SEM DIAGNÓSTICO"` como categoria especial (não sumir “silenciosamente”).

2. **Filtros globais (sidebar)**
   - Intervalo de datas (min/max de `data_atendimento`)
   - Diagnóstico (multi-select, com opção de incluir/excluir “SEM DIAGNÓSTICO”)
   - Unidade (multi-select)
   - Profissional do atendimento (multi-select)
   - Campo de busca por `paciente_id` (texto, filtra contains/igual com toggle)
   - Botão “Reset filtros”

3. **KPIs (topo)**
   - Total de atendimentos (filtrados)
   - Nº de pacientes únicos (filtrados)
   - Nº de diagnósticos distintos (filtrados, incluindo/excluindo “SEM DIAGNÓSTICO” conforme seleção)
   - % atendimentos “SEM DIAGNÓSTICO” (no recorte atual)

4. **Visualizações**
   - Série temporal (mensal) de atendimentos (linha/área), com opção de segmentar por diagnóstico (stacked) quando poucos diagnósticos selecionados.
   - Top diagnósticos (barra horizontal).
   - Diagnóstico × Unidade (heatmap ou tabela pivot com formatação).
   - Diagnóstico × Profissional (top N com controle N).
   - Tabela detalhada dos atendimentos filtrados com paginação (ou `st.dataframe` com height fixo) e ordenação por data desc.

5. **Seção QA (aba/página específica)**
   - Exibir a aba `QA` do Excel (ou, se não existir, computar mínimos: quantidade de “SEM DIAGNÓSTICO”, duplicatas por chave, datas mín/max).
   - Mostrar também: contagem de duplicatas na base filtrada por chave (`paciente_id + data_atendimento + profissional_atendimento + unidade`).
   - Explicar em texto curto as regras de negócio (vigência: `inicio <= atendimento < fim`, e mesmo dia entra no diagnóstico novo).

6. **Exportação/Downloads**
   - Download dos **atendimentos filtrados** em CSV (UTF-8-SIG).
   - Download de um “Resumo do recorte” (por diagnóstico, por unidade, por profissional) em Excel ou CSVs múltiplos.

### Requisitos não-funcionais (qualidade)

- Usar `st.cache_data` para cache de leitura e de agregações.
- Código organizado em funções: `load_data()`, `apply_filters()`, `make_charts()`, etc.
- Tratar erros com mensagens claras (ex.: engine do Excel, arquivo não encontrado).
- Não travar em datasets grandes: evitar loops linha-a-linha; usar `groupby`.
- Interface limpa: usar `st.tabs()` ou `st.page_link`/multipage (se preferir, gere `app.py` + `pages/`).

### Entregáveis (o que você deve gerar)

1. Um arquivo **`app.py`** Streamlit pronto para rodar.
2. Um **`requirements.txt`** mínimo (ex.: `streamlit`, `pandas`, `openpyxl`, `plotly`).
3. Um **README** curto com:
   - Como instalar e rodar (`python -m venv`, `pip install -r requirements.txt`, `streamlit run app.py`)
   - Estrutura dos arquivos esperados.

### Preferências de implementação

- Gráficos com **Plotly** (interativos).
- Layout com `st.set_page_config(page_title=..., layout="wide")`.
- Use cores consistentes e destaque “SEM DIAGNÓSTICO”.

### Importante

- Não assuma colunas que não existem.
- Sempre que excluir “SEM DIAGNÓSTICO” de um gráfico/resumo, deixe isso explícito no subtítulo/legenda.

