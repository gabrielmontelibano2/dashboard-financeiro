# 📊 Dashboard Financeiro - Como Usar

## ⚡ Início Rápido

### 1. **Iniciar o Servidor** 
Execute um destes comandos no terminal:

```powershell
# Opção 1: Executar o servidor diretamente
python servidor_upload.py

# Opção 2: Usando a ativação do virtual env
.venv\Scripts\python.exe servidor_upload.py
```

**Resultado esperado:**
```
🚀 Servidor de upload iniciado em http://localhost:5000
O dashboard pode agora fazer upload de arquivos Excel!
```

### 2. **Abrir o Dashboard**
- Abra `dashboard.html` no navegador
- Você verá: "📤 Faça upload de um arquivo Excel para carregar os dados"

### 3. **Fazer Upload do Arquivo**
- Clique no botão **`📤 Upload Excel`** no topo
- Selecione seu arquivo Excel com as abas:
  - **CONTAS**
  - **GANHO MENSAL**
  - **GASTOS**
- Aguarde a mensagem: **"✅ Atualizado com sucesso!"**

---

## 🔧 Estrutura de Arquivos

```
analise-contas/
├── dashboard.html              ← Abra isto no navegador
├── gerar_dashboard.py          ← Gera o dashboard (não precisa rodar)
├── servidor_upload.py          ← 🚀 RODE ISTO PRIMEIRO
└── INSTRUÇÕES.md              ← Este arquivo
```

---

## 📋 Formato do Excel Obrigatório

Seu arquivo Excel **DEVE TER** estas abas com exatamente estes nomes:

1. **CONTAS**
   - Linha 2: Nomes dos meses (A partir da coluna 17)
   - Linha 3-28: Nomes das contas
   - Colunas 17-28: Valores dos meses
   - Linha 29: Totais (será calculado automaticamente)

2. **GANHO MENSAL**
   - Linha 20-29: Dados mensais
   - Coluna B: Mês
   - Coluna C: Entrada
   - Coluna D: Saída
   - Coluna E: Total

3. **GASTOS**
   - Linha 13+: Dados de gastos
   - Coluna A: Data
   - Coluna B: Mês
   - Coluna C: Categoria/Local
   - Coluna D: Valor

---

## ⚠️ Troubleshooting

### Erro: "Servidor não está rodando"
**Solução:** Abra um terminal e execute:
```powershell
python servidor_upload.py
```
Deixe o terminal aberto enquanto usar o dashboard!

### Erro: "Port 5000 already in use"
**Solução:** A porta 5000 já está em uso. Escolha uma:
1. Feche outros programas usando a porta 5000
2. Ou edite `servidor_upload.py` e mude a linha:
   ```python
   app.run(host='localhost', port=5001)  # Use 5001 ao invés
   ```

### Arquivo não carrega
1. Verifique os **nomes exatos das abas** (maiúsculas/minúsculas!)
2. Abra F12 → Console para ver mensagens de erro
3. Certifique-se que o servidor está rodando

---

## 🎯 Fluxo de Uso

```
1. Terminal: python servidor_upload.py
   ↓
2. Navegador: Abra dashboard.html
   ↓
3. Botão: 📤 Upload Excel
   ↓
4. Selecione: Seu arquivo .xlsx
   ↓
5. Resultado: ✅ Dashboard atualizado!
   ↓
6. Explore: Todos os gráficos e filtros
```

---

## 💡 Dica: Executar em um Clique

### Windows: Criar atalho .bat

Crie um arquivo `iniciar_servidor.bat` com:
```batch
@echo off
cd /d "%~dp0"
.venv\Scripts\python.exe servidor_upload.py
pause
```

Depois é só dar **duplo clique** no arquivo!

---

## 📞 Resumo Rápido

| Ação | Como Fazer |
|------|-----------|
| **Iniciar servidor** | `python servidor_upload.py` |
| **Abrir dashboard** | Clique em `dashboard.html` |
| **Fazer upload** | Botão `📤 Upload Excel` |
| **Ver erros** | F12 → Console |
| **Parar servidor** | Ctrl+C no terminal |

---

**Pronto! Seu dashboard está funcionando! 🚀**
