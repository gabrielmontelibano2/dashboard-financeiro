# 📚 Guia de Publicação no GitHub

## Passo 1: Criar Conta GitHub (se não tiver)
1. Acesse [github.com](https://github.com)
2. Clique em **Sign up**
3. Preencha username, email e senha
4. Confirme email

## Passo 2: Criar Novo Repositório

1. Acesse [github.com/new](https://github.com/new)
2. **Repository name**: `dashboard-financeiro`
3. **Description**: "Dashboard para análise de contas, ganhos e gastos pessoais"
4. **Public** (para ser acessível)
5. ✅ **Initialize with README** (deixe marcado)
6. Clique **Create repository**

## Passo 3: Clonar Repositório Localmente

```bash
cd c:\Users\GabrielOliveiraDeFar\OneDrive -"Argus Solutions\Gabriel\"
git clone https://github.com/seu-username/dashboard-financeiro.git
cd dashboard-financeiro
```

## Passo 4: Copiar Arquivos

Copie para a pasta:
- `dashboard.html`
- `servidor_dash.py`
- `requirements.txt`
- `README.md`
- `.gitignore`

Pode deletar o README.md original ou renomear.

## Passo 5: Fazer Commit e Push

```bash
git add .
git commit -m "Inicializar dashboard financeiro"
git push origin main
```

Se pedir autenticação:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Gere um token e use como senha

## Passo 6: Habilitar GitHub Pages

1. Vá para o repositório no GitHub
2. Settings → Pages
3. **Source**: `main` branch
4. Clique **Save**
5. Espere 2-5 minutos

Seu site estará em:
```
https://seu-username.github.io/dashboard-financeiro
```

## Passo 7: Atualizar README

No `README.md`, substitua:
```
seu-usuario.github.io/dashboard-financeiro
seu-usuario
```

Pelo seu username real.

## Atualizações Futuras

Sempre que fizer mudanças:

```bash
git add .
git commit -m "Descrição da mudança"
git push origin main
```

---

## ⚙️ Configuração Alternativa: PythonAnywhere (Com Backend)

Se quiser o dashboard COMPLETO (com upload) online:

1. Acesse [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up (grátis)
3. Upload os arquivos
4. Configure como Web app com Flask
5. Seu site estará em: `seu-username.pythonanywhere.com`

**Vantagens:**
- ✅ Upload de arquivo funciona
- ✅ Dados processam no servidor
- ✅ Múltiplos usuários simultâneos
- ✅ Gratuito

**Desvantagens:**
- Um pouco mais complexo de configurar
- Limite de requisições (gratuito)

---

## 🚀 Resultado Final

Depois de publicado, outras pessoas conseguem:

**GitHub Pages** (versão estática):
- Acessar o link direto
- Ver o design
- Não conseguem fazer upload (sem backend)

**Com Servidor Local** (você rodando o Flask):
- Outras na mesma rede acessam seu IP:5000
- Fazem upload completo
- Usam dashboard funcional

**Com PythonAnywhere** (recomendado):
- Qualquer pessoa online acessa
- Upload funciona 100%
- Sempre ativo

---

Qual opção você prefere? Posso ajudar com a configuração!
