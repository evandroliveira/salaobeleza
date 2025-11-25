from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from .db import db
import secrets

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'cliente' ou 'proprietaria'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Campos para reset de senha
    reset_token = db.Column(db.String(100), nullable=True, unique=True)
    reset_token_expiracao = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, senha):
        self.senha = generate_password_hash(senha)
    
    def check_password(self, senha):
        return check_password_hash(self.senha, senha)
    
    def gerar_reset_token(self, expiracao_minutos=30):
        """Gera um token seguro para reset de senha com expiração."""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiracao = datetime.utcnow() + timedelta(minutes=expiracao_minutos)
        return self.reset_token
    
    def verificar_reset_token(self, token):
        """Verifica se o token de reset é válido e não expirou."""
        if not self.reset_token or self.reset_token != token:
            return False
        if datetime.utcnow() > self.reset_token_expiracao:
            return False
        return True
    
    def limpar_reset_token(self):
        """Remove o token de reset após uso."""
        self.reset_token = None
        self.reset_token_expiracao = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'tipo': self.tipo,
            'data_criacao': self.data_criacao.isoformat(),
            'ativo': self.ativo
        }
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'
