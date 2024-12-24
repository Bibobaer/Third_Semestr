from datetime import date, timedelta
from random import randint

id_user: int = 1

class User:
    def __init__(self, dateOR: date, username: str, name: str):
        global id_user
        self.id = id_user
        id_user += 1
        self.date_of_registration = dateOR
        self.username = username
        self.name = name
        self.reputation = 0

    def __str__(self) -> str:
        return f"\033[32m{self.username}\033[0m ({self.id:04})\n\033[33m\"{self.name}\"\033[0m {self.date_of_registration}"
    
def get_random_name() -> str:
    return ["Nikita", "Ivan", "Marina", "Alex", "John", "Mike", "Roman", "Igor", "Harry", "Tim", "Svyatoslav"][randint(0, 10)]

def get_random_username() -> str:
    return ["Unc3rtain", "Portqw12", "Qwert52", "Jimpy6", "Maga_2007", "GoldenWhisper", "GlamVixen", "SweetBaby01", "AscedBascet", "Yella.P", "Fантазер"][randint(0, 10)]

def get_random_date() -> date:
    start = date(2000, 1, 1)
    end = date(2023, 12, 31)
    delta = end - start
    random_days = randint(0, delta.days)
    return start + timedelta(days=random_days)