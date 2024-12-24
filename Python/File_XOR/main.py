# Задание 1
# print((lambda **args: [arg for key, arg in args.items() if 'a' in key.lower()])(a=1, g = '54', Asf = 5, fAt = 'VDFSdvfd'))

#Задание 2
from datetime import datetime

tmp: datetime = datetime.now()
output_filename: str = str(f"Results\\result_{tmp.year}_{tmp.month}_{tmp.day}_{tmp.hour}_{tmp.minute}_{tmp.second}_{tmp.microsecond}")

while True:
    try:
        x: int = int(input("Введите число: ")) 
        break
    except ValueError:
        print("Ввод не является числом")

output_file = open(output_filename, "w")  

while True:
    filename = input("Введите имя файла: ")
    if (filename == '0'):
        break

    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("Не получилось открыть файл")
        continue

    strbuf = "".join([chr(ord(char) ^ x) for char in file.read()])

    output_file.write(strbuf)
    file.close()

output_file.close() 