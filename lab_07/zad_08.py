import poplib


def check_individual_message_sizes(host, user, password):
    try:

        server = poplib.POP3_SSL(host)
        server.user(user)
        server.pass_(password)
        message_list = server.list()[1]

        for i, message in enumerate(message_list, start=1):
            size = int(message.split()[1])
            print(f"Wiadomość {i} ma {size} bajtów")
        server.quit()

    except Exception as e:
        print(f"Nie udało się połączyć z serwerem: {e}")


if __name__ == "__main__":
    host = "poczta.interia.pl"
    user = "pas2025inf@interia.pl"
    password = "dq4cCRSta4VM&qqN9vesJcVeW*"

    check_individual_message_sizes(host, user, password)
