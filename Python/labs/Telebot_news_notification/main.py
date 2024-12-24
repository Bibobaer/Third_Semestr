import asyncio
import logging
import sys
from config import *
from time import sleep, time
from typing import Union

from DateBase import DB
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# ← →

first_pars = True

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

first_pars = True

users: list[int] = [
    1241922337,
    1549656976
]


async def Parse_News():
    try:
        DateBase = DB()
        await DateBase.initialize_connection()
    except Exception:
        return

    driver = webdriver.WebDriver()
    driver.get("https://stopgame.ru/news")
    news_div = driver.find_element(By.XPATH, "/html/body/main/section/div[2]/section/div/div[1]")
    news_list = news_div.find_elements(By.CSS_SELECTOR, "div[data-key]")
    await asyncio.sleep(5)

    for el in news_list:
        title = el.find_element(By.CSS_SELECTOR, 'div[class=_card_1vlem_1]>div[class=_content_1vlem_159]>a')
        if not await DateBase.is_news_exists(title.text):
            link = title.get_attribute('href')
            full_news = Parse_Text_By_Link(link)
            date = el.find_element(By.CSS_SELECTOR, 'div>div>div>div>span').text
            await asyncio.sleep(4)
            await DateBase.add_news(title.text, date, link, full_news)
            for _id in users:
                tmp = bot_send_mes + title.text
                await bot.send_message(chat_id=_id, text=tmp)    
        else:
            driver.close()
            return

    driver.close()

def Parse_Text_By_Link(link: str) -> str:
    driver = webdriver.WebDriver()
    driver.get(link)

    result_text = ""

    text_div = driver.find_element(By.CSS_SELECTOR, 'div[class=_content_ghawu_13]')
    text_list = text_div.find_elements(By.CSS_SELECTOR, 'p')

    cnt = 0
    for elem in text_list:
        result_text += elem.text
        cnt += 1
        if (cnt == 2):
            break

    driver.close()
    return result_text

@dp.callback_query(F.data.startswith("next_"))
async def Process_Callback_Button_Next_News(callback_query: CallbackQuery):
    _, s_id = callback_query.data.split('_')
    s_id: int = int(s_id)

    try:
        db = DB()
        await db.initialize_connection()
    except Exception:
        return

    keyboard = []
    if (s_id == 1):
        keyboard.append([InlineKeyboardButton(text="→", callback_data=f"next_{s_id+1}")])
    elif (s_id == await db.max_id()):
        keyboard.append([InlineKeyboardButton(text="←", callback_data=f"next_{s_id-1}")])
    else:
        keyboard.append([InlineKeyboardButton(text="←", callback_data=f"next_{s_id-1}"), InlineKeyboardButton(text="→", callback_data=f"next_{s_id+1}")])

    keyboard.append([InlineKeyboardButton(text="Посмотреть полную новость", callback_data=f"get_{s_id}")])

    info = await db.get_info(s_id)
    result_message = f"Номер новости: {info[0]}\n<b>{info[1]}</b>\nДата выпуска: {info[2]}"
    await callback_query.message.edit_text(result_message, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

@dp.callback_query(F.data.startswith("get_"))
async def Process_Callback_Button_Get_News(callback_query: CallbackQuery):
    _, s_id = callback_query.data.split('_')
    try:
        db = DB()
        await db.initialize_connection()
    except Exception:
        return
    
    full_n = await db.get_full_news(s_id)
    link = await db.get_link(s_id)
    full_n += f"\nСсылка на новость: {link}"

    keyboard = []
    keyboard.append([InlineKeyboardButton(text="Вернуться назад", callback_data=f"next_{s_id}")])

    await callback_query.message.edit_text(full_n, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

@dp.message(CommandStart())
async def Start_Command(message: Message):
    global users
    if message.from_user.id not in users:
        users.append(message.from_user.id)

    await message.answer(start_mes)

@dp.message(Command("list"))
async def List_Command(message: Union[Message, CallbackQuery]):
    keyboard = []
    try:
        DateBase = DB()
        await DateBase.initialize_connection()
    except Exception:
        return
    
    news = await DateBase.get_info(1)

    keyboard.append([InlineKeyboardButton(text="→", callback_data="next_2")])
    keyboard.append([InlineKeyboardButton(text="Посмотреть полную новость", callback_data="get_1")])
    if isinstance(message, CallbackQuery):
        await message.answer("")

    res_mes = f"Номер новости: {news[0]}\n<b>{news[1]}</b>\nДата выпуска: {news[2]}"
    await bot.send_message(chat_id=message.chat.id if isinstance(message, Message) else message.message.chat.id,
                           text = res_mes,
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
                        )

@dp.message()
async def Echo_Handler(message: Message):
    return

async def Check_Updates():
    while True:
        before_comp = time()
        await Parse_News()
        after_comp = time()
        await asyncio.sleep(900 - (after_comp - before_comp))

async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(Check_Updates())
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")