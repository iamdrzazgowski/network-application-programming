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

        # Logowanie
        print("Logowanie...")
        mail.login(user, password)
        print("Zalogowano pomyślnie.")

        mail.select("inbox")

        print("Sprawdzanie wszystkich wiadomości...")
        result, data = mail.search(None, 'ALL')

        if result == 'OK' and data[0]:
            message_ids = data[0].split()  # ID wszystkich wiadomości
            print(f"Znaleziono {len(message_ids)} wiadomości.")

            for i, msg_id in enumerate(message_ids, 1):
                result, msg_data = mail.fetch(msg_id, "(BODY[HEADER.FIELDS (FROM SUBJECT DATE)])")
                if result == 'OK':
                    msg = email.message_from_bytes(msg_data[0][1])
                    subject = decode_header_value(msg["Subject"])
                    from_ = decode_header_value(msg["From"])
                    date_ = msg["Date"]
                    print(f"{i}. ID: {msg_id.decode()} | Temat: {subject} | Od: {from_} | Data: {date_}")

            while True:
                try:
                    message_number = int(input("Wybierz numer wiadomości do usunięcia (wpisz numer): "))
                    if 1 <= message_number <= len(message_ids):
                        message_id_to_delete = message_ids[message_number - 1]
                        break
                    else:
                        print(f"Wybierz numer między 1 a {len(message_ids)}.")
                except ValueError:
                    print("Proszę podać poprawny numer wiadomości.")

            print(f"Usuwamy wiadomość o ID: {message_id_to_delete.decode()}")

            mail.store(message_id_to_delete, '+FLAGS', '\\Deleted')
            print(f"Wiadomość {message_id_to_delete.decode()} oznaczona jako usunięta.")

            mail.expunge()
            print(f"Wiadomość {message_id_to_delete.decode()} została fizycznie usunięta.")
        else:
            print("Nie znaleziono żadnych wiadomości.")

        mail.logout()
        print("Połączenie zakończone.")

    except imaplib.IMAP4.error as e:
        print(f"Błąd IMAP: {e}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    imap_client()
