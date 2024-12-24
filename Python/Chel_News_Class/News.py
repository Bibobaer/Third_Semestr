import User
import Comment
from datetime import date

id_news = 1

class News:
    def __init__(self, date: date, shortnews: str, fullnews: str, author: User.User, section: str, comments: list[Comment.Comment], cnt_likes: int):
        global id_news
        self.id = id_news
        id_news += 1
        self.date = date
        self.short_news = shortnews
        self.full_news = fullnews
        self.author = author
        self.section = section
        self.comments = comments
        self.count_likes = cnt_likes
        self.who_like = []

    def delete_comment_by_id(self, id: int):
        for i in range(len(self.comments)):
            if (id == self.comments[i].id):
                self.comments.pop(i)
                return True
        return False
        
    
    def like_comment_by_id(self, id: int):
        for i in range(len(self.comments)):
            if (id == self.comments[i].id):
                self.comments[i].like_comment()
                return True
        return False

    def like_news(self):
        self.author.reputation += 1
        self.count_likes += 1

    def __str__(self) -> str:
        return f"""Раздел: {self.section}.({self.id:04})\n-------------------\n{self.short_news}\nКол-во лайков под новостью: {self.count_likes}\n-------------------
Автор: {self.author.username}\nДата выпуска новости: {self.date}\n-------------------\n{self.full_news}\n-------------------\nКомментарии:
{"\n-------------------\n".join(str(i) for i in self.comments)}"""