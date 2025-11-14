# Sistema de Agendamento para Salão de Beleza

Um sistema MVC completo para gerenciar agendamentos de um salão de beleza com áreas separadas para clientes e proprietários.

## Características

✨ **Funcionalidades Principais:**
- 👤 Autenticação de usuários (Cliente e Proprietário)
- 📅 Sistema de agendamentos com validação de conflitos
- ⏱️ Serviços com duração configurável (Escova Progressiva e Mechas = 4 horas)
- 💇 Cadastro de clientes
- 🛍️ Cadastro de produtos
- 🔐 Controle de permissões por tipo de usuário

## Estrutura do Projeto

```
salao/
├── app/
│   ├── models/              # Modelos de dados
│   │   ├── usuario.py
│   │   ├── cliente.py
│   │   ├── servico.py
│   │   ├── produto.py
│   │   ├── agendamento.py
│   │   └── db.py
│   ├── controllers/         # Lógica de negócio
│   │   ├── auth.py         # Autenticação
│   │   ├── cliente.py      # Funções do cliente
│   │   ├── admin.py        # Funções do admin
│   │   └── main.py         # Rotas gerais
│   ├── views/              # Templates HTML
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── cliente/
│   │   └── admin/
│   └── static/             # CSS e JS
│       ├── css/
│       └── js/
├── run.py                  # Arquivo principal
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## Instalação

1. **Clone ou extraia o projeto:**
```bash
cd c:\projetos\salao
```

2. **Crie um ambiente virtual (opcional mas recomendado):**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## Execução

```bash
python run.py
```

A aplicação estará disponível em `http://localhost:5000`

## Credenciais Padrão

**Usuário Admin (Proprietário):**
- Email: `admin@salao.com`
- Senha: `admin123`

## Funcionalidades por Tipo de Usuário

### 👥 Cliente
- Visualizar agendamentos
- Agendar novos serviços
- Cancelar agendamentos confirmados
- Atualizar perfil pessoal
- Visualizar serviços disponíveis

### 👩‍💼 Proprietário (Admin)
- Dashboard com resumo geral
- Gerenciar clientes (CRUD)
- Gerenciar serviços (CRUD)
- Gerenciar produtos (CRUD)
- Gerenciar agendamentos (CRUD)
- Visualizar agendamentos por período
- Controlar status de agendamentos

## Validações Importantes

### ⏱️ Conflito de Horários
- O sistema valida automaticamente conflitos de horários
- Escova Progressiva: 240 minutos (4 horas)
- Mechas: 240 minutos (4 horas)
- Não permite agendamentos sobrepostos

### 📅 Agendamentos
- Apenas datas futuras
- Serviços com duração variável
- Status: Confirmado, Realizado, Cancelado

## Banco de Dados

A aplicação usa SQLite que é criado automaticamente em `salao.db`.

**Tabelas:**
- `usuarios` - Usuários do sistema (clientes e proprietários)
- `clientes` - Dados detalhados dos clientes
- `servicos` - Serviços oferecidos
- `produtos` - Produtos para venda
- `agendamentos` - Agendamentos realizados

## Segurança

- Senhas criptografadas com Werkzeug
- Sessões de usuário
- Validação de permissões em cada rota
- CSRF protection (padrão do Flask)

## Melhorias Futuras

- [ ] Integração com pagamento
- [ ] Notificações por email
- [ ] SMS de lembretes
- [ ] Relatórios e gráficos
- [ ] Sistema de avaliação
- [ ] Histórico de atendimentos
- [ ] Integração com calendário externo

## Suporte

Para dúvidas ou problemas, consulte a documentação do Flask em: https://flask.palletsprojects.com/

---

**Versão:** 1.0.0  
**Data:** 14 de Novembro de 2024
