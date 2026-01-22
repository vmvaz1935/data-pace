# ✅ Checklist para Commit e Deploy

## Arquivos Prontos para Commit

### Código e Configuração
- [x] `app.py` - Dashboard principal
- [x] `requirements.txt` - Dependências
- [x] `.streamlit/config.toml` - Tema teal clínico
- [x] `.gitignore` - Arquivos a ignorar

### Dados
- [x] `atendimentos_por_diagnostico.xlsx` (6.02 MB) - Dados principais
- [x] `Atendimentos_Com_Diagnostico.csv` (7.54 MB) - Fallback
- [x] `Resumos.xlsx` (0.06 MB) - Resumos

### Documentação
- [x] `README.md` - Documentação completa
- [x] `DEPLOY.md` - Guia de deploy
- [x] `COMMIT_CHECKLIST.md` - Este arquivo

## Comandos Rápidos

### Primeiro Commit
```bash
git init
git add .
git commit -m "feat: Dashboard de Atendimentos por Diagnóstico - Streamlit"
git branch -M main
git remote add origin <URL_DO_SEU_REPO>
git push -u origin main
```

### Atualizações Futuras
```bash
git add .
git commit -m "feat: Descrição da mudança"
git push
```

## Verificações Finais

Antes de fazer push, verifique:

1. ✅ Todos os arquivos necessários estão no diretório
2. ✅ `.gitignore` está configurado corretamente
3. ✅ `requirements.txt` tem todas as dependências
4. ✅ `app.py` não tem caminhos absolutos
5. ✅ Arquivos de dados estão acessíveis

## Tamanho Total

- Código: ~0.1 MB
- Dados: ~15 MB
- **Total: ~15 MB** (bem abaixo do limite de 1GB do GitHub)

## Próximos Passos

1. ✅ Fazer commit e push
2. ✅ Conectar no Streamlit Cloud
3. ✅ Deploy
4. ✅ Testar o dashboard online

## Notas

- Os arquivos de dados são necessários no repositório para o app funcionar
- O Streamlit Cloud recarrega automaticamente após cada push
- Use branches para testar mudanças antes de merge no main
