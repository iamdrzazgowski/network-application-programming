import poplib

host = "127.0.0.1"
port = 110
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"

def connect_pop3_server():
    try:

        server = poplib.POP3(host, port)
        print("Połączono z serwerem POP3.")

        server.user(user)
        server.pass_(password)
        print("Zalogowano pomyślnie.")

        print("Pobieram listę wiadomości...")
        messages = server.list()[1]

        print(f"Liczba wiadomości: {len(messages)}")
        for message in messages:
            parts = message.decode('utf-8').split()
            if len(parts) == 2:
                msg_id = parts[0]
                msg_size = parts[1]
                print(f"ID: {msg_id}, Rozmiar: {msg_size} bajtów")

        print("\nPobieram treść wiadomości...")
        for message in messages:
            parts = message.decode('utf-8').split()
            if len(parts) == 2:
                msg_id = parts[0]
                msg_size = int(parts[1])

                response = server.retr(msg_id)
                message_content = b"\n".join(response[1])

                print(f"\nTreść wiadomości ID {msg_id}:")
                print(message_content.decode('utf-8'))

        server.quit()
        print("\nPołączenie z serwerem zostało zakończone.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    connect_pop3_server()
