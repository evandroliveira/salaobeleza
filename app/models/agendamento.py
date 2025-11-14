from datetime import datetime
from .db import db

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    data_agendamento = db.Column(db.DateTime, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmado')  # confirmado, cancelado, realizado
    notas = db.Column(db.Text, nullable=True)
    valor_total = db.Column(db.Float, nullable=True)
    
    # Relacionamentos
    cliente = db.relationship('Cliente', backref='agendamentos')
    servico = db.relationship('Servico', backref='agendamentos')
    
    def get_hora_fim(self):
        """Calcula a hora de término do agendamento baseado na duração do serviço"""
        from datetime import timedelta
        return self.data_agendamento + timedelta(minutes=self.servico.duracao_minutos)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome,
            'servico_id': self.servico_id,
            'servico_nome': self.servico.nome,
            'data_agendamento': self.data_agendamento.isoformat(),
            'data_fim': self.get_hora_fim().isoformat(),
            'status': self.status,
            'notas': self.notas,
            'valor_total': self.valor_total,
            'data_criacao': self.data_criacao.isoformat()
        }
    
    def __repr__(self):
        return f'<Agendamento {self.cliente.nome} - {self.servico.nome}>'
