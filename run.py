import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models.db import db
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.servico import Servico
from app.models.produto import Produto
from app.models.agendamento import Agendamento

def create_app():
    app = Flask(__name__, template_folder='app/views', static_folder='app/static')
    
    # Configuração do banco de dados
    # Em produção usa PostgreSQL, em desenvolvimento usa SQLite
    if os.getenv('DATABASE_URL'):
        # Converter postgres:// para postgresql:// (novo formato)
        database_url = os.getenv('DATABASE_URL')
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salao.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Usar variável de ambiente ou valor padrão
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Inicializar banco de dados
    db.init_app(app)
    
    # Registrar blueprints (rotas)
    from app.controllers.main import main_bp
    from app.controllers.auth import auth_bp
    from app.controllers.cliente import cliente_bp
    from app.controllers.admin import admin_bp
    from app.controllers.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        if not Usuario.query.filter_by(email='admin@salao.com').first():
            admin = Usuario(
                nome='Administrador',
                email='admin@salao.com',
                tipo='proprietaria'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Criar alguns serviços padrão
            servicos_padrao = [
                Servico(nome='Escova Progressiva', preco=250.00, duracao_minutos=240, 
                       descricao='Escova progressiva de 4 horas'),
                Servico(nome='Mechas', preco=200.00, duracao_minutos=240,
                       descricao='Aplicação de mechas de 4 horas'),
                Servico(nome='Corte de Cabelo', preco=80.00, duracao_minutos=60,
                       descricao='Corte e modelagem'),
                Servico(nome='Coloração', preco=150.00, duracao_minutos=120,
                       descricao='Tinta e tonalização'),
            ]
            
            for servico in servicos_padrao:
                db.session.add(servico)
            
            db.session.commit()
    
    return app

# Expor a aplicação no nível do módulo para WSGI servers (gunicorn, uwsgi, etc.)
app = create_app()

if __name__ == '__main__':
    # Configurações para produção vs desenvolvimento
    debug = os.getenv('FLASK_ENV') != 'production'
    port = int(os.getenv('PORT', 5000))

    app.run(debug=debug, host='0.0.0.0', port=port)
