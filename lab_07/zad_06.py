import poplib


def check_email_count(host, user, password):
    try:
        server = poplib.POP3_SSL(host)
        server.user(user)
        server.pass_(password)
        num_messages = len(server.list()[1])
        print(f"Liczba wiadomości w skrzynce: {num_messages}")
        server.quit()

    except Exception as e:
        print(f"Nie udało się połączyć z serwerem: {e}")


if __name__ == "__main__":
    host = "poczta.interia.pl"  # Serwer POP3
    user = "pas2025inf@interia.pl"  # Twój login
    password = "dq4cCRSta4VM&qqN9vesJcVeW*"  # Twoje hasło

    check_email_count(host, user, password)
