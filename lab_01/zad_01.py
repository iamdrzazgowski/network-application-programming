import shutil

filename = str(input("Podaj nazwe pliku: "))
destFile = "lab1zad1.txt"

shutil.copy(filename, destFile)