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

        print("Wybieranie skrzynki INBOX...")
        mail.select("inbox")

        print("Sprawdzanie liczby wiadomości...")
        result, data = mail.status("inbox", "(MESSAGES)")

        if result == 'OK':

            response = data[0].decode('utf-8')
            print(f"Odpowiedź serwera: {response}")
            num_messages = response.split()[2][0]
            print(f"Liczba wiadomości w skrzynce INBOX: {num_messages}")
        else:
            print("Nie udało się pobrać statusu skrzynki.")

        mail.logout()
        print("Połączenie zakończone.")

    except imaplib.IMAP4.error as e:
        print(f"Błąd IMAP: {e}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    imap_client()
