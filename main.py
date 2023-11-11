import os
import asyncio
import logging
from PIL import Image
import pytesseract
import replicate
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from typing import BinaryIO

load_dotenv(dotenv_path=".env")

token: str = os.getenv("TOKEN")
model: str = os.getenv("MODEL")

bot = Bot(token=token)
dp = Dispatcher()
MyBinaryIO = BinaryIO
my_object = MyBinaryIO()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# -- LLM API -- #
async def llm_prompt(prompt: str):
    output = replicate.run(
        model,
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": prompt,
            "temperature": 0.75,
            "system_prompt":
            '''
            You are writing high quality documentation for code you are provided with.
            The documentation should concisely cover key aspects of the code.
            ''',
            "max_new_tokens": 500,
            "min_new_tokens": -1
        }
    )

    return "".join(str(item) for item in output)


# -- BOT Handlers -- #
@dp.message(Command("start", "help"))
async def handle_start(message: types.Message):
    await message.answer(text='''
Greetings!
I'm a bot that helps you document your code.
Please send code as plain text, screenshot or a file.
    ''')


@dp.message()
async def handle_message(message: types.Message):
    processing_msg = await message.reply("Processing...")
    if message.photo:
        photo = message.photo[-1]  # Get the last photo
        file_content = await bot.download(photo.file_id)
        image = Image.open(file_content)
        scanned_text = pytesseract.image_to_string(image, lang="eng")
        print(scanned_text)
        llm_response = await llm_prompt(scanned_text)
        await bot.edit_message_text(chat_id=processing_msg.chat.id, message_id=processing_msg.message_id,
                                    text=llm_response)
    if message.document:
        file_info = message.document
        if file_info.file_size <= MAX_FILE_SIZE:
            file_content = await bot.download(file_info)
            file_extension = file_info.file_name.split(".")[-1].lower()
            if file_extension in ["jpg", "jpeg", "png"]:
                try:
                    image = Image.open(file_content)
                    scanned_text = pytesseract.image_to_string(image, lang="eng")
                    print(scanned_text)
                    llm_response = await llm_prompt(scanned_text)
                    await bot.edit_message_text(chat_id=processing_msg.chat.id, message_id=processing_msg.message_id,
                                                text=llm_response)
                except Exception as e:
                    print(e)
                    await message.reply("An error occurred while processing the image. Please try again.")
            file_content_text = file_content.read().decode("utf-8")
            print(file_content_text)
            llm_response = await llm_prompt(file_content_text)
            await bot.edit_message_text(chat_id=processing_msg.chat.id, message_id=processing_msg.message_id,
                                        text=llm_response)
        else:
            await message.reply("Please upload a file less than 5mb.")
    if message.text:
        llm_response = await llm_prompt(message.text)
        await bot.edit_message_text(chat_id=processing_msg.chat.id, message_id=processing_msg.message_id,
                                    text=llm_response)
    await bot.edit_message_text(chat_id=processing_msg.chat.id, message_id=processing_msg.message_id,
                                text="Format is not supported.")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
