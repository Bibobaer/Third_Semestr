class BotUser:
    def __init__(self, name: str, lastname: str, middlename: str, age: int, interests: list[str]):
        self.name: str = name
        self.lastname: str = lastname
        self.middlename: str = middlename
        self.age: int = age
        self.interests: list[str] = interests

    def __str__(self):
        return "Фамилия: {}\nИмя: {}\nОтчество: {}\nВозрост: {}\nИнтересы: {}".format(self.lastname, self.name, self.middlename, self.age, ", ".join(i for i in self.interests))