import poplib
from email import parser
from email.header import decode_header

# Parametry połączenia
host = "poczta.interia.pl"
port = 995
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"

# Połączenie z serwerem POP3 przez SSL
server = poplib.POP3_SSL(host, port)

# Logowanie na serwerze
server.user(user)
server.pass_(password)

# Pobieranie listy wiadomości
messages = server.list()[1]


# Funkcja do dekodowania nagłówków wiadomości
def decode_header_value(value):
    decoded_parts = decode_header(value)
    decoded_str = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):  # Jeśli część jest typu bytes, dekodujemy
            decoded_str += part.decode(encoding if encoding else 'utf-8')
        else:  # Jeśli część jest już ciągiem znaków, po prostu ją dodajemy
            decoded_str += part
    return decoded_str


# Funkcja do dekodowania treści wiadomości
def decode_message_content(content):
    try:
        # Próbujemy dekodować w utf-8
        return content.decode('utf-8', errors='replace')
    except UnicodeDecodeError:
        # Jeśli nie uda się, próbujemy innego kodowania (np. windows-1250)
        return content.decode('windows-1250', errors='replace')


# Iteracja po wiadomościach
for message in messages:
    parts = message.decode('utf-8').split()
    if len(parts) == 2:
        message_number = parts[0]  # Numer wiadomości

        # Pobranie pełnej wiadomości
        response = server.retr(message_number)

        # Łączenie danych wiadomości
        message_content = b"\n".join(response[1])

        # Parsowanie treści wiadomości
        msg = parser.Parser().parsestr(message_content.decode('utf-8'))

        # Wyświetlenie nagłówków wiadomości (np. temat, nadawca)
        print(f"\n\nWiadomość numer {message_number}")

        # Dekodowanie tematu i nadawcy, jeśli są zakodowane
        subject = decode_header_value(msg['Subject']) if msg['Subject'] else "Brak tematu"
        sender = decode_header_value(msg['From']) if msg['From'] else "Brak nadawcy"

        print(f"Temat: {subject}")
        print(f"Nadawca: {sender}")

        # Wyświetlenie treści wiadomości
        print("\nTreść wiadomości:")
        try:
            # Dekodowanie treści wiadomości w odpowiednim kodowaniu
            print(decode_message_content(msg.get_payload(decode=True)))
        except Exception as e:
            print(f"Nie udało się zdekodować treści wiadomości: {e}")

# Zakończenie połączenia z serwerem
server.quit()
