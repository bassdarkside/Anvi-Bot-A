import telebot
from telebot import types, apihelper, util
from decouple import config
from .logger_run import start_logging

listen_chat = config("listen_chat")
TOKEN = config("TOKEN")
bot = telebot.TeleBot(TOKEN)


catalog = {
    "chapter1": {
        "markup": "deodorants",
        "chapter_name": "Дезодорант (3)",
        "message": "Фізіологічні дезодоранти",
        "items": ["1", "2", "3"],
    },
    "chapter2": {
        "markup": "balms",
        "chapter_name": "Бальзам для губ (3)",
        "message": "Бальзами для губ і не тільки",
        "items": ["4", "5", "6"],
    },
    "chapter3": {
        "markup": "shampoo",
        "chapter_name": "Очищення (3)",
        "message": "Тверді шампуні",
        "items": ["7", "8", "9"],
    },
    "chapter4": {
        "markup": "care",
        "chapter_name": "Догляд (3)",
        "message": "Бальзами для волосся",
        "items": ["10", "11", "12"],
    },
    "chapter5": {
        "markup": "other",
        "chapter_name": "Інше",
        "message": "Інше",
        "items": ["13"],
    },
}


# Reply Buttons
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📒 Каталог")
    btn2 = types.KeyboardButton("🛍️ Кошик")
    btn3 = types.KeyboardButton("🥑 Корисності")

    markup.row(btn1, btn2)
    markup.add(btn3)

    bot.send_message(
        message.chat.id,
        "Hi, {0.first_name}!".format(message.from_user),
        reply_markup=markup,
    )


# Reply on Catalog button click
@bot.message_handler()
def check_reply(message: types.Message):
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
    from .catalog import read_catalog_from_file

    catalog_items = read_catalog_from_file()
    # go to chapter
    if callback.data in catalog.keys():
        for callback_data_catalog in catalog.keys():
            if callback.data == callback_data_catalog:
                items = catalog[callback_data_catalog]["items"]
                message = catalog[callback_data_catalog]["message"]
                markup = types.InlineKeyboardMarkup()
                for item in items:
                    item_name = catalog_items[item]["name"]
                    item_id = item
                    button = types.InlineKeyboardButton(
                        item_name, callback_data=item_id
                    )
                    markup.row(button)
                bot.edit_message_text(
                    message,
                    callback.message.chat.id,
                    callback.message.message_id,
                    reply_markup=markup,
                )
    # go to item page
    elif callback.data in catalog_items.keys():
        markup = types.InlineKeyboardMarkup()
        for id in catalog_items.keys():
            if callback.data == id:
                chapter = catalog_items[id]["chapter"]
                back = types.InlineKeyboardButton(
                    "⬅️ Назад до категорії",
                    callback_data=f"back_to_chapter_{chapter}",
                )
                item_name = catalog_items[id]["name"]
                item_image = catalog_items[id]["image"]
                item_price = catalog_items[id]["price"]
                id_description = str(id) + "_description"
                description = types.InlineKeyboardButton(
                    "Опис продукту", callback_data=f"{id}_description"
                )
                add_to_cart = types.InlineKeyboardButton(
                    "Додати у кошик", callback_data="cart"
                )
                sum = types.InlineKeyboardButton(
                    item_price, callback_data="sum"
                )
                markup.row(description)
                markup.row(add_to_cart)
                markup.row(sum)
                markup.row(back)
                bot.delete_message(
                    callback.message.chat.id, callback.message.message_id
                )
                bot.send_photo(
                    callback.message.chat.id,
                    item_image,
                    caption=item_name,
                    reply_markup=markup,
                )
    # go to item description
    elif callback.data.endswith("_description"):
        item_id = callback.data.replace("_description", "")
        markup = types.InlineKeyboardMarkup()
        for id in catalog_items.keys():
            if item_id == id:
                item_name = catalog_items[id]["name"]
                item_image = catalog_items[id]["image"]
                item_description = catalog_items[id]["description"]
                back = types.InlineKeyboardButton(
                    "⬅️ Назад до продукту",
                    callback_data=f"back_to_item_{item_id}",
                )
                markup.row(back)
                bot.delete_message(
                    callback.message.chat.id, callback.message.message_id
                )
                bot.send_photo(
                    callback.message.chat.id, item_image, caption=item_name
                )
                for description in util.split_string(item_description, 3000):
                    bot.send_message(
                        callback.message.chat.id,
                        item_description,
                        parse_mode="HTML",
                        reply_markup=markup,
                    )
    # back description -> item (the description message is left)
    elif callback.data.startswith("back_to_item_"):
        item_id = callback.data.replace("back_to_item_", "")
        markup = types.InlineKeyboardMarkup()
        for id in catalog_items.keys():
            if item_id == id:
                chapter = catalog_items[id]["chapter"]
                back = types.InlineKeyboardButton(
                    "⬅️ Назад до категорії",
                    callback_data=f"back_to_chapter_{chapter}",
                )
                item_name = catalog_items[id]["name"]
                item_image = catalog_items[id]["image"]
                item_price = catalog_items[id]["price"]
                description = types.InlineKeyboardButton(
                    "Опис продукту", callback_data=f"{id}_description"
                )
                add_to_cart = types.InlineKeyboardButton(
                    "Додати у кошик", callback_data="cart"
                )
                sum = types.InlineKeyboardButton(
                    item_price, callback_data="sum"
                )
                markup.row(description)
                markup.row(add_to_cart)
                markup.row(sum)
                markup.row(back)
                bot.send_photo(
                    callback.message.chat.id,
                    item_image,
                    caption=item_name,
                    reply_markup=markup,
                )
    # back item -> chapter
    elif callback.data.startswith("back_to_chapter_"):
        chapter = callback.data.replace("back_to_chapter_", "")
        markup = types.InlineKeyboardMarkup()
        for chapter_catalog in catalog.keys():
            if chapter_catalog == chapter:
                items = catalog[chapter]["items"]
                message = catalog[chapter]["message"]
                markup = types.InlineKeyboardMarkup()
                for item in items:
                    item_name = catalog_items[item]["name"]
                    item_id = item
                    button = types.InlineKeyboardButton(
                        item_name, callback_data=item_id
                    )
                    markup.row(button)
                bot.delete_message(
                    callback.message.chat.id, callback.message.message_id
                )
                bot.send_message(
                    callback.message.chat.id, message, reply_markup=markup
                )


def listener(messages):
    for m in messages:
        chat_id = m.chat.id
        user_name = m.chat.username
        text = m.text

    bot.send_message(
        listen_chat,
        f"user_id: {chat_id}\nuser_name: {user_name}\n message: {text}",
    )


# Starting the bot
def bot_run():
    try:
        print("Bot starting..")
        apihelper.SESSION_TIME_TO_LIVE = 5 * 60
        apihelper.RETRY_ON_ERROR = True
        start_logging()
        bot.set_update_listener(listener)
        bot.infinity_polling()
    except Exception as err:
        print(err)


if __name__ == "__main__":
    bot_run()
