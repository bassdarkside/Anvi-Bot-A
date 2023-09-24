import telebot
from telebot import types
from telebot import util


# Function to read the token from a file
def read_token(filename):
    try:
        with open(filename, 'r') as file:
            token = file.read().strip()
        return token
    except FileNotFoundError:
        raise Exception(f"File {filename} with the token "
                        f"was not found. Make sure the file "
                        f"exists and contains the bot token.")


# Reading the token from a file
TOKEN_FILE = 'token_anvi.txt'
TOKEN = read_token(TOKEN_FILE)

bot = telebot.TeleBot(TOKEN)

catalog = {
    "chapter1": {
        "markup": "deodorants",
        "chapter_name": "Дезодорант (3)",
        "message": "Фізіологічні дезодоранти",
        "items": {
            "item1": {
                "id": "1",
                "name": "Фізіологічний дезодорант SUN",
                "price": "",
                "url": "",
                "description": "SUN",
                "image": "https://static.wixstatic.com/media/626c22_6ec1b2baf2b6438e958adfd1b325be4e~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "item2": {
                "id": "2",
                "name": "Фізіологічний дезодорант PURE",
                "price": "",
                "url": "",
                "description": "PURE",
                "image": "https://static.wixstatic.com/media/626c22_5a5df9591a1d4cd6a2f36315c38fd41f~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "item3": {
                "id": "3",
                "name": "Фізіологічний дезодорант FOREST",
                "price": "",
                "url": "",
                "description": "FOREST",
                "image": "https://static.wixstatic.com/media/15e500_a9081b244820411088f896189c608271~mv2.jpeg/v1/fit/w_500,h_500,q_90/file.jpg"
            }
        }
    },
    "chapter2": {
        "markup": "balms",
        "chapter_name": "Бальзам для губ (3)",
        "message": "Бальзами для губ і не тільки",
        "items": {
            "item1": {
                "id": "4",
                "name": "Бальзам CITRUS",
                "price": "",
                "url": "",
                "description": "CITRUS",
                "image": "https://static.wixstatic.com/media/15e500_82e75b444b654f9087794cc44ec42073~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "item2": {
                "id": "5",
                "name": "Бальзам MINT",
                "price": "",
                "url": "",
                "description": "MINT",
                "image": "https://static.wixstatic.com/media/15e500_b1932764b84b42f38a641af4fdadf28c~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg"
            },
            "item3": {
                "id": "6",
                "name": "Бальзам COCO",
                "price": "",
                "url": "",
                "description": "COCO",
                "image": "https://static.wixstatic.com/media/15e500_d46a44c840d14c9191957b0baafc3277~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg"
            }
        }
    },
    "chapter3": {
        "markup": "shampoo",
        "chapter_name": "Очищення (3)",
        "message": "Тверді шампуні",
        "items": {
            "item1": {
                "id": "7",
                "name": "Фізіологічний шампуть VIRGIN",
                "price": "",
                "url": "",
                "description": "VIRGIN",
                "image": "https://static.wixstatic.com/media/626c22_83f2928502bc4e39b643aa566c17e321~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "item2": {
                "id": "8",
                "name": "Фізіологічний шампуть WILD",
                "price": "",
                "url": "",
                "description": "WILD",
                "image": "https://static.wixstatic.com/media/15e500_c5002c3e106a415a874e2a93d60329bf~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "item3": {
                "id": "9",
                "name": "Фізіологічний шампуть PURE",
                "price": "",
                "url": "",
                "description": "Фізіологічний шампуть PURE",
                "image": "https://static.wixstatic.com/media/626c22_3529dae377b841e783211f09ea0c5c5b~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            }
        }
    },
    "chapter4": {
        "markup": "care",
        "chapter_name": "Догляд (3)",
        "message": "Бальзами для волосся",
        "items": {
            "item1": {
                "id": "10",
                "name": "Захисна сироватка GLOW",
                "price": "",
                "url": "",
                "description": ""
            },
            "item2": {
                "id": "11",
                "name": "SHINE твердий бальзам кондиціонер",
                "price": "",
                "url": "",
                "description": ""
            },
            "item3": {
                "id": "12",
                "name": "SILK твердий бальзам кондиціонер",
                "price": "",
                "url": "",
                "description": ""
            }
        }
    }
}


catalog_items = {
            "1": {
                "name": "Фізіологічний дезодорант SUN",
                "price": "",
                "url": "",
                "description": "SUN",
                "image": "https://static.wixstatic.com/media/626c22_6ec1b2baf2b6438e958adfd1b325be4e~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "2": {
                "name": "Фізіологічний дезодорант PURE",
                "price": "",
                "url": "",
                "description": "PURE",
                "image": "https://static.wixstatic.com/media/626c22_5a5df9591a1d4cd6a2f36315c38fd41f~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "3": {
                "name": "Фізіологічний дезодорант FOREST",
                "price": "",
                "url": "",
                "description": "FOREST",
                "image": "https://static.wixstatic.com/media/15e500_a9081b244820411088f896189c608271~mv2.jpeg/v1/fit/w_500,h_500,q_90/file.jpg"
            },
            "4": {
                "name": "Бальзам CITRUS",
                "price": "",
                "url": "",
                "description": "CITRUS",
                "image": "https://static.wixstatic.com/media/15e500_82e75b444b654f9087794cc44ec42073~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "5": {
                "name": "Бальзам MINT",
                "price": "",
                "url": "",
                "description": "MINT",
                "image": "https://static.wixstatic.com/media/15e500_b1932764b84b42f38a641af4fdadf28c~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg"
            },
            "6": {
                "name": "Бальзам COCO",
                "price": "",
                "url": "",
                "description": "COCO",
                "image": "https://static.wixstatic.com/media/15e500_d46a44c840d14c9191957b0baafc3277~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg"
            },
            "7": {
                "name": "Фізіологічний шампуть VIRGIN",
                "price": "",
                "url": "",
                "description": "VIRGIN",
                "image": "https://static.wixstatic.com/media/626c22_83f2928502bc4e39b643aa566c17e321~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "8": {
                "name": "Фізіологічний шампуть WILD",
                "price": "",
                "url": "",
                "description": "WILD",
                "image": "https://static.wixstatic.com/media/15e500_c5002c3e106a415a874e2a93d60329bf~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "9": {
                "name": "Фізіологічний шампуть PURE",
                "price": "",
                "url": "",
                "description": "Фізіологічний шампуть PURE",
                "image": "https://static.wixstatic.com/media/626c22_3529dae377b841e783211f09ea0c5c5b~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "10": {
                "name": "Захисна сироватка GLOW",
                "price": "",
                "url": "",
                "description": "Захисна сироватка glow Новий інноваційний екологічний продукт по догляду за волоссям. Високоінтенсивний догляд-покрашує структуру волосини глибоко з середини,живить та наповнює цінними рослинними компонентами. 100% рослинний склад,без силіконів Поєднання цінних олій та емолентів у “сухій” олійці для волосся дарує миттевий ефект сяяння та розгладження на поверхні волосини тапролонговану дію в кортексі. Сироватка для всіх типів волосся,особливо для схильного до ламкості, сухого та пористог. • Живить і запечатує зневоднені та пошкоджені кінчики • Захищає кінчики від негативного впливу зовнішніх факторів • Підходить для волосся будь якої будь-якої довжини та текстури • Миттєво надає блиску,та розплутує • Полірує кутикулу та зберігає контроль над завитками. • Волосся залишається м'яким і шовковистим. Результат: ущільнення кінчиків ,блискуче,гладке та відновденеволосся.",
                "image": "https://static.wixstatic.com/media/626c22_4d8c793b09af4d899d3033c6dc91f78d~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "11": {
                "name": "SHINE твердий бальзам кондиціонер",
                "price": "",
                "url": "",
                "description": "SHINE твердий кондиціонер, який полірує кутикулуволосся,дарує блиск і гладкість. Результат живе, еластичне та доглянуте волосся без обтяження. Чудово знімає статичний заряд та полегшує розчісування. Він містить цінні та корисні: оліїконоплі, зародків пшениці, кокосу, стероли гірчиці, пантенол та вітамін Е. Ніжно огортає кожну волосинку цінними ліпідами,закриває лусочки кутикули і твоє волосся стає міцнішим,легшим у догляді та захищеним від негативних факторів зовнішнього середовища. ANVI –дієвий високоінтенсивний доглядза волоссям, а не просто Zero Waste альтернатива. Завдяки новітнім досягненням в розробці екологічної косметики нам вдалося створити багатофункціональний продукт що замінює мінімум три звичайні продукти для волосся. Кондиціонер Маска Незмивний засіб для кінчиків Живе, еластичне та доглянуте волосся без обтяження. Чудово знімає статичний заряд та полегшує розчісування. Жодного зайвого чи не етичного компонента: Купуючи засоби догляду ANVIтипідтримуєшУкраїнське виробництво, етичне використання природних ресурсів,скорочення кількості відходів та піклуєшся про себе та планету.",
                "image": "https://static.wixstatic.com/media/626c22_304a58304091435aa6b2b77e4d30c4a2~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
            },
            "12": {
                "name": "SILK твердий бальзам кондиціонер",
                "price": "",
                "url": "",
                "description": "SILK- твердий кондиціонер, який ідеально розплутує волосся, та надастьблиск і гладкість. Він містить багато кориснихдля волосся олій авокадо,брокколіта какао, амінокислоти пшениці,пантенол та вітамін Е. Ніжно огортає кожну волосинку цінними ліпідами,закриває лусочки кутикули і твоє волосся стає міцнішим,легшим у догляді та захищеним від негативних факторів зовнішнього середовища. Без краплі силіконів та барвників,віддущок,та інщих непотрібних тобі та природі компонентів. Твердий кондиціонер ANVI –дієвий високоінтенсивний доглядза волоссям, а не просто Zero Waste альтернатива. Завдяки новітнім досягненням в розробці екологічної косметики нам вдалося створити багатофункціональний продукт що замінює мінімум три звичайні продукти для волосся. Кондиціонер Маска Незмивний засіб для кінчиків Живе, еластичне та доглянуте волосся без обтяження. Чудово знімає статичний заряд та полегшує розчісування. Жодного зайвого чи не етичного компонента: Купуючи засоби догляду ANVIтипідтримуєшУкраїнське виробництво, етичне використання природних ресурсів,скорочення кількості відходів та піклуєшся про себе та планету.",
                "image": "https://static.wixstatic.com/media/626c22_489161c6883d49989db2b99923af0c2c~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
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
    # go to chapter
    if callback.data in catalog.keys():
        for callback_data_catalog in catalog.keys():
            if callback.data == callback_data_catalog:
                items = catalog[callback_data_catalog]["items"]
                message = catalog[callback_data_catalog]["message"]
                markup = types.InlineKeyboardMarkup()
                for item in items:
                    item_name = items[item]["name"]
                    item_id = catalog[callback_data_catalog]["items"][item]["id"]
                    button = types.InlineKeyboardButton(item_name,
                                                        callback_data=item_id)
                    markup.row(button)
                bot.edit_message_text(message,
                                    callback.message.chat.id,
                                    callback.message.message_id,
                                    reply_markup=markup)
    # go to item page       
    elif callback.data in catalog_items.keys():
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
                    "⬅️ Назад", callback_data="back_chapter")
        for id in catalog_items.keys():
            if callback.data == id:
                item_name = catalog_items[id]["name"]
                item_image = catalog_items[id]["image"]
                id_description = str(id) + "_description"
                description = types.InlineKeyboardButton(
                    "Опис продукту", callback_data=id_description)
                add_to_cart = types.InlineKeyboardButton(
                    "Додати у кошик", callback_data="cart")
                sum = types.InlineKeyboardButton(
                    "тут буде сума", callback_data="sum")
                markup.row(description)
                markup.row(add_to_cart)
                markup.row(sum)
                markup.row(back)
                bot.send_photo(callback.message.chat.id,
                               item_image,
                               caption=item_name,
                               reply_markup=markup)
# go to item description           
    elif callback.data.endswith("_description"):
        item_id = callback.data.replace("_description", "")
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
                    "⬅️ Назад", callback_data="back_item")
        for id in catalog_items.keys():
            if item_id == id:
                item_name = catalog_items[id]["name"]
                item_image = catalog_items[id]["image"]
                item_description = catalog_items[id]["description"]
                markup.row(back)
                bot.send_photo(callback.message.chat.id,
                               item_image,
                               caption=item_name,
                               reply_markup=markup)
                for description in util.split_string(item_description, 3000):
                    bot.send_message(callback.message.chat.id,
                                     item_description)





# Starting the bot
if __name__ == '__main__':
    bot.polling(none_stop=True)
