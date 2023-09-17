

catalog = {
    "chapter1": {
        "markup": "deodorants",
        "chapter_name": "Дезодорант (3)",
        "message": "Фізіологічні дезодоранти",
        "items": {
            "item1": {
                "name": "Фізіологічний дезодорант SUN",
                "price": "",
                "url": "",
                "description": ""
            },
            "item2": {
                "name": "Фізіологічний дезодорант PURE",
                "price": "",
                "url": "",
                "description": ""
            },
            "item3": {
                "name": "Фізіологічний дезодорант FOREST",
                "price": "",
                "url": "",
                "description": ""
            }
        }
    },
    "chapter2": {
        "markup": "balms",
        "chapter_name": "Бальзам для губ (3)",
        "message": "Бальзами для губ і не тільки",
        "items": {
            "item1": {
                "name": "Бальзам CITRUS",
                "price": "",
                "url": "",
                "description": ""
            },
            "item2": {
                "name": "Бальзам MINT",
                "price": "",
                "url": "",
                "description": ""
            },
            "item3": {
                "name": "Бальзам COCO",
                "price": "",
                "url": "",
                "description": ""
            }
        }
    },
    "chapter3": {
        "markup": "shampoo",
        "chapter_name": "Очищення (3)",
        "message": "Тверді шампуні",
        "items": {
            "item1": {
                "name": "Фізіологічний шампуть VIRGIN",
                "price": "",
                "url": "",
                "description": ""
            },
            "item2": {
                "name": "Фізіологічний шампуть WILD",
                "price": "",
                "url": "",
                "description": ""
            },
            "item3": {
                "name": "Фізіологічний шампуть PURE",
                "price": "",
                "url": "",
                "description": ""
            }
        }
    },
    "chapter4": {
        "markup": "care",
        "chapter_name": "Догляд (3)",
        "message": "Бальзами для волосся",
        "items": {
            "item1": {
                "name": "Захисна сироватка GLOW",
                "price": "",
                "url": "",
                "description": ""
            },
            "item2": {
                "name": "SHINE твердий бальзам кондиціонер",
                "price": "",
                "url": "",
                "description": ""
            },
            "item3": {
                "name": "SILK твердий бальзам кондиціонер",
                "price": "",
                "url": "",
                "description": ""
            }
        }
    }
}


# Reply Buttons
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📒 Каталог')
    btn2 = types.KeyboardButton('🛍️ Кошик')
    btn3 = types.KeyboardButton('🥑 Корисності')

    markup.row(btn1, btn2)
    markup.add(btn3)

    bot.send_message(message.chat.id,
                     'Hi, {0.first_name}!'.format(message.from_user),
                     reply_markup=markup)


# Reply on Catalog button click
@bot.message_handler()
def check_reply(message: types.Message):
    if message.text == '📒 Каталог':
        markup = types.InlineKeyboardMarkup()
        for chapter in catalog.keys():
            name = catalog[chapter]["chapter_name"]
            button = chapter
            button = types.InlineKeyboardButton(
                name, callback_data=chapter)
            markup.row(button)
        bot.send_message(message.chat.id, 'Дивись, що в нас є 🥰',
                         reply_markup=markup)
       

# Chapter -> Items (InlineButtons menu updating)
@bot.callback_query_handler(func=lambda callback: True)
def callback_chapter(callback):
    for callback_data_catalog, chapter_v in catalog.items():
        items = catalog[callback_data_catalog]["items"]
        message = catalog[callback_data_catalog]["message"]
        if callback.data == callback_data_catalog:
            markup = types.InlineKeyboardMarkup()
            for item in items:
                item_name = items[item]["name"]
                button = item
                button = types.InlineKeyboardButton(item_name,
                                                    callback_data=item)
                markup.row(button)
            bot.edit_message_text(message,
                                  callback.message.chat.id,
                                  callback.message.message_id,
                                  reply_markup=markup)
