from typing import Union

def Disk_C(a: float, b: float, c: float) -> Union[tuple[float, float], float, None]:
    D = b**2 - 4*a*c
    if (D < 0):
        return None
    elif (D == 0):
        return -b / (2*a)
    else:
        return ((-b + D**0.5)/(2*a), (-b - D**0.5)/(2*a))
    
if __name__ == "__main__":
    try:
        a = float(input("Enter tne a: "))
        b = float(input("Enter tne b: "))
        c = float(input("Enter tne c: "))
        
        print(Disk_C(a, b, c))
    except ZeroDivisionError:
        print("You cant div by zero")
        