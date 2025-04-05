import imaplib
import email
from email.header import decode_header

host = "poczta.interia.pl"
port = 993
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"

def imap_client():
    try:

        mail = imaplib.IMAP4_SSL(host, port)
        print("Połączono z serwerem IMAP.")

        mail.login(user, password)
        print("Zalogowano pomyślnie.")

        mail.select("inbox")

        result, data = mail.status("inbox", "(MESSAGES)")
        print(f"Liczba wiadomości w skrzynce: {data[0].decode()}")

        result, data = mail.fetch("1", "(RFC822)")
        if result == "OK":
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            print(f"Temat wiadomości: {subject}")

            from_ = msg.get("From")
            print(f"Od: {from_}")

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        print(f"Treść wiadomości:\n{body}")
            else:
                body = msg.get_payload(decode=True).decode()
                print(f"Treść wiadomości:\n{body}")

        mail.store("1", "+FLAGS", "\\Seen")
        print("Wiadomość oznaczona jako przeczytana.")

        mail.logout()
        print("Połączenie zakończone.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    imap_client()
