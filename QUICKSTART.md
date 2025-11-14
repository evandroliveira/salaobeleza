# ⚡ Quick Start - 5 Minutos

## 1️⃣ Instalar (30 segundos)
```bash
cd c:\projetos\salao
pip install -r requirements.txt
```

## 2️⃣ Executar (10 segundos)
```bash
python run.py
```

## 3️⃣ Abrir no Navegador (5 segundos)
```
http://localhost:5000
```

## 4️⃣ Login Admin
```
Email: admin@salao.com
Senha: admin123
```

---

## 🎯 O Que Fazer Primeiro

### Como Admin
1. ✅ Vá para **Serviços** → Veja os serviços pré-cadastrados
2. ✅ Clique em **Clientes** → Cadastre alguns clientes
3. ✅ Clique em **Agendamentos** → Veja agendamentos (vazio no início)
4. ✅ Clique em **Relatórios** → Veja estatísticas

### Como Cliente (Nova Conta)
1. ✅ Clique em **Registro**
2. ✅ Preencha dados → Selecione **Cliente**
3. ✅ Faça **Login** com sua conta
4. ✅ Clique em **Novo Agendamento**
5. ✅ Escolha serviço, data e hora
6. ✅ Confirme!

---

## 📱 Acessar a API

Abra seu navegador em:
```
http://localhost:5000/api/v1/estatisticas
```

Você verá um JSON com estatísticas do sistema!

---

## 🔑 Funções Principais

| Função | Admin | Cliente |
|--------|-------|---------|
| Ver Agendamentos | ✅ Todos | ✅ Seus |
| Criar Agendamento | ✅ | ✅ |
| Editar Agendamento | ✅ | ❌ |
| Cancelar Agendamento | ✅ | ✅ Confirmados |
| Gerenciar Clientes | ✅ | ❌ |
| Gerenciar Serviços | ✅ | ❌ |
| Ver Relatórios | ✅ | ❌ |

---

## ⚠️ Importante!

⏰ **Escova Progressiva** = 4 horas  
⏰ **Mechas** = 4 horas

Se agendar Escova de 14:00-18:00, NÃO PODE agendar outro serviço de 13:00-18:00!

---

## 🛠️ Troubleshooting

### Erro ao iniciar?
```bash
# Delete o banco antigo
del salao.db

# Tente novamente
python run.py
```

### Porta já em uso?
Edite `run.py` linha 58:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude para 5001
```

### Esqueceu a senha?
Delete `salao.db` e reinicie. Admin será recriado.

---

## 📚 Mais Informações

- **Documentação Completa:** README.md
- **Guia de Uso:** GUIA_USO.md
- **Documentação Técnica:** TECNICO.md
- **API REST:** API.md

---

**Pronto! Seu salão está online! 🎉**
