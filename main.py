import os
import asyncio
import logging

import replicate
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

load_dotenv(dotenv_path=".env")

# -- BOT -- #
token: str = os.getenv("TOKEN")

bot = Bot(token=token)
dp = Dispatcher()


# -- LLM API -- #
async def llm_prompt(prompt):
    output = replicate.run(
        "joehoover/zephyr-7b-alpha:14ec63365a1141134c41b652fe798633f48b1fd28b356725c4d8842a0ac151ee",
        input={
            "system_prompt": "You are writing high quality documentation for code.",
            "min_new_tokens": 1,
            "max_new_tokens": 500,
            "temperature": 0.75,
            "top_p": 0.9,
            "top_k": 50,
            "prompt": prompt,  # Use the user's message as the prompt
        }
    )

    return "".join(str(item) for item in output)


# -- BOT Handlers -- #
@dp.message(Command("start"))
async def handle_start(message: types.Message):
    await message.answer(text='''
Greetings!
I'm a bot that helps you document your code.
Please send code as plain text or a file.
    ''')


@dp.message()
async def echo(message: types.Message):
    processing_msg = await message.reply("Processing...")
    llm_response = await llm_prompt(message.text)
    await bot.edit_message_text(chat_id=processing_msg.chat.id, message_id=processing_msg.message_id, text=llm_response)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    