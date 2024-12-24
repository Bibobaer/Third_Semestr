import asyncio
from config import *

from Bots_User import BotUser
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

bot: Bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

users: dict[int, list[BotUser]] = {
    ADMIN_ID : []
}

book: list[list[tuple[int, BotUser]]] = []

list_of_id_needful_users: list[int] = []

def isAdmin(id: int) -> bool:
    return True if id == ADMIN_ID else False

@dp.message(CommandStart())
async def Start_Command(message: Message) -> None:
    global users, bot
    if message.from_user.id not in users:
        return

    us = await bot.get_me()
    await message.answer("Привет! Я <b>" + us.first_name + "</b> - являюсь подопытным кроликом <b>Артурчика</b>.\nСписок команд:\n1) <u>/test</u> - Начало тестирования\n2) <u>/admin</u> - Просмотор всех пользователей (для админа)\n3) <u>/send</u> - Ищет Айди пользователей с общими интересами и отправляет сообщение от админа (для админа)")

@dp.message(Command("test"))
async def Test_Command(message: Message) -> None:
    global users, STATE_OF_USER, temp_name, temp_lastname, temp_midname, temp_age, temp_interests
    if message.from_user.id not in users:
        return
    
    STATE_OF_USER[message.from_user.id] = 1

    temp_name = ""
    temp_lastname = ""
    temp_midname = ""
    temp_age = 0
    temp_interests = []
    
    cur_st = STATE_OF_USER[message.from_user.id]

    if cur_st == 1:
        return await TStep_One(message)
    if cur_st == 2:
        return await TStep_Two(message)
    if cur_st == 3:
        return await TStep_Three(message)
    if cur_st == 4:
        return await TStep_Four(message)

async def TStep_One(message: Message) -> None:
    global STATE_OF_USER
    if message.text is not None and message.text == "/test":
        STATE_OF_USER[message.from_user.id] = 2
        await message.answer("Введите ФИО через пробел.")
    else:
        await message.answer("Для начала теста нужно ввести команду /test")


async def TStep_Two(message: Message) -> None:
    global STATE_OF_USER, temp_lastname, temp_name, temp_midname

    if message.text is not None:
        LNm: list[str] = message.text.split(' ')
        if len(LNm) != 3:
            await message.answer("Вы не ввели какие то данные")
            return
        temp_lastname, temp_name, temp_midname = LNm

        STATE_OF_USER[message.from_user.id] = 3
        await message.answer("Отлично! Теперь введите ваш возраст.")
    else:
        await message.answer("Е, орыс тілінде жазылған. мәтінді енгізіңіз")

async def TStep_Three(message: Message) -> None:
    global STATE_OF_USER, temp_age
    if message.text is not None:
        Age: int = int(message.text)
        if Age <= 0 or message.text.isdigit() == False:
            await message.answer("Возраст не может быть меньше нуля")
            return
        temp_age = Age
        STATE_OF_USER[message.from_user.id] = 4
        await message.answer("Готово! Теперь введите интересы через запятую")
    else:
        await message.answer("Е, орыс тілінде жазылған. мәтінді енгізіңіз")

async def TStep_Four(message: Message) -> None:
    global STATE_OF_USER, temp_interests, temp_age, temp_lastname, temp_midname, temp_name, users
    if message.text is not None:
        temp_interests = message.text.split(', ')

        STATE_OF_USER.pop(message.from_user.id)

        users[message.from_user.id].append(BotUser(temp_name, temp_lastname, temp_midname, temp_age, temp_interests))
        await message.answer("Пользователь создан!")
    else:
        await message.answer("Е, орыс тілінде жазылған. мәтінді енгізіңіз")

@dp.message(Command("admin"))
async def Admin_Command(message: Message) -> None:
    global book
    if message.from_user.id not in users:
        return
    if isAdmin(message.from_user.id) == False:
        await message.answer("Вы не являетесь админом")
        return
    
    tests_list = [(us_id, test) for us_id, tests in users.items() for test in tests]

    for i in range(0, len(tests_list), 3):
        book.append(tests_list[i:i + 3])

    STATE_OF_USER[message.from_user.id] = 52
    await message.answer("Введите страницу (от 1 до кол-ва страниц). Текущие кол-во страниц: {}".format(len(book)))

async def Adm_Step(message: Message) -> None:
    if message.text is not None:
        if message.text.isdigit() == False:
            await message.answer("Вы ввели не число")
            return
        index_of_page: int = int(message.text) - 1
        if (index_of_page < 0 or index_of_page >= len(book)):
            await message.answer("Вы пытаетесь выйти за пределы кол-ва страниц")
            return
        
        page = book[index_of_page]
        STATE_OF_USER.pop(message.from_user.id)
        for i in page:
            tmp = await bot.get_chat(i[0])
            await message.answer("User: <b>{}</b>\n{}".format(tmp.first_name, str(i[1])))
        book.clear()
        await message.answer("Номер страницы: {}".format(index_of_page+1))
    else:
        await message.answer("Е, орыс тілінде жазылған. мәтінді енгізіңіз")

@dp.message(Command("send"))
async def Sending_Func(message: Message) -> None:
    if message.from_user.id not in users:
        return
    if isAdmin(message.from_user.id) == False:
        await message.answer("Вы не являетесь админом")
        return 
    
    STATE_OF_USER[message.from_user.id] = 1486
    await message.answer("Введите интерес по которому надо искать пользователей")

async def Send_Step_One(message: Message) -> None:
    global list_of_id_needful_users
    if message.text is not None:
        for user_id, list_of_tests in users.items():
            for us in list_of_tests:
                if (message.text in us.interests):
                    list_of_id_needful_users.append(user_id)
                    
        list_of_id_needful_users = list(set(list_of_id_needful_users))
        
        if (len(list_of_id_needful_users) == 0):
            await message.answer("Не удалось найти пользователей с таким интересом")
            return
        
        STATE_OF_USER[message.from_user.id] = 1487
        await message.answer("Супер! теперь введите сообщение, которое надо выслать")
    else:
        await message.answer("Е, орыс тілінде жазылған. мәтінді енгізіңіз")

async def Send_Step_Two(message: Message):
    if message.text is not None:
        for id in list_of_id_needful_users:
            await bot.send_message(chat_id=id, text=message.text)
        
        STATE_OF_USER.pop(message.from_user.id)
        list_of_id_needful_users.clear()
    else:
        await message.answer("Е, орыс тілінде жазылған. мәтінді енгізіңіз")

@dp.message()
async def handle_state(message: Message) -> None:
    global STATE_OF_USER
    user_id = message.from_user.id
    if user_id not in STATE_OF_USER:
        return
    
    current_state = STATE_OF_USER[user_id]
    if current_state == 2:
        await TStep_Two(message)
    elif current_state == 3:
        await TStep_Three(message)
    elif current_state == 4:
        await TStep_Four(message)
    elif current_state == 52:
        await Adm_Step(message)
    elif current_state == 1486:
        await Send_Step_One(message)
    elif current_state == 1487:
        await Send_Step_Two(message)

async def main() -> None:
    global bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")