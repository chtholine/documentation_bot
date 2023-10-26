import logging
import replicate
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# -- BOT -- #

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    application = ApplicationBuilder().token('6717943592:AAH94Y12ASClJwACDdF19YQSnYeQGJx0_0w').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()


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
