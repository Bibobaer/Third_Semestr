from var import *
import os

print(f"{"\n\n".join(str(user) for user in users)}")

os.system("pause")

c = ''
while True:
    print(f"{"\n\n".join(str(n) for n in news)}")

    c = input("Хочешь лайкнуть новость(коммент)? (Y/n): ")

    if (c == 'n'):
        break
    if (c != 'Y'):
        os.system("cls")
        continue

    id_n = int(input("Введи айди новости, которую хочешь лайкнуть: "))
    N: News = None
    for i in range(len(news)):
        if (id_n == news[i].id):
            N = news[i]
            break
    if (N is None):
        print("Этой новости нет")
    else:
        ch = input("Ты хочешь лайкнуть саму новость или коммент под ней? (News/Comment): ")
        id_user = int(input("Введите айди пользователя: "))
        needful_user = None
        for i in range(len(users)):
            if (id_user == users[i].id):
                needful_user = users[i]
                break
        if (needful_user is None):
            print("Пользователь не найден")
        else:
            if (ch == "News"):
                if (needful_user not in N.who_like):
                    N.who_like.append(needful_user)
                    N.like_news()
            elif (ch == "Comment"):
                id_com = int(input("Введи айди коммента: "))
                for i in range(len(N.comments)):
                    if (id_com == N.comments[i].id and needful_user not in N.comments[i].who_like):
                        N.comments[i].who_like.append(needful_user)
                        N.like_comment_by_id(id_com)
                        break

os.system("pause")
os.system("cls")

print(f"Репутация пользователей: ")
print("Username -> Reputation")
for i in range(len(users)):
    print(f"{i+1}) {users[i].username} -> {users[i].reputation}")