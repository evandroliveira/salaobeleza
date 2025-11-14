# 🛠️ Documentação Técnica - Sistema Salão Beauty

## 📁 Estrutura do Projeto

```
salao/
├── app/
│   ├── __init__.py              # Inicialização da aplicação
│   ├── models/                  # Modelos de dados (ORM)
│   │   ├── __init__.py
│   │   ├── db.py               # Configuração do banco de dados
│   │   ├── usuario.py          # Modelo de usuários
│   │   ├── cliente.py          # Modelo de clientes
│   │   ├── servico.py          # Modelo de serviços
│   │   ├── produto.py          # Modelo de produtos
│   │   └── agendamento.py      # Modelo de agendamentos
│   ├── controllers/             # Lógica de negócio (Controllers)
│   │   ├── __init__.py
│   │   ├── main.py             # Rotas principais
│   │   ├── auth.py             # Autenticação
│   │   ├── cliente.py          # Funções do cliente
│   │   └── admin.py            # Funções do administrador
│   ├── views/                   # Templates HTML (Views)
│   │   ├── base.html           # Template base
│   │   ├── index.html          # Página inicial
│   │   ├── sobre.html          # Página sobre
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── registro.html
│   │   ├── cliente/
│   │   │   ├── dashboard.html
│   │   │   ├── agendar.html
│   │   │   └── perfil.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── clientes/
│   │       │   ├── listar.html
│   │       │   ├── cadastrar.html
│   │       │   └── editar.html
│   │       ├── servicos/
│   │       │   ├── listar.html
│   │       │   ├── cadastrar.html
│   │       │   └── editar.html
│   │       ├── produtos/
│   │       │   ├── listar.html
│   │       │   ├── cadastrar.html
│   │       │   └── editar.html
│   │       └── agendamentos/
│   │           ├── listar.html
│   │           └── editar.html
│   └── static/                  # Arquivos estáticos
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── run.py                       # Arquivo de execução principal
├── requirements.txt             # Dependências Python
├── salao.db                     # Banco de dados SQLite (criado automaticamente)
├── README.md                    # Documentação principal
└── GUIA_USO.md                 # Guia de uso
```

## 🗄️ Banco de Dados

### Tabelas

#### usuarios
```sql
id (PK) | nome | email (UNIQUE) | senha | telefone | tipo | data_criacao | ativo
```

#### clientes
```sql
id (PK) | nome | email | telefone | data_nascimento | endereco | cidade | usuario_id (FK) | data_criacao | ativo
```

#### servicos
```sql
id (PK) | nome (UNIQUE) | descricao | preco | duracao_minutos | ativo | data_criacao
```

#### produtos
```sql
id (PK) | nome (UNIQUE) | descricao | preco | quantidade | categoria | ativo | data_criacao
```

#### agendamentos
```sql
id (PK) | cliente_id (FK) | servico_id (FK) | data_agendamento | data_criacao | status | notas | valor_total
```

## 🔐 Autenticação

### Fluxo de Login
1. Usuário acessa `/auth/login`
2. Credenciais são validadas contra banco de dados
3. Se válidas, `session['usuario_id']` é criada
4. Redirecionamento baseado em `session['usuario_tipo']`
   - `cliente` → `/cliente/dashboard`
   - `proprietaria` → `/admin/dashboard`

### Decoradores de Proteção
```python
@login_required      # Verifica se usuário está logado
@cliente_required    # Verifica se é cliente
@admin_required      # Verifica se é proprietário
```

## 🗺️ Rotas (Routes/Endpoints)

### Autenticação (`/auth`)
- `GET/POST /auth/registro` - Registrar novo usuário
- `GET/POST /auth/login` - Fazer login
- `GET /auth/logout` - Desconectar

### Cliente (`/cliente`)
- `GET /cliente/dashboard` - Dashboard do cliente
- `GET/POST /cliente/agendar` - Novo agendamento
- `GET/POST /cliente/perfil` - Editar perfil
- `POST /cliente/cancelar/<id>` - Cancelar agendamento

### Admin (`/admin`)
- `GET /admin/dashboard` - Dashboard admin

**Clientes:**
- `GET /admin/clientes` - Listar clientes
- `GET/POST /admin/clientes/cadastrar` - Novo cliente
- `GET/POST /admin/clientes/<id>/editar` - Editar cliente
- `POST /admin/clientes/<id>/deletar` - Deletar cliente

**Serviços:**
- `GET /admin/servicos` - Listar serviços
- `GET/POST /admin/servicos/cadastrar` - Novo serviço
- `GET/POST /admin/servicos/<id>/editar` - Editar serviço
- `POST /admin/servicos/<id>/deletar` - Deletar serviço

**Produtos:**
- `GET /admin/produtos` - Listar produtos
- `GET/POST /admin/produtos/cadastrar` - Novo produto
- `GET/POST /admin/produtos/<id>/editar` - Editar produto
- `POST /admin/produtos/<id>/deletar` - Deletar produto

**Agendamentos:**
- `GET /admin/agendamentos` - Listar agendamentos (com filtro)
- `GET/POST /admin/agendamentos/<id>/editar` - Editar agendamento
- `POST /admin/agendamentos/<id>/deletar` - Deletar agendamento

## ⏱️ Validação de Conflitos

### Função: `verificar_conflito_horario()`
```python
def verificar_conflito_horario(data_agendamento, duracao_minutos):
    hora_fim = data_agendamento + timedelta(minutes=duracao_minutos)
    
    # Busca agendamentos não-cancelados que se sobrepõem
    agendamentos = Agendamento.query.filter(
        Agendamento.status != 'cancelado',
        Agendamento.data_agendamento < hora_fim,
        Agendamento.get_hora_fim() > data_agendamento
    ).all()
    
    return len(agendamentos) > 0
```

### Exemplos de Conflito
**Cenário 1:** Escova Progressiva 13:00-17:00
- ❌ Novo agendamento 14:00-15:00 = CONFLITO
- ❌ Novo agendamento 12:00-14:00 = CONFLITO
- ✅ Novo agendamento 17:00-18:00 = OK

**Cenário 2:** Mechas 10:00-14:00
- ❌ Novo agendamento 09:00-11:00 = CONFLITO
- ✅ Novo agendamento 14:00-16:00 = OK

## 🎨 Frontend

### Bootstrap 5
- Framework CSS responsivo
- Componentes prontos (navbar, cards, tabelas, forms)
- Tema personalizado com `style.css`

### Jinja2 Templates
- Herança de templates (`extends`, `blocks`)
- Iteração sobre dados (`for`, `if`)
- Filtros (`strftime`, `format`)

### CSS Customizado
- Variáveis CSS para cores
- Media queries para responsividade
- Transições e animações suaves

## 🔄 Fluxo de Dados

### Criar Agendamento (Cliente)
1. Cliente acessa `/cliente/agendar` (GET)
2. Lista de serviços é carregada
3. Cliente preenche formulário e submete (POST)
4. Servidor valida dados e conflitos
5. Agendamento é criado em banco de dados
6. Redirecionamento para dashboard com mensagem de sucesso

### Gerenciar Agendamento (Admin)
1. Admin acessa `/admin/agendamentos`
2. Lista filtrada por status é exibida
3. Admin clica em "Editar" para um agendamento
4. Formulário é preenchido com dados atuais
5. Admin altera dados necessários
6. Validação ocorre antes de salvar
7. Agendamento é atualizado ou erro é exibido

## 📊 Padrões de Projeto

### MVC (Model-View-Controller)
- **Models:** `app/models/` - Definição de estruturas de dados
- **Views:** `app/views/` - Templates HTML
- **Controllers:** `app/controllers/` - Lógica de roteamento e negócio

### Blueprints (Flask)
Cada área funcional é um Blueprint separado:
- `auth_bp` - Autenticação
- `cliente_bp` - Funções de cliente
- `admin_bp` - Funções de admin
- `main_bp` - Páginas gerais

## 🔐 Segurança

### Criptografia de Senhas
```python
from werkzeug.security import generate_password_hash, check_password_hash

usuario.set_password(senha)        # Hash e armazena
usuario.check_password(senha_user) # Valida contra hash
```

### Proteção de Sessão
```python
session['usuario_id']    # ID do usuário logado
session['usuario_tipo']  # Tipo: cliente ou proprietaria
session['usuario_nome']  # Nome para exibição
```

### Validação de Requisições
- Uso de `@login_required` para autenticação
- Tipo de usuário verificado em cada rota
- CSRF protection padrão do Flask

## 📈 Escalabilidade

### Futuras Melhorias
1. **Pagination** - Para listas grandes
2. **Search/Filter** - Busca avançada
3. **Reports** - Relatórios e gráficos
4. **Email Notifications** - Lembretes por email
5. **SMS** - Confirmações por SMS
6. **Payment Integration** - Pagamento online
7. **APIs REST** - Endpoints para integração
8. **Mobile App** - Versão mobile

## 🧪 Testes

### Teste Manual
1. Criar usuário cliente
2. Criar usuário proprietário
3. Admin cadastra serviços
4. Cliente agenda serviço
5. Validar conflito de horário
6. Admin visualiza agendamento
7. Admin edita agendamento

### Teste de Conflito
1. Agendar Escova Progressiva: 14:00-18:00
2. Tentar agendar no mesmo horário: 15:00-16:00
3. Verificar mensagem de erro

## 📝 Convenções de Código

- **Nomes em português:** Para clareza no contexto brasileiro
- **Type Hints:** Opcional mas recomendado em futuras versões
- **Docstrings:** Em funções importantes
- **PEP 8:** Padrão Python de formatação

---

**Versão:** 1.0.0  
**Última Atualização:** 14 de Novembro de 2024
