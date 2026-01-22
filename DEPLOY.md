# 🚀 Guia de Deploy - Streamlit Cloud

## Checklist antes do Commit

- [x] ✅ `app.py` - Arquivo principal do dashboard
- [x] ✅ `requirements.txt` - Dependências Python
- [x] ✅ `.streamlit/config.toml` - Configuração do tema
- [x] ✅ `.gitignore` - Arquivos a ignorar
- [x] ✅ `README.md` - Documentação atualizada
- [x] ✅ Arquivos de dados necessários

## Arquivos para Commitar

### Obrigatórios:
```
✅ app.py
✅ requirements.txt
✅ .streamlit/config.toml
✅ .gitignore
✅ README.md
✅ atendimentos_por_diagnostico.xlsx (6.02 MB)
✅ Atendimentos_Com_Diagnostico.csv (7.54 MB - fallback)
✅ Resumos.xlsx (0.06 MB)
```

### Opcionais (mas recomendados):
```
✅ DEPLOY.md (este arquivo)
✅ packages.txt
```

### NÃO commitar:
```
❌ __pycache__/
❌ venv/
❌ *.pyc
❌ .DS_Store
❌ arquivos temporários
```

## Comandos Git

### 1. Inicializar repositório (se ainda não foi feito):
```bash
git init
```

### 2. Adicionar arquivos:
```bash
git add app.py
git add requirements.txt
git add .streamlit/
git add .gitignore
git add README.md
git add DEPLOY.md
git add atendimentos_por_diagnostico.xlsx
git add Atendimentos_Com_Diagnostico.csv
git add Resumos.xlsx
```

Ou adicionar tudo (exceto o que está no .gitignore):
```bash
git add .
```

### 3. Fazer commit:
```bash
git commit -m "feat: Dashboard de Atendimentos por Diagnóstico com análise de avaliações"
```

### 4. Criar branch main (se necessário):
```bash
git branch -M main
```

### 5. Adicionar remote (substitua pela URL do seu repositório):
```bash
git remote add origin https://github.com/seu-usuario/seu-repositorio.git
```

### 6. Push para GitHub:
```bash
git push -u origin main
```

## Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com GitHub
3. Clique em "New app"
4. Preencha:
   - **Repository**: Seu repositório
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Clique em "Deploy"

## Verificações Pós-Deploy

- [ ] App carrega sem erros
- [ ] Dados são carregados corretamente
- [ ] Filtros funcionam
- [ ] Gráficos aparecem
- [ ] Exportação funciona
- [ ] Tema teal está aplicado

## Troubleshooting

### Erro: "Module not found"
- Verifique se todas as dependências estão no `requirements.txt`
- Streamlit Cloud instala automaticamente do `requirements.txt`

### Erro: "File not found"
- Verifique se os arquivos de dados estão no repositório
- Verifique os caminhos no código (devem ser relativos)

### App lento
- Normal para datasets grandes
- O cache ajuda, mas pode demorar no primeiro carregamento

### Tema não aplicado
- Verifique se `.streamlit/config.toml` está commitado
- Verifique se está na pasta `.streamlit/` (com ponto)

## Atualização de Dados

Para atualizar os dados no dashboard:

1. Processe os novos dados (use `processar_dados.py` localmente)
2. Faça commit dos novos arquivos:
   ```bash
   git add atendimentos_por_diagnostico.xlsx
   git add Atendimentos_Com_Diagnostico.csv
   git commit -m "chore: Atualizar dados de atendimentos"
   git push
   ```
3. O Streamlit Cloud recarregará automaticamente

## Limites do Streamlit Cloud

- ✅ **Tamanho do repositório**: Até 1GB (seus arquivos: ~15 MB - OK)
- ✅ **Tamanho de arquivo**: Até 100 MB por arquivo (seus arquivos: < 10 MB - OK)
- ✅ **Uso de memória**: Até 1GB RAM
- ✅ **CPU**: Compartilhado

## Segurança

⚠️ **Importante**: 
- Não commite dados sensíveis sem criptografia
- Use `.gitignore` para arquivos com informações pessoais
- Considere usar variáveis de ambiente para credenciais (se necessário no futuro)

## Suporte

Se tiver problemas:
1. Verifique os logs no Streamlit Cloud
2. Teste localmente primeiro: `streamlit run app.py`
3. Verifique se todos os arquivos estão commitados
