# 🚀 Dashboard Financeiro - Setup 24/7

## Como deixar o Dashboard rodando 24/7 no seu PC

### Opção 1: Rodar agora (Rápido) ⚡

Abra a pasta do projeto e **clique 2 vezes** em:
```
iniciar_24_7.bat
```

Pronto! O servidor está rodando! 

**Acesse em:**
- Local: http://localhost:5000
- Rede: http://192.168.20.157:5000

---

### Opção 2: Iniciar automaticamente ao ligar o PC 🔄

1. Abra a pasta do projeto
2. Clique com **botão direito** em:
   ```
   agendar_24_7.bat
   ```
3. Selecione: **"Executar como administrador"**
4. Clique OK

Pronto! Agora o Dashboard inicia automaticamente quando você faz login! ✅

---

## O que cada arquivo faz:

| Arquivo | Função |
|---------|--------|
| `iniciar_24_7.bat` | Inicia o servidor e reinicia se cair |
| `iniciar_24_7.ps1` | PowerShell com logging detalhado |
| `agendar_24_7.bat` | Agenda para iniciar automaticamente |
| `server_24_7.log` | Log detalhado (criado automaticamente) |

---

## ✅ Verificar se está online

Abra seu navegador e acesse:
```
http://localhost:5000
```

Se aparecer o Dashboard = **Rodando com sucesso!** 🎉

---

## 🛑 Parar o servidor

Clique no console **Ctrl+C** ou feche a janela.

Será reiniciado em 5 segundos automaticamente!

---

## 📊 Acessar de outro PC (mesma rede WiFi)

```
http://192.168.20.157:5000
```

Pronto! Qualquer pessoa na sua rede consegue usar!

---

**Última atualização:** 7 de abril de 2026
