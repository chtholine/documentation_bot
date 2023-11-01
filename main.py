import os
import asyncio
import logging
import replicate
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

load_dotenv(dotenv_path=".env")

# -- BOT -- #
token: str = os.getenv("TOKEN")

bot = Bot(token=token)
dp = Dispatcher()


@dp.message
async def echo(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,

    )


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


# -- LLM API -- #

def llm():
    output = replicate.run(
        "joehoover/zephyr-7b-alpha:14ec63365a1141134c41b652fe798633f48b1fd28b356725c4d8842a0ac151ee",
        input={"system_prompt": "You are writing high quality documentation for code.",
               "min_new_tokens": 1,
               "max_new_tokens": 500,
               "temperature": 0.75,
               "top_p": 0.9,
               "top_k": 50,
               "prompt": '''
                    
               '''}
    )
    # The joehoover/zephyr-7b-alpha model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    for item in output:
        # https://replicate.com/joehoover/zephyr-7b-alpha/versions/14ec63365a1141134c41b652fe798633f48b1fd28b356725c4d8842a0ac151ee/api#output-schema
        print(item, end="")
