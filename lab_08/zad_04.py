import imaplib
import email
from email.header import decode_header

host = "poczta.interia.pl"
port = 993
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"


def decode_header_value(header_value):
    """Funkcja dekodująca nagłówki wiadomości"""
    if header_value is None:
        return "Brak danych"
    decoded_parts = decode_header(header_value)
    decoded_str = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_str += part.decode(encoding if encoding else 'utf-8')
        else:
            decoded_str += part
    return decoded_str


def imap_client():
    try:

        print("Łączenie z serwerem IMAP...")
        mail = imaplib.IMAP4_SSL(host, port)

        print("Logowanie...")
        mail.login(user, password)
        print("Zalogowano pomyślnie.")

        mail.select("inbox")

        print("Sprawdzanie nieprzeczytanych wiadomości...")
        result, data = mail.search(None, 'UNSEEN')

        if result == 'OK' and data[0]:
            unread_ids = data[0].split()
            print(f"Znaleziono {len(unread_ids)} nieprzeczytanych wiadomości.")

            for msg_id in unread_ids:
                result, msg_data = mail.fetch(msg_id, "(BODY[TEXT])")

                if result == 'OK' and msg_data:
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])

                            subject = decode_header_value(msg.get("Subject"))
                            from_ = decode_header_value(msg.get("From"))
                            print(f"\nTemat: {subject}")
                            print(f"Od: {from_}")

                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        print(f"\nTreść wiadomości:\n{body}")
                            else:
                                body = msg.get_payload(decode=True).decode()
                                print(f"\nTreść wiadomości:\n{body}")

                    mail.store(msg_id, '+FLAGS', '\\Seen')
                    print(f"Wiadomość {msg_id} oznaczona jako przeczytana.")
                else:
                    print(f"Błąd podczas pobierania treści wiadomości {msg_id}")
        else:
            print("Nie znaleziono żadnych nieprzeczytanych wiadomości.")

        mail.logout()
        print("Połączenie zakończone.")

    except imaplib.IMAP4.error as e:
        print(f"Błąd IMAP: {e}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    imap_client()
