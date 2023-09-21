import asyncio
import logging
from decouple import config
import telebot
from telebot import apihelper, types
from parser_v2_1.main import main
from catalog import get_data_from_file

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# @AnviTest_Bot
TEST_BOT = config("TEST_BOT")
bot = telebot.TeleBot(TEST_BOT)
parse_ = main()
print(parse_)
catalog = get_data_from_file()


# Reply Buttons
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📒 Каталог")
    btn2 = types.KeyboardButton("🛍️ Кошик")
    btn3 = types.KeyboardButton("🥑 Корисності")
    btn_ = types.KeyboardButton("test_btn_update_cat_")
    markup.row(btn1, btn2)
    markup.add(btn3)
    markup.add(btn_)

    text = (
        "Привіт, {user_fist_name}!\n"
        "Я AnviBot, твій помічник у придбанні,\n"
        "косметичних товарів бренду Anvibodycare.\n\n"
        "Віримо у світле екологічне майбутнє нашої землі🤍\n"
    )
    text = text.format(user_fist_name=message.from_user.first_name)
    bot.send_message(
        message.chat.id,
        text.format(message.from_user),
        reply_markup=markup,
    )


# Reply on Catalog button click
@bot.message_handler()
def check_reply(message: types.Message):
    global catalog
    if message.text == "test_btn_update_cat_":
        bot.send_message(message.chat.id, "Updating...Please wait...")
        try:
            main()
            bot.send_message(message.chat.id, "Data updated.")
            catalog = get_data_from_file()
            bot.send_message(message.chat.id, "Catalog updated.")
        except Exception as e:
            bot.send_message(message.chat.id, e)
    if message.text == "📒 Каталог":
        markup = types.InlineKeyboardMarkup()
        for chapter in catalog.keys():
            name = catalog[chapter]["chapter_name"]
            button = chapter
            button = types.InlineKeyboardButton(name, callback_data=chapter)
            markup.row(button)
        bot.send_message(
            message.chat.id, "Дивись, що в нас є 🥰", reply_markup=markup
        )


# Chapter -> Items (InlineButtons menu updating)
@bot.callback_query_handler(func=lambda callback: True)
def callback_chapter(callback):
    global catalog
    for callback_data_catalog, chapter_v in catalog.items():
        items = catalog[callback_data_catalog]["items"]
        message = catalog[callback_data_catalog]["message"]

        if callback.data == callback_data_catalog:
            markup = types.InlineKeyboardMarkup()
            for item in items:
                item_name = items[item]["name"]
                # item_price = items[item]["price"]

                button = item
                button = types.InlineKeyboardButton(
                    item_name, callback_data=item
                )
                markup.row(button)

            bot.edit_message_text(
                message,
                callback.message.chat.id,
                callback.message.message_id,
                reply_markup=markup,
            )


if __name__ == "__main__":
    try:
        apihelper.SESSION_TIME_TO_LIVE = 5 * 60
        apihelper.RETRY_ON_ERROR = True
        asyncio.run(bot.infinity_polling())
    except Exception as e:
        print(e)
