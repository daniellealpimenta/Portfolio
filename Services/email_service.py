import os
import smtplib
from email.message import EmailMessage

# SMTP Configurações (via .env)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')


class EmailDeliveryError(Exception):
    """O e-mail não pôde ser entregue ao servidor SMTP."""


def _smtp_configured() -> bool:
    return bool(SMTP_USER and SMTP_PASSWORD)


def _send(msg: EmailMessage) -> None:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


def send_contact_email_task(name: str, email: str, subject: str, message_body: str, target_email: str):
    """
    Função executada via BackgroundTasks no FastAPI.
    """
    if not _smtp_configured():
        # Modo de simulação se as credenciais não estiverem configuradas
        print("="*40)
        print(" [email] SIMULANDO ENVIO DE E-MAIL (SMTP NÃO CONFIGURADO)")
        print(f"Para: {target_email}")
        print(f"Assunto: {subject} - Contato de {name}")
        print(f"Corpo:\nNome: {name}\nEmail de Retorno: {email}\n\nMensagem:\n{message_body}")
        print("="*40)
        return

    try:
        msg = EmailMessage()
        msg['Subject'] = f"{subject} - Contato de {name}"
        msg['From'] = SMTP_USER
        msg['To'] = target_email
        msg['Reply-To'] = email

        content = f"Novo contato recebido do Portfólio:\n\nNome: {name}\nEmail de Retorno: {email}\n\nMensagem:\n{message_body}"
        msg.set_content(content)

        _send(msg)
        print("OK: Email enviado com sucesso via BackgroundTask.")
    except Exception as e:
        print(f"ERRO: Erro ao enviar email na BackgroundTask: {e}")


def send_login_code_email(target_email: str, code: str):
    """
    Envia o código de acesso de uso único pro e-mail do admin.
    Lança EmailDeliveryError se o envio falhar, pra que o login mostre o erro.
    """
    if not _smtp_configured():
        print("="*40)
        print(" [email] SIMULANDO ENVIO DE CÓDIGO DE LOGIN (SMTP NÃO CONFIGURADO)")
        print(f"Para: {target_email}")
        print(f"Código: {code}")
        print("="*40)
        return

    msg = EmailMessage()
    msg['Subject'] = "Seu código de acesso"
    msg['From'] = SMTP_USER
    msg['To'] = target_email
    msg.set_content(
        f"Seu código de acesso é: {code}\n\n"
        f"Ele expira em 10 minutos. Se você não solicitou esse código, pode ignorar este e-mail."
    )

    try:
        _send(msg)
    except Exception as e:
        print(f"ERRO: Erro ao enviar código de login: {e}")
        raise EmailDeliveryError(str(e)) from e
