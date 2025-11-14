# 🔌 Documentação da API REST

## Base URL
```
http://localhost:5000/api/v1
```

## Endpoints Disponíveis

### 👥 Clientes

#### Listar Clientes
```
GET /api/v1/clientes
```

**Parâmetros Query:**
- `page` (int): Número da página (padrão: 1)
- `per_page` (int): Itens por página (padrão: 10)

**Resposta (200):**
```json
{
    "total": 5,
    "paginas": 1,
    "pagina_atual": 1,
    "clientes": [
        {
            "id": 1,
            "nome": "João Silva",
            "email": "joao@email.com",
            "telefone": "11999999999",
            "data_nascimento": "1990-05-15",
            "endereco": "Rua A, 123",
            "cidade": "São Paulo",
            "data_criacao": "2024-11-14T10:30:00",
            "ativo": true
        }
    ]
}
```

#### Obter Cliente Específico
```
GET /api/v1/clientes/<cliente_id>
```

**Resposta (200):**
```json
{
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "telefone": "11999999999",
    "data_nascimento": "1990-05-15",
    "endereco": "Rua A, 123",
    "cidade": "São Paulo",
    "data_criacao": "2024-11-14T10:30:00",
    "ativo": true
}
```

---

### 💇 Serviços

#### Listar Serviços Ativos
```
GET /api/v1/servicos
```

**Resposta (200):**
```json
{
    "total": 4,
    "servicos": [
        {
            "id": 1,
            "nome": "Escova Progressiva",
            "descricao": "Escova progressiva de 4 horas",
            "preco": 250.0,
            "duracao_minutos": 240,
            "ativo": true,
            "data_criacao": "2024-11-14T10:30:00"
        }
    ]
}
```

#### Obter Serviço Específico
```
GET /api/v1/servicos/<servico_id>
```

---

### 📅 Agendamentos

#### Listar Agendamentos
```
GET /api/v1/agendamentos
```

**Parâmetros Query:**
- `status` (string): Filtro por status (confirmado, realizado, cancelado, todos)
- `cliente_id` (int): Filtrar por cliente
- `data_inicio` (string): Data inicial (formato: YYYY-MM-DD)
- `data_fim` (string): Data final (formato: YYYY-MM-DD)

**Exemplo:**
```
GET /api/v1/agendamentos?status=confirmado&data_inicio=2024-11-14&data_fim=2024-11-21
```

**Resposta (200):**
```json
{
    "total": 3,
    "agendamentos": [
        {
            "id": 1,
            "cliente_id": 1,
            "cliente_nome": "João Silva",
            "servico_id": 1,
            "servico_nome": "Escova Progressiva",
            "data_agendamento": "2024-11-15T14:00:00",
            "data_fim": "2024-11-15T18:00:00",
            "status": "confirmado",
            "notas": "Cliente é alérgica a certos produtos",
            "valor_total": 250.0,
            "data_criacao": "2024-11-14T10:30:00"
        }
    ]
}
```

#### Obter Agendamento Específico
```
GET /api/v1/agendamentos/<agendamento_id>
```

#### Validar Horário Disponível
```
POST /api/v1/agendamentos/validar-horario
Content-Type: application/json
```

**Body:**
```json
{
    "data_agendamento": "2024-11-15T14:00",
    "servico_id": 1
}
```

**Resposta (200):**
```json
{
    "disponivel": true,
    "mensagem": "Horário disponível"
}
```

---

### 📊 Estatísticas

#### Obter Estatísticas Gerais
```
GET /api/v1/estatisticas
```

**Resposta (200):**
```json
{
    "total_clientes": 5,
    "total_agendamentos_confirmados": 12,
    "total_servicos": 4,
    "proximos_7_dias": 3,
    "receita_mes": 2450.50
}
```

---

## Códigos de Status HTTP

| Código | Significado |
|--------|------------|
| 200 | OK - Requisição bem-sucedida |
| 400 | Bad Request - Dados inválidos |
| 404 | Not Found - Recurso não encontrado |
| 500 | Internal Server Error - Erro no servidor |

---

## Exemplos de Uso

### cURL

#### Listar clientes
```bash
curl http://localhost:5000/api/v1/clientes
```

#### Validar horário
```bash
curl -X POST http://localhost:5000/api/v1/agendamentos/validar-horario \
  -H "Content-Type: application/json" \
  -d '{
    "data_agendamento": "2024-11-15T14:00",
    "servico_id": 1
  }'
```

### Python

```python
import requests

# Listar agendamentos confirmados
response = requests.get(
    'http://localhost:5000/api/v1/agendamentos',
    params={'status': 'confirmado'}
)
agendamentos = response.json()
print(agendamentos)

# Validar horário
response = requests.post(
    'http://localhost:5000/api/v1/agendamentos/validar-horario',
    json={
        'data_agendamento': '2024-11-15T14:00',
        'servico_id': 1
    }
)
resultado = response.json()
print(resultado)
```

### JavaScript/Fetch API

```javascript
// Listar clientes
fetch('http://localhost:5000/api/v1/clientes')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Erro:', error));

// Validar horário
fetch('http://localhost:5000/api/v1/agendamentos/validar-horario', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        'data_agendamento': '2024-11-15T14:00',
        'servico_id': 1
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Erro:', error));
```

---

## Autenticação

Atualmente, a API **não requer autenticação** (aberta). Para produção, recomenda-se implementar:
- JWT (JSON Web Tokens)
- API Keys
- OAuth 2.0

---

## Rate Limiting

Não implementado na versão atual. Para produção, recomenda-se limitar requisições por IP/usuário.

---

## CORS (Cross-Origin Resource Sharing)

CORS não está ativado por padrão. Para ativar, adicione a seguinte extensão:

```python
from flask_cors import CORS
CORS(app)
```

E instale: `pip install flask-cors`

---

**Versão da API:** 1.0.0  
**Última Atualização:** 14 de Novembro de 2024
