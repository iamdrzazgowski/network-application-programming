import ipaddress

ip = str(input("Podaj adres IP: "))

try:
    ipaddress.ip_address(ip)
    print("Poprawne IP")
except ValueError:
    print("Niepoprawne IP")
