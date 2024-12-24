from ctypes import *

lib = cdll.LoadLibrary(r"C:\Windows\System32\msvcrt.dll")
lib2 = CDLL(r"C:\Windows\System32\user32.dll")
MesB = getattr(lib2, "MessageBoxA")

def read_from_cons(prompt):
    lib.printf(prompt)
    number = c_double()
    lib.scanf(b"%lf", byref(number))
    return number.value

def main():
    a = read_from_cons(b"Enter a: ")

    if (a == 0):
        MesB(0, b"first coef cant be zero", b"result", 2)
        return

    b = read_from_cons(b"Enter b: ")
    c = read_from_cons(b"Enter c: ")

    D = b*b - 4*a*c

    if (D < 0):
        MesB(0, b"No roots", b"roots1", 0)
    elif (D == 0):
        x = -b / (2*a)
        MesB(0, f"Root: {x}".encode("utf-8"), b"roots2", 0)
    else:
        x1 = (-b + D**0.5)/(2*a)
        x2 = (-b - D**0.5)/(2*a)
        MesB(0, f"Roots: {x1} and {x2}".encode("utf-8"), b"roots3", 0)

if __name__ == "__main__":
    main()