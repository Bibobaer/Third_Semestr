import asyncio
import json
import logging
import subprocess
import sys
import time
from pathlib import Path
from random import randint

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, File
from aiogram.utils.markdown import hlink
from vosk import Model, KaldiRecognizer

TOKEN = "Your_Token"

dp = Dispatcher()
bot: Bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

model = None

def text_to_number(text):
    numbers = {
        'ноль': 0,
        'один': 1,
        'два': 2,
        'три': 3,
        'четыре': 4,
        'пять': 5,
        'шесть': 6,
        'семь': 7,
        'восемь': 8,
        'девять': 9,
        'десять': 10,
        'одиннадцать': 11,
        'двенадцать': 12,
        'тринадцать': 13,
        'четырнадцать': 14,
        'пятнадцать': 15,
        'шестнадцать': 16,
        'семнадцать': 17,
        'восемнадцать': 18,
        'девятнадцать': 19,
        'двадцать': 20
    }
    return numbers.get(text)

async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")

@dp.message(F.voice)
async def Voice_handle(message: Message):
    file_id = message.voice.file_id
    voice = await bot.get_file(file_id)
    path = "./files/voices"

    await handle_file(file=voice, file_name=f"{voice.file_id}.ogg", path=path)
    bot_msg = await message.reply("Успешно скачено! Ожидайте преобразования в текст...")

    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    process = subprocess.Popen(
        ["ffmpeg.exe",
         "-loglevel", "quiet",
         "-i", f"{path}/{voice.file_id}.ogg",  # имя входного файла
         "-ar", "16000",  # частота выборки
         "-ac", "1",  # кол-во каналов
         "-f", "s16le",  # кодек для перекодирования, у нас wav
         "-"  # имя выходного файла нет, тк читаем из stdout
         ],
        stdout=subprocess.PIPE
    )

    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            pass

    # Возвращаем распознанный текст в виде str
    result_json = rec.FinalResult()  # это json в виде str
    result_dict = json.loads(result_json)  # это dict

    print(result_dict["text"])

    if ("погода" in result_dict["text"] or "какая погода" in result_dict["text"] or "скажи погоду" in result_dict["text"] or "скинь погоду" in result_dict["text"]):
        if ("москв" in result_dict["text"]):
            city: str = "Moscow"
        elif ("курган" in result_dict["text"]):
            city: str = "Kurgan"
        elif ("астан" in result_dict["text"]):
            city: str = "Astana"
        else:
            city: str = "Chelyabinsk"

        print(city)

        if (("через" in result_dict["text"] and "дней" in result_dict["text"]) or ("через" in result_dict["text"] and "час" in result_dict["text"]) or ("через" in result_dict["text"] and "день" in result_dict["text"]) or ("через" in result_dict["text"] and "дня" in result_dict["text"])):
            start = result_dict["text"].find("через")
            if ("дней" in result_dict["text"]):
                end = result_dict["text"].find("дней")
                len_mes = len("дней")
            elif ("день" in result_dict["text"]):
                end = result_dict["text"].find("день")
                len_mes = len("день")
            elif ("дня" in result_dict["text"]):
                end = result_dict["text"].find("дня")
                len_mes = len("дня")
            else:
                end = result_dict["text"].find("час")
                len_mes = len("час")

            number = text_to_number(''.join(result_dict["text"][start+len_mes:end].split(' ')[1:-1]))
            if (("дней" in result_dict["text"]) or ("день" in result_dict["text"]) or "дня" in result_dict["text"]):
                number *= 3600 * 24
            else:
                number *= 3600
        else:
            number = 0

        if ("послезавтра" in result_dict["text"]):
            number = 3600 * 24 * 2
        elif ("завтра" in result_dict["text"]):
            number = 3600 * 24

        print(number)
            
        ts_now = int(time.time()) + number
        url = f"https://vwapi.mxf.su/?lang=ru&city={city}&timestamp={ts_now}"
        await message.answer(text=f"Погода{hlink(" ", url=url)}в {city}", disable_web_page_preview=False)
    if (("спасибо" in result_dict["text"]) or ("благодарю" in result_dict["text"]) or ("большое спасибо" in result_dict["text"]) or ("родина вас не забудет" in result_dict["text"])):
        excuse_message = ["Всегда пожалуйства", "Рад помочь", "Не за что", "Готов к вашим услугам", "На здоровье! Теперь ты мне должен один виртуальный поцелуй! 😘", "Вам спасибо, что сделали мою вычислительную жизнь чуть-чуть веселее! 🎉"]
        await bot_msg.answer(text=f"{excuse_message[randint(0, len(excuse_message)-1)]}")
        return
    return
    

@dp.message(CommandStart())
async def Start_handle(message: Message):
    ts_now = int(time.time())
    url = f"https://vwapi.mxf.su/?lang=ru&city=Chelyabinsk&timestamp={ts_now}"
    await bot.send_message(message.from_user.id, f"Погода{hlink(" ", url=url)}сейчас", disable_web_page_preview=False)

async def main():
    global model
    model = Model("vosk-model-small-ru-0.22")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")