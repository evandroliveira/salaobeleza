# 🎯 RESUMO RÁPIDO - SUBIR ONLINE

## 3 Plataformas: Escolha Uma

| Plataforma | Dificuldade | Custo | Recomendação |
|-----------|------------|-------|-------------|
| **Render** | ⭐ Fácil | Gratuito | ✅ **COMECE POR AQUI** |
| **Heroku** | ⭐ Fácil | Pago ($7+) | OK, conhecido |
| **PythonAnywhere** | ⭐⭐ Médio | Gratuito | Bom alternativa |

---

## ⚡ Render em 20 Minutos

### 1. GitHub (5 min)
```bash
# No PowerShell em c:\projetos\salao
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU_USER/salao-agendamento.git
git push -u origin main
```

### 2. Render Web Service (10 min)
- Acesse: https://dashboard.render.com
- New + → Web Service
- Selecione seu repositório GitHub
- Build: `pip install -r requirements.txt`
- Start: `gunicorn run:app`
- Add environment: `FLASK_ENV=production`
- Add environment: `SECRET_KEY=gerar_chave`

### 3. Banco PostgreSQL (5 min)
- New + → PostgreSQL
- Copie a URL
- Add na web service: `DATABASE_URL=url_copiada`
- Deploy

### 4. Teste
- Acesse: https://seu-app.onrender.com
- Login: admin@salao.com / admin123

✅ **PRONTO!**

---

## 🔐 Gerar SECRET_KEY

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado e cole em `SECRET_KEY` no Render.

---

## 📝 Arquivos Preparados

✅ **Procfile** - Deploy configurado
✅ **requirements.txt** - Dependências (com gunicorn)
✅ **.gitignore** - Segurança
✅ **run.py** - Pronto para produção
✅ **Documentação** - 4 arquivos de ajuda

---

## 🔗 Links Úteis

- Render: https://dashboard.render.com
- GitHub: https://github.com/signup
- Git: https://git-scm.com/download/win

---

## 🆘 Erros?

Leia: **TROUBLESHOOTING.md** (no seu projeto)

---

**Comece agora! 🚀 Seu app estará online em 20 minutos!**
