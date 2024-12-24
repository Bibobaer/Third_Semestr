from aiogram import Bot, Dispatcher, F
import asyncio
import sys
import logging
from config import *
from DateBase import *
import game

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

user_sessions = {}

global_keyboard = [
    [InlineKeyboardButton(text="⬆", callback_data="move_w")],
    [InlineKeyboardButton(text="⬅", callback_data="move_a"), InlineKeyboardButton(text="⬇", callback_data="move_s"), InlineKeyboardButton(text="➡", callback_data="move_d")],
    [InlineKeyboardButton(text="Пауза", callback_data="stop_1")],
    [InlineKeyboardButton(text="Выйти", callback_data="stop_3")]
]


@dp.message(Command("game"))
async def game_command_handler(message: Message):
    user_id = message.from_user.id

    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "in_game": True,
            "score": 0,
            "field": game._init_field(),
        }

    if user_id in user_sessions and user_sessions[user_id]["in_game"]:
        await message.answer("Вы уже в игре.")
        return

    user_sessions[user_id] = {
        "in_game": True,
        "score": 0,
        "field": game._init_field(),
    }

    caption = f"Game 2048\nСчёт: {0}"
    field = user_sessions[user_id]["field"]

    game._draw_field(field, user_id)
    photo = FSInputFile(f"game_grid_{user_id}.png")

    await bot.send_photo(chat_id=user_id, photo=photo, caption=caption, reply_markup=InlineKeyboardMarkup(inline_keyboard=global_keyboard))

@dp.callback_query(F.data.startswith("stop_"))
async def pause_handler(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    _, s_id = callback_query.data.split('_')
    s_id = int(s_id)

    keyboard = global_keyboard
    res_text = "Game 2048"
    photo = FSInputFile(f"game_grid_{user_id}.png")

    if (s_id == 1):
        Score = user_sessions[user_id]["score"]
        photo = FSInputFile("pause.png")
        keyboard = [[InlineKeyboardButton(text="Вернуться в игру", callback_data="stop_2")]]
        res_text = f"Ваши очки: {Score}"
    elif (s_id == 3):
        score = user_sessions[user_id]["score"]
        try:
            db = DataBase()
            await db.initialize_connection()
        except Exception as e:
            print(e)

        if await db.is_top_one(score):
            list_top = await db.get_first_five_raiting()
            us = await bot.get_chat(user_id)
            for el in list_top:
                if (el == user_id):
                    await bot.send_message(chat_id=user_id, text="Вы побили свой рекорд!")
                else:
                    await bot.send_message(chat_id=el, text=f"Игрок {us.first_name} побил ваш рекорд!")

        if (score > await db.get_rank(user_id)):
            await db.update_rank(user_id, score)

        user_sessions[user_id]["in_game"] = False
        photo = FSInputFile("exit.png")
        Record = await db.get_rank(user_id)
        keyboard = [[]]
        res_text=f"Вы вышли из игры.\nВаши текущие очки: {score}\nВаш рекорд: {Record}"
        

    await callback_query.message.edit_media(media=InputMediaPhoto(media=photo,caption=res_text), reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    
@dp.callback_query(F.data.startswith("move_"))
async def movement_handler(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id not in user_sessions or not user_sessions[user_id]["in_game"]:
        await callback_query.answer("Вы не в игре.")
        return

    user_session = user_sessions[user_id]
    field = user_session["field"]
    score = user_session["score"]

    _, direction = callback_query.data.split('_')

    old_field = [row[:] for row in field]
    field, score = game.move(field, direction, score)

    if field != old_field:
        game._add_tile(field)

    if game._game_over(field):
        try:
            db = DataBase()
            await db.initialize_connection()
        except Exception as e:
            print(e)


        if await db.is_top_one(score):
            list_top = await db.get_first_five_raiting()
            us = await bot.get_chat(user_id)
            for el in list_top:
                if el == user_id:
                    await bot.send_message(chat_id=user_id, text="Вы побили свой рекорд")
                else:
                    await bot.send_message(chat_id=el, text=f"Игрок {us.first_name} побил ваш рекорд!")

        if (score > await db.get_rank(user_id)):
            await db.update_rank(user_id, score)

        user_sessions[user_id]["in_game"] = False
        photo = FSInputFile("lose.png")
        Record = await db.get_rank(user_id)
        await callback_query.message.edit_media(media=InputMediaPhoto(media=photo, caption=f"Вы проиграли.\nВаши текущие очки: {score}\nВаш рекорд: {Record}"))
        return

    user_sessions[user_id]["field"] = field
    user_sessions[user_id]["score"] = score

    game._draw_field(field, user_id)
    photo = FSInputFile(f"game_grid_{user_id}.png")
    caption = f"Game 2048\nСчёт: {score}"
    markup = InlineKeyboardMarkup(inline_keyboard=global_keyboard)

    await callback_query.message.edit_media(
        media=InputMediaPhoto(media=photo, caption=caption),
        reply_markup=markup
    )


@dp.message(Command("rank"))
async def rating_handler(message: Message):
    if message.from_user.id not in user_sessions or user_sessions[message.from_user.id]["in_game"]:
        await message.answer("Вы не можете использовать эту команду, пока находитесь в игре.")
        return

    try:
        db = DataBase()
        await db.initialize_connection()
    except Exception as e:
        print(e)

    list_users = await db.get_raiting()
    if len(list_users) == 0:
        await message.answer("База пуста")
        return

    index = 0
    for k, v in list_users.items():
        tmp = await bot.get_chat(k)
        index += 1
        await message.answer(f"{index}) User: {tmp.first_name}\nRank: {v}")


@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "in_game": False,
            "score": 0,
            "field": game._init_field(),
        }

    try:
        db = DataBase()
        await db.initialize_connection()
    except Exception as e:
        print(e)

    if not await db.is_exist(user_id):
        await db.add_user(user_id)

    await message.answer(start_message)


@dp.message(Command("description"))
async def help_handler(message: Message):
    await message.answer(descr_message)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
