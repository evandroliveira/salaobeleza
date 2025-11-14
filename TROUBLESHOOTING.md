# 🔧 Troubleshooting - Resolvendo Problemas

## Problemas no Deploy

### ❌ Erro: "ModuleNotFoundError: No module named 'flask'"

**Causa**: `requirements.txt` não foi enviado ou está incompleto

**Solução**:
```bash
# Verificar arquivo local
cat requirements.txt

# Deve ter:
# flask==3.0.0
# flask-sqlalchemy==3.1.1
# werkzeug==3.0.1
# gunicorn==21.2.0
# psycopg2-binary==2.9.9

# Se estiver errado:
git add requirements.txt
git commit -m "Fix: requirements.txt"
git push

# No Render, clique: Manual Deploy → Latest Commit
```

---

### ❌ Erro: "DATABASE_URL not provided"

**Causa**: Variável de ambiente não configurada

**Solução**:
1. No Render Dashboard, clique em seu Web Service
2. Vá para **Environment**
3. Verifique se `DATABASE_URL` existe
4. Se não, clique **Add Environment Variable**:
   ```
   DATABASE_URL=postgresql://...
   ```
5. Clique **Save Changes**
6. Clique **Manual Deploy**

---

### ❌ Erro: "Could not connect to database"

**Causa**: Banco de dados não foi criado ou URL está errada

**Solução**:
```bash
# 1. Verificar se banco existe no Render
#    Dashboard → PostgreSQL → Status (deve ser Available)

# 2. Copiar URL correta
#    PostgreSQL → Internal Database URL

# 3. Adicionar ao Web Service
#    Environment → DATABASE_URL = (cole a URL)

# 4. Reiniciar
#    Manual Deploy → Latest Commit
```

---

### ❌ Erro: "gunicorn: command not found"

**Causa**: Procfile errado ou gunicorn não instalado

**Solução**:
```bash
# 1. Verificar Procfile (deve existir na raiz)
cat Procfile
# Deve ter apenas: web: gunicorn run:app

# 2. Verificar requirements.txt (deve ter gunicorn)
grep gunicorn requirements.txt

# 3. Se não tiver:
echo gunicorn==21.2.0 >> requirements.txt
git add requirements.txt requirements.txt
git commit -m "Add: gunicorn"
git push
```

---

### ❌ Erro: "Secret key not set"

**Causa**: Variável `SECRET_KEY` não configurada

**Solução**:
1. Gerar chave segura:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. No Render, adicione variável:
   ```
   Key: SECRET_KEY
   Value: (cole o resultado acima)
   ```

3. Clique **Save** e **Manual Deploy**

---

## Problemas Locais

### ❌ "Python não foi encontrado"

**Causa**: Python não está no PATH

**Solução**:
Use caminho completo:
```powershell
C:/Users/evand/AppData/Local/Programs/Python/Python314/python.exe run.py
```

---

### ❌ "ModuleNotFoundError: No module named 'flask'" (local)

**Causa**: Dependências não instaladas

**Solução**:
```powershell
C:/Users/evand/AppData/Local/Programs/Python/Python314/python.exe -m pip install -r requirements.txt
```

---

### ❌ "Port 5000 already in use"

**Causa**: Outra aplicação está usando porta 5000

**Solução**:
```powershell
# Encontrar processo na porta 5000
netstat -ano | findstr :5000

# Matar processo (substitua PID pelo número)
taskkill /PID 1234 /F

# Ou usar porta diferente
C:/Users/evand/AppData/Local/Programs/Python/Python314/python.exe run.py --port 5001
```

---

## Problemas com Git

### ❌ "fatal: not a git repository"

**Causa**: Git não foi inicializado

**Solução**:
```powershell
cd c:\projetos\salao
git init
git add .
git commit -m "Initial commit"
```

---

### ❌ "fatal: remote origin already exists"

**Causa**: Remote já foi adicionado

**Solução**:
```powershell
# Remover remote antigo
git remote remove origin

# Adicionar novo
git remote add origin https://github.com/SEU_USUARIO/salao-agendamento.git
git push -u origin main
```

---

### ❌ "fatal: no changes added to commit"

**Causa**: Nenhum arquivo para commit

**Solução**:
```powershell
# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Initial commit"

# Enviar
git push -u origin main
```

---

## Problemas na Aplicação

### ❌ "Agendamento: A table could not be created"

**Causa**: Banco de dados não foi inicializado

**Solução**:
Execute no console Render:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Banco criado!")
```

---

### ❌ Login não funciona

**Causa**: Usuário admin não foi criado

**Solução**:
1. Aguarde o app inicializar completamente
2. Verifique nos logs se o admin foi criado
3. Se não, execute:
   ```python
   from app import create_app, db
   from app.models.usuario import Usuario
   
   app = create_app()
   with app.app_context():
       admin = Usuario(
           nome='Admin',
           email='admin@salao.com',
           tipo='proprietaria'
       )
       admin.set_password('admin123')
       db.session.add(admin)
       db.session.commit()
       print("Admin criado!")
   ```

---

### ❌ App muito lento

**Causa**: PostgreSQL em tier grátis é lento

**Solução**:
- Upgrade para plano pago (a partir de $5/mês)
- Ou adicione índices no banco:
  ```sql
  CREATE INDEX idx_agendamentos_data ON agendamentos(data_agendamento);
  CREATE INDEX idx_agendamentos_cliente ON agendamentos(cliente_id);
  ```

---

## Verificação de Status

### Checklist do Deploy

- [ ] Git inicializado (`git status` funciona)
- [ ] requirements.txt atualizado (`pip install -r requirements.txt` funciona)
- [ ] Procfile existe e tem: `web: gunicorn run:app`
- [ ] `.gitignore` criado
- [ ] run.py suporta PORT dinâmica
- [ ] Código enviado para GitHub (`git log` mostra commits)
- [ ] Render conectado ao GitHub
- [ ] Web Service criado e Building
- [ ] PostgreSQL criado
- [ ] DATABASE_URL adicionado
- [ ] SECRET_KEY adicionado
- [ ] FLASK_ENV=production adicionado
- [ ] Deploy completado sem erros
- [ ] App online e respondendo

---

## Logs Úteis

### Ver logs do Render

1. Dashboard → Seu Web Service
2. Clique em **Logs**
3. Procure por:
   - "Deployment successful" = OK
   - "ERROR" = problema
   - "WARNING" = atenção

### Ver logs locais

```powershell
# Executar app e ver erros
C:/Users/evand/AppData/Local/Programs/Python/Python314/python.exe run.py
```

---

## Performance

### Se app ficar lento

1. **Upgrade Render** (plano pago)
2. **Adicionar cache**:
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

3. **Otimizar queries**:
   ```python
   # Ruim
   servicos = Servico.query.all()
   
   # Bom
   servicos = Servico.query.filter_by(ativo=True).all()
   ```

4. **Adicionar índices**:
   ```sql
   CREATE INDEX idx_name ON table(column);
   ```

---

## Contactar Suporte

Se nenhuma solução funcionar:

1. **Render Support**: https://render.com/docs/support
2. **Flask Docs**: https://flask.palletsprojects.com/
3. **Stack Overflow**: Tag `flask` e `render`
4. **GitHub Issues**: Procure por issue similar

---

## Dica de Ouro 🏆

Se tudo falhar:

```powershell
# Delete tudo e comece novamente
rm -r .git
git init
git add .
git commit -m "Fresh start"
git push -u origin main
```

---

**Boa sorte! 🍀 Qualquer dúvida, consulte os logs!**
