import asyncio
import json
import logging
import sys
from typing import Union
from config import TOKEN

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


dp = Dispatcher()

file_name = "3_lec.json"

json_data = {}

value_keys = {
    
}

id_keys = {
    # id1 = key1
    # id2 = key1->key1.1
    # id3 = key1->key1.2
    # id4 = key2
}

bot: Bot = None


@dp.callback_query(F.data.startswith("get_"))
async def process_callback_button1(callback_query: CallbackQuery):
    _, s_id = callback_query.data.split('_')
    s_id: int = int(s_id)
    
    result_message = f"Получение данных из: {'.'.join(id_keys[str(s_id)])}\n\n"
    keyboard = [[InlineKeyboardButton(text="Вернуться назад", callback_data=get_parent_callback(s_id))]]

    if (tuple(id_keys[str(s_id)]) not in value_keys.keys()):
        for key in id_keys.values():
            if set(key).issuperset(set(id_keys[str(s_id)])) and len(key) == (len(id_keys[str(s_id)]) + 1):
                e_id: int = get_id_by_keys(list(key))
                start_ind = list(key).index(id_keys[str(s_id)][0])
                end_ind = start_ind + len(id_keys[str(s_id)])
                elem = (list(key)[:start_ind] + list(key)[end_ind:])[0]
                if (len(elem) > 64):
                    elem = elem[:61] + "..."
                keyboard.append([InlineKeyboardButton(text=f"{elem}", callback_data=f"get_{e_id}")])
    else:
        result_message += str(value_keys[tuple(id_keys[str(s_id)])])
    
    await callback_query.message.edit_text(result_message,
                                           reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


def get_id_by_keys(keys: list[str]):
    global id_keys
    for s_id, value in id_keys.items():
        if value == keys:
            return s_id
    raise RuntimeError("Not found key!")

def get_all_keys_and_values(d, parent_key=None):
    items = {}
    if parent_key is None:
        parent_key = []
    for k, v in d.items():
        new_key = parent_key + [k]
        if isinstance(v, dict):
            items.update(get_all_keys_and_values(v, new_key))
        else:
            items[tuple(new_key)] = v
    return items

def get_parent_callback(s_id: int):
    global id_keys
    value = id_keys[str(s_id)]
    if len(value) == 1:
        return "home"
    return f"get_{get_id_by_keys(value[:-1])}"


@dp.callback_query(F.data.startswith("home"))
@dp.message(CommandStart())
async def echo_handler(message: Union[Message, CallbackQuery]) -> None:
    global json_data
    keyboard = []
    for key in json_data.keys():
        keyboard.append([InlineKeyboardButton(text=f"{key}", callback_data=f"get_{get_id_by_keys([key])}")])
    if isinstance(message, CallbackQuery):
        await message.answer("")
    await bot.send_message(chat_id=message.chat.id if isinstance(message, Message) else message.message.chat.id,
                           text="Выберите ключ для получения значения", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        ))


def generate_ids(filename: str):
    global value_keys
    global id_keys
    global json_data
    with open(filename, "r", encoding="utf-8") as file:
        json_data = json.load(file)
        i = 0
        for key in [*get_keys(json_data)]:
            id_keys[str(i)] = key.split('.')
            i += 1
        print(id_keys)
    value_keys = get_all_keys_and_values(json_data)

def get_keys(d, curr_key=[]):
    if isinstance(d, dict):
        for k, v in d.items():
            yield '.'.join(curr_key + [k])
            if isinstance(v, dict):
                yield from get_keys(v, curr_key + [k])
            elif isinstance(v, list):
                for i in v:
                    yield from get_keys(i, curr_key + [k])

async def main() -> None:
    global bot
    generate_ids(filename=file_name)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")