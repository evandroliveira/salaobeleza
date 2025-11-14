# 📊 Mapa Visual do Sistema

## 🌍 Rotas da Aplicação

### Públicas
```
GET  /                    → Página inicial
GET  /sobre              → Página sobre
GET  /auth/login         → Login
GET  /auth/registro      → Registro
GET  /auth/logout        → Logout
```

### Cliente (Autenticado)
```
GET  /cliente/dashboard              → Meus agendamentos
GET  /cliente/agendar                → Novo agendamento
POST /cliente/agendar                → Criar agendamento
GET  /cliente/perfil                 → Meu perfil
POST /cliente/perfil                 → Atualizar perfil
POST /cliente/cancelar/<id>          → Cancelar agendamento
```

### Admin (Autenticado + Proprietário)
```
GET  /admin/dashboard                → Dashboard principal

CLIENTES:
GET    /admin/clientes               → Listar
GET    /admin/clientes/cadastrar     → Formulário novo
POST   /admin/clientes/cadastrar     → Criar
GET    /admin/clientes/<id>/editar   → Formulário editar
POST   /admin/clientes/<id>/editar   → Atualizar
POST   /admin/clientes/<id>/deletar  → Deletar

SERVIÇOS:
GET    /admin/servicos               → Listar
GET    /admin/servicos/cadastrar     → Formulário novo
POST   /admin/servicos/cadastrar     → Criar
GET    /admin/servicos/<id>/editar   → Formulário editar
POST   /admin/servicos/<id>/editar   → Atualizar
POST   /admin/servicos/<id>/deletar  → Deletar

PRODUTOS:
GET    /admin/produtos               → Listar
GET    /admin/produtos/cadastrar     → Formulário novo
POST   /admin/produtos/cadastrar     → Criar
GET    /admin/produtos/<id>/editar   → Formulário editar
POST   /admin/produtos/<id>/editar   → Atualizar
POST   /admin/produtos/<id>/deletar  → Deletar

AGENDAMENTOS:
GET    /admin/agendamentos           → Listar (com filtros)
GET    /admin/agendamentos/<id>/editar → Formulário editar
POST   /admin/agendamentos/<id>/editar → Atualizar
POST   /admin/agendamentos/<id>/deletar → Deletar

RELATÓRIOS:
GET    /admin/relatorios             → Estatísticas
```

### API REST
```
GET    /api/v1/clientes                          → JSON
GET    /api/v1/clientes/<id>                     → JSON
GET    /api/v1/servicos                          → JSON
GET    /api/v1/servicos/<id>                     → JSON
GET    /api/v1/agendamentos                      → JSON
GET    /api/v1/agendamentos/<id>                 → JSON
POST   /api/v1/agendamentos/validar-horario      → JSON
GET    /api/v1/estatisticas                      → JSON
```

## 📊 Fluxo de Dados

### Novo Agendamento (Cliente)
```
Cliente
   ↓
[Clica em "Novo Agendamento"]
   ↓
GET /cliente/agendar
   ↓
[Carrega lista de serviços]
   ↓
[Preenche formulário]
   ↓
POST /cliente/agendar
   ↓
[Valida dados no servidor]
   ↓
[Checa conflito de horários]
   ↓
IF conflito THEN erro ELSE criar
   ↓
[Salva no banco de dados]
   ↓
[Redireciona para dashboard]
```

### Editar Agendamento (Admin)
```
Admin
   ↓
[Clica em "Editar" no agendamento]
   ↓
GET /admin/agendamentos/<id>/editar
   ↓
[Carrega dados atuais]
   ↓
[Carrega lista de serviços]
   ↓
[Preenche formulário]
   ↓
POST /admin/agendamentos/<id>/editar
   ↓
[Valida dados]
   ↓
[Se data mudou, checa conflito]
   ↓
IF conflito THEN erro ELSE atualizar
   ↓
[Salva alterações]
   ↓
[Redireciona para listagem]
```

## 💾 Modelo de Dados Relacional

```
┌─────────────────────────────────┐
│         USUARIO                 │
├─────────────────────────────────┤
│ PK: id                          │
│ nome (string)                   │
│ email (unique)                  │
│ senha (hash)                    │
│ tipo (cliente/proprietaria)     │
│ data_criacao (datetime)         │
│ ativo (boolean)                 │
└─────────────────────────────────┘
         ↑
         │ 1:N
         │
┌─────────────────────────────────┐
│        CLIENTE                  │
├─────────────────────────────────┤
│ PK: id                          │
│ nome                            │
│ email                           │
│ telefone                        │
│ data_nascimento (opcional)      │
│ endereco                        │
│ cidade                          │
│ FK: usuario_id (opcional)       │
│ data_criacao                    │
│ ativo                           │
└─────────────────────────────────┘
         ↑
         │ 1:N
         │
    ┌────┴────┬────────────────┐
    │         │                │
    │    ┌────────────────────────────┐
    │    │    AGENDAMENTO           │
    │    ├────────────────────────────┤
    │    │ PK: id                     │
    │    │ FK: cliente_id      ───────┤──┐
    │    │ FK: servico_id      ───────┤──┼──┐
    │    │ data_agendamento           │  │  │
    │    │ data_criacao               │  │  │
    │    │ status                     │  │  │
    │    │ notas                      │  │  │
    │    │ valor_total                │  │  │
    │    └────────────────────────────┘  │  │
    │                                     │  │
    └─────────────────────────────────────┘  │
                                             │
                        ┌────────────────────┘
                        │
                   ┌────────────────────┐
                   │     SERVICO        │
                   ├────────────────────┤
                   │ PK: id             │
                   │ nome (unique)      │
                   │ descricao          │
                   │ preco              │
                   │ duracao_minutos    │
                   │ ativo              │
                   │ data_criacao       │
                   └────────────────────┘

┌────────────────────┐
│     PRODUTO        │
├────────────────────┤
│ PK: id             │
│ nome (unique)      │
│ descricao          │
│ preco              │
│ quantidade         │
│ categoria          │
│ ativo              │
│ data_criacao       │
└────────────────────┘
```

## 🎨 Estrutura de Pastas do Frontend

```
views/
├── base.html                   # Template master (herança)
├── index.html                  # Página inicial
├── sobre.html                  # Página sobre
│
├── auth/
│   ├── login.html
│   └── registro.html
│
├── cliente/
│   ├── dashboard.html          # Mostra agendamentos
│   ├── agendar.html            # Formulário novo
│   └── perfil.html             # Editar perfil
│
└── admin/
    ├── dashboard.html           # Resumo geral
    ├── relatorios.html          # Estatísticas
    │
    ├── clientes/
    │   ├── listar.html
    │   ├── cadastrar.html
    │   └── editar.html
    │
    ├── servicos/
    │   ├── listar.html
    │   ├── cadastrar.html
    │   └── editar.html
    │
    ├── produtos/
    │   ├── listar.html
    │   ├── cadastrar.html
    │   └── editar.html
    │
    └── agendamentos/
        ├── listar.html
        └── editar.html
```

## 🔄 Ciclo de Vida de um Agendamento

```
Estado: CONFIRMADO
├─ Cliente agenda serviço
├─ Admin recebe
├─ Aparece na listagem
│
Estado: REALIZADO
├─ Admin marca como realizado
├─ Serviço foi prestado
├─ Gera receita
│
Estado: CANCELADO
├─ Cliente cancela (confirmado)
├─ Admin cancela
├─ Horário fica disponível
└─ NÃO gera receita
```

## 📱 Fluxo da Interface

### Homepage
```
┌─────────────────────────────────┐
│   SALÃO BEAUTY (Navbar)         │
├─────────────────────────────────┤
│                                 │
│  [Login]  [Registro]           │
│                                 │
│  ┌──────────────────────────┐  │
│  │ Bem-vindo ao Salão Beauty│  │
│  │ Agende seus serviços!    │  │
│  │ [Login] [Cadastre-se]    │  │
│  └──────────────────────────┘  │
│                                 │
│  ┌──────────────────────────┐  │
│  │ Serviços  Agendamentos   │  │
│  │ Produtos  ...            │  │
│  └──────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

### Dashboard Cliente
```
┌─────────────────────────────────┐
│   Olá, João Silva               │
├─────────────────────────────────┤
│ [Novo Agendamento] [Meu Perfil] │
│                                 │
│ ┌────────────────────────────┐  │
│ │ Meus Agendamentos:         │  │
│ ├────────────────────────────┤  │
│ │ Serviço      Data    Hora   │  │
│ │ Escova       15/11   14:00  │  │
│ │ [Cancelar]                 │  │
│ │                            │  │
│ │ Mechas       16/11   10:00  │  │
│ │ [Cancelar]                 │  │
│ └────────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

### Dashboard Admin
```
┌────────────────────────────────────┐
│   Dashboard Admin                  │
├────────────────────────────────────┤
│ [👥 Clientes] [💇 Serviços]       │
│ [🛍️ Produtos] [📅 Agendamentos]    │
│ [📊 Relatórios]                    │
│                                    │
│ ┌──────────────────────────────┐  │
│ │ Total de Clientes: 15        │  │
│ │ Agendamentos Confirmados: 8  │  │
│ │ Serviços Ativos: 4           │  │
│ └──────────────────────────────┘  │
│                                    │
│ ┌──────────────────────────────┐  │
│ │ Próximos 7 Dias              │  │
│ │ (listagem de agendamentos)   │  │
│ └──────────────────────────────┘  │
│                                    │
└────────────────────────────────────┘
```

## 🔐 Fluxo de Autenticação

```
Novo Usuário:
   GET /auth/registro
   └─ Preenche formulário
   └─ POST /auth/registro
   └─ Valida dados
   └─ Criptografa senha
   └─ Salva no banco
   └─ Redireciona para login

Login:
   GET /auth/login
   └─ Preenche credenciais
   └─ POST /auth/login
   └─ Busca usuário no banco
   └─ Verifica senha
   └─ IF válido THEN
      ├─ session['usuario_id'] = id
      ├─ session['usuario_tipo'] = tipo
      └─ Redireciona para dashboard
   └─ IF inválido THEN erro

Logout:
   GET /auth/logout
   └─ Limpa sessão
   └─ Redireciona para login
```

---

**Versão:** 1.0.0  
**Data:** 14 de Novembro de 2024
