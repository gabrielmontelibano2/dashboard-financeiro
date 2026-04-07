# 📊 Dashboard Financeiro Pessoal

Um dashboard interativo para análise de contas, ganhos e gastos financeiros. Desenvolvido com HTML5, JavaScript e Plotly.

## ✨ Funcionalidades

- 📈 **Visualização de Contas** - Gráficos de barras e pizza com top 10 contas
- 📅 **Evolução Mensal** - Acompanhamento de saldo ao longo dos meses
- 💰 **Análise de Ganhos** - Comparação entre entrada e saída
- 🛒 **Gastos Detalhados** - Categorização e distribução de gastos
- 📊 **Insights Automáticos** - Análise de saúde financeira, riscos por mês, top gastos
- 💾 **Persistência Local** - Dados salvos no localStorage
- 🌐 **Multi-usuário** - Cada pessoa tem seus próprios dados

## 🚀 Como Usar

### **Opção 1: Localmente (Com Upload de Arquivo)**

1. **Certifique-se que tem Python 3.8+**
   ```bash
   python --version
   ```

2. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/dashboard-financeiro.git
   cd dashboard-financeiro
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o servidor**
   ```bash
   python servidor_dash.py
   ```

5. **Abra no navegador**
   - Localmente: `http://localhost:5000`
   - Rede local: `http://SEU-IP:5000`

### **Opção 2: Online (GitHub Pages - Sem Backend)**

Acesse diretamente: [seu-usuario.github.io/dashboard-financeiro](seu-usuario.github.io/dashboard-financeiro)

*(Versão só de visualização - sem upload)*

## 📁 Estrutura do Projeto

```
dashboard-financeiro/
├── dashboard.html          # Interface principal
├── servidor_dash.py        # Backend Flask
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
└── exemplo-dados.xlsx     # Arquivo de exemplo
```

## 📋 Formato do Arquivo Excel

O arquivo deve ter as seguintes abas:

### **Aba: CONTAS**
- Colunas 16-27: Nomes dos meses (JANEIRO, FEVEREIRO, etc)
- Linhas 2+: Nomes das contas e seus valores mensais

### **Aba: GANHO MENSAL**
- Linhas 19-28: Dados de entrada, saída e total por mês
- Colunas: Data | Mês | Entrada | Saída | Total

### **Aba: GASTOS**
- Colunas: Data | Mês | Categoria | Valor
- Linha inicial: 12

## 🛠️ Tecnologias

- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Gráficos**: Plotly.js 2.26.0
- **Backend**: Flask 3.1.3, Pandas 3.0.2
- **Armazenamento**: localStorage (navegador)
- **API**: JSON REST

## 📊 Gráficos Inclusos

- ✅ Barras horizontais (Top 10 contas/gastos)
- ✅ Gráficos de pizza (distribuição percentual)
- ✅ Gráficos de linha (evolução temporal)
- ✅ Gráficos de barras agrupadas (Entrada vs Saída)

## 🎨 Recursos de UX

- 4 abas principais (Visão Geral, Contas, Ganhos, Gastos)
- Filtros por conta, mês
- Métricas (Total, Média, Maior, Menor)
- 4 Insights automáticos com emojis
- Indicadores de saúde financeira
- Análise de riscos por mês
- Responsivo (desktop + tablet)

## 🔐 Privacidade

- ✅ Todos os dados ficam no seu navegador (localStorage)
- ✅ Nenhum dado é enviado para servidores externos
- ✅ Cada usuário tem seus próprios dados
- ✅ Dados persistem entre sessões

## 📦 Instalação de Dependências

```bash
pip install flask==3.1.3
pip install flask-cors==4.0.0
pip install pandas==3.0.2
pip install openpyxl==3.1.5
```

Ou use:
```bash
pip install -r requirements.txt
```

## 🐛 Troubleshooting

### Erro: "Arquivo CONTAS não encontrado"
- Verifique se a aba CONTAS existe no Excel
- Certifique-se da ortografia (sem espaços extras)

### "Port 5000 already in use"
- Mude para outra porta: `python servidor_dash.py --port 5001`
- Ou feche o processo anterior: `lsof -i :5000` (Mac/Linux)

### Dashboard carrega mas não aceita upload
- Verifique CORS (deve estar habilitado)
- Teste a conectividade: `curl http://localhost:5000/saude`

## 📧 Suporte

Para reportar bugs ou sugerir melhorias, abra uma issue no repositório.

## 📄 Licença

MIT - Use livremente!

---

**Desenvolvido com ❤️ para análise financeira pessoal**
