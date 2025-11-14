from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime, timedelta
from ..models.cliente import Cliente
from ..models.agendamento import Agendamento
from ..models.servico import Servico
from ..models.db import db
from functools import wraps

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login primeiro!', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def cliente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('usuario_tipo') != 'cliente':
            flash('Acesso negado!', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@cliente_bp.route('/dashboard')
@login_required
@cliente_required
def dashboard():
    usuario_id = session['usuario_id']
    cliente = Cliente.query.filter_by(usuario_id=usuario_id).first()
    
    if cliente:
        agendamentos = Agendamento.query.filter_by(cliente_id=cliente.id).order_by(Agendamento.data_agendamento).all()
    else:
        agendamentos = []
    
    servicos = Servico.query.filter_by(ativo=True).all()
    
    return render_template('cliente/dashboard.html', 
                         agendamentos=agendamentos,
                         servicos=servicos)

@cliente_bp.route('/agendar', methods=['GET', 'POST'])
@login_required
@cliente_required
def agendar():
    usuario_id = session['usuario_id']
    cliente = Cliente.query.filter_by(usuario_id=usuario_id).first()
    
    if not cliente:
        flash('Cadastre seus dados pessoais primeiro!', 'warning')
        return redirect(url_for('cliente.perfil'))
    
    servicos = Servico.query.filter_by(ativo=True).all()
    
    if request.method == 'POST':
        servico_id = request.form.get('servico_id')
        data_str = request.form.get('data_agendamento')
        hora_str = request.form.get('hora_agendamento')
        notas = request.form.get('notas', '')
        
        try:
            data_agendamento = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            flash('Data ou hora inválida!', 'danger')
            return redirect(url_for('cliente.agendar'))
        
        servico = Servico.query.get(servico_id)
        if not servico:
            flash('Serviço inválido!', 'danger')
            return redirect(url_for('cliente.agendar'))
        
        # Validar conflito de horários
        conflito = verificar_conflito_horario(data_agendamento, servico.duracao_minutos)
        if conflito:
            flash(f'Horário indisponível! Serviço conflita com agendamento existente.', 'danger')
            return redirect(url_for('cliente.agendar'))
        
        # Validar se data é no futuro
        if data_agendamento <= datetime.now():
            flash('Selecione uma data e hora futuras!', 'danger')
            return redirect(url_for('cliente.agendar'))
        
        novo_agendamento = Agendamento(
            cliente_id=cliente.id,
            servico_id=servico_id,
            data_agendamento=data_agendamento,
            notas=notas,
            valor_total=servico.preco,
            status='confirmado'
        )
        
        db.session.add(novo_agendamento)
        db.session.commit()
        
        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('cliente.dashboard'))
    
    return render_template('cliente/agendar.html', servicos=servicos)

@cliente_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@cliente_required
def perfil():
    usuario_id = session['usuario_id']
    cliente = Cliente.query.filter_by(usuario_id=usuario_id).first()
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        data_nascimento = request.form.get('data_nascimento')
        endereco = request.form.get('endereco')
        cidade = request.form.get('cidade')
        
        if cliente:
            cliente.nome = nome
            cliente.email = email
            cliente.telefone = telefone
            cliente.endereco = endereco
            cliente.cidade = cidade
            if data_nascimento:
                cliente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        else:
            cliente = Cliente(
                nome=nome,
                email=email,
                telefone=telefone,
                usuario_id=usuario_id,
                endereco=endereco,
                cidade=cidade
            )
            if data_nascimento:
                cliente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
            db.session.add(cliente)
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('cliente.dashboard'))
    
    return render_template('cliente/perfil.html', cliente=cliente)

@cliente_bp.route('/cancelar/<int:agendamento_id>', methods=['POST'])
@login_required
@cliente_required
def cancelar_agendamento(agendamento_id):
    agendamento = Agendamento.query.get(agendamento_id)
    
    if not agendamento:
        flash('Agendamento não encontrado!', 'danger')
        return redirect(url_for('cliente.dashboard'))
    
    usuario_id = session['usuario_id']
    cliente = Cliente.query.filter_by(usuario_id=usuario_id).first()
    
    if agendamento.cliente_id != cliente.id:
        flash('Você não tem permissão para cancelar este agendamento!', 'danger')
        return redirect(url_for('cliente.dashboard'))
    
    if agendamento.status == 'realizado':
        flash('Não é possível cancelar um agendamento realizado!', 'danger')
        return redirect(url_for('cliente.dashboard'))
    
    agendamento.status = 'cancelado'
    db.session.commit()
    
    flash('Agendamento cancelado com sucesso!', 'success')
    return redirect(url_for('cliente.dashboard'))

def verificar_conflito_horario(data_agendamento, duracao_minutos):
    """Verifica se há conflito de horários com agendamentos existentes"""
    hora_fim = data_agendamento + timedelta(minutes=duracao_minutos)
    
    # Busca agendamentos que não estão cancelados
    agendamentos = Agendamento.query.filter(
        Agendamento.status != 'cancelado'
    ).all()
    
    # Verifica conflitos em Python (usando o método get_hora_fim)
    for agendamento in agendamentos:
        agendamento_fim = agendamento.get_hora_fim()
        # Se houver sobreposição de horários
        if agendamento.data_agendamento < hora_fim and agendamento_fim > data_agendamento:
            return True
    
    return False
