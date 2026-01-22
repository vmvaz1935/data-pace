# Dashboard Streamlit - Atendimentos por Diagnóstico

Dashboard interativo para análise de atendimentos atribuídos ao diagnóstico vigente.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Arquivos de dados processados (ver seção "Estrutura de Arquivos")

## 🚀 Instalação e Execução

### 1. Criar ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 2. Ativar ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o dashboard

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no navegador em `http://localhost:8501`

## 📁 Estrutura de Arquivos Esperados

O dashboard espera encontrar os seguintes arquivos no mesmo diretório:

### Arquivo Principal (preferencial):
- `atendimentos_por_diagnostico.xlsx` com as seguintes abas:
  - `Atendimentos_Com_Diagnostico` (obrigatória)
  - `Resumo_Diagnostico` (opcional)
  - `Resumo_Diag_Unidade` (opcional)
  - `Resumo_Diag_Profissional` (opcional)
  - `QA` (opcional)

### Arquivos de Fallback:
- `Atendimentos_Com_Diagnostico.csv` (se o Excel não estiver disponível)
- `Resumos.xlsx` (opcional, para resumos consolidados)

## 🎯 Funcionalidades

### Dashboard Principal

- **KPIs**: Total de atendimentos, pacientes únicos, diagnósticos distintos, % sem diagnóstico
- **Filtros Interativos**:
  - Intervalo de datas
  - Diagnóstico (multi-select)
  - Unidade (multi-select)
  - Profissional do atendimento (multi-select)
  - Busca por paciente (ID)
- **Visualizações**:
  - Série temporal mensal (com opção de segmentar por diagnóstico)
  - Top diagnósticos (gráfico de barras)
  - Heatmap: Diagnóstico × Unidade
  - Tabela: Diagnóstico × Profissional (top N)
  - Tabela detalhada dos atendimentos filtrados
- **Exportação**:
  - Download dos atendimentos filtrados em CSV
  - Download do resumo do recorte em Excel

### Página QA

- Relatório de qualidade e consistência
- Análise de duplicatas
- Verificação de dados faltantes
- Documentação das regras de negócio aplicadas

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Framework para criação do dashboard
- **Pandas**: Manipulação de dados
- **Plotly**: Gráficos interativos
- **OpenPyXL**: Leitura de arquivos Excel

## 📊 Estrutura de Dados

### Colunas Esperadas em `Atendimentos_Com_Diagnostico`:

- `atendimento_id`: ID único do atendimento
- `paciente_id`: ID do paciente
- `data_atendimento`: Data do atendimento (datetime)
- `profissional_atendimento`: Nome do profissional
- `unidade`: Unidade de atendimento
- `diagnostico_vigente`: Diagnóstico vigente na data do atendimento
- `data_avaliacao_origem`: Data da avaliação que originou o diagnóstico
- `profissional_avaliacao_origem`: Profissional que fez a avaliação

## ⚠️ Notas Importantes

- O dashboard usa cache (`st.cache_data`) para melhor performance
- Atendimentos com `diagnostico_vigente == "SEM DIAGNÓSTICO"` são tratados como categoria especial
- Os filtros são aplicados em cascata (todos os filtros ativos simultaneamente)
- O dashboard faz fallback automático para CSV se o Excel não estiver disponível

## 🐛 Solução de Problemas

### Erro ao carregar Excel
- Verifique se o arquivo `atendimentos_por_diagnostico.xlsx` existe no diretório
- Verifique se a aba `Atendimentos_Com_Diagnostico` existe no arquivo
- O dashboard tentará fazer fallback para CSV automaticamente

### Performance lenta
- O dashboard usa cache, mas com datasets muito grandes (>100k linhas) pode ser lento
- Considere filtrar os dados antes de carregar

### Gráficos não aparecem
- Verifique se o Plotly está instalado: `pip install plotly`
- Verifique o console do navegador para erros JavaScript

## ☁️ Deploy no Streamlit Cloud

### Pré-requisitos
1. Conta no [Streamlit Cloud](https://streamlit.io/cloud)
2. Repositório no GitHub com o código

### Passos para Deploy

1. **Fazer commit e push para o GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Dashboard de Atendimentos por Diagnóstico"
   git branch -M main
   git remote add origin <seu-repositorio-github>
   git push -u origin main
   ```

2. **Conectar no Streamlit Cloud:**
   - Acesse [share.streamlit.io](https://share.streamlit.io)
   - Faça login com sua conta GitHub
   - Clique em "New app"
   - Selecione seu repositório
   - Selecione o branch (geralmente `main`)
   - Defina o arquivo principal: `app.py`
   - Clique em "Deploy"

3. **Arquivos necessários no repositório:**
   - ✅ `app.py` (arquivo principal)
   - ✅ `requirements.txt` (dependências)
   - ✅ `atendimentos_por_diagnostico.xlsx` (dados principais)
   - ✅ `Atendimentos_Com_Diagnostico.csv` (fallback)
   - ✅ `Resumos.xlsx` (opcional)
   - ✅ `.streamlit/config.toml` (configuração do tema)

### Estrutura do Repositório para Deploy

```
seu-repositorio/
├── app.py                          # Arquivo principal
├── requirements.txt                 # Dependências Python
├── README.md                        # Documentação
├── .gitignore                      # Arquivos a ignorar
├── .streamlit/
│   └── config.toml                 # Configuração do tema
├── atendimentos_por_diagnostico.xlsx  # Dados principais
├── Atendimentos_Com_Diagnostico.csv   # Fallback CSV
└── Resumos.xlsx                     # Resumos (opcional)
```

### Notas para Deploy

- ⚠️ **Arquivos de dados**: Os arquivos Excel/CSV devem estar no repositório ou em um storage externo (S3, Google Drive, etc.)
- 📦 **Tamanho do repositório**: Streamlit Cloud tem limite de 1GB. Se os dados forem muito grandes, considere usar storage externo
- 🔄 **Atualização de dados**: Para atualizar os dados, faça commit dos novos arquivos e o Streamlit Cloud recarregará automaticamente
- ⚡ **Performance**: O cache do Streamlit ajuda, mas datasets muito grandes podem ser lentos no cloud

### Alternativa: Dados Externos

Se os arquivos forem muito grandes, você pode:
1. Usar Google Sheets (com `gspread`)
2. Usar AWS S3 (com `boto3`)
3. Usar banco de dados (PostgreSQL, MySQL, etc.)

## 📝 Licença

Este projeto é para uso interno.
