import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PALETA DE CORES - TEMA CLÍNICO CLEAN
# ============================================================================
COLORS = {
    # Brand (Teal)
    'primary': '#00A9A1',
    'primary_hover': '#007671',
    'primary_darker': '#005D59',
    'primary_tint': '#E6F6F6',
    'primary_tint2': '#CCEEEC',
    'primary_tint3': '#A6E1DE',
    
    # Neutros
    'background': '#F7FAFA',
    'surface': '#FFFFFF',
    'border': '#E5E7EB',
    'text_primary': '#0F172A',
    'text_secondary': '#475569',
    'disabled': '#94A3B8',
    
    # Acentos
    'accent_warm': '#F59E0B',
    'accent_cool': '#3B82F6',
    
    # Status
    'success': '#16A34A',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'info': '#3B82F6',
}

# Paleta categórica para gráficos
COLOR_PALETTE = [
    "#00A9A1",  # Primary teal
    "#0F172A",  # Text primary
    "#3B82F6",  # Accent cool
    "#F59E0B",  # Accent warm
    "#16A34A",  # Success
    "#8B5CF6",  # Purple
    "#EF4444",  # Error
    "#475569",  # Text secondary
]

# Template Plotly com tema customizado
PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': COLORS['surface'],
        'plot_bgcolor': COLORS['surface'],
        'font': {
            'color': COLORS['text_primary'],
            'family': 'sans serif'
        },
        'colorway': COLOR_PALETTE,
    }
}

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Dashboard - Atendimentos por Diagnóstico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para aplicar o tema
st.markdown(f"""
<style>
    /* Aplicar cores de fundo */
    .stApp {{
        background-color: {COLORS['background']};
    }}
    
    /* Cards e containers */
    .stMetric {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 1rem;
    }}
    
    /* Headers com tint do teal */
    h1, h2, h3 {{
        color: {COLORS['text_primary']};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['surface']};
    }}
    
    /* Botões primários */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 6px;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['primary_hover']};
    }}
    
    /* Caixas informativas com tint */
    .info-box {{
        background-color: {COLORS['primary_tint']};
        border-left: 4px solid {COLORS['primary']};
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES DE CARREGAMENTO DE DADOS (COM CACHE)
# ============================================================================

@st.cache_data
def load_data():
    """
    Carrega os dados do arquivo Excel ou faz fallback para CSV.
    Retorna um dicionário com os dataframes necessários.
    """
    data = {}
    
    # Tentar carregar do Excel primeiro
    try:
        excel_file = pd.ExcelFile('atendimentos_por_diagnostico.xlsx')
        
        # Carregar aba principal
        data['atendimentos'] = pd.read_excel(excel_file, sheet_name='Atendimentos_Com_Diagnostico')
        data['atendimentos']['data_atendimento'] = pd.to_datetime(data['atendimentos']['data_atendimento'])
        if 'data_avaliacao_origem' in data['atendimentos'].columns:
            data['atendimentos']['data_avaliacao_origem'] = pd.to_datetime(
                data['atendimentos']['data_avaliacao_origem'], errors='coerce'
            )
        
        # Carregar avaliações
        try:
            data['avaliacoes'] = pd.read_excel(excel_file, sheet_name='Base_Avaliacoes_Limpa')
            data['avaliacoes']['data_avaliacao'] = pd.to_datetime(data['avaliacoes']['data_avaliacao'], errors='coerce')
        except:
            data['avaliacoes'] = None
        
        # Carregar resumos
        try:
            data['resumo_diag'] = pd.read_excel(excel_file, sheet_name='Resumo_Diagnostico')
        except:
            data['resumo_diag'] = None
            
        try:
            data['resumo_diag_unidade'] = pd.read_excel(excel_file, sheet_name='Resumo_Diag_Unidade')
        except:
            data['resumo_diag_unidade'] = None
            
        try:
            data['resumo_diag_prof'] = pd.read_excel(excel_file, sheet_name='Resumo_Diag_Profissional')
        except:
            data['resumo_diag_prof'] = None
            
        try:
            data['qa'] = pd.read_excel(excel_file, sheet_name='QA')
        except:
            data['qa'] = None
            
        st.success("✅ Dados carregados do arquivo Excel")
        return data
        
    except FileNotFoundError:
        st.warning("⚠️ Arquivo Excel não encontrado. Tentando fallback para CSV...")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar Excel: {str(e)}. Tentando fallback para CSV...")
    
    # Fallback: carregar CSV
    try:
        data['atendimentos'] = pd.read_csv('Atendimentos_Com_Diagnostico.csv', encoding='utf-8-sig')
        data['atendimentos']['data_atendimento'] = pd.to_datetime(data['atendimentos']['data_atendimento'])
        if 'data_avaliacao_origem' in data['atendimentos'].columns:
            data['atendimentos']['data_avaliacao_origem'] = pd.to_datetime(
                data['atendimentos']['data_avaliacao_origem'], errors='coerce'
            )
        
        # Tentar carregar resumos do Resumos.xlsx
        try:
            resumos_excel = pd.ExcelFile('Resumos.xlsx')
            data['resumo_diag'] = pd.read_excel(resumos_excel, sheet_name='Por_Diagnostico')
            data['resumo_diag_unidade'] = pd.read_excel(resumos_excel, sheet_name='Por_Diagnostico_Unidade')
            data['resumo_diag_prof'] = pd.read_excel(resumos_excel, sheet_name='Por_Diagnostico_Profissional')
        except:
            data['resumo_diag'] = None
            data['resumo_diag_unidade'] = None
            data['resumo_diag_prof'] = None
        
        data['qa'] = None
        st.success("✅ Dados carregados do arquivo CSV")
        return data
        
    except FileNotFoundError:
        st.error("❌ Arquivo CSV também não encontrado. Verifique se os arquivos estão no diretório correto.")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao carregar CSV: {str(e)}")
        return None

@st.cache_data
def compute_resumos(df):
    """Computa resumos a partir da base filtrada se não existirem."""
    resumos = {}
    
    df_com_diag = df[df['diagnostico_vigente'] != 'SEM DIAGNÓSTICO']
    
    resumos['diag'] = df_com_diag.groupby('diagnostico_vigente').size().reset_index(name='n_atendimentos')
    resumos['diag'] = resumos['diag'].sort_values('n_atendimentos', ascending=False)
    
    resumos['diag_unidade'] = df_com_diag.groupby(['diagnostico_vigente', 'unidade']).size().reset_index(name='n_atendimentos')
    resumos['diag_unidade'] = resumos['diag_unidade'].sort_values(['diagnostico_vigente', 'n_atendimentos'], ascending=[True, False])
    
    resumos['diag_prof'] = df_com_diag.groupby(['diagnostico_vigente', 'profissional_atendimento']).size().reset_index(name='n_atendimentos')
    resumos['diag_prof'] = resumos['diag_prof'].sort_values(['diagnostico_vigente', 'n_atendimentos'], ascending=[True, False])
    
    return resumos

# ============================================================================
# FUNÇÕES DE FILTROS
# ============================================================================

def apply_filters(df, filtros):
    """Aplica os filtros selecionados ao dataframe."""
    df_filtrado = df.copy()
    
    # Filtro de datas
    if filtros['data_min'] and filtros['data_max']:
        # Converter date para datetime (início do dia)
        data_min_dt = pd.Timestamp(filtros['data_min']).normalize()
        # Final do dia (incluir todo o dia final)
        data_max_dt = pd.Timestamp(filtros['data_max']).normalize() + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
        
        df_filtrado = df_filtrado[
            (pd.to_datetime(df_filtrado['data_atendimento']) >= data_min_dt) &
            (pd.to_datetime(df_filtrado['data_atendimento']) <= data_max_dt)
        ]
    
    # Filtro de diagnóstico
    if filtros['diagnosticos'] and len(filtros['diagnosticos']) > 0:
        df_filtrado = df_filtrado[df_filtrado['diagnostico_vigente'].isin(filtros['diagnosticos'])]
    
    # Filtro de unidade
    if filtros['unidades'] and len(filtros['unidades']) > 0:
        df_filtrado = df_filtrado[df_filtrado['unidade'].isin(filtros['unidades'])]
    
    # Filtro de profissional
    if filtros['profissionais'] is not None and len(filtros['profissionais']) > 0:
        df_filtrado = df_filtrado[df_filtrado['profissional_atendimento'].isin(filtros['profissionais'])]
    
    # Filtro de paciente
    if filtros['paciente_busca']:
        if filtros['paciente_exato']:
            df_filtrado = df_filtrado[df_filtrado['paciente_id'] == filtros['paciente_busca']]
        else:
            df_filtrado = df_filtrado[df_filtrado['paciente_id'].str.contains(filtros['paciente_busca'], case=False, na=False)]
    
    return df_filtrado

# ============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================================================

def plot_serie_temporal(df, segmentar_por_diag=False):
    """Gera gráfico de série temporal mensal."""
    df_ts = df.copy()
    df_ts['ano_mes'] = df_ts['data_atendimento'].dt.to_period('M').astype(str)
    
    if segmentar_por_diag and len(df_ts['diagnostico_vigente'].unique()) <= 10:
        # Stacked area chart por diagnóstico
        df_agg = df_ts.groupby(['ano_mes', 'diagnostico_vigente']).size().reset_index(name='n_atendimentos')
        fig = px.area(
            df_agg, 
            x='ano_mes', 
            y='n_atendimentos', 
            color='diagnostico_vigente',
            title='Série Temporal de Atendimentos (por Diagnóstico)',
            labels={'ano_mes': 'Mês', 'n_atendimentos': 'Nº de Atendimentos'},
            color_discrete_sequence=COLOR_PALETTE
        )
    else:
        # Linha simples com cor primária teal
        df_agg = df_ts.groupby('ano_mes').size().reset_index(name='n_atendimentos')
        fig = px.line(
            df_agg, 
            x='ano_mes', 
            y='n_atendimentos',
            title='Série Temporal de Atendimentos',
            labels={'ano_mes': 'Mês', 'n_atendimentos': 'Nº de Atendimentos'},
            markers=True,
            color_discrete_sequence=[COLORS['primary']]
        )
    
    fig.update_layout(
        xaxis_title='Mês',
        yaxis_title='Nº de Atendimentos',
        hovermode='x unified',
        height=400,
        paper_bgcolor=COLORS['surface'],
        plot_bgcolor=COLORS['surface'],
        font=dict(color=COLORS['text_primary'], family='sans serif'),
        xaxis=dict(gridcolor=COLORS['border']),
        yaxis=dict(gridcolor=COLORS['border'])
    )
    return fig

def plot_top_diagnosticos(df, top_n=10):
    """Gráfico de barras horizontais com top diagnósticos."""
    df_com_diag = df[df['diagnostico_vigente'] != 'SEM DIAGNÓSTICO']
    df_top = df_com_diag.groupby('diagnostico_vigente').size().reset_index(name='n_atendimentos')
    df_top = df_top.sort_values('n_atendimentos', ascending=True).tail(top_n)
    
    # Gradiente customizado do teal claro ao escuro
    color_scale = [
        [0, COLORS['primary_tint3']],
        [0.5, COLORS['primary']],
        [1, COLORS['primary_darker']]
    ]
    
    fig = px.bar(
        df_top,
        x='n_atendimentos',
        y='diagnostico_vigente',
        orientation='h',
        title=f'Top {top_n} Diagnósticos',
        labels={'n_atendimentos': 'Nº de Atendimentos', 'diagnostico_vigente': 'Diagnóstico'},
        color='n_atendimentos',
        color_continuous_scale=color_scale
    )
    fig.update_layout(
        height=400, 
        yaxis=dict(categoryorder='total ascending', gridcolor=COLORS['border']),
        paper_bgcolor=COLORS['surface'],
        plot_bgcolor=COLORS['surface'],
        font=dict(color=COLORS['text_primary'], family='sans serif'),
        xaxis=dict(gridcolor=COLORS['border'])
    )
    return fig

def plot_heatmap_diag_unidade(df):
    """Heatmap de diagnóstico × unidade."""
    df_com_diag = df[df['diagnostico_vigente'] != 'SEM DIAGNÓSTICO']
    df_pivot = df_com_diag.groupby(['diagnostico_vigente', 'unidade']).size().reset_index(name='n_atendimentos')
    
    # Limitar a top diagnósticos e unidades para legibilidade
    top_diag = df_com_diag.groupby('diagnostico_vigente').size().nlargest(10).index
    top_unidades = df_com_diag.groupby('unidade').size().nlargest(10).index
    
    df_pivot = df_pivot[
        df_pivot['diagnostico_vigente'].isin(top_diag) &
        df_pivot['unidade'].isin(top_unidades)
    ]
    
    pivot_table = df_pivot.pivot(index='diagnostico_vigente', columns='unidade', values='n_atendimentos').fillna(0)
    
    # Escala de cores customizada (teal claro a escuro)
    color_scale = [
        [0, COLORS['primary_tint']],
        [0.3, COLORS['primary_tint3']],
        [0.6, COLORS['primary']],
        [1, COLORS['primary_darker']]
    ]
    
    fig = px.imshow(
        pivot_table,
        labels=dict(x='Unidade', y='Diagnóstico', color='Nº Atendimentos'),
        title='Heatmap: Diagnóstico × Unidade (Top 10 cada)',
        color_continuous_scale=color_scale,
        aspect='auto'
    )
    fig.update_layout(
        height=500,
        paper_bgcolor=COLORS['surface'],
        plot_bgcolor=COLORS['surface'],
        font=dict(color=COLORS['text_primary'], family='sans serif')
    )
    return fig

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def display_logo():
    """Exibe o logo no topo da sidebar."""
    try:
        st.sidebar.image("Logo Clinica Pace (1) (1).png", use_container_width=True)
        st.sidebar.markdown("---")
    except:
        pass  # Se o logo não for encontrado, continua sem ele

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    st.title("📊 Dashboard - Atendimentos por Diagnóstico")
    st.markdown("---")
    
    # Carregar dados
    data = load_data()
    if data is None:
        st.stop()
    
    df = data['atendimentos']
    
    # ========================================================================
    # SIDEBAR - FILTROS
    # ========================================================================
    st.sidebar.header("🔍 Filtros")
    
    # Datas
    data_min = df['data_atendimento'].min().date()
    data_max = df['data_atendimento'].max().date()
    
    filtros = {}
    filtros['data_min'] = st.sidebar.date_input(
        "Data Inicial",
        value=data_min,
        min_value=data_min,
        max_value=data_max
    )
    filtros['data_max'] = st.sidebar.date_input(
        "Data Final",
        value=data_max,
        min_value=data_min,
        max_value=data_max
    )
    
    st.sidebar.markdown("---")
    
    # Diagnósticos
    diagnosticos_disponiveis = sorted(df['diagnostico_vigente'].unique())
    tem_sem_diag = 'SEM DIAGNÓSTICO' in diagnosticos_disponiveis
    
    if tem_sem_diag:
        incluir_sem_diag = st.sidebar.checkbox("Incluir 'SEM DIAGNÓSTICO'", value=True)
        if not incluir_sem_diag:
            diagnosticos_disponiveis = [d for d in diagnosticos_disponiveis if d != 'SEM DIAGNÓSTICO']
    
    filtros['diagnosticos'] = st.sidebar.multiselect(
        "Diagnóstico",
        options=diagnosticos_disponiveis,
        default=diagnosticos_disponiveis  # Selecionar todos por padrão
    )
    
    st.sidebar.markdown("---")
    
    # Unidades
    unidades_disponiveis = sorted(df['unidade'].dropna().unique())
    filtros['unidades'] = st.sidebar.multiselect(
        "Unidade",
        options=unidades_disponiveis,
        default=unidades_disponiveis
    )
    
    # Profissionais
    profissionais_disponiveis = sorted(df['profissional_atendimento'].dropna().unique())
    
    # Checkbox para selecionar todos
    selecionar_todos_prof = st.sidebar.checkbox("Selecionar todos os profissionais", value=True)
    
    if selecionar_todos_prof:
        profissionais_selecionados = profissionais_disponiveis
    else:
        profissionais_selecionados = st.sidebar.multiselect(
            "Profissional do Atendimento",
            options=profissionais_disponiveis,
            default=[]
        )
    
    filtros['profissionais'] = profissionais_selecionados if profissionais_selecionados else None
    
    st.sidebar.markdown("---")
    
    # Busca por paciente
    filtros['paciente_busca'] = st.sidebar.text_input("Buscar Paciente (ID)")
    filtros['paciente_exato'] = st.sidebar.checkbox("Busca exata", value=False)
    
    st.sidebar.markdown("---")
    
    # Botão reset
    if st.sidebar.button("🔄 Resetar Filtros"):
        st.rerun()
    
    # ========================================================================
    # APLICAR FILTROS
    # ========================================================================
    df_filtrado = apply_filters(df, filtros)
    
    # Debug: mostrar contagem antes e depois (remover depois)
    # st.write(f"Total antes dos filtros: {len(df)}")
    # st.write(f"Total depois dos filtros: {len(df_filtrado)}")
    
    # ========================================================================
    # KPIs
    # ========================================================================
    st.header("📈 Indicadores (KPIs)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_atendimentos = len(df_filtrado)
    pacientes_unicos = df_filtrado['paciente_id'].nunique()
    diagnosticos_distintos = df_filtrado['diagnostico_vigente'].nunique()
    sem_diag_count = len(df_filtrado[df_filtrado['diagnostico_vigente'] == 'SEM DIAGNÓSTICO'])
    pct_sem_diag = (sem_diag_count / total_atendimentos * 100) if total_atendimentos > 0 else 0
    
    # KPIs com containers estilizados
    with col1:
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_tint']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['primary']};">
            <h3 style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">Total de Atendimentos</h3>
            <h2 style="color: {COLORS['primary_darker']}; margin: 0.5rem 0 0 0;">{total_atendimentos:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_tint']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['primary']};">
            <h3 style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">Pacientes Únicos</h3>
            <h2 style="color: {COLORS['primary_darker']}; margin: 0.5rem 0 0 0;">{pacientes_unicos:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_tint']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['primary']};">
            <h3 style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">Diagnósticos Distintos</h3>
            <h2 style="color: {COLORS['primary_darker']}; margin: 0.5rem 0 0 0;">{diagnosticos_distintos}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        cor_sem_diag = COLORS['warning'] if pct_sem_diag > 10 else COLORS['text_secondary']
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_tint']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {cor_sem_diag};">
            <h3 style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">% Sem Diagnóstico</h3>
            <h2 style="color: {cor_sem_diag}; margin: 0.5rem 0 0 0;">{pct_sem_diag:.1f}%</h2>
            <p style="color: {COLORS['text_secondary']}; margin: 0.5rem 0 0 0; font-size: 0.8rem;">{sem_diag_count:,} atendimentos</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # VISUALIZAÇÕES
    # ========================================================================
    st.header("📊 Visualizações")
    
    # Tabs para organizar visualizações
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Série Temporal", 
        "Top Diagnósticos", 
        "Diagnóstico × Unidade",
        "Diagnóstico × Profissional",
        "Tabela Detalhada"
    ])
    
    with tab1:
        segmentar = st.checkbox("Segmentar por diagnóstico (máx. 10)", value=False)
        fig_ts = plot_serie_temporal(df_filtrado, segmentar_por_diag=segmentar)
        st.plotly_chart(fig_ts, use_container_width=True)
    
    with tab2:
        top_n = st.slider("Top N diagnósticos", min_value=5, max_value=30, value=10)
        fig_top = plot_top_diagnosticos(df_filtrado, top_n=top_n)
        st.plotly_chart(fig_top, use_container_width=True)
    
    with tab3:
        st.markdown("**Nota:** Mostrando apenas top 10 diagnósticos e top 10 unidades para legibilidade.")
        fig_heat = plot_heatmap_diag_unidade(df_filtrado)
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # Tabela pivot completa
        if data['resumo_diag_unidade'] is not None:
            st.subheader("Tabela Completa: Diagnóstico × Unidade")
            df_resumo = data['resumo_diag_unidade'].copy()
            df_resumo_filtrado = df_resumo[
                df_resumo['diagnostico_vigente'].isin(df_filtrado['diagnostico_vigente'].unique()) &
                df_resumo['unidade'].isin(df_filtrado['unidade'].unique())
            ]
            st.dataframe(df_resumo_filtrado, use_container_width=True, height=400)
        else:
            # Computar se não existir
            resumos = compute_resumos(df_filtrado)
            st.dataframe(resumos['diag_unidade'], use_container_width=True, height=400)
    
    with tab4:
        top_n_prof = st.slider("Top N profissionais por diagnóstico", min_value=5, max_value=20, value=10)
        
        if data['resumo_diag_prof'] is not None:
            df_resumo_prof = data['resumo_diag_prof'].copy()
            df_resumo_prof_filtrado = df_resumo_prof[
                df_resumo_prof['diagnostico_vigente'].isin(df_filtrado['diagnostico_vigente'].unique())
            ]
            
            # Top N por diagnóstico
            df_top_prof = df_resumo_prof_filtrado.groupby('diagnostico_vigente').apply(
                lambda x: x.nlargest(top_n_prof, 'n_atendimentos')
            ).reset_index(drop=True)
            
            st.dataframe(df_top_prof, use_container_width=True, height=500)
        else:
            resumos = compute_resumos(df_filtrado)
            df_top_prof = resumos['diag_prof'].groupby('diagnostico_vigente').head(top_n_prof)
            st.dataframe(df_top_prof, use_container_width=True, height=500)
    
    with tab5:
        st.subheader("Atendimentos Filtrados")
        st.markdown(f"**Total de registros:** {len(df_filtrado):,}")
        
        # Ordenar por data descendente
        df_tabela = df_filtrado.sort_values('data_atendimento', ascending=False)
        
        st.dataframe(
            df_tabela,
            use_container_width=True,
            height=500
        )
    
    st.markdown("---")
    
    # ========================================================================
    # EXPORTAÇÃO
    # ========================================================================
    st.header("💾 Exportação de Dados")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        # CSV dos atendimentos filtrados
        csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download Atendimentos Filtrados (CSV)",
            data=csv,
            file_name=f"atendimentos_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col_exp2:
        # Resumo do recorte
        resumos = compute_resumos(df_filtrado)
        resumo_consolidado = {
            'Por_Diagnostico': resumos['diag'],
            'Por_Diagnostico_Unidade': resumos['diag_unidade'],
            'Por_Diagnostico_Profissional': resumos['diag_prof']
        }
        
        # Criar Excel em memória
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, df_sheet in resumo_consolidado.items():
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
        
        st.download_button(
            label="📥 Download Resumo do Recorte (Excel)",
            data=output.getvalue(),
            file_name=f"resumo_recorte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ============================================================================
# PÁGINA QA
# ============================================================================

def page_qa():
    st.title("🔍 Qualidade e Consistência (QA)")
    st.markdown("---")
    
    data = load_data()
    if data is None:
        st.stop()
    
    df = data['atendimentos']
    
    # Exibir QA do Excel se existir
    if data['qa'] is not None:
        st.subheader("Relatório de QA (do processamento original)")
        st.dataframe(data['qa'], use_container_width=True)
        st.markdown("---")
    
    # QA adicional da base atual
    st.subheader("Análise de Qualidade da Base Atual")
    
    qa_items = []
    
    # 1. Atendimentos sem diagnóstico
    sem_diag = len(df[df['diagnostico_vigente'] == 'SEM DIAGNÓSTICO'])
    qa_items.append({
        'Métrica': 'Atendimentos sem diagnóstico vigente',
        'Quantidade': sem_diag,
        'Percentual': f"{(sem_diag/len(df)*100):.2f}%"
    })
    
    # 2. Duplicatas por chave
    chave_dup = df.groupby(['paciente_id', 'data_atendimento', 'profissional_atendimento', 'unidade']).size()
    duplicatas = chave_dup[chave_dup > 1]
    qa_items.append({
        'Métrica': 'Atendimentos duplicados (mesma chave)',
        'Quantidade': len(duplicatas),
        'Percentual': f"{(len(duplicatas)/len(df)*100):.2f}%"
    })
    
    # 3. Datas
    data_min = df['data_atendimento'].min()
    data_max = df['data_atendimento'].max()
    qa_items.append({
        'Métrica': 'Período dos dados',
        'Quantidade': f"{data_min.strftime('%Y-%m-%d')} a {data_max.strftime('%Y-%m-%d')}",
        'Percentual': f"{(data_max - data_min).days} dias"
    })
    
    # 4. Pacientes sem avaliação
    pacientes_atend = set(df['paciente_id'].unique())
    pacientes_com_diag = set(df[df['diagnostico_vigente'] != 'SEM DIAGNÓSTICO']['paciente_id'].unique())
    pacientes_sem_avaliacao = pacientes_atend - pacientes_com_diag
    qa_items.append({
        'Métrica': 'Pacientes sem avaliação (apenas "SEM DIAGNÓSTICO")',
        'Quantidade': len(pacientes_sem_avaliacao),
        'Percentual': f"{(len(pacientes_sem_avaliacao)/len(pacientes_atend)*100):.2f}%"
    })
    
    df_qa_atual = pd.DataFrame(qa_items)
    st.dataframe(df_qa_atual, use_container_width=True)
    
    st.markdown("---")
    
    # Regras de negócio
    st.subheader("📋 Regras de Negócio Aplicadas")
    st.markdown("""
    **Vigência de Diagnóstico:**
    - Para cada paciente, as avaliações são ordenadas por data.
    - Cada avaliação cria um intervalo de vigência: `inicio <= data_atendimento < fim`
    - O diagnóstico vigente para um atendimento é o da avaliação mais recente anterior (ou no mesmo dia) ao atendimento.
    - Se um atendimento ocorrer **no mesmo dia** de uma nova avaliação, ele entra no **diagnóstico novo**.
    - A última avaliação de um paciente tem vigência aberta (sem data fim).
    
    **Tratamento de Empates:**
    - Se houver múltiplas avaliações no mesmo dia para o mesmo paciente, é mantida a última (maior `avaliacao_id`).
    """)

# ============================================================================
# NAVEGAÇÃO
# ============================================================================

# ============================================================================
# PÁGINA AVALIAÇÕES
# ============================================================================

def page_avaliacoes():
    st.title("📋 Análise de Avaliações (Diagnósticos Realizados)")
    st.markdown("---")
    
    data = load_data()
    if data is None:
        st.stop()
    
    # Carregar avaliações
    if data.get('avaliacoes') is None:
        st.error("❌ Dados de avaliações não encontrados. Verifique se a aba 'Base_Avaliacoes_Limpa' existe no arquivo Excel.")
        st.stop()
    
    df_avaliacoes = data['avaliacoes'].copy()
    df_atendimentos = data['atendimentos'].copy()
    
    # Extrair ano da avaliação
    df_avaliacoes['ano'] = pd.to_datetime(df_avaliacoes['data_avaliacao']).dt.year
    
    # Para obter unidade, vamos cruzar com atendimentos do mesmo paciente na mesma data ou próxima
    # Criar uma chave de paciente + data (apenas data, sem hora)
    df_avaliacoes['data_avaliacao_date'] = pd.to_datetime(df_avaliacoes['data_avaliacao']).dt.date
    df_atendimentos['data_atendimento_date'] = pd.to_datetime(df_atendimentos['data_atendimento']).dt.date
    
    # Fazer merge para obter unidade (pegar a unidade do atendimento mais próximo)
    # Primeiro, tentar match exato por paciente e data
    df_atend_agg = df_atendimentos.groupby(['paciente_id', 'data_atendimento_date', 'unidade']).size().reset_index(name='count')
    df_atend_agg = df_atend_agg.sort_values(['paciente_id', 'data_atendimento_date']).drop_duplicates(['paciente_id', 'data_atendimento_date'], keep='first')
    
    df_avaliacoes_com_unidade = df_avaliacoes.merge(
        df_atend_agg[['paciente_id', 'data_atendimento_date', 'unidade']],
        left_on=['paciente_id', 'data_avaliacao_date'],
        right_on=['paciente_id', 'data_atendimento_date'],
        how='left'
    )
    
    # Para avaliações sem unidade, pegar a unidade mais recente do paciente
    pacientes_sem_unidade = df_avaliacoes_com_unidade[df_avaliacoes_com_unidade['unidade'].isna()]['paciente_id'].unique()
    if len(pacientes_sem_unidade) > 0:
        df_atend_paciente = df_atendimentos[df_atendimentos['paciente_id'].isin(pacientes_sem_unidade)]
        df_atend_paciente = df_atend_paciente.sort_values('data_atendimento').groupby('paciente_id').last()[['unidade']].reset_index()
        df_atend_paciente.columns = ['paciente_id', 'unidade_mais_recente']
        
        df_avaliacoes_com_unidade = df_avaliacoes_com_unidade.merge(
            df_atend_paciente,
            on='paciente_id',
            how='left'
        )
        df_avaliacoes_com_unidade['unidade'] = df_avaliacoes_com_unidade['unidade'].fillna(df_avaliacoes_com_unidade['unidade_mais_recente'])
        df_avaliacoes_com_unidade = df_avaliacoes_com_unidade.drop(columns=['unidade_mais_recente', 'data_atendimento_date'], errors='ignore')
    
    df_avaliacoes = df_avaliacoes_com_unidade.drop(columns=['data_atendimento_date'], errors='ignore')
    
    # ========================================================================
    # FILTROS
    # ========================================================================
    st.sidebar.header("🔍 Filtros - Avaliações")
    
    # Filtro de ano
    anos_disponiveis = sorted(df_avaliacoes['ano'].dropna().unique(), reverse=True)
    anos_selecionados = st.sidebar.multiselect(
        "Ano",
        options=anos_disponiveis,
        default=anos_disponiveis[:3] if len(anos_disponiveis) > 3 else anos_disponiveis
    )
    
    # Filtro de unidade
    unidades_disponiveis = sorted(df_avaliacoes['unidade'].dropna().unique())
    unidades_selecionadas = st.sidebar.multiselect(
        "Unidade",
        options=unidades_disponiveis,
        default=unidades_disponiveis
    )
    
    # Filtro de diagnóstico
    diagnosticos_disponiveis = sorted(df_avaliacoes['diagnostico'].dropna().unique())
    diagnosticos_selecionados = st.sidebar.multiselect(
        "Diagnóstico",
        options=diagnosticos_disponiveis,
        default=diagnosticos_disponiveis  # Selecionar TODOS por padrão
    )
    
    # Filtro de profissional (para análises específicas)
    profissionais_disponiveis = sorted(df_avaliacoes['profissional_avaliacao'].dropna().unique())
    profissionais_selecionados = st.sidebar.multiselect(
        "Profissional de Avaliação",
        options=profissionais_disponiveis,
        default=[]
    )
    
    # Aplicar filtros
    df_filtrado = df_avaliacoes.copy()
    if anos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]
    if unidades_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['unidade'].isin(unidades_selecionadas)]
    if diagnosticos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['diagnostico'].isin(diagnosticos_selecionados)]
    if profissionais_selecionados:
        df_filtrado = df_filtrado[df_filtrado['profissional_avaliacao'].isin(profissionais_selecionados)]
    
    # ========================================================================
    # KPIs
    # ========================================================================
    st.header("📈 Indicadores")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_avaliacoes = len(df_filtrado)
    pacientes_avaliados = df_filtrado['paciente_id'].nunique()
    diagnosticos_distintos = df_filtrado['diagnostico'].nunique()
    unidades_distintas = df_filtrado['unidade'].nunique()
    
    with col1:
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_tint']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['primary']};">
            <h3 style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">Total de Avaliações</h3>
            <h2 style="color: {COLORS['primary_darker']}; margin: 0.5rem 0 0 0;">{total_avaliacoes:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_tint']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['primary']};">
            <h3 style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">Pacientes Avaliados</h3>
            <h2 style="color: {COLORS['primary_darker']}; margin: 0.5rem 0 0 0;">{pacientes_avaliados:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_tint']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['primary']};">
            <h3 style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">Diagnósticos Distintos</h3>
            <h2 style="color: {COLORS['primary_darker']}; margin: 0.5rem 0 0 0;">{diagnosticos_distintos}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_tint']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['primary']};">
            <h3 style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">Unidades</h3>
            <h2 style="color: {COLORS['primary_darker']}; margin: 0.5rem 0 0 0;">{unidades_distintas}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # VISUALIZAÇÕES
    # ========================================================================
    st.header("📊 Visualizações")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Por Diagnóstico",
        "Por Unidade",
        "Ano × Unidade",
        "Diagnóstico × Unidade",
        "Por Profissional",
        "Tabela Detalhada"
    ])
    
    with tab1:
        st.subheader("Avaliações por Diagnóstico")
        
        df_diag = df_filtrado.groupby('diagnostico').size().reset_index(name='n_avaliacoes')
        df_diag = df_diag.sort_values('n_avaliacoes', ascending=True)
        
        # Limitar a top N para melhor visualização
        top_n_diag = st.slider("Top N diagnósticos", min_value=5, max_value=50, value=15, key='top_diag_avaliacoes')
        df_diag_top = df_diag.tail(top_n_diag)
        
        fig = px.bar(
            df_diag_top,
            x='n_avaliacoes',
            y='diagnostico',
            orientation='h',
            title=f'Top {top_n_diag} Diagnósticos por Número de Avaliações',
            labels={'diagnostico': 'Diagnóstico', 'n_avaliacoes': 'Nº de Avaliações'},
            color='n_avaliacoes',
            color_continuous_scale=[[0, COLORS['primary_tint3']], [0.5, COLORS['primary']], [1, COLORS['primary_darker']]]
        )
        fig.update_layout(
            paper_bgcolor=COLORS['surface'],
            plot_bgcolor=COLORS['surface'],
            font=dict(color=COLORS['text_primary'], family='sans serif'),
            xaxis=dict(gridcolor=COLORS['border']),
            yaxis=dict(gridcolor=COLORS['border'], categoryorder='total ascending'),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela completa
        st.subheader("Tabela Completa: Avaliações por Diagnóstico")
        st.dataframe(df_diag.sort_values('n_avaliacoes', ascending=False), use_container_width=True, height=400)
    
    with tab2:
        st.subheader("Avaliações por Unidade")
        
        df_unidade = df_filtrado.groupby('unidade').size().reset_index(name='n_avaliacoes')
        df_unidade = df_unidade.sort_values('n_avaliacoes', ascending=True)
        
        fig = px.bar(
            df_unidade,
            x='n_avaliacoes',
            y='unidade',
            orientation='h',
            title='Total de Avaliações por Unidade',
            labels={'unidade': 'Unidade', 'n_avaliacoes': 'Nº de Avaliações'},
            color='n_avaliacoes',
            color_continuous_scale=[[0, COLORS['primary_tint3']], [0.5, COLORS['primary']], [1, COLORS['primary_darker']]]
        )
        fig.update_layout(
            paper_bgcolor=COLORS['surface'],
            plot_bgcolor=COLORS['surface'],
            font=dict(color=COLORS['text_primary'], family='sans serif'),
            xaxis=dict(gridcolor=COLORS['border']),
            yaxis=dict(gridcolor=COLORS['border'], categoryorder='total ascending'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela
        st.dataframe(df_unidade, use_container_width=True, height=200)
    
    with tab3:
        st.subheader("Avaliações por Ano × Unidade")
        
        df_ano_unidade = df_filtrado.groupby(['ano', 'unidade']).size().reset_index(name='n_avaliacoes')
        
        # Heatmap
        pivot_table = df_ano_unidade.pivot(index='unidade', columns='ano', values='n_avaliacoes').fillna(0)
        
        color_scale = [
            [0, COLORS['primary_tint']],
            [0.3, COLORS['primary_tint3']],
            [0.6, COLORS['primary']],
            [1, COLORS['primary_darker']]
        ]
        
        fig = px.imshow(
            pivot_table,
            labels=dict(x='Ano', y='Unidade', color='Nº Avaliações'),
            title='Heatmap: Avaliações por Ano × Unidade',
            color_continuous_scale=color_scale,
            aspect='auto'
        )
        fig.update_layout(
            paper_bgcolor=COLORS['surface'],
            plot_bgcolor=COLORS['surface'],
            font=dict(color=COLORS['text_primary'], family='sans serif'),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela
        st.dataframe(df_ano_unidade.sort_values(['ano', 'n_avaliacoes'], ascending=[True, False]), use_container_width=True, height=400)
    
    with tab4:
        st.subheader("Avaliações por Diagnóstico × Unidade")
        st.markdown("**Nota:** Use os filtros na sidebar para filtrar por ano e profissional.")
        
        # Filtros específicos para esta análise
        col_filt1, col_filt2 = st.columns(2)
        with col_filt1:
            ano_filtro_diag_unid = st.selectbox(
                "Filtrar por Ano (opcional)",
                options=['Todos'] + [str(a) for a in sorted(df_filtrado['ano'].dropna().unique(), reverse=True)],
                key='ano_filtro_diag_unid'
            )
        with col_filt2:
            prof_filtro_diag_unid = st.selectbox(
                "Filtrar por Profissional (opcional)",
                options=['Todos'] + sorted(df_filtrado['profissional_avaliacao'].dropna().unique()),
                key='prof_filtro_diag_unid'
            )
        
        # Aplicar filtros específicos
        df_diag_unid = df_filtrado.copy()
        if ano_filtro_diag_unid != 'Todos':
            df_diag_unid = df_diag_unid[df_diag_unid['ano'] == int(ano_filtro_diag_unid)]
        if prof_filtro_diag_unid != 'Todos':
            df_diag_unid = df_diag_unid[df_diag_unid['profissional_avaliacao'] == prof_filtro_diag_unid]
        
        # Agrupar por diagnóstico × unidade
        df_diag_unidade = df_diag_unid.groupby(['diagnostico', 'unidade']).size().reset_index(name='n_avaliacoes')
        
        # Limitar a top diagnósticos e unidades para legibilidade
        top_diag = df_diag_unid.groupby('diagnostico').size().nlargest(15).index
        top_unidades = df_diag_unid.groupby('unidade').size().nlargest(10).index
        
        df_diag_unidade_filtrado = df_diag_unidade[
            df_diag_unidade['diagnostico'].isin(top_diag) &
            df_diag_unidade['unidade'].isin(top_unidades)
        ]
        
        # Heatmap
        pivot_table = df_diag_unidade_filtrado.pivot(index='diagnostico', columns='unidade', values='n_avaliacoes').fillna(0)
        
        color_scale = [
            [0, COLORS['primary_tint']],
            [0.3, COLORS['primary_tint3']],
            [0.6, COLORS['primary']],
            [1, COLORS['primary_darker']]
        ]
        
        fig = px.imshow(
            pivot_table,
            labels=dict(x='Unidade', y='Diagnóstico', color='Nº Avaliações'),
            title='Heatmap: Avaliações por Diagnóstico × Unidade (Top 15 diagnósticos, Top 10 unidades)',
            color_continuous_scale=color_scale,
            aspect='auto'
        )
        fig.update_layout(
            paper_bgcolor=COLORS['surface'],
            plot_bgcolor=COLORS['surface'],
            font=dict(color=COLORS['text_primary'], family='sans serif'),
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela completa
        st.subheader("Tabela Completa: Diagnóstico × Unidade")
        st.dataframe(
            df_diag_unidade.sort_values(['diagnostico', 'n_avaliacoes'], ascending=[True, False]),
            use_container_width=True,
            height=400
        )
    
    with tab5:
        st.subheader("Avaliações por Profissional (por Ano)")
        
        # Agrupar por profissional e ano
        df_prof_ano = df_filtrado.groupby(['profissional_avaliacao', 'ano']).size().reset_index(name='n_avaliacoes')
        
        # Limitar a top profissionais
        top_n_prof = st.slider("Top N profissionais", min_value=5, max_value=30, value=10, key='top_prof_avaliacoes')
        top_profissionais = df_filtrado.groupby('profissional_avaliacao').size().nlargest(top_n_prof).index
        df_prof_ano_top = df_prof_ano[df_prof_ano['profissional_avaliacao'].isin(top_profissionais)]
        
        # Gráfico de barras agrupadas
        fig = px.bar(
            df_prof_ano_top,
            x='ano',
            y='n_avaliacoes',
            color='profissional_avaliacao',
            title=f'Top {top_n_prof} Profissionais: Avaliações por Ano',
            labels={'ano': 'Ano', 'n_avaliacoes': 'Nº de Avaliações', 'profissional_avaliacao': 'Profissional'},
            barmode='group',
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(
            paper_bgcolor=COLORS['surface'],
            plot_bgcolor=COLORS['surface'],
            font=dict(color=COLORS['text_primary'], family='sans serif'),
            xaxis=dict(gridcolor=COLORS['border']),
            yaxis=dict(gridcolor=COLORS['border']),
            height=500,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap profissional × ano
        pivot_prof_ano = df_prof_ano_top.pivot(index='profissional_avaliacao', columns='ano', values='n_avaliacoes').fillna(0)
        
        color_scale = [
            [0, COLORS['primary_tint']],
            [0.3, COLORS['primary_tint3']],
            [0.6, COLORS['primary']],
            [1, COLORS['primary_darker']]
        ]
        
        fig2 = px.imshow(
            pivot_prof_ano,
            labels=dict(x='Ano', y='Profissional', color='Nº Avaliações'),
            title=f'Heatmap: Top {top_n_prof} Profissionais × Ano',
            color_continuous_scale=color_scale,
            aspect='auto'
        )
        fig2.update_layout(
            paper_bgcolor=COLORS['surface'],
            plot_bgcolor=COLORS['surface'],
            font=dict(color=COLORS['text_primary'], family='sans serif'),
            height=500
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Tabela
        st.subheader("Tabela: Profissional × Ano")
        st.dataframe(
            df_prof_ano.sort_values(['profissional_avaliacao', 'ano'], ascending=[True, True]),
            use_container_width=True,
            height=400
        )
    
    with tab6:
        st.subheader("Avaliações Detalhadas")
        st.markdown(f"**Total de registros:** {len(df_filtrado):,}")
        
        df_tabela = df_filtrado.sort_values('data_avaliacao', ascending=False)
        colunas_tabela = ['data_avaliacao', 'paciente_id', 'diagnostico', 'profissional_avaliacao', 'unidade', 'ano']
        colunas_tabela = [c for c in colunas_tabela if c in df_tabela.columns]
        
        st.dataframe(
            df_tabela[colunas_tabela],
            use_container_width=True,
            height=500
        )
    
    st.markdown("---")
    
    # Exportação
    st.header("💾 Exportação")
    csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Download Avaliações Filtradas (CSV)",
        data=csv,
        file_name=f"avaliacoes_filtradas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def main_app():
    # Logo no topo da sidebar (aparece em todas as páginas)
    display_logo()
    
    # Menu de navegação
    page = st.sidebar.selectbox(
        "📑 Navegação",
        ["Dashboard Principal", "Avaliações", "QA - Qualidade"]
    )
    
    if page == "Dashboard Principal":
        main()
    elif page == "Avaliações":
        page_avaliacoes()
    elif page == "QA - Qualidade":
        page_qa()

if __name__ == "__main__":
    main_app()
