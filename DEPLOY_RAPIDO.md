# 🚀 DEPLOY RÁPIDO - Dashboard Financeiro no GitHub

**gabriel019pira**, seu projeto está pronto para publicar! Siga estes 3 passos:

---

## ✅ PASSO 1: Criar Repositório no GitHub

1. Acesse: **https://github.com/new**
2. Preencha assim:
   - **Repository name**: `dashboard-financeiro`
   - **Description**: `Dashboard para análise de contas, ganhos e gastos pessoais`
   - **Public** ✓ (marcar)
   - **NOT inicialize with README** (deixar desmarcado - já temos)
3. Clique **Create repository**

**Copie a URL que aparece** (exemplo):
```
https://github.com/gabriel019pira/dashboard-financeiro.git
```

---

## ✅ PASSO 2: Executar o Script Deploy

Duplo-clique em **`deploy.bat`** que criamos.

Quando pedir "URL:", cole a URL do repositório que copiou no passo 1 e aperte Enter.

```
URL: https://github.com/gabriel019pira/dashboard-financeiro.git
```

**Espere terminar** (pode pedir sua senha do GitHub).

---

## ✅ PASSO 3: Verificar Deploy

1. Acesse seu repositório: https://github.com/gabriel019pira/dashboard-financeiro
2. Vá em **Settings** → **Pages**
3. No campo **Source**, selecione **main** e clique **Save**
4. Espere 2-5 minutos

Seu dashboard estará ATIVO em:
```
🌐 https://gabriel019pira.github.io/dashboard-financeiro
```

---

## 🎉 Pronto!

Agora outras pessoas conseguem:
- ✅ Acessar seu dashboard visualmente
- ✅ Ver todos os gráficos
- ✅ Clonar seu projeto
- ✅ Fazer fork do repositório

---

## ⚠️ Se der erro de "Senha"

Quando o Git pedir senha:

1. Não é sua senha do GitHub normal
2. Crie um **Personal Access Token**:
   - Acesse: https://github.com/settings/tokens
   - Clique **Generate new token**
   - Selecione `repo`
   - Copie o token
   - Cole no prompt do Git como "senha"

---

## 📱 BONUS: Adicionar Upload Completo (PythonAnywhere)

Se quiser que outras pessoas façam upload de arquivo:

1. Acesse: https://www.pythonanywhere.com
2. Sign up
3. Upload dos arquivos
4. Configure como Web app com Flask
5. URL final: `https://seu-usuario.pythonanywhere.com`

---

## ❓ Dúvidas?

Teste localmente primeiro:
```bash
cd "seu-pasta"
.\.venv\Scripts\python.exe servidor_dash.py
```

Depois acesse: http://localhost:5000

---

**Sucesso no deploy! 🚀**
