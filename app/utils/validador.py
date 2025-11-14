import re
from datetime import datetime

class ValidadorFormulario:
    """Classe para centralizar validações de formulários"""
    
    @staticmethod
    def validar_email(email):
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validar_telefone(telefone):
        """Valida formato de telefone brasileiro"""
        # Remove caracteres especiais
        telefone_limpo = re.sub(r'\D', '', telefone)
        # Valida se tem 10 ou 11 dígitos
        return len(telefone_limpo) >= 10
    
    @staticmethod
    def validar_nome(nome):
        """Valida se nome tem pelo menos 3 caracteres"""
        return len(nome.strip()) >= 3
    
    @staticmethod
    def validar_preco(preco):
        """Valida se preço é válido"""
        try:
            valor = float(preco)
            return valor > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validar_duracao(duracao):
        """Valida se duração é válida"""
        try:
            valor = int(duracao)
            return valor > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validar_data_futura(data_string):
        """Valida se data é futura"""
        try:
            data = datetime.strptime(data_string, '%Y-%m-%d')
            return data > datetime.now()
        except ValueError:
            return False
    
    @staticmethod
    def validar_senhas_iguais(senha1, senha2):
        """Valida se senhas são iguais"""
        return len(senha1) >= 6 and senha1 == senha2
    
    @staticmethod
    def validar_quantidade(quantidade):
        """Valida quantidade"""
        try:
            valor = int(quantidade)
            return valor >= 0
        except (ValueError, TypeError):
            return False
