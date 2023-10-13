import time
import telebot
import schedule
import threading
from decouple import config
from schedule import every, repeat
from telebot.util import quick_markup
from telebot.types import InputMediaPhoto
from telebot import types, custom_filters, util
from bot_start.catalog import catalog, read_catalog, read_about, read_contacts
from parser_v2.main import scrape_url, make_catalog
from parser_v2.config import URL

TOKEN = config("TOKEN")
bot = telebot.TeleBot(TOKEN)
ADMIN = int(config("ADMIN"))
listen_chat = config("listen_chat")

# user cart dict
user_cart = {}
# {user_id: total_sum, ...}
user_total_sum = {}
# for storing the last message_id
bot_data = {}

# variable for weight and packing
item_weight_def = ""
item_packing_def = ""


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📒 Каталог")
    btn2 = types.KeyboardButton("🛍️ Кошик")
    btn3 = types.KeyboardButton("🌿 Про Нас")
    btn4 = types.KeyboardButton("💌 Наші контакти")

    markup.row(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Вітаю, {0.first_name}!\n Я допоможу тобі підібрати косметику"
        " 🌱ANVI🌱🥰".format(message.from_user),
        reply_markup=markup,
    )


############        ADMIN     HANDLERS        ############
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


############        CONTACTS     HANDLER        ############
@bot.message_handler(func=lambda message: message.text == "💌 Наші контакти")
def contacts_handler(message):
    contacts = read_contacts()
    markup = types.ReplyKeyboardMarkup(True, False)
    bot.send_message(
        message.chat.id,
        text=contacts,
        parse_mode="HTML",
        reply_markup=markup,
    )


############        ABOUT_US     HANDLER        ############
@bot.message_handler(func=lambda message: message.text == "🌿 Про Нас")
def about_us_handler(message):
    about = read_about()
    markup = types.ReplyKeyboardMarkup(True, False)
    bot.send_message(
        message.chat.id,
        text=about,
        parse_mode="HTML",
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
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        # item_price_str = catalog_items[item_id]["price"]
        item_price = catalog_items[item_id]["price_int"]
        # item_price = 0
        chapter = catalog_items[item_id]["chapter"]
        product_id = catalog_items[item_id]["product_id"]

        img_caption = InputMediaPhoto(media=item_image, caption=item_name)
        global item_weight_def
        global item_packing_def

        # check if the item has weight, pacj=king options
        variations = True
        if len(catalog_items[item_id]["variations"]) == 0:
            variations = False

        if user_id not in user_cart:
            user_total_sum[user_id] = 0

        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )
        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )

        # change the button for items with variations
        text = ""
        if variations:
            # default price
            varios = catalog_items[item_id]["variations"]
            key_price_dict = {}  # dict with the {key: vario_price}

            key_price_dict = {
                key: details["vario_price"] for key, details in varios.items()
            }

            # find min the key with the min price
            def_key = min(key_price_dict, key=key_price_dict.get)

            product_id = catalog_items[item_id]["variations"][def_key][
                "vario_id"
            ]
            item_price = catalog_items[item_id]["variations"][def_key][
                "vario_price"
            ]
            item_weight_def = catalog_items[item_id]["variations"][def_key][
                "vario_weight"
            ]
            item_packing_def = catalog_items[item_id]["variations"][def_key][
                "packing_name"
            ]
            text = (
                f"{item_name}\n"
                f"• вага: {item_weight_def} гр.\n"
                f"• {item_packing_def} \n"
                f"• ціна: {item_price} ₴."
            )
        else:
            # item_price = int(item_price_str.replace(" ₴", ""))
            text = f"{item_name}\n" f"• ціна: {item_price} ₴."

        img_caption = InputMediaPhoto(media=item_image, caption=text)
        add_to_cart = types.InlineKeyboardButton(
            "Додати у кошик",
            callback_data=f"{item_id}--{product_id}_add_to_cart",
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        markup.row(description)
        markup.row(add_to_cart)
        markup.row(sum)
        markup.row(back)

        bot.edit_message_media(
            img_caption,
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=markup,
        )
    # go to item description
    elif callback.data.endswith("_description"):
        item_id = callback.data.replace("_description", "")
        chat_id = callback.message.chat.id

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

                photo_message = bot.send_photo(
                    callback.message.chat.id, item_image, caption=item_name
                )
                photo_message_id = photo_message.message_id
                # Store the message_id
                bot_data[chat_id] = {"last_message_id": photo_message_id}

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
        # item_price_str = catalog_items[item_id]["price"]
        item_price = catalog_items[item_id]["price_int"]
        chapter = catalog_items[item_id]["chapter"]
        chat_id = callback.message.chat.id
        product_id = catalog_items[item_id]["product_id"]

        img_caption = InputMediaPhoto(media=item_image, caption=item_name)

        # Retrieve the message_id from context.user_data
        photo_message_id = bot_data[chat_id]["last_message_id"]

        # check if the item has weight, pacj=king options
        variations = True
        if len(catalog_items[item_id]["variations"]) == 0:
            variations = False

        if user_id not in user_cart:
            user_total_sum[user_id] = 0

        markup = types.InlineKeyboardMarkup()

        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )
        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )
        text = ""
        if variations:
            # default price
            varios = catalog_items[item_id]["variations"]
            key_price_dict = {}  # dict with the {key: vario_price}

            key_price_dict = {
                key: details["vario_price"] for key, details in varios.items()
            }

            # find min the key with the min price
            def_key = min(key_price_dict, key=key_price_dict.get)

            product_id = catalog_items[item_id]["variations"][def_key][
                "vario_id"
            ]
            item_price = catalog_items[item_id]["variations"][def_key][
                "vario_price"
            ]
            item_weight_def = catalog_items[item_id]["variations"][def_key][
                "vario_weight"
            ]
            item_packing_def = catalog_items[item_id]["variations"][def_key][
                "packing_name"
            ]
            text = (
                f"{item_name}\n"
                f"• вага: {item_weight_def} гр.\n"
                f"• {item_packing_def} \n"
                f"• ціна: {item_price} ₴."
            )
        else:
            # item_price = int(item_price_str.replace(" ₴", ""))
            text = f"{item_name}\n" f"• ціна: {item_price} ₴."

        img_caption = InputMediaPhoto(media=item_image, caption=text)

        add_to_cart = types.InlineKeyboardButton(
            "Додати у кошик",
            callback_data=f"{item_id}--{product_id}_add_to_cart",
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
        if photo_message_id:
            bot.edit_message_media(
                media=img_caption,
                chat_id=chat_id,
                message_id=photo_message_id,
                reply_markup=markup,
            )
        else:
            bot.edit_message_media(
                img_caption,
                callback.message.chat.id,
                callback.message.message_id,
                reply_markup=markup,
            )

    # back item -> chapter
    elif callback.data.startswith("back_to_chapter_"):
        chapter = callback.data.replace("back_to_chapter_", "")
        chapter_img = catalog[chapter]["chapter_img"]
        markup = types.InlineKeyboardMarkup()
        for chapter_catalog in catalog.keys():
            if chapter_catalog == chapter:
                items = catalog[chapter]["items"]
                message = catalog[chapter]["message"]
                img_caption = InputMediaPhoto(
                    media=chapter_img, caption=message
                )

                markup = types.InlineKeyboardMarkup()
                for item in items:
                    item_name = catalog_items[item]["name"]
                    item_id = item
                    button = types.InlineKeyboardButton(
                        item_name, callback_data=item_id
                    )
                    markup.row(button)

                bot.edit_message_media(
                    img_caption,
                    callback.message.chat.id,
                    callback.message.message_id,
                    reply_markup=markup,
                )
    # add to cart
    elif callback.data.endswith("_add_to_cart"):
        item_id_product_id = callback.data.replace("_add_to_cart", "")
        item_id_product_id_list = item_id_product_id.split("--")
        item_id = item_id_product_id_list[0]
        product_id = item_id_product_id_list[1]

        user_id = callback.from_user.id
        chat_id = callback.message.chat.id
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        # item_price_str = catalog_items[item_id]["price"]
        item_price = catalog_items[item_id]["price_int"]
        chapter = catalog_items[item_id]["chapter"]

        img_caption = InputMediaPhoto(media=item_image, caption=item_name)

        # check if the item has weight, packing options
        variations = True
        if len(catalog_items[item_id]["variations"]) == 0:
            variations = False

        if user_id not in user_cart:  # creating a user_cart dict for this user
            user_cart[user_id] = {}
            user_total_sum[user_id] = 0
        # cart has this item -> add the current
        if product_id in user_cart[user_id]:
            if variations:
                # add vario price
                varios = catalog_items[item_id]["variations"]
                vario_key = ""
                for key, details in varios.items():
                    if (
                        details["vario_weight"] == item_weight_def
                        and details["packing_name"] == item_packing_def
                    ):
                        vario_key = key

                item_price = catalog_items[item_id]["variations"][vario_key][
                    "vario_price"
                ]
                text = (
                    f"{item_name}\n"
                    f"• вага: {item_weight_def} гр.\n"
                    f"• {item_packing_def}\n"
                    f"• ціна: {item_price} ₴"
                )
            else:
                # item_price = int(item_price_str.replace(" ₴", ""))
                text = f"{item_name}\n" f"• ціна: {item_price} ₴"

            user_cart[user_id][product_id]["quantity"] += 1
            user_total_sum[user_id] += item_price  # Update the total sum
            img_caption = InputMediaPhoto(media=item_image, caption=text)
        # cart doesn't have this product
        else:
            if variations:
                # add default price
                varios = catalog_items[item_id]["variations"]
                key_price_dict = {}  # dict with the {key: vario_price}

                key_price_dict = {
                    key: details["vario_price"]
                    for key, details in varios.items()
                }

                # find min the key with the min price
                def_key = min(key_price_dict, key=key_price_dict.get)

                item_price = catalog_items[item_id]["variations"][def_key][
                    "vario_price"
                ]
                item_weight_def = catalog_items[item_id]["variations"][
                    def_key
                ]["vario_weight"]
                item_packing_def = catalog_items[item_id]["variations"][
                    def_key
                ]["packing_name"]
                product_id = catalog_items[item_id]["variations"][def_key][
                    "vario_id"
                ]
                text = (
                    f"{item_name}\n"
                    f"• вага: {item_weight_def} гр.\n"
                    f"• {item_packing_def}\n"
                    f"• ціна: {item_price} ₴"
                )
            # price for item without options
            else:
                # item_price = int(item_price_str.replace(" ₴", ""))
                item_weight_def = ""
                item_packing_def = ""
                text = text = f"{item_name}\n" f"• ціна: {item_price} ₴"

            img_caption = InputMediaPhoto(media=item_image, caption=text)

            user_cart[user_id][product_id] = {
                "name": item_name,
                "quantity": 1,
                "price": item_price,
                "weight": item_weight_def,
                "packing": item_packing_def,
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
            "✏️-1", callback_data=f"{item_id}--{product_id}_remove_1_from_cart"
        )
        n_items = types.InlineKeyboardButton(
            f"{user_cart[user_id][product_id]['quantity']} шт.",
            callback_data="none",
        )
        add_1 = types.InlineKeyboardButton(
            "✏️+1", callback_data=f"{item_id}--{product_id}_add_1_to_cart"
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )

        # add the button for options
        if variations:
            weight_opt = types.InlineKeyboardButton(
                "Обери вагу",
                callback_data=f"{item_id}--{product_id}_weight_opt",
            )
            packing_opt = types.InlineKeyboardButton(
                "Обери пакування",
                callback_data=f"{item_id}--{product_id}_packing_opt",
            )
            markup.row(description)
            markup.row(weight_opt, packing_opt)
            markup.row(remove_1, n_items, add_1)
            markup.row(sum)
            markup.row(back)

            photo_message = bot.edit_message_media(
                img_caption,
                callback.message.chat.id,
                callback.message.message_id,
                reply_markup=markup,
            )
            photo_message_id = photo_message.message_id
            # Store the message_id
            bot_data[chat_id] = {"last_message_id": photo_message_id}
        else:
            markup.row(description)
            markup.row(remove_1, n_items, add_1)
            markup.row(sum)
            markup.row(back)
            photo_message = bot.edit_message_media(
                img_caption,
                callback.message.chat.id,
                callback.message.message_id,
                reply_markup=markup,
            )
            photo_message_id = photo_message.message_id
            # Store the message_id
            bot_data[chat_id] = {"last_message_id": photo_message_id}
    # # weight_options message
    elif callback.data.endswith("_weight_opt"):
        item_id_product_id = callback.data.replace("_weight_opt", "")
        item_id_product_id_list = item_id_product_id.split("--")
        item_id = item_id_product_id_list[0]
        product_id = item_id_product_id_list[1]

        user_id = callback.from_user.id
        # weight_options
        varios = catalog_items[item_id]["variations"]
        weight_opt_list = []  # list with weight options

        weight_opt_list = [
            details["vario_weight"] for key, details in varios.items()
        ]
        unique_weight = list(set(weight_opt_list))
        unique_weight.sort()

        markup = types.InlineKeyboardMarkup()
        for w in unique_weight:
            button = types.InlineKeyboardButton(
                w, callback_data=f"{item_id}--{product_id}--{w}_weight"
            )
            markup.row(button)
        bot.send_message(
            callback.message.chat.id, "Обери вагу", reply_markup=markup
        )
    # # packing_options message
    elif callback.data.endswith("_packing_opt"):
        item_id_product_id = callback.data.replace("_packing_opt", "")
        item_id_product_id_list = item_id_product_id.split("--")
        item_id = item_id_product_id_list[0]
        product_id = item_id_product_id_list[1]

        user_id = callback.from_user.id
        # weight_options
        varios = catalog_items[item_id]["variations"]
        packing_opt_list = []  # list with packing options

        packing_opt_list = [
            details["packing_name"] for key, details in varios.items()
        ]
        unique_packing = list(set(packing_opt_list))
        unique_packing.sort()

        markup = types.InlineKeyboardMarkup()
        for p in unique_packing:
            button = types.InlineKeyboardButton(
                p, callback_data=f"{item_id}--{product_id}--{p}_packing"
            )
            markup.row(button)
        bot.send_message(
            callback.message.chat.id, "Обери пакування", reply_markup=markup
        )

    # # weight selection -> upd the "add_to_car screen"
    elif callback.data.endswith("_weight"):
        item_id_product_id_weight = callback.data.replace("_weight", "")
        item_id_product_id_weight_list = item_id_product_id_weight.split("--")
        item_id = item_id_product_id_weight_list[0]
        product_id_old = item_id_product_id_weight_list[1]
        item_weight_def = item_id_product_id_weight_list[2]

        user_id = callback.from_user.id
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        # item_price_str = catalog_items[item_id]["price"]
        item_price = catalog_items[item_id]["price_int"]
        chapter = catalog_items[item_id]["chapter"]

        img_caption = InputMediaPhoto(media=item_image, caption=item_name)
        #  find vario_key by weight and packing
        varios = catalog_items[item_id]["variations"]
        # vario_key = ""
        for key, details in varios.items():
            if (
                details["vario_weight"] == item_weight_def
                and details["packing_name"] == item_packing_def
            ):
                vario_key = key

        item_price = catalog_items[item_id]["variations"][vario_key][
            "vario_price"
        ]
        product_id = catalog_items[item_id]["variations"][vario_key][
            "vario_id"
        ]

        item_price_old = user_cart[user_id][product_id_old]["price"]
        user_total_sum[user_id] -= item_price_old
        del user_cart[user_id][product_id_old]
        user_cart[user_id][product_id] = {
            "name": item_name,
            "quantity": 1,
            "price": item_price,
            "weight": item_weight_def,
            "packing": item_packing_def,
        }
        user_total_sum[user_id] += item_price

        text = (
            f"{item_name}\n"
            f"• вага: {item_weight_def} гр.\n"
            f"• {item_packing_def}\n"
            f"• ціна: {item_price} ₴"
        )
        img_caption = InputMediaPhoto(media=item_image, caption=text)

        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )
        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )
        remove_1 = types.InlineKeyboardButton(
            "✏️-1", callback_data=f"{item_id}--{product_id}_remove_1_from_cart"
        )
        n_items = types.InlineKeyboardButton(
            f"{user_cart[user_id][product_id]['quantity']} шт.",
            callback_data="none",
        )
        add_1 = types.InlineKeyboardButton(
            "✏️+1", callback_data=f"{item_id}--{product_id}_add_1_to_cart"
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )

        # add the button for options
        weight_opt = types.InlineKeyboardButton(
            "Обери вагу", callback_data=f"{item_id}--{product_id}_weight_opt"
        )
        packing_opt = types.InlineKeyboardButton(
            "Обери пакування",
            callback_data=f"{item_id}--{product_id}_packing_opt",
        )
        markup.row(description)
        markup.row(weight_opt, packing_opt)
        markup.row(remove_1, n_items, add_1)
        markup.row(sum)
        markup.row(back)

        bot.send_photo(
            callback.message.chat.id, item_image, text, reply_markup=markup
        )

    # # packing selection -> upd the "add_to_car screen"
    elif callback.data.endswith("_packing"):
        item_id_product_id_pack = callback.data.replace("_packing", "")
        item_id_product_id_pack_list = item_id_product_id_pack.split("--")
        item_id = item_id_product_id_pack_list[0]
        product_id_old = item_id_product_id_pack_list[1]
        item_packing_def = item_id_product_id_pack_list[2]

        user_id = callback.from_user.id
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        # item_price_str = catalog_items[item_id]["price"]
        item_price = catalog_items[item_id]["price_int"]
        chapter = catalog_items[item_id]["chapter"]

        img_caption = InputMediaPhoto(media=item_image, caption=item_name)
        #  find vario_key by weight and packing
        varios = catalog_items[item_id]["variations"]
        vario_key = ""
        for key, details in varios.items():
            if (
                details["vario_weight"] == item_weight_def
                and details["packing_name"] == item_packing_def
            ):
                vario_key = key

        item_price = catalog_items[item_id]["variations"][vario_key][
            "vario_price"
        ]
        product_id = catalog_items[item_id]["variations"][vario_key][
            "vario_id"
        ]

        item_price_old = user_cart[user_id][product_id_old]["price"]
        user_total_sum[user_id] -= item_price_old
        del user_cart[user_id][product_id_old]

        user_cart[user_id][product_id] = {
            "name": item_name,
            "quantity": 1,
            "price": item_price,
            "weight": item_weight_def,
            "packing": item_packing_def,
        }
        user_total_sum[user_id] += item_price

        text = (
            f"{item_name}\n"
            f"• вага: {item_weight_def} гр.\n"
            f"• {item_packing_def}\n"
            f"• ціна: {item_price} ₴"
        )
        img_caption = InputMediaPhoto(media=item_image, caption=text)

        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
            "⬅️ Назад до категорії",
            callback_data=f"back_to_chapter_{chapter}",
        )
        description = types.InlineKeyboardButton(
            "Опис продукту", callback_data=f"{item_id}_description"
        )
        remove_1 = types.InlineKeyboardButton(
            "✏️-1", callback_data=f"{item_id}--{product_id}_remove_1_from_cart"
        )
        n_items = types.InlineKeyboardButton(
            f"{user_cart[user_id][product_id]['quantity']} шт.",
            callback_data="none",
        )
        add_1 = types.InlineKeyboardButton(
            "✏️+1", callback_data=f"{item_id}--{product_id}_add_1_to_cart"
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )

        # add the button for options
        weight_opt = types.InlineKeyboardButton(
            "Обери вагу", callback_data=f"{item_id}--{product_id}_weight_opt"
        )
        packing_opt = types.InlineKeyboardButton(
            "Обери пакування",
            callback_data=f"{item_id}--{product_id}_packing_opt",
        )
        markup.row(description)
        markup.row(weight_opt, packing_opt)
        markup.row(remove_1, n_items, add_1)
        markup.row(sum)
        markup.row(back)

        bot.send_photo(
            callback.message.chat.id, item_image, text, reply_markup=markup
        )

    # remove_1_from_cart
    elif callback.data.endswith("_remove_1_from_cart"):
        item_id_product_id = callback.data.replace("_remove_1_from_cart", "")
        item_id_product_id_list = item_id_product_id.split("--")
        item_id = item_id_product_id_list[0]
        product_id = item_id_product_id_list[1]
        user_id = callback.from_user.id
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        chapter = catalog_items[item_id]["chapter"]

        item_price = user_cart[user_id][product_id]["price"]

        # check if the item has weight, pacj=king options
        variations = True
        if len(catalog_items[item_id]["variations"]) == 0:
            variations = False

        text = ""
        if variations:
            item_weight_def = user_cart[user_id][product_id]["weight"]
            item_packing_def = user_cart[user_id][product_id]["packing"]

            text = (
                f"{item_name}\n"
                f"• вага: {item_weight_def} гр.\n"
                f"• {item_packing_def}\n"
                f"• ціна: {item_price} ₴"
            )
        else:
            text = f"{item_name}\n" f"• ціна: {item_price} ₴"

        img_caption = InputMediaPhoto(media=item_image, caption=text)

        user_cart[user_id][product_id]["quantity"] -= 1
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
            "✏️-1", callback_data=f"{item_id}--{product_id}_remove_1_from_cart"
        )
        n_items = types.InlineKeyboardButton(
            f"{user_cart[user_id][product_id]['quantity']} шт.",
            callback_data="none",
        )
        add_1 = types.InlineKeyboardButton(
            "✏️+1", callback_data=f"{item_id}--{product_id}_add_1_to_cart"
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )

        if variations:
            # add the button for options
            weight_opt = types.InlineKeyboardButton(
                "Обери вагу",
                callback_data=f"{item_id}--{product_id}_weight_opt",
            )
            packing_opt = types.InlineKeyboardButton(
                "Обери пакування",
                callback_data=f"{item_id}--{product_id}_packing_opt",
            )
            if user_cart[user_id][product_id]["quantity"] == 0:
                markup.row(description)
                markup.row(weight_opt, packing_opt)
                markup.row(n_items, add_1)
                markup.row(sum)
                markup.row(back)
            else:
                markup.row(description)
                markup.row(weight_opt, packing_opt)
                markup.row(remove_1, n_items, add_1)
                markup.row(sum)
                markup.row(back)

            bot.edit_message_media(
                img_caption,
                callback.message.chat.id,
                callback.message.message_id,
                reply_markup=markup,
            )

        else:
            if user_cart[user_id][product_id]["quantity"] == 0:
                markup.row(description)
                markup.row(n_items, add_1)
                markup.row(sum)
                markup.row(back)
            else:
                markup.row(description)
                markup.row(remove_1, n_items, add_1)
                markup.row(sum)
                markup.row(back)
            bot.edit_message_media(
                img_caption,
                callback.message.chat.id,
                callback.message.message_id,
                reply_markup=markup,
            )
    # _add_1_to_cart"
    elif callback.data.endswith("_add_1_to_cart"):
        item_id_product_id = callback.data.replace("_add_1_to_cart", "")
        item_id_product_id_list = item_id_product_id.split("--")
        item_id = item_id_product_id_list[0]
        product_id = item_id_product_id_list[1]

        user_id = callback.from_user.id
        item_name = catalog_items[item_id]["name"]
        item_image = catalog_items[item_id]["image"]
        chapter = catalog_items[item_id]["chapter"]

        item_price = user_cart[user_id][product_id]["price"]

        # check if the item has weight, pacj=king options
        variations = True
        if len(catalog_items[item_id]["variations"]) == 0:
            variations = False

        text = ""
        if variations:
            item_weight_def = user_cart[user_id][product_id]["weight"]
            item_packing_def = user_cart[user_id][product_id]["packing"]

            text = (
                f"{item_name}\n"
                f"• вага: {item_weight_def} гр.\n"
                f"• {item_packing_def}\n"
                f"• ціна: {item_price} ₴"
            )
        else:
            text = f"{item_name}\n" f"• ціна: {item_price} ₴"

        img_caption = InputMediaPhoto(media=item_image, caption=text)
        user_cart[user_id][product_id]["quantity"] += 1
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
            "✏️-1", callback_data=f"{item_id}--{product_id}_remove_1_from_cart"
        )
        n_items = types.InlineKeyboardButton(
            f"{user_cart[user_id][product_id]['quantity']} шт.",
            callback_data="none",
        )
        add_1 = types.InlineKeyboardButton(
            "✏️+1", callback_data=f"{item_id}--{product_id}_add_1_to_cart"
        )
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )

        if variations:
            # add the button for options
            weight_opt = types.InlineKeyboardButton(
                "Обери вагу",
                callback_data=f"{item_id}--{product_id}_weight_opt",
            )
            packing_opt = types.InlineKeyboardButton(
                "Обери пакування",
                callback_data=f"{item_id}--{product_id}_packing_opt",
            )
            markup.row(description)
            markup.row(weight_opt, packing_opt)
            markup.row(remove_1, n_items, add_1)
            markup.row(sum)
            markup.row(back)

            bot.edit_message_media(
                img_caption,
                callback.message.chat.id,
                callback.message.message_id,
                reply_markup=markup,
            )
        else:
            markup.row(description)
            markup.row(remove_1, n_items, add_1)
            markup.row(sum)
            markup.row(back)

            bot.edit_message_media(
                img_caption,
                callback.message.chat.id,
                callback.message.message_id,
                reply_markup=markup,
            )
    # # cart edit
    elif callback.data == "cart_edit":
        user_id = callback.from_user.id
        items = user_cart[user_id]
        markup = types.InlineKeyboardMarkup()
        message_cart_edit = "Редагування"
        for product_id, details in items.items():
            item_name = details["name"]
            if len(user_cart) > 0:
                name = types.InlineKeyboardButton(
                    item_name, callback_data=product_id
                )
                remove_1 = types.InlineKeyboardButton(
                    "✏️-1",
                    callback_data=f"{product_id}_remove_1_from_cart_incart",
                )
                n_items = types.InlineKeyboardButton(
                    f"{user_cart[user_id][product_id]['quantity']} шт.",
                    callback_data="none",
                )
                add_1 = types.InlineKeyboardButton(
                    "✏️+1", callback_data=f"{product_id}_add_1_to_cart_incart"
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
    # # _remove_1_from_cart_incart - cart edit
    elif callback.data.endswith("_remove_1_from_cart_incart"):
        product_id = callback.data.replace("_remove_1_from_cart_incart", "")
        user_id = callback.from_user.id
        items = user_cart[user_id]

        item_price = user_cart[user_id][product_id]["price"]

        user_cart[user_id][product_id]["quantity"] -= 1
        user_total_sum[user_id] -= item_price

        markup = types.InlineKeyboardMarkup()
        message_cart_edit = "Редагування"
        for product_id, details in items.items():
            item_name = details["name"]
            if user_cart[user_id][product_id]["quantity"] > 0:
                name = types.InlineKeyboardButton(
                    item_name, callback_data=product_id
                )
                remove_1 = types.InlineKeyboardButton(
                    "✏️-1",
                    callback_data=f"{product_id}_remove_1_from_cart_incart",
                )
                n_items = types.InlineKeyboardButton(
                    f"{user_cart[user_id][product_id]['quantity']} шт.",
                    callback_data="none",
                )
                add_1 = types.InlineKeyboardButton(
                    "✏️+1", callback_data=f"{product_id}_add_1_to_cart_incart"
                )

                markup.row(name)
                markup.row(remove_1, n_items, add_1)
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        markup.row(sum)

        bot.edit_message_text(
            message_cart_edit,
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=markup,
        )

    # #_add_1_to_cart_incart - cart edit
    elif callback.data.endswith("_add_1_to_cart_incart"):
        product_id = callback.data.replace("_add_1_to_cart_incart", "")
        user_id = callback.from_user.id
        items = user_cart[user_id]
        item_price = user_cart[user_id][product_id]["price"]
        user_cart[user_id][product_id]["quantity"] += 1
        user_total_sum[user_id] += item_price

        markup = types.InlineKeyboardMarkup()
        message_cart_edit = "Редагування"
        for product_id, details in items.items():
            item_name = details["name"]
            if user_cart[user_id][product_id]["quantity"] > 0:
                name = types.InlineKeyboardButton(
                    item_name, callback_data=product_id
                )
                remove_1 = types.InlineKeyboardButton(
                    "✏️-1",
                    callback_data=f"{product_id}_remove_1_from_cart_incart",
                )
                n_items = types.InlineKeyboardButton(
                    f"{user_cart[user_id][product_id]['quantity']} шт.",
                    callback_data="none",
                )
                add_1 = types.InlineKeyboardButton(
                    "✏️+1", callback_data=f"{product_id}_add_1_to_cart_incart"
                )
                markup.row(name)
                markup.row(remove_1, n_items, add_1)
        sum = types.InlineKeyboardButton(
            f"🛍️ {user_total_sum[user_id]} ₴", callback_data="sum"
        )
        markup.row(sum)
        bot.edit_message_text(
            message_cart_edit,
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=markup,
        )
    # empty cart
    elif callback.data == "cart_empty":
        # Remove all items from the user's cart
        user_cart[callback.from_user.id] = {}
        user_total_sum[callback.from_user.id] = 0
        bot.answer_callback_query(callback.id, "Товари видалено 🫡")
        # Optionally, update the cart message to reflect the empty cart
        bot.edit_message_text(
            "Кошик порожній 🍃",
            callback.message.chat.id,
            callback.message.message_id,
        )


############        CHECKOUT     CALLBACK        ############
@bot.callback_query_handler(func=lambda call: call.data == "checkout")
def callback_checkout(call):
    for items in user_cart.values():
        for item_id, values in items.items():
            id_ = item_id
            qty = values["quantity"]
    checkout_link = f"{URL}/checkout/?add-to-cart={id_}&quantity={qty}"
    markup = quick_markup(
        {"anvibodycare.com": {"url": checkout_link}},
        row_width=2,
    )
    bot.edit_message_text(
        "✅ Оформити замовлення",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
    )


############              LISTENER               ############
def listener(messages):
    for m in messages:
        bot.send_message(
            listen_chat,
            str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text,
        )


############              SCHEDULE               ############
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
