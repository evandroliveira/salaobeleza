# 🚀 Deploy Rápido - Passo-a-Passo

## ⚡ Versão Rápida (5 minutos)

### Passo 1: Instalar Git
```
https://git-scm.com/download/win
```

### Passo 2: Criar conta GitHub
```
https://github.com/signup
```

### Passo 3: Iniciar Git no projeto
```powershell
cd c:\projetos\salao
git init
git add .
git commit -m "Initial commit"
```

### Passo 4: Enviar para GitHub
1. Acesse: https://github.com/new
2. Crie repositório: `salao-agendamento`
3. Execute:
```powershell
git remote add origin https://github.com/SEU_USUARIO/salao-agendamento.git
git branch -M main
git push -u origin main
```

### Passo 5: Deploy no Render
1. Acesse: https://dashboard.render.com (crie conta)
2. Clique: **New +** → **Web Service**
3. Selecione seu repositório GitHub
4. Preencha:
   - **Name**: salao-agendamento
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
5. Em **Environment**, adicione:
   - `FLASK_ENV=production`
   - `SECRET_KEY=seu-valor-aleatorio-aqui`
6. Clique **Deploy**

### Passo 6: Criar Banco (IMPORTANTE!)
1. No Render, crie novo PostgreSQL:
   - Clique: **New +** → **PostgreSQL**
   - **Name**: salao-db
   - Clique **Create Database**
2. Copie a **Internal Database URL**
3. No Web Service, adicione variável:
   - `DATABASE_URL=seu-valor-aqui`
4. Clique **Deploy** novamente

### Pronto! 🎉
Seu app está online em: `https://salao-agendamento.onrender.com`

---

## 🔐 Gerar SECRET_KEY Segura

Execute no PowerShell:
```powershell
C:/Users/evand/AppData/Local/Programs/Python/Python314/python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado e coloque em `FLASK_ENV` no Render.

---

## 🆘 Se der erro no Deploy

### 1. Verificar logs
- No Render, clique em **Logs**
- Procure por mensagens de erro

### 2. Erros comuns

| Erro | Solução |
|------|---------|
| ModuleNotFoundError | Verificar `requirements.txt` |
| DATABASE_URL not found | Adicionar variável ambiente |
| Connection refused | Aguarde banco inicializar |

### 3. Reiniciar serviço
- Dashboard do Render
- Clique **Manual Deploy** → **Latest Commit**

---

## 📱 Testar App Online

1. Acesse: `https://seu-app.onrender.com`
2. Login: `admin@salao.com` / `admin123`
3. Teste agendamento

---

## 📚 Links Úteis

- [Documentação Render](https://render.com/docs)
- [Render Deploy Flask](https://render.com/docs/deploy-flask)
- [PostgreSQL Free Tier](https://render.com/docs/databases)

---

## 💡 Dicas

✅ Use **Render** - é o mais fácil  
✅ PostgreSQL é melhor que SQLite  
✅ Guarde sua `DATABASE_URL` com segurança  
✅ Mude o SECRET_KEY sempre em produção  
✅ Tome backup antes de atualizar  

---

**Pronto para ir ao ar? Comece pelo Passo 1! 🚀**
