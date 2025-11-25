"""
Utilitários para envio de emails.
Nota: Este é um exemplo simples. Em produção, configure Flask-Mail com seu provedor SMTP.
"""

import os
from flask import render_template_string, current_app


def enviar_email_reset_senha(usuario, token, app):
    """
    Envia email de reset de senha para o usuário.
    
    Em produção, use Flask-Mail com configurações reais do SMTP.
    Para desenvolvimento, este é um exemplo de como seria feito.
    """
    
    # URL do link de redefinição
    reset_url = f"http://localhost:5000/auth/redefinir/{token}"
    
    # Mensagem de email
    assunto = "Redefina sua Senha - Studio Fanciele Cesario"
    corpo_html = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #ff69b4; color: white; padding: 20px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 10px; }}
                .footer {{ text-align: center; color: #666; margin-top: 20px; font-size: 12px; }}
                .button {{ 
                    background-color: #ff69b4; 
                    color: white; 
                    padding: 12px 20px; 
                    text-decoration: none; 
                    border-radius: 5px;
                    display: inline-block;
                    margin-top: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Studio Fanciele Cesario</h1>
                </div>
                <div class="content">
                    <p>Olá <strong>{usuario.nome}</strong>,</p>
                    <p>Você solicitou uma redefinição de senha. Clique no botão abaixo para criar uma nova senha:</p>
                    <a href="{reset_url}" class="button">Redefinir Senha</a>
                    <p><small>Este link é válido por 30 minutos.</small></p>
                    <p>Se você não solicitou esta redefinição, ignore este email.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 Studio Fanciele Cesario. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    # Em desenvolvimento, apenas imprimir no console/logs
    if os.getenv('FLASK_ENV') != 'production':
        print(f"\n{'='*60}")
        print(f"EMAIL PARA: {usuario.email}")
        print(f"ASSUNTO: {assunto}")
        print(f"LINK DE RESET: {reset_url}")
        print(f"{'='*60}\n")
        return True
    
    # Em produção, você configuraria Flask-Mail:
    # from flask_mail import Mail, Message
    # mail = Mail(app)
    # msg = Message(assunto, recipients=[usuario.email], html=corpo_html)
    # mail.send(msg)
    
    return True
