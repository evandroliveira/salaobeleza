# 📋 Guia de Uso - Sistema de Agendamento Salão Beauty

## 🚀 Inicializando o Sistema

### Passo 1: Instalar Dependências
```bash
cd c:\projetos\salao
pip install -r requirements.txt
```

### Passo 2: Executar a Aplicação
```bash
python run.py
```

A aplicação estará disponível em: **http://localhost:5000**

---

## 👤 Login

### Credenciais Padrão - Proprietário (Admin)
- **Email:** `admin@salao.com`
- **Senha:** `admin123`

### Primeiro Acesso
1. Vá para http://localhost:5000
2. Clique em **"Login"**
3. Digite as credenciais acima
4. Você será direcionado para o **Dashboard Admin**

---

## 👥 Para Clientes

### 1️⃣ Criar Nova Conta
1. Clique em **"Registro"** na página inicial
2. Selecione tipo de usuário: **Cliente**
3. Preencha seus dados
4. Clique em **"Cadastrar"**

### 2️⃣ Agendar um Serviço
1. Faça login com sua conta
2. Clique em **"Novo Agendamento"**
3. Selecione o serviço desejado
4. Escolha data e hora (sem conflitos)
5. Adicione notas (opcional)
6. Clique em **"Confirmar Agendamento"**

### 3️⃣ Visualizar Agendamentos
- Todos os seus agendamentos aparecem no **Dashboard**
- Veja status (Confirmado, Realizado, Cancelado)

### 4️⃣ Cancelar Agendamento
- Clique no botão **"Cancelar"** ao lado do agendamento
- Apenas agendamentos confirmados podem ser cancelados

### 5️⃣ Atualizar Perfil
- Clique em **"Meu Perfil"**
- Atualize suas informações
- Clique em **"Salvar Alterações"**

---

## 👩‍💼 Para Proprietários (Admin)

### 📊 Dashboard Admin
Acesso rápido para:
- Total de clientes
- Agendamentos confirmados
- Serviços ativos
- Próximos 7 dias de agendamentos

### 👥 Gerenciar Clientes

#### Listar Clientes
- Clique em **"Clientes"** no menu
- Visualize todos os clientes cadastrados

#### Adicionar Cliente
1. Clique em **"+ Novo Cliente"**
2. Preencha todos os dados
3. Clique em **"Cadastrar"**

#### Editar Cliente
1. Clique em **"Editar"** ao lado do cliente
2. Altere os dados necessários
3. Clique em **"Salvar Alterações"**

#### Deletar Cliente
1. Clique em **"Deletar"** (com confirmação)
2. Cliente e seus agendamentos serão removidos

### 💇 Gerenciar Serviços

#### Listar Serviços
- Clique em **"Serviços"** no menu

#### Criar Serviço
1. Clique em **"+ Novo Serviço"**
2. Preencha os dados:
   - **Nome:** Nome do serviço
   - **Descrição:** Detalhes
   - **Preço:** Valor em R$
   - **Duração:** Em minutos (ex: 240 para 4 horas)
3. Clique em **"Cadastrar"**

#### ⏱️ Serviços Padrão
- **Escova Progressiva:** 240 minutos (4 horas)
- **Mechas:** 240 minutos (4 horas)

#### Editar Serviço
1. Clique em **"Editar"**
2. Altere os dados
3. Marque/desmarque "Ativo" se necessário
4. Clique em **"Salvar Alterações"**

#### Deletar Serviço
1. Clique em **"Deletar"** com confirmação
2. Serviço será removido

### 🛍️ Gerenciar Produtos

#### Listar Produtos
- Clique em **"Produtos"** no menu

#### Adicionar Produto
1. Clique em **"+ Novo Produto"**
2. Preencha:
   - Nome, Descrição
   - Categoria (ex: Xampus, Condicionadores)
   - Preço
   - Quantidade em estoque
3. Clique em **"Cadastrar"**

#### Editar Produto
1. Clique em **"Editar"**
2. Atualize informações
3. Clique em **"Salvar Alterações"**

#### Deletar Produto
1. Clique em **"Deletar"** com confirmação

### 📅 Gerenciar Agendamentos

#### Visualizar Agendamentos
- Clique em **"Agendamentos"**
- Use filtros: Todos, Confirmados, Realizados, Cancelados

#### Editar Agendamento
1. Clique em **"Editar"** ao lado do agendamento
2. Você pode alterar:
   - Cliente (visualizar)
   - Serviço
   - Data e hora (com validação de conflito)
   - Status (Confirmado, Realizado, Cancelado)
   - Notas
3. Clique em **"Salvar Alterações"**

#### Deletar Agendamento
1. Clique em **"Deletar"** com confirmação

---

## ⚠️ Validações Importantes

### Conflito de Horários
O sistema **impede automaticamente** agendamentos que:
- Se sobrepõem com outros já marcados
- Não respeitam o tempo de duração do serviço

**Exemplo:**
- Serviço de Escova Progressiva: 4 horas (13:00 - 17:00)
- Sistema bloqueia agendamentos de 12:00 até 17:00 para essa cliente

### Datas
- Apenas datas futuras podem ser agendadas
- Data mínima é sempre o dia seguinte

---

## 🔐 Segurança

✅ **Senhas:** Criptografadas com Werkzeug  
✅ **Sessões:** Identificação de usuário por sessão  
✅ **Permissões:** Cada tipo de usuário tem acesso específico  
✅ **Validação:** Todos os dados são validados

---

## 🐛 Troubleshooting

### A aplicação não inicia
```bash
# Verifique se as dependências estão instaladas
pip install -r requirements.txt

# Verifique a porta 5000
# Se estiver em uso, edite run.py e mude para outra porta
```

### Erro de banco de dados
```bash
# Delete o arquivo salao.db (será recriado)
del salao.db

# Execute novamente
python run.py
```

### Esqueça a senha admin
```bash
# Delete salao.db e execute novamente
# As credenciais padrão serão recriadas
```

---

## 📞 Contato & Suporte

Para dúvidas sobre Flask: https://flask.palletsprojects.com/  
Para dúvidas sobre SQLAlchemy: https://docs.sqlalchemy.org/

---

**Versão:** 1.0.0  
**Última Atualização:** 14 de Novembro de 2024
