import time
import threading
import schedule
from schedule import every, repeat
import telebot
from telebot import types, custom_filters, util
from decouple import config
from bot_start.catalog import read_catalog
from parser_v2.main import scrape_url, make_catalog

listen_chat = config("listen_chat")
ADMIN = int(config("ADMIN"))
TOKEN = config("TOKEN")
bot = telebot.TeleBot(TOKEN)


catalog = {
    "body": {
        "markup": "body",
        "chapter_name": "Тіло",
        "message": "Фізіологічні дезодоранти, крем для рук",
        "items": ["body1", "body3", "body4"],  # "body2"
        "chapter_img": "https://anvibodycare.com/wp-content/uploads/2023/09/katehoriia-1-300x300.jpg",
    },
    "face": {
        "markup": "face",
        "chapter_name": "Бальзами для губ",
        "message": "Бальзами для губ і не тільки",
        "items": ["face1", "face2", "face3"],
        "chapter_img": "https://anvibodycare.com/wp-content/uploads/2023/09/katehoriia-2-300x300.jpg",
    },
    "hair": {
        "markup": "hair",
        "chapter_name": "Волосся",
        "message": "Шампуні та бальзами",
        "items": ["hair1", "hair2", "hair3", "hair4", "hair5", "hair6"],
        "chapter_img": "https://anvibodycare.com/wp-content/uploads/2023/09/katehoriia-3-300x300.jpg",
    },
    "gift_card": {
        "markup": "gift_card",
        "chapter_name": "Подарункова карта",
        "message": "ANVI — український бренд.\n Поєднуючи веганську косметику та кращі активні інградієнти, ми підклуємося про вас.\n Використовуючи натуральні тари ми піклуємося про довкілля.",
        "items": ["gift_card"],
        "chapter_img": "https://anvibodycare.com/wp-content/uploads/2023/09/podarunkovyj-sertyfikat.jpg",
    },
}

# user cart dict
user_cart = {}
# {user_id: total_sum, ...}
user_total_sum = {}


# Reply Buttons
# regexp="ривіт"
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
        "Вітаю, {0.first_name}!\n Я допоможу тобі підібрати косметику"
        " 🌱ANVI🌱🥰".format(message.from_user),
        reply_markup=markup,
    )


@bot.message_handler(
    chat_id=[ADMIN],
    commands=["admin"],
)
def admin_rep(message):
    bot.send_message(
        message.chat.id,
        "Hello admin! You can use /update for update catalog "
        + "or /status for show current schedule.",
    )


@bot.message_handler(commands=["admin"])
def not_admin(message):
    bot.send_message(message.chat.id, "You are not admin! I call to 911!")


bot.add_custom_filter(custom_filters.ChatFilter())


@bot.message_handler(chat_id=[ADMIN], commands=["update"])
def manual_upd(message):
    bot.send_message(message.chat.id, "Start update..")
    make_catalog()
    bot.send_message(message.chat.id, "Catalog is up-to-date!")


@bot.message_handler(chat_id=[ADMIN], commands=["status"])
def show_job(message):
    all_jobs = schedule.get_jobs()
    bot.send_message(message.chat.id, str(all_jobs))


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
    elif message.text == "🛍️ Кошик":
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        message_list = [f"Вітаю, {user_name}! \n⋯⋯⋯⋯⋯⋯⋯⋯⋯\n"]
        if user_id not in user_cart:
            message_list.append("Чекаю на товари для тебе 😌\n \n Твій кошик 🌱")
            message_cart = "\n".join(message_list)
            bot.send_message(message.chat.id, message_cart)
        elif all(
            item["quantity"] == 0 for item in user_cart[user_id].values()
        ):
            message_list.append("Чекаю на нові товари 🐣\n \n Твій кошик 🌱")
            message_cart = "\n".join(message_list)
            bot.send_message(message.chat.id, message_cart)
        else:
            items = user_cart[user_id]
            for item_id, details in items.items():
                item_cost = details["quantity"] * details["price"]
                if details["quantity"] > 0:
                    message_list.append(
                        f"{details['name']}\n"
                        f"{details['quantity']} шт х "
                        f"{details['price']} ₴"
                        f" = {item_cost} ₴\n"
                    )
            message_list.append(
                "⋯⋯⋯⋯⋯⋯⋯⋯⋯\n"
                f"Загалом: {user_total_sum[user_id]} ₴\n \n"
                "Твій кошик 🌳"
            )
            message_cart = "\n".join(message_list)
            markup = types.InlineKeyboardMarkup()
            cart_edit_btn = types.InlineKeyboardButton(
                "✏️Редагувати", callback_data="cart_edit"
            )
            cart_empty_btn = types.InlineKeyboardButton(
                "❌ Очистити кошик", callback_data="cart_empty"
            )
            checkout_btn = types.InlineKeyboardButton(
                "✅ Оформити замовлення", callback_data="checkout"
            )
            markup.row(cart_edit_btn, cart_empty_btn)
            markup.row(checkout_btn)
            bot.send_message(
                message.chat.id, message_cart, reply_markup=markup
            )


# Chapter -> Items (InlineButtons menu updating)
@bot.callback_query_handler(func=lambda callback: True)
def callback_chapter(callback):
    catalog_items = read_catalog()
    # go to chapter
    if callback.data in catalog.keys():
        for callback_data_catalog in catalog.keys():
            if callback.data == callback_data_catalog:
                items = catalog[callback_data_catalog]["items"]
                message = catalog[callback_data_catalog]["message"]
                chapter_img = catalog[callback_data_catalog]["chapter_img"]
                markup = types.InlineKeyboardMarkup()
                for item in items:
                    item_name = catalog_items[item]["name"]
                    item_id = item
                    button = types.InlineKeyboardButton(
                        item_name, callback_data=item_id
                    )
                    markup.row(button)
                bot.send_photo(
                    callback.message.chat.id,
                    chapter_img,
                    caption=message,
                    reply_markup=markup,
                )
    # go to item page
    elif callback.data in catalog_items.keys():
        item_id = callback.data
        user_id = callback.from_user.id
        if user_id not in user_cart:
            user_total_sum[user_id] = 0

        markup = types.InlineKeyboardMarkup()
        chapter = catalog_items[item_id]["chapter"]
        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        item_price_str = catalog_items[item_id]["price"]
        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )
        add_to_cart = types.InlineKeyboardButton(
            f"Додати у кошик - {item_price_str}",
            callback_data=f"{item_id}_add_to_cart",
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
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
        user_id = callback.from_user.id
        item_id = callback.data.replace("back_to_item_", "")
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        item_price_str = catalog_items[item_id]["price"]
        chapter = catalog_items[item_id]["chapter"]
        markup = types.InlineKeyboardMarkup()

        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )

        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )
        add_to_cart = types.InlineKeyboardButton(
            f"Додати у кошик - {item_price_str}",
            callback_data=f"{item_id}_add_to_cart",
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
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
    # add to cart
    elif callback.data.endswith("_add_to_cart"):
        item_id = callback.data.replace("_add_to_cart", "")
        user_id = callback.from_user.id
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        item_price_str = catalog_items[item_id]["price"]
        item_price = int(item_price_str.replace(" ₴", ""))
        chapter = catalog_items[item_id]["chapter"]

        if user_id not in user_cart:  # creating a user_cart dict for this user
            user_cart[user_id] = {}
            user_total_sum[user_id] = 0

        if item_id in user_cart[user_id]:
            user_cart[user_id][item_id][
                "quantity"
            ] += 1  # If the item is already in the cart, increase the quantity by 1
            user_total_sum[user_id] += item_price  # Update the total sum
        else:
            user_cart[user_id][item_id] = {
                "name": item_name,
                "quantity": 1,
                "price": item_price,
            }
            user_total_sum[user_id] += item_price  # Update the total sum
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )
        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )
        remove_1 = types.InlineKeyboardButton(
            "✏️-1", callback_data=f"{item_id}_remove_1_from_cart"
        )
        n_items = types.InlineKeyboardButton(
            f"{user_cart[user_id][item_id]['quantity']} шт.",
            callback_data="none",
        )
        add_1 = types.InlineKeyboardButton(
            "✏️+1", callback_data=f"{item_id}_add_1_to_cart"
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        markup.row(description)
        markup.row(remove_1, n_items, add_1)
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
    # remove_1_from_cart
    elif callback.data.endswith("_remove_1_from_cart"):
        item_id = callback.data.replace("_remove_1_from_cart", "")
        user_id = callback.from_user.id
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        item_price_str = catalog_items[item_id]["price"]
        item_price = int(item_price_str.replace(" ₴", ""))
        chapter = catalog_items[item_id]["chapter"]

        user_cart[user_id][item_id]["quantity"] -= 1
        user_total_sum[user_id] -= item_price  # Update the total sum

        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )
        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )
        remove_1 = types.InlineKeyboardButton(
            "✏️-1", callback_data=f"{item_id}_remove_1_from_cart"
        )
        n_items = types.InlineKeyboardButton(
            f"{user_cart[user_id][item_id]['quantity']} шт.",
            callback_data="none",
        )
        add_1 = types.InlineKeyboardButton(
            "✏️+1", callback_data=f"{item_id}_add_1_to_cart"
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        if user_cart[user_id][item_id]["quantity"] == 0:
            markup.row(description)
            markup.row(n_items, add_1)
            markup.row(sum)
            markup.row(back)
        else:
            markup.row(description)
            markup.row(remove_1, n_items, add_1)
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
    # _add_1_to_cart"
    elif callback.data.endswith("_add_1_to_cart"):
        item_id = callback.data.replace("_add_1_to_cart", "")
        user_id = callback.from_user.id
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        item_price_str = catalog_items[item_id]["price"]
        item_price = int(item_price_str.replace(" ₴", ""))
        chapter = catalog_items[item_id]["chapter"]

        user_cart[user_id][item_id]["quantity"] += 1
        user_total_sum[user_id] += item_price  # Update the total sum

        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )
        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )
        remove_1 = types.InlineKeyboardButton(
            "✏️-1", callback_data=f"{item_id}_remove_1_from_cart"
        )
        n_items = types.InlineKeyboardButton(
            f"{user_cart[user_id][item_id]['quantity']} шт.",
            callback_data="none",
        )
        add_1 = types.InlineKeyboardButton(
            "✏️+1", callback_data=f"{item_id}_add_1_to_cart"
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        markup.row(description)
        markup.row(remove_1, n_items, add_1)
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
    # cart edit
    elif callback.data == "cart_edit":
        user_id = callback.from_user.id
        items = user_cart[user_id]
        markup = types.InlineKeyboardMarkup()
        message_cart_edit = "Редагування"
        for item_id, details in items.items():
            item_name = details["name"]
            if user_cart[user_id][item_id]["quantity"] > 0:
                name = types.InlineKeyboardButton(
                    item_name, callback_data=item_id
                )
                remove_1 = types.InlineKeyboardButton(
                    "✏️-1",
                    callback_data=f"{item_id}_remove_1_from_cart_incart",
                )
                n_items = types.InlineKeyboardButton(
                    f"{user_cart[user_id][item_id]['quantity']} шт.",
                    callback_data="none",
                )
                add_1 = types.InlineKeyboardButton(
                    "✏️+1", callback_data=f"{item_id}_add_1_to_cart_incart"
                )
                markup.row(name)
                markup.row(remove_1, n_items, add_1)
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        markup.row(sum)
        bot.send_message(
            callback.message.chat.id, message_cart_edit, reply_markup=markup
        )
    # _remove_1_from_cart_incart - cart edit
    elif callback.data.endswith("_remove_1_from_cart_incart"):
        item_id = callback.data.replace("_remove_1_from_cart_incart", "")
        user_id = callback.from_user.id
        items = user_cart[user_id]
        item_price = user_cart[user_id][item_id]["price"]

        user_cart[user_id][item_id]["quantity"] -= 1
        user_total_sum[user_id] -= item_price

        markup = types.InlineKeyboardMarkup()
        message_cart_edit = "Редагування"
        for item_id, details in items.items():
            item_name = details["name"]
            if user_cart[user_id][item_id]["quantity"] > 0:
                name = types.InlineKeyboardButton(
                    item_name, callback_data=item_id
                )
                remove_1 = types.InlineKeyboardButton(
                    "✏️-1",
                    callback_data=f"{item_id}_remove_1_from_cart_incart",
                )
                n_items = types.InlineKeyboardButton(
                    f"{user_cart[user_id][item_id]['quantity']} шт.",
                    callback_data="none",
                )
                add_1 = types.InlineKeyboardButton(
                    "✏️+1", callback_data=f"{item_id}_add_1_to_cart_incart"
                )
                markup.row(name)
                markup.row(remove_1, n_items, add_1)
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        markup.row(sum)
        bot.delete_message(
            callback.message.chat.id, callback.message.message_id
        )
        bot.send_message(
            callback.message.chat.id, message_cart_edit, reply_markup=markup
        )
    # _add_1_to_cart_incart - cart edit
    elif callback.data.endswith("_add_1_to_cart_incart"):
        item_id = callback.data.replace("_add_1_to_cart_incart", "")
        user_id = callback.from_user.id
        items = user_cart[user_id]
        item_price = user_cart[user_id][item_id]["price"]

        user_cart[user_id][item_id]["quantity"] += 1
        user_total_sum[user_id] += item_price

        markup = types.InlineKeyboardMarkup()
        message_cart_edit = "Редагування"
        for item_id, details in items.items():
            item_name = details["name"]
            if user_cart[user_id][item_id]["quantity"] > 0:
                name = types.InlineKeyboardButton(
                    item_name, callback_data=item_id
                )
                remove_1 = types.InlineKeyboardButton(
                    "✏️-1",
                    callback_data=f"{item_id}_remove_1_from_cart_incart",
                )
                n_items = types.InlineKeyboardButton(
                    f"{user_cart[user_id][item_id]['quantity']} шт.",
                    callback_data="none",
                )
                add_1 = types.InlineKeyboardButton(
                    "✏️+1", callback_data=f"{item_id}_add_1_to_cart_incart"
                )
                markup.row(name)
                markup.row(remove_1, n_items, add_1)
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        markup.row(sum)
        bot.delete_message(
            callback.message.chat.id, callback.message.message_id
        )
        bot.send_message(
            callback.message.chat.id, message_cart_edit, reply_markup=markup
        )
    # empty cart
    elif callback.data == "cart_empty":
        # Remove all items from the user's cart
        user_cart[callback.from_user.id] = {}
        user_total_sum[callback.from_user.id] = {}
        bot.answer_callback_query(callback.id, "Товари видалено 🫡")
        # Optionally, update the cart message to reflect the empty cart
        bot.edit_message_text(
            "Кошик порожній 🍃",
            callback.message.chat.id,
            callback.message.message_id,
        )


def listener(messages):
    for m in messages:
        bot.send_message(
            listen_chat,
            str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text,
        )


@repeat(every().day.at(time_str="06:00", tz="Europe/Kyiv"))
def update_catalog_every_day():
    global catalog_items
    scrape_url()
    make_catalog()
    catalog_items = read_catalog()


def bot_run():
    global catalog_items
    try:
        print("Bot starting..")
        catalog_items = read_catalog()
        threading.Thread(
            target=bot.infinity_polling,
            name="bot_infinity_polling",
            daemon=True,
        ).start()
        while True:
            schedule.run_pending()
            time.sleep(1)
        # apihelper.SESSION_TIME_TO_LIVE = 5 * 60
        # apihelper.RETRY_ON_ERROR = True
        # # bot.set_update_listener(listener)
        # bot.infinity_polling()
    except Exception as err:
        print(err)


if __name__ == "__main__":
    bot_run()
