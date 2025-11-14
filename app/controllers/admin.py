from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime, timedelta
from ..models.cliente import Cliente
from ..models.agendamento import Agendamento
from ..models.servico import Servico
from ..models.produto import Produto
from ..models.db import db
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login primeiro!', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('usuario_tipo') != 'proprietaria':
            flash('Acesso negado! Apenas proprietários podem acessar.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============ DASHBOARD ============

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_clientes = Cliente.query.count()
    total_agendamentos = Agendamento.query.filter_by(status='confirmado').count()
    total_servicos = Servico.query.filter_by(ativo=True).count()
    
    # Agendamentos dos próximos 7 dias
    agora = datetime.now()
    proximos_7_dias = agora + timedelta(days=7)
    agendamentos_proximos = Agendamento.query.filter(
        Agendamento.data_agendamento >= agora,
        Agendamento.data_agendamento <= proximos_7_dias,
        Agendamento.status != 'cancelado'
    ).order_by(Agendamento.data_agendamento).all()
    
    return render_template('admin/dashboard.html',
                         total_clientes=total_clientes,
                         total_agendamentos=total_agendamentos,
                         total_servicos=total_servicos,
                         agendamentos_proximos=agendamentos_proximos)

# ============ CLIENTES ============

@admin_bp.route('/clientes')
@login_required
@admin_required
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('admin/clientes/listar.html', clientes=clientes)

@admin_bp.route('/clientes/cadastrar', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        data_nascimento = request.form.get('data_nascimento')
        endereco = request.form.get('endereco')
        cidade = request.form.get('cidade')
        
        novo_cliente = Cliente(
            nome=nome,
            email=email,
            telefone=telefone,
            endereco=endereco,
            cidade=cidade
        )
        
        if data_nascimento:
            novo_cliente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        
        db.session.add(novo_cliente)
        db.session.commit()
        
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.listar_clientes'))
    
    return render_template('admin/clientes/cadastrar.html')

@admin_bp.route('/clientes/<int:cliente_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    
    if request.method == 'POST':
        cliente.nome = request.form.get('nome')
        cliente.email = request.form.get('email')
        cliente.telefone = request.form.get('telefone')
        cliente.endereco = request.form.get('endereco')
        cliente.cidade = request.form.get('cidade')
        
        data_nascimento = request.form.get('data_nascimento')
        if data_nascimento:
            cliente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        
        db.session.commit()
        
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('admin.listar_clientes'))
    
    return render_template('admin/clientes/editar.html', cliente=cliente)

@admin_bp.route('/clientes/<int:cliente_id>/deletar', methods=['POST'])
@login_required
@admin_required
def deletar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente deletado com sucesso!', 'success')
    return redirect(url_for('admin.listar_clientes'))

# ============ SERVIÇOS ============

@admin_bp.route('/servicos')
@login_required
@admin_required
def listar_servicos():
    servicos = Servico.query.all()
    return render_template('admin/servicos/listar.html', servicos=servicos)

@admin_bp.route('/servicos/cadastrar', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastrar_servico():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        duracao_minutos = int(request.form.get('duracao_minutos'))
        
        novo_servico = Servico(
            nome=nome,
            descricao=descricao,
            preco=preco,
            duracao_minutos=duracao_minutos
        )
        
        db.session.add(novo_servico)
        db.session.commit()
        
        flash('Serviço cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.listar_servicos'))
    
    return render_template('admin/servicos/cadastrar.html')

@admin_bp.route('/servicos/<int:servico_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_servico(servico_id):
    servico = Servico.query.get_or_404(servico_id)
    
    if request.method == 'POST':
        servico.nome = request.form.get('nome')
        servico.descricao = request.form.get('descricao')
        servico.preco = float(request.form.get('preco'))
        servico.duracao_minutos = int(request.form.get('duracao_minutos'))
        servico.ativo = request.form.get('ativo') == 'on'
        
        db.session.commit()
        
        flash('Serviço atualizado com sucesso!', 'success')
        return redirect(url_for('admin.listar_servicos'))
    
    return render_template('admin/servicos/editar.html', servico=servico)

@admin_bp.route('/servicos/<int:servico_id>/deletar', methods=['POST'])
@login_required
@admin_required
def deletar_servico(servico_id):
    servico = Servico.query.get_or_404(servico_id)
    db.session.delete(servico)
    db.session.commit()
    flash('Serviço deletado com sucesso!', 'success')
    return redirect(url_for('admin.listar_servicos'))

# ============ PRODUTOS ============

@admin_bp.route('/produtos')
@login_required
@admin_required
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('admin/produtos/listar.html', produtos=produtos)

@admin_bp.route('/produtos/cadastrar', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        quantidade = int(request.form.get('quantidade'))
        categoria = request.form.get('categoria')
        
        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            quantidade=quantidade,
            categoria=categoria
        )
        
        db.session.add(novo_produto)
        db.session.commit()
        
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.listar_produtos'))
    
    return render_template('admin/produtos/cadastrar.html')

@admin_bp.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    
    if request.method == 'POST':
        produto.nome = request.form.get('nome')
        produto.descricao = request.form.get('descricao')
        produto.preco = float(request.form.get('preco'))
        produto.quantidade = int(request.form.get('quantidade'))
        produto.categoria = request.form.get('categoria')
        produto.ativo = request.form.get('ativo') == 'on'
        
        db.session.commit()
        
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin.listar_produtos'))
    
    return render_template('admin/produtos/editar.html', produto=produto)

@admin_bp.route('/produtos/<int:produto_id>/deletar', methods=['POST'])
@login_required
@admin_required
def deletar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('admin.listar_produtos'))

# ============ AGENDAMENTOS ============

@admin_bp.route('/agendamentos')
@login_required
@admin_required
def listar_agendamentos():
    filtro_status = request.args.get('status', 'todos')
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')
    
    query = Agendamento.query
    
    if filtro_status != 'todos':
        query = query.filter_by(status=filtro_status)
    
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(Agendamento.data_agendamento >= data_inicio_dt)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
            data_fim_dt = data_fim_dt + timedelta(days=1)
            query = query.filter(Agendamento.data_agendamento < data_fim_dt)
        except ValueError:
            pass
    
    agendamentos = query.order_by(Agendamento.data_agendamento.desc()).all()
    
    return render_template('admin/agendamentos/listar.html', 
                         agendamentos=agendamentos, 
                         filtro_status=filtro_status,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

@admin_bp.route('/agendamentos/<int:agendamento_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_agendamento(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    servicos = Servico.query.filter_by(ativo=True).all()
    
    if request.method == 'POST':
        servico_id = request.form.get('servico_id')
        data_str = request.form.get('data_agendamento')
        hora_str = request.form.get('hora_agendamento')
        status = request.form.get('status')
        notas = request.form.get('notas', '')
        
        try:
            nova_data = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            flash('Data ou hora inválida!', 'danger')
            return redirect(url_for('admin.editar_agendamento', agendamento_id=agendamento_id))
        
        servico = Servico.query.get(servico_id)
        if not servico:
            flash('Serviço inválido!', 'danger')
            return redirect(url_for('admin.editar_agendamento', agendamento_id=agendamento_id))
        
        # Verificar conflito apenas se a data/hora mudou
        if nova_data != agendamento.data_agendamento:
            conflito = verificar_conflito_horario_admin(nova_data, servico.duracao_minutos, agendamento_id)
            if conflito:
                flash(f'Horário indisponível! Serviço conflita com agendamento existente.', 'danger')
                return redirect(url_for('admin.editar_agendamento', agendamento_id=agendamento_id))
        
        agendamento.servico_id = servico_id
        agendamento.data_agendamento = nova_data
        agendamento.status = status
        agendamento.notas = notas
        agendamento.valor_total = servico.preco
        
        db.session.commit()
        
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('admin.listar_agendamentos'))
    
    return render_template('admin/agendamentos/editar.html', agendamento=agendamento, servicos=servicos)

@admin_bp.route('/agendamentos/<int:agendamento_id>/deletar', methods=['POST'])
@login_required
@admin_required
def deletar_agendamento(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    db.session.delete(agendamento)
    db.session.commit()
    flash('Agendamento deletado com sucesso!', 'success')
    return redirect(url_for('admin.listar_agendamentos'))

def verificar_conflito_horario_admin(data_agendamento, duracao_minutos, agendamento_id_atual=None):
    """Verifica se há conflito de horários com agendamentos existentes (para admin)"""
    hora_fim = data_agendamento + timedelta(minutes=duracao_minutos)
    
    query = Agendamento.query.filter(
        Agendamento.status != 'cancelado'
    )
    
    if agendamento_id_atual:
        query = query.filter(Agendamento.id != agendamento_id_atual)
    
    agendamentos = query.all()
    
    # Verifica conflitos em Python (usando o método get_hora_fim)
    for agendamento in agendamentos:
        agendamento_fim = agendamento.get_hora_fim()
        # Se houver sobreposição de horários
        if agendamento.data_agendamento < hora_fim and agendamento_fim > data_agendamento:
            return True
    
    return False

# ============ RELATÓRIOS ============

@admin_bp.route('/relatorios')
@login_required
@admin_required
def relatorios():
    agora = datetime.now()
    mes_atual = agora.month
    ano_atual = agora.year
    
    # Agendamentos realizados este mês
    primeiro_dia = datetime(ano_atual, mes_atual, 1)
    ultimo_dia = datetime(ano_atual, mes_atual, 28) + timedelta(days=4)
    ultimo_dia = ultimo_dia.replace(day=1) - timedelta(days=1)
    
    agendamentos_mes = Agendamento.query.filter(
        Agendamento.status == 'realizado',
        Agendamento.data_agendamento >= primeiro_dia,
        Agendamento.data_agendamento <= ultimo_dia
    ).all()
    
    # Estatísticas
    total_realizado = sum(ag.valor_total for ag in agendamentos_mes if ag.valor_total)
    agendamentos_confirmados_proximos = Agendamento.query.filter(
        Agendamento.status == 'confirmado',
        Agendamento.data_agendamento >= agora
    ).count()
    
    # Por serviço
    servicos_populares = db.session.query(
        Servico.nome,
        db.func.count(Agendamento.id).label('total')
    ).join(Agendamento).filter(
        Agendamento.status == 'realizado'
    ).group_by(Servico.id).order_by(db.func.count(Agendamento.id).desc()).limit(5).all()
    
    # Clientes mais frequentes
    clientes_frequentes = db.session.query(
        Cliente.nome,
        db.func.count(Agendamento.id).label('total')
    ).join(Agendamento).group_by(Cliente.id).order_by(db.func.count(Agendamento.id).desc()).limit(5).all()
    
    return render_template('admin/relatorios.html',
                         total_realizado=total_realizado,
                         agendamentos_confirmados_proximos=agendamentos_confirmados_proximos,
                         servicos_populares=servicos_populares,
                         clientes_frequentes=clientes_frequentes,
                         mes_ano=f"{mes_atual}/{ano_atual}")
