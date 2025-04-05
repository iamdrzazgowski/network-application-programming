import poplib

def check_total_size(host, user, password):
    try:

        server = poplib.POP3_SSL(host)
        server.user(user)
        server.pass_(password)
        message_list = server.list()[1]
        total_size = 0

        for message in message_list:
            size = int(message.split()[1])
            total_size += size

        print(f"Łączny rozmiar wszystkich wiadomości: {total_size} bajtów")

        server.quit()

    except Exception as e:
        print(f"Nie udało się połączyć z serwerem: {e}")


if __name__ == "__main__":
    host = "poczta.interia.pl"
    user = "pas2025inf@interia.pl"
    password = "dq4cCRSta4VM&qqN9vesJcVeW*"

    check_total_size(host, user, password)
