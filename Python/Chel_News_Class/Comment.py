import User
from random import randint

id_comment = 1

class Comment:
    def __init__(self, text: str, author: User.User, cnt_likes: int):
        global id_comment
        self.id = id_comment
        id_comment += 1
        self.text = text
        self.author = author
        self.count_likes = cnt_likes
        self.who_like = []

    def like_comment(self):
        self.author.reputation += 1
        self.count_likes += 1
    
    def __str__(self) -> str:
        return f"{str(self.author)}. Айди коммента ({self.id:04})\n{self.text} \n(Кол-во лайков: {self.count_likes})"
    
def generate_random_comment(users: list[User.User]) -> list[Comment]:
    com_text: list[str] = ["Нормально", "Лучшая новость дня!", "Интересная перспектива!", "Удивительно, спасибо за поделиться!",
                "Вопрос на засыпку: что вы думаете об этом?", "Я тоже так думаю!", "Надеюсь увидеть больше таких материалов!",
                "Отличная работа!", "Полностью согласен с вами!", "Это заставляет задуматься!", "Прекрасный пример!", "Очень полезная информация!"]
    return [Comment(com_text[randint(0, 11)], users[randint(0, len(users)-1)], 0) for _ in range(10)]