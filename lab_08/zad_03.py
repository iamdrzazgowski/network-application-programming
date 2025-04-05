import imaplib

host = "poczta.interia.pl"
port = 993
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"


def imap_client():
    try:

        print("Łączenie z serwerem IMAP...")
        mail = imaplib.IMAP4_SSL(host, port)

        print("Logowanie...")
        mail.login(user, password)
        print("Zalogowano pomyślnie.")

        print("Pobieranie listy skrzynek...")
        result, mailboxes = mail.list()

        if result == 'OK':
            total_messages = 0

            for mailbox in mailboxes:

                mailbox_name = mailbox.decode().split(' "/" ')[-1].strip('"')
                print(f"Sprawdzanie skrzynki: {mailbox_name}")
                mail.select(mailbox_name)

                result, data = mail.status(mailbox_name, "(MESSAGES)")

                if result == 'OK':
                    response = data[0].decode('utf-8')

                    try:
                        num_messages = int(response.split()[2].strip(")"))
                        print(f"Liczba wiadomości w skrzynce '{mailbox_name}': {num_messages}")
                        total_messages += num_messages
                    except ValueError:
                        print(f"Błąd przetwarzania liczby wiadomości w skrzynce '{mailbox_name}'.")
                else:
                    print(f"Nie udało się pobrać liczby wiadomości dla skrzynki '{mailbox_name}'.")

            print(f"\nŁączna liczba wiadomości we wszystkich skrzynkach: {total_messages}")
        else:
            print("Nie udało się pobrać listy skrzynek.")

        mail.logout()
        print("Połączenie zakończone.")

    except imaplib.IMAP4.error as e:
        print(f"Błąd IMAP: {e}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    imap_client()
