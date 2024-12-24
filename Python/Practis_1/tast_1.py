def Square(len: int):
    if (len <= 0):
        return
    for i in range(len):
        print("*"*len)

def Rectangle(width: int, height: int):
    if (width <= 0 or height <= 0):
        return
    for i in range(height):
        print("*"*width)

def RightTriangle(size: int):
    if (size <= 0):
        return
    cnt = 1
    for i in range(size):
        print("*"*cnt)
        cnt += 1

def Triangle(size: int):
    if (size <= 0):
        return
    for i in range(size):
        print(' ' * (size - i - 1) + '*' * (2 * i + 1))


if __name__ == "__main__":
    Square(4)
    print("--------------")
    Rectangle(2, 3)
    print("--------------")
    RightTriangle(7)
    print("--------------")
    Triangle(7)