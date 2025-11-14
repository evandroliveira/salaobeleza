# 🚀 Guia de Deploy - Subindo Online

## Opções de Hosting (Recomendadas)

### 1️⃣ **Render (MAIS FÁCIL - RECOMENDADO)**
- ✅ Gratuito com plano hobby
- ✅ Deploy automático via GitHub
- ✅ Suporte a PostgreSQL
- ✅ SSL/HTTPS automático
- ✅ Muito fácil para iniciantes

### 2️⃣ **Heroku**
- ✅ Deploy rápido
- ✅ Banco de dados PostgreSQL
- ⚠️ Plano gratuito descontinuado (pago a partir de $7/mês)

### 3️⃣ **PythonAnywhere**
- ✅ Especializado em Python/Flask
- ✅ Plano gratuito disponível
- ✅ Fácil configuração

### 4️⃣ **Railway / Replit**
- ✅ Modernas
- ✅ Gratuitas com limites

---

## 📋 Pré-requisitos

```bash
# 1. Instalar Git
https://git-scm.com/download/win

# 2. Criar conta no GitHub
https://github.com/signup

# 3. Criar conta no Render
https://dashboard.render.com
```

---

## ✅ PASSO 1: Preparar Projeto Localmente

### 1.1 Criar arquivo `Procfile`
Na raiz do projeto (c:\projetos\salao):

```
web: gunicorn run:app
```

### 1.2 Atualizar `requirements.txt`
Adicionar gunicorn (servidor de produção):

```txt
flask==3.0.0
flask-sqlalchemy==3.1.1
werkzeug==3.0.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### 1.3 Criar arquivo `.gitignore`
Na raiz do projeto:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
instance/
.env
*.db
*.sqlite
*.sqlite3
.DS_Store
salao.db
```

### 1.4 Atualizar `run.py` para Produção

**IMPORTANTE**: Modifique o arquivo `run.py`:

```python
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Determinar se está em produção
    debug = os.getenv('FLASK_ENV') != 'production'
    port = int(os.getenv('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=debug)
```

### 1.5 Atualizar config do app no `app/__init__.py`

Adicione suporte a banco de dados em produção:

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    
    # Configuração do banco de dados
    if os.getenv('DATABASE_URL'):
        # PostgreSQL em produção
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')
    else:
        # SQLite em desenvolvimento
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salao.db'
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-mude-em-producao')
    
    db.init_app(app)
    
    # ... resto do código
```

---

## 📤 PASSO 2: Upload para GitHub

### 2.1 Inicializar Git (primeira vez)

```powershell
cd c:\projetos\salao
git init
git add .
git commit -m "Initial commit - Sistema de agendamento para salão"
```

### 2.2 Criar repositório no GitHub

1. Acesse https://github.com/new
2. Nome do repositório: `salao-agendamento` (ou outro nome)
3. Descrição: `Sistema de agendamento para salão de beleza`
4. Escolha: **Public** ou **Private**
5. Clique em **Create repository**

### 2.3 Conectar ao repositório

```powershell
git remote add origin https://github.com/SEU_USUARIO/salao-agendamento.git
git branch -M main
git push -u origin main
```

⚠️ Será pedido login - use **GitHub Credentials** ou **Personal Access Token**

---

## 🌐 PASSO 3: Deploy no Render (RECOMENDADO)

### 3.1 Criar novo Web Service

1. Acesse https://dashboard.render.com
2. Clique em **New +** → **Web Service**
3. Selecione **Connect a repository**
4. Busque: `salao-agendamento`
5. Clique em **Connect**

### 3.2 Configurar serviço

| Campo | Valor |
|-------|-------|
| **Name** | salao-agendamento |
| **Environment** | Python 3 |
| **Region** | USA (São Paulo se disponível) |
| **Branch** | main |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn run:app` |

### 3.3 Adicionar variáveis de ambiente

Clique em **Environment** e adicione:

```
FLASK_ENV=production
SECRET_KEY=sua-chave-segura-aqui-mude-isto
```

Para gerar chave segura:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3.4 Criar banco de dados PostgreSQL

1. No Render, clique em **New +** → **PostgreSQL**
2. Nome: `salao-db`
3. Deixe as outras opções padrão
4. Clique em **Create Database**

### 3.5 Copiar URL do banco

1. Acesse o banco criado
2. Copie a **Internal Database URL**
3. No Web Service, adicione ambiente:

```
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
```

### 3.6 Iniciar deploy

1. Clique em **Deploy**
2. Acompanhe os logs
3. Pronto! Seu app está online em: `https://salao-agendamento.onrender.com`

---

## 🔄 PASSO 4: Deploy no Heroku (Alternativa)

### 4.1 Instalar Heroku CLI

```powershell
# Baixar em: https://devcenter.heroku.com/articles/heroku-cli
choco install heroku-cli
# ou download direto
```

### 4.2 Login no Heroku

```powershell
heroku login
```

### 4.3 Criar app no Heroku

```powershell
cd c:\projetos\salao
heroku create salao-agendamento
```

### 4.4 Adicionar banco PostgreSQL

```powershell
heroku addons:create heroku-postgresql:mini
```

### 4.5 Deploy

```powershell
git push heroku main
```

### 4.6 Executar migrações

```powershell
heroku run python run.py
```

---

## 🔧 PASSO 5: Configurações Finais

### 5.1 Alterar SECRET_KEY (CRÍTICO!)

Gere uma chave segura:

```powershell
C:/Users/evand/AppData/Local/Programs/Python/Python314/python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado e coloque nas variáveis de ambiente da plataforma.

### 5.2 Ativar HTTPS

- **Render**: Automático ✅
- **Heroku**: Automático ✅
- **PythonAnywhere**: Configurar no painel

### 5.3 Inicializar Banco em Produção

Execute este comando UMA VEZ após o deploy:

```bash
# No terminal do seu servidor
python -c "from app import create_app, db; app = create_app(); with app.app_context(): db.create_all(); print('Banco criado!')"
```

---

## 📱 PASSO 6: Testar Online

1. Acesse: `https://seu-app.onrender.com` (ou Heroku)
2. Faça login com: `admin@salao.com` / `admin123`
3. Teste as funcionalidades

---

## 🚨 Checklist de Segurança

- [ ] SECRET_KEY alterada e segura
- [ ] DEBUG=False em produção
- [ ] HTTPS ativado
- [ ] Banco de dados PostgreSQL (não SQLite)
- [ ] Variáveis sensíveis em environment variables
- [ ] .gitignore com `*.db` e `.env`
- [ ] Senha admin alterada
- [ ] Backup do banco configurado

---

## 📊 Estrutura do Deploy

```
GitHub Repository
    ↓
Render / Heroku (CI/CD)
    ↓
Build (pip install)
    ↓
Deploy (gunicorn)
    ↓
PostgreSQL Database
    ↓
APP ONLINE! 🎉
```

---

## 🔗 URLs Úteis

| Serviço | URL |
|---------|-----|
| Render | https://dashboard.render.com |
| Heroku | https://dashboard.heroku.com |
| GitHub | https://github.com |
| PostgreSQL Docs | https://www.postgresql.org/docs/ |

---

## 💡 Dicas Importantes

1. **Primeiro deploy é o mais importante**
   - Tome seu tempo
   - Verifique cada passo
   - Leia os logs se houver erro

2. **Banco de dados**
   - SQLite NÃO funciona bem em produção
   - Use PostgreSQL
   - Faça backups regulares

3. **Variáveis de ambiente**
   - NUNCA coloque senhas no código
   - Use environment variables
   - Diferentes configs para dev e prod

4. **Monitoramento**
   - Configure alertas
   - Monitore logs regularmente
   - Acompanhe performance

5. **Atualizações**
   - Faça deploy via GitHub (pull)
   - Teste em desenvolvimento primeiro
   - Tenha rollback pronto

---

## ❓ Troubleshooting

### Erro: "ModuleNotFoundError"
- Verificar `requirements.txt`
- Rodar `pip install -r requirements.txt` localmente
- Fazer novo commit e push

### Erro: "Database connection refused"
- Verificar `DATABASE_URL`
- Confirmar banco está criado
- Revisar credenciais

### Erro: "SECRET_KEY not found"
- Adicionar variável de ambiente
- Reiniciar o serviço
- Verificar no painel de config

### App lento
- Usar PostgreSQL em vez de SQLite
- Adicionar índices no banco
- Ativar caching
- Considerar upgrade de plano

---

## 🎯 Próximos Passos

1. ✅ Preparar projeto
2. ✅ Subir para GitHub
3. ✅ Fazer deploy no Render/Heroku
4. ✅ Testar aplicação online
5. ✅ Configurar domínio próprio (opcional)
6. ✅ Configurar email (opcional)
7. ✅ Monitore performance

---

## 📞 Suporte

Se tiver dúvidas durante o deploy:

1. Verifique os logs da plataforma
2. Busque o erro no Google
3. Consulte documentação oficial
4. Pergunte em comunidades (Stack Overflow, Reddit)

---

**Seu app estará online em minutos! 🚀**

Escolha uma plataforma acima e comece!
