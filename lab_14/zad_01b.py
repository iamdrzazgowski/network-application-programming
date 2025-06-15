import smtplib
import ssl
from email.message import EmailMessage

def main():
    smtp_server = input("Podaj serwer SMTP (np. interia.pl): ").strip()
    smtp_port = 465

    login = input("Adres e-mail (login): ").strip()
    password = input("Hasło: ").strip()

    sender = login
    to_addrs = input("Podaj odbiorców (oddzielone przecinkami): ").strip().split(",")
    subject = input("Temat wiadomości: ").strip()
    body = input("Treść wiadomości:\n")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.set_debuglevel(1)
            server.login(login, password)
            server.send_message(msg)
            print("✅ Wiadomość została wysłana.")
    except Exception as e:
        print("❌ Błąd:", e)

if __name__ == "__main__":
    main()
