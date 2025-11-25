from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.usuario import Usuario
from ..models.db import db
from werkzeug.security import generate_password_hash
from ..utils.email_utils import enviar_email_reset_senha
from flask import current_app

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirma_senha = request.form.get('confirma_senha')
        tipo = request.form.get('tipo', 'cliente')
        
        if senha != confirma_senha:
            flash('Senhas não conferem!', 'danger')
            return redirect(url_for('auth.registro'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'danger')
            return redirect(url_for('auth.registro'))
        
        novo_usuario = Usuario(nome=nome, email=email, tipo=tipo)
        novo_usuario.set_password(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Usuário cadastrado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(senha):
            session['usuario_id'] = usuario.id
            session['usuario_tipo'] = usuario.tipo
            session['usuario_nome'] = usuario.nome
            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            
            if usuario.tipo == 'proprietaria':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('cliente.dashboard'))
        else:
            flash('Email ou senha inválidos!', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado!', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    """Página para solicitar reset de senha."""
    if request.method == 'POST':
        email = request.form.get('email')
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario:
            # Gerar token de reset
            token = usuario.gerar_reset_token()
            db.session.commit()
            
            # Enviar email com link de reset
            enviar_email_reset_senha(usuario, token, current_app)
            
            flash('Se o email existe em nossa base, você receberá um link para redefinir a senha.', 'info')
        else:
            # Não revelar se o email existe (segurança)
            flash('Se o email existe em nossa base, você receberá um link para redefinir a senha.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/esqueci_senha.html')


@auth_bp.route('/redefinir/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    """Página para redefinir a senha usando o token."""
    usuario = Usuario.query.filter_by(reset_token=token).first()
    
    if not usuario or not usuario.verificar_reset_token(token):
        flash('Link de redefinição inválido ou expirado!', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        confirma_senha = request.form.get('confirma_senha')
        
        if not nova_senha or not confirma_senha:
            flash('Preencha todos os campos!', 'danger')
            return render_template('auth/redefinir_senha.html', token=token)
        
        if nova_senha != confirma_senha:
            flash('As senhas não conferem!', 'danger')
            return render_template('auth/redefinir_senha.html', token=token)
        
        if len(nova_senha) < 6:
            flash('A senha deve ter no mínimo 6 caracteres!', 'danger')
            return render_template('auth/redefinir_senha.html', token=token)
        
        # Redefinir a senha
        usuario.set_password(nova_senha)
        usuario.limpar_reset_token()
        db.session.commit()
        
        flash('Sua senha foi redefinida com sucesso! Faça login com a nova senha.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/redefinir_senha.html', token=token)

