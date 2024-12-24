import User
import Comment
from News import News
from datetime import date
import random
from config import *


users: list[User.User] = [User.User(User.get_random_date(), User.get_random_username(), User.get_random_name()) for _ in range(10)]

news: list[News] = []

news.append(News(date(2024, 9, 12), news_1[0], news_1[1], users[random.randint(0, 9)], news_1[2], Comment.generate_random_comment(users), 0))# 1
news.append(News(date(2024, 9, 13), news_2[0], news_2[1], users[random.randint(0, 9)], news_2[2], Comment.generate_random_comment(users), 0))# 2
news.append(News(date(2024, 8, 25), news_3[0], news_3[1], users[random.randint(0, 9)], news_3[2], Comment.generate_random_comment(users), 0))# 3
news.append(News(date(2020, 8, 31), news_4[0], news_4[1], users[random.randint(0, 9)], news_4[2], Comment.generate_random_comment(users), 0))# 4
news.append(News(date(2024, 1, 14), news_5[0], news_5[1], users[random.randint(0, 9)], news_5[2], Comment.generate_random_comment(users), 0))# 5
news.append(News(date(2016, 6, 26), news_6[0], news_6[1], users[random.randint(0, 9)], news_6[2], Comment.generate_random_comment(users), 0))# 6
news.append(News(date(2016, 6, 14), news_7[0], news_7[1], users[random.randint(0, 9)], news_7[2], Comment.generate_random_comment(users), 0))# 7
news.append(News(date(2021, 12, 2), news_8[0], news_8[1], users[random.randint(0, 9)], news_8[2], Comment.generate_random_comment(users), 0))# 8
news.append(News(date(2021, 12, 2), news_9[0], news_9[1], users[random.randint(0, 9)], news_9[2], Comment.generate_random_comment(users), 0))# 9
news.append(News(date(2018, 4, 12), news_10[0], news_10[1], users[random.randint(0, 9)], news_10[2], Comment.generate_random_comment(users), 0))# 10