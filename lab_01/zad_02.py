import shutil

filename = str(input("Podaj nazwe pliku: "))
destFile = "lab1zad1.png"

shutil.copy(filename, destFile)