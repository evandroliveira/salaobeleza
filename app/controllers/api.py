from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from ..models.cliente import Cliente
from ..models.servico import Servico
from ..models.agendamento import Agendamento
from ..models.db import db

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# ============ CLIENTES ============

@api_bp.route('/clientes', methods=['GET'])
def get_clientes():
    """Lista todos os clientes"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    clientes = Cliente.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': clientes.total,
        'paginas': clientes.pages,
        'pagina_atual': page,
        'clientes': [cliente.to_dict() for cliente in clientes.items]
    }), 200

@api_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    """Retorna um cliente específico"""
    cliente = Cliente.query.get(cliente_id)
    
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    
    return jsonify(cliente.to_dict()), 200

# ============ SERVIÇOS ============

@api_bp.route('/servicos', methods=['GET'])
def get_servicos():
    """Lista todos os serviços ativos"""
    servicos = Servico.query.filter_by(ativo=True).all()
    
    return jsonify({
        'total': len(servicos),
        'servicos': [servico.to_dict() for servico in servicos]
    }), 200

@api_bp.route('/servicos/<int:servico_id>', methods=['GET'])
def get_servico(servico_id):
    """Retorna um serviço específico"""
    servico = Servico.query.get(servico_id)
    
    if not servico:
        return jsonify({'erro': 'Serviço não encontrado'}), 404
    
    return jsonify(servico.to_dict()), 200

# ============ AGENDAMENTOS ============

@api_bp.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    """Lista agendamentos com filtros opcionais"""
    status = request.args.get('status', 'todos')
    cliente_id = request.args.get('cliente_id', type=int)
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Agendamento.query
    
    if status != 'todos':
        query = query.filter_by(status=status)
    
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(Agendamento.data_agendamento >= data_inicio_dt)
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    if data_fim:
        try:
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Agendamento.data_agendamento < data_fim_dt)
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    agendamentos = query.order_by(Agendamento.data_agendamento.desc()).all()
    
    return jsonify({
        'total': len(agendamentos),
        'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]
    }), 200

@api_bp.route('/agendamentos/<int:agendamento_id>', methods=['GET'])
def get_agendamento(agendamento_id):
    """Retorna um agendamento específico"""
    agendamento = Agendamento.query.get(agendamento_id)
    
    if not agendamento:
        return jsonify({'erro': 'Agendamento não encontrado'}), 404
    
    return jsonify(agendamento.to_dict()), 200

@api_bp.route('/agendamentos/validar-horario', methods=['POST'])
def validar_horario():
    """Valida se um horário está disponível"""
    data = request.json.get('data_agendamento')
    servico_id = request.json.get('servico_id')
    
    if not data or not servico_id:
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    try:
        data_agendamento = datetime.strptime(data, '%Y-%m-%dT%H:%M')
    except ValueError:
        return jsonify({'erro': 'Formato de data inválido'}), 400
    
    servico = Servico.query.get(servico_id)
    if not servico:
        return jsonify({'erro': 'Serviço não encontrado'}), 404
    
    hora_fim = data_agendamento + timedelta(minutes=servico.duracao_minutos)
    
    conflito = Agendamento.query.filter(
        Agendamento.status != 'cancelado',
        Agendamento.data_agendamento < hora_fim,
        Agendamento.get_hora_fim() > data_agendamento
    ).first()
    
    return jsonify({
        'disponivel': conflito is None,
        'mensagem': 'Horário disponível' if not conflito else 'Horário indisponível'
    }), 200

# ============ ESTATÍSTICAS ============

@api_bp.route('/estatisticas', methods=['GET'])
def get_estatisticas():
    """Retorna estatísticas gerais do sistema"""
    agora = datetime.now()
    
    total_clientes = Cliente.query.count()
    total_agendamentos_confirmados = Agendamento.query.filter_by(status='confirmado').count()
    total_servicos = Servico.query.filter_by(ativo=True).count()
    
    proximos_7_dias = Agendamento.query.filter(
        Agendamento.status != 'cancelado',
        Agendamento.data_agendamento >= agora,
        Agendamento.data_agendamento <= agora + timedelta(days=7)
    ).count()
    
    receita_mes = db.session.query(db.func.sum(Agendamento.valor_total)).filter(
        Agendamento.status == 'realizado',
        db.func.extract('month', Agendamento.data_agendamento) == agora.month,
        db.func.extract('year', Agendamento.data_agendamento) == agora.year
    ).scalar() or 0
    
    return jsonify({
        'total_clientes': total_clientes,
        'total_agendamentos_confirmados': total_agendamentos_confirmados,
        'total_servicos': total_servicos,
        'proximos_7_dias': proximos_7_dias,
        'receita_mes': round(receita_mes, 2)
    }), 200
