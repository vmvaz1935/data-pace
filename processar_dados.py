import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("PROCESSAMENTO DE DADOS - ATENDIMENTOS POR DIAGNÓSTICO")
print("=" * 80)

# ============================================================================
# 1. LEITURA E IDENTIFICAÇÃO DOS DADOS
# ============================================================================
print("\n[1/8] Lendo arquivo Excel...")
excel_file = pd.ExcelFile('avaliacoes-atendimentos.xlsx')

# Ler abas
df_avaliacoes_raw = pd.read_excel(excel_file, sheet_name='Avaliação')
df_atendimentos_raw = pd.read_excel(excel_file, sheet_name='Atendimentos')

print(f"  - Avaliações: {len(df_avaliacoes_raw)} registros")
print(f"  - Atendimentos: {len(df_atendimentos_raw)} registros")

# ============================================================================
# 2. PADRONIZAÇÃO - AVALIAÇÕES
# ============================================================================
print("\n[2/8] Padronizando dados de avaliações...")

df_avaliacoes = df_avaliacoes_raw.copy()

# Padronizar nomes de colunas
df_avaliacoes.columns = df_avaliacoes.columns.str.strip()
df_avaliacoes = df_avaliacoes.rename(columns={
    'Data': 'data_avaliacao',
    'Profissional': 'profissional_avaliacao',
    'Paciente': 'paciente_id',
    'Diagnóstico': 'diagnostico'
})

# Tratar datas
df_avaliacoes['data_avaliacao'] = pd.to_datetime(df_avaliacoes['data_avaliacao'], errors='coerce')
df_avaliacoes['data_avaliacao_raw'] = df_avaliacoes_raw['Data'].copy()

# Normalizar diagnóstico (trim, case, etc)
df_avaliacoes['diagnostico'] = df_avaliacoes['diagnostico'].astype(str).str.strip()
df_avaliacoes['diagnostico'] = df_avaliacoes['diagnostico'].str.title()  # Primeira letra maiúscula
df_avaliacoes['diagnostico_raw'] = df_avaliacoes_raw['Diagnóstico'].copy()

# Normalizar profissional
df_avaliacoes['profissional_avaliacao'] = df_avaliacoes['profissional_avaliacao'].astype(str).str.strip()
df_avaliacoes['profissional_avaliacao_raw'] = df_avaliacoes_raw['Profissional'].copy()

# Normalizar paciente
df_avaliacoes['paciente_id'] = df_avaliacoes['paciente_id'].astype(str).str.strip()
df_avaliacoes['paciente_id_raw'] = df_avaliacoes_raw['Paciente'].copy()

# Criar ID de avaliação (se não existir)
if 'avaliacao_id' not in df_avaliacoes.columns:
    df_avaliacoes['avaliacao_id'] = range(1, len(df_avaliacoes) + 1)

# Remover linhas com dados essenciais faltando
df_avaliacoes = df_avaliacoes.dropna(subset=['paciente_id', 'data_avaliacao', 'diagnostico'])
df_avaliacoes = df_avaliacoes[df_avaliacoes['paciente_id'] != 'nan']
df_avaliacoes = df_avaliacoes[df_avaliacoes['diagnostico'] != 'nan']

print(f"  - Avaliações válidas após limpeza: {len(df_avaliacoes)}")

# ============================================================================
# 3. PADRONIZAÇÃO - ATENDIMENTOS
# ============================================================================
print("\n[3/8] Padronizando dados de atendimentos...")

df_atendimentos = df_atendimentos_raw.copy()

# Padronizar nomes de colunas
df_atendimentos.columns = df_atendimentos.columns.str.strip()
df_atendimentos = df_atendimentos.rename(columns={
    'Data': 'data_atendimento',
    'Paciente': 'paciente_id',
    'Profissional ': 'profissional_atendimento',
    'Profissional': 'profissional_atendimento',  # Caso não tenha espaço
    'Unidade': 'unidade'
})

# Tratar datas
df_atendimentos['data_atendimento'] = pd.to_datetime(df_atendimentos['data_atendimento'], errors='coerce')
df_atendimentos['data_atendimento_raw'] = df_atendimentos_raw['Data'].copy()

# Normalizar profissional
df_atendimentos['profissional_atendimento'] = df_atendimentos['profissional_atendimento'].astype(str).str.strip()
if 'Profissional ' in df_atendimentos_raw.columns:
    df_atendimentos['profissional_atendimento_raw'] = df_atendimentos_raw['Profissional '].copy()
else:
    df_atendimentos['profissional_atendimento_raw'] = df_atendimentos_raw['Profissional'].copy()

# Normalizar unidade
df_atendimentos['unidade'] = df_atendimentos['unidade'].astype(str).str.strip()
df_atendimentos['unidade_raw'] = df_atendimentos_raw['Unidade'].copy()

# Normalizar paciente
df_atendimentos['paciente_id'] = df_atendimentos['paciente_id'].astype(str).str.strip()
df_atendimentos['paciente_id_raw'] = df_atendimentos_raw['Paciente'].copy()

# Criar ID de atendimento (se não existir)
if 'atendimento_id' not in df_atendimentos.columns:
    df_atendimentos['atendimento_id'] = range(1, len(df_atendimentos) + 1)

# Remover linhas com dados essenciais faltando
df_atendimentos = df_atendimentos.dropna(subset=['paciente_id', 'data_atendimento'])
df_atendimentos = df_atendimentos[df_atendimentos['paciente_id'] != 'nan']

print(f"  - Atendimentos válidos após limpeza: {len(df_atendimentos)}")

# ============================================================================
# 4. TRATAR EMPATES - MÚLTIPLAS AVALIAÇÕES NO MESMO DIA
# ============================================================================
print("\n[4/8] Tratando empates (múltiplas avaliações no mesmo dia)...")

# Ordenar avaliações por paciente, data e avaliacao_id
df_avaliacoes = df_avaliacoes.sort_values(['paciente_id', 'data_avaliacao', 'avaliacao_id'])

# Identificar duplicatas no mesmo dia
duplicatas = df_avaliacoes.groupby(['paciente_id', 'data_avaliacao']).size()
duplicatas = duplicatas[duplicatas > 1]

if len(duplicatas) > 0:
    print(f"  - Encontradas {len(duplicatas)} combinações paciente+data com múltiplas avaliações")
    print(f"  - Total de avaliações duplicadas: {duplicatas.sum() - len(duplicatas)}")
    print("  - Regra aplicada: manter a última avaliação do dia (maior avaliacao_id)")
    
    # Manter apenas a última avaliação do dia (maior avaliacao_id)
    df_avaliacoes = df_avaliacoes.drop_duplicates(
        subset=['paciente_id', 'data_avaliacao'],
        keep='last'
    )
    print(f"  - Avaliações após remoção de duplicatas: {len(df_avaliacoes)}")
else:
    print("  - Nenhuma duplicata encontrada")

# ============================================================================
# 5. CRIAR INTERVALOS DE VIGÊNCIA
# ============================================================================
print("\n[5/8] Criando intervalos de vigência dos diagnósticos...")

# Ordenar avaliações por paciente e data
df_avaliacoes = df_avaliacoes.sort_values(['paciente_id', 'data_avaliacao', 'avaliacao_id'])

vigencia_list = []

for paciente in df_avaliacoes['paciente_id'].unique():
    aval_paciente = df_avaliacoes[df_avaliacoes['paciente_id'] == paciente].copy()
    aval_paciente = aval_paciente.sort_values(['data_avaliacao', 'avaliacao_id'])
    
    for idx, row in aval_paciente.iterrows():
        inicio_diag = row['data_avaliacao']
        
        # Fim é a próxima avaliação do mesmo paciente
        proxima_aval = aval_paciente[aval_paciente['data_avaliacao'] > inicio_diag]
        if len(proxima_aval) > 0:
            fim_diag = proxima_aval.iloc[0]['data_avaliacao']
        else:
            fim_diag = None  # Última avaliação - vigência aberta
        
        vigencia_list.append({
            'paciente_id': paciente,
            'inicio_diag': inicio_diag,
            'fim_diag': fim_diag,
            'diagnostico': row['diagnostico'],
            'profissional_avaliacao': row['profissional_avaliacao'],
            'avaliacao_id': row['avaliacao_id']
        })

df_vigencia = pd.DataFrame(vigencia_list)
print(f"  - Intervalos de vigência criados: {len(df_vigencia)}")

# ============================================================================
# 6. CRUZAR ATENDIMENTOS COM DIAGNÓSTICOS VIGENTES
# ============================================================================
print("\n[6/8] Cruzando atendimentos com diagnósticos vigentes...")

atendimentos_com_diag = []

for idx, atend in df_atendimentos.iterrows():
    paciente = atend['paciente_id']
    data_atend = atend['data_atendimento']
    
    # Buscar vigências do paciente
    vig_paciente = df_vigencia[df_vigencia['paciente_id'] == paciente].copy()
    
    diagnostico_vigente = None
    data_avaliacao_origem = None
    profissional_avaliacao_origem = None
    
    # Encontrar diagnóstico vigente
    for idx_vig, vig in vig_paciente.iterrows():
        inicio = vig['inicio_diag']
        fim = vig['fim_diag']
        
        # Regra: inicio <= data_atendimento < fim (ou fim é None para última avaliação)
        if pd.isna(fim):
            # Última avaliação - vigência aberta
            if data_atend >= inicio:
                diagnostico_vigente = vig['diagnostico']
                data_avaliacao_origem = vig['inicio_diag']
                profissional_avaliacao_origem = vig['profissional_avaliacao']
                break
        else:
            # Avaliação intermediária
            if inicio <= data_atend < fim:
                diagnostico_vigente = vig['diagnostico']
                data_avaliacao_origem = vig['inicio_diag']
                profissional_avaliacao_origem = vig['profissional_avaliacao']
                break
    
    atendimentos_com_diag.append({
        'atendimento_id': atend['atendimento_id'],
        'paciente_id': paciente,
        'data_atendimento': data_atend,
        'profissional_atendimento': atend['profissional_atendimento'],
        'unidade': atend['unidade'],
        'diagnostico_vigente': diagnostico_vigente if diagnostico_vigente else 'SEM DIAGNÓSTICO',
        'data_avaliacao_origem': data_avaliacao_origem,
        'profissional_avaliacao_origem': profissional_avaliacao_origem
    })

df_atendimentos_com_diag = pd.DataFrame(atendimentos_com_diag)

sem_diag = len(df_atendimentos_com_diag[df_atendimentos_com_diag['diagnostico_vigente'] == 'SEM DIAGNÓSTICO'])
print(f"  - Atendimentos com diagnóstico: {len(df_atendimentos_com_diag) - sem_diag}")
print(f"  - Atendimentos sem diagnóstico: {sem_diag}")

# ============================================================================
# 7. GERAR RESUMOS
# ============================================================================
print("\n[7/8] Gerando resumos...")

# Resumo por diagnóstico
df_resumo_diag = df_atendimentos_com_diag[
    df_atendimentos_com_diag['diagnostico_vigente'] != 'SEM DIAGNÓSTICO'
].groupby('diagnostico_vigente').size().reset_index(name='n_atendimentos')
df_resumo_diag = df_resumo_diag.sort_values('n_atendimentos', ascending=False)

# Resumo por diagnóstico × profissional
df_resumo_diag_prof = df_atendimentos_com_diag[
    df_atendimentos_com_diag['diagnostico_vigente'] != 'SEM DIAGNÓSTICO'
].groupby(['diagnostico_vigente', 'profissional_atendimento']).size().reset_index(name='n_atendimentos')
df_resumo_diag_prof = df_resumo_diag_prof.sort_values(['diagnostico_vigente', 'n_atendimentos'], ascending=[True, False])

# Resumo por diagnóstico × unidade
df_resumo_diag_unidade = df_atendimentos_com_diag[
    df_atendimentos_com_diag['diagnostico_vigente'] != 'SEM DIAGNÓSTICO'
].groupby(['diagnostico_vigente', 'unidade']).size().reset_index(name='n_atendimentos')
df_resumo_diag_unidade = df_resumo_diag_unidade.sort_values(['diagnostico_vigente', 'n_atendimentos'], ascending=[True, False])

# Resumo por diagnóstico × unidade × profissional
df_resumo_diag_unidade_prof = df_atendimentos_com_diag[
    df_atendimentos_com_diag['diagnostico_vigente'] != 'SEM DIAGNÓSTICO'
].groupby(['diagnostico_vigente', 'unidade', 'profissional_atendimento']).size().reset_index(name='n_atendimentos')
df_resumo_diag_unidade_prof = df_resumo_diag_unidade_prof.sort_values(['diagnostico_vigente', 'unidade', 'n_atendimentos'], ascending=[True, True, False])

print(f"  - Resumo por diagnóstico: {len(df_resumo_diag)} linhas")
print(f"  - Resumo por diagnóstico × profissional: {len(df_resumo_diag_prof)} linhas")
print(f"  - Resumo por diagnóstico × unidade: {len(df_resumo_diag_unidade)} linhas")
print(f"  - Resumo por diagnóstico × unidade × profissional: {len(df_resumo_diag_unidade_prof)} linhas")

# ============================================================================
# 8. QA - QUALIDADE E CONSISTÊNCIA
# ============================================================================
print("\n[8/8] Gerando relatório de QA...")

qa_items = []

# 1. Pacientes sem nenhuma avaliação
pacientes_atendimentos = set(df_atendimentos['paciente_id'].unique())
pacientes_avaliacoes = set(df_avaliacoes['paciente_id'].unique())
pacientes_sem_avaliacao = pacientes_atendimentos - pacientes_avaliacoes
qa_items.append({
    'Categoria': 'Pacientes sem avaliação',
    'Quantidade': len(pacientes_sem_avaliacao),
    'Detalhes': f"Pacientes que têm atendimentos mas não têm avaliações: {len(pacientes_sem_avaliacao)}"
})

# 2. Atendimentos sem paciente_id ou data
atend_sem_paciente = len(df_atendimentos_raw[df_atendimentos_raw['Paciente'].isna()])
atend_sem_data = len(df_atendimentos_raw[df_atendimentos_raw['Data'].isna()])
qa_items.append({
    'Categoria': 'Atendimentos com dados faltando (antes da limpeza)',
    'Quantidade': atend_sem_paciente + atend_sem_data,
    'Detalhes': f"Sem paciente: {atend_sem_paciente}, Sem data: {atend_sem_data}"
})

# 3. Duplicatas de atendimentos
chave_atend = df_atendimentos.groupby(['paciente_id', 'data_atendimento', 'profissional_atendimento', 'unidade']).size()
duplicatas_atend = chave_atend[chave_atend > 1]
qa_items.append({
    'Categoria': 'Atendimentos duplicados (mesma chave)',
    'Quantidade': len(duplicatas_atend),
    'Detalhes': f"Combinações paciente+data+profissional+unidade duplicadas: {len(duplicatas_atend)}"
})

# 4. Avaliações duplicadas no mesmo dia (já tratadas)
qa_items.append({
    'Categoria': 'Avaliações no mesmo dia (tratadas)',
    'Quantidade': len(duplicatas) if len(duplicatas) > 0 else 0,
    'Detalhes': f"Regra aplicada: manter última avaliação do dia (maior avaliacao_id)"
})

# 5. Atendimentos sem diagnóstico
qa_items.append({
    'Categoria': 'Atendimentos sem diagnóstico vigente',
    'Quantidade': sem_diag,
    'Detalhes': f"Atendimentos que ocorreram antes da primeira avaliação do paciente"
})

# 6. Verificação de datas
data_min_aval = df_avaliacoes['data_avaliacao'].min()
data_max_aval = df_avaliacoes['data_avaliacao'].max()
data_min_atend = df_atendimentos['data_atendimento'].min()
data_max_atend = df_atendimentos['data_atendimento'].max()

atend_antes_primeira_aval = len(df_atendimentos[df_atendimentos['data_atendimento'] < data_min_aval])
atend_muito_posterior = len(df_atendimentos[df_atendimentos['data_atendimento'] > data_max_aval + pd.Timedelta(days=365)])

qa_items.append({
    'Categoria': 'Verificação de datas',
    'Quantidade': atend_antes_primeira_aval + atend_muito_posterior,
    'Detalhes': f"Atendimentos antes da primeira avaliação: {atend_antes_primeira_aval}. Atendimentos muito posteriores (>1 ano): {atend_muito_posterior}"
})

df_qa = pd.DataFrame(qa_items)

# ============================================================================
# 9. EXPORTAR PARA EXCEL
# ============================================================================
print("\n[9/9] Exportando para Excel...")

output_file = 'atendimentos_por_diagnostico.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Aba 1: Base_Avaliacoes_Limpa
    cols_aval = ['avaliacao_id', 'paciente_id', 'data_avaliacao', 'diagnostico', 
                 'profissional_avaliacao', 'paciente_id_raw', 'data_avaliacao_raw', 
                 'diagnostico_raw', 'profissional_avaliacao_raw']
    df_avaliacoes[cols_aval].to_excel(writer, sheet_name='Base_Avaliacoes_Limpa', index=False)
    
    # Aba 2: Base_Atendimentos_Limpa
    cols_atend = ['atendimento_id', 'paciente_id', 'data_atendimento', 
                  'profissional_atendimento', 'unidade', 'paciente_id_raw', 
                  'data_atendimento_raw', 'profissional_atendimento_raw', 'unidade_raw']
    df_atendimentos[cols_atend].to_excel(writer, sheet_name='Base_Atendimentos_Limpa', index=False)
    
    # Aba 3: Vigencia_Diagnosticos
    df_vigencia.to_excel(writer, sheet_name='Vigencia_Diagnosticos', index=False)
    
    # Aba 4: Atendimentos_Com_Diagnostico
    df_atendimentos_com_diag.to_excel(writer, sheet_name='Atendimentos_Com_Diagnostico', index=False)
    
    # Aba 5: Resumo_Diagnostico
    df_resumo_diag.to_excel(writer, sheet_name='Resumo_Diagnostico', index=False)
    
    # Aba 6: Resumo_Diag_Profissional
    df_resumo_diag_prof.to_excel(writer, sheet_name='Resumo_Diag_Profissional', index=False)
    
    # Aba 7: Resumo_Diag_Unidade
    df_resumo_diag_unidade.to_excel(writer, sheet_name='Resumo_Diag_Unidade', index=False)
    
    # Aba 8: Resumo_Diag_Unidade_Prof
    df_resumo_diag_unidade_prof.to_excel(writer, sheet_name='Resumo_Diag_Unidade_Prof', index=False)
    
    # Aba 9: QA
    df_qa.to_excel(writer, sheet_name='QA', index=False)

print(f"  [OK] Arquivo gerado: {output_file}")

# ============================================================================
# 10. EXPORTAR CSVs PRINCIPAIS
# ============================================================================
print("\n[10/10] Exportando CSVs principais...")

df_atendimentos_com_diag.to_csv('Atendimentos_Com_Diagnostico.csv', index=False, encoding='utf-8-sig')
print("  [OK] Atendimentos_Com_Diagnostico.csv")

# Consolidar resumos em um arquivo
with pd.ExcelWriter('Resumos.xlsx', engine='openpyxl') as writer:
    df_resumo_diag.to_excel(writer, sheet_name='Por_Diagnostico', index=False)
    df_resumo_diag_prof.to_excel(writer, sheet_name='Por_Diagnostico_Profissional', index=False)
    df_resumo_diag_unidade.to_excel(writer, sheet_name='Por_Diagnostico_Unidade', index=False)
    df_resumo_diag_unidade_prof.to_excel(writer, sheet_name='Por_Diagnostico_Unidade_Prof', index=False)

print("  [OK] Resumos.xlsx")

print("\n" + "=" * 80)
print("PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
print("=" * 80)
print(f"\nArquivos gerados:")
print(f"  - {output_file}")
print(f"  - Atendimentos_Com_Diagnostico.csv")
print(f"  - Resumos.xlsx")
