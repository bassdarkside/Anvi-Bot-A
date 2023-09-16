
from telebot import types


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
  

# Message handler for the Reply Button '📒 Каталог'
@bot.message_handler()
def check_reply(message: types.Message):
    if message.text == '📒 Каталог':
        chapters = types.InlineKeyboardMarkup()
        chapter1 = types.InlineKeyboardButton(
            'Дезодорант (3)', callback_data='chapter1')
        chapter2 = types.InlineKeyboardButton(
            'Бальзам для губ (3)', callback_data='chapter2')
        chapter3 = types.InlineKeyboardButton(
            'Очищення (3)', callback_data='chapter3')
        chapter4 = types.InlineKeyboardButton(
            'Догляд (3)', callback_data='chapter4')
        chapters.row(chapter1)
        chapters.row(chapter2)
        chapters.row(chapter3)
        chapters.row(chapter4)
        bot.send_message(message.chat.id, 'Дивись, що в нас є 🥰',
                         reply_markup=chapters)


@bot.callback_query_handler(func=lambda callback: True)
def callback_chapter(callback):
    if callback.data == 'chapter1':
        deodorants = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(
            'Фізіологічний дезодорант SUN', callback_data='item1')
        item2 = types.InlineKeyboardButton(
            'Фізіологічний дезодорант PURE', callback_data='item2')
        item3 = types.InlineKeyboardButton(
            'Фізіологічний дезодорант FOREST', callback_data='item3')
        deodorants.row(item1)
        deodorants.row(item2)
        deodorants.row(item3)
        bot.edit_message_text('Фізіологічні дезодоранти',
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=deodorants)
    elif callback.data == 'chapter2':
        balms = types.InlineKeyboardMarkup()
        item4 = types.InlineKeyboardButton(
            'Бальзам CITRUS', callback_data='item4')
        item5 = types.InlineKeyboardButton(
            'Бальзам MINT', callback_data='item5')
        item6 = types.InlineKeyboardButton(
            'Бальзам COCO', callback_data='item6')
        balms.row(item4)
        balms.row(item5)
        balms.row(item6)
        bot.edit_message_text('Бальзами для губ і не тільки',
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=balms)
    elif callback.data == 'chapter3':
        shampoo = types.InlineKeyboardMarkup()
        item7 = types.InlineKeyboardButton(
            'Фізіологічний шампуть VIRGIN', callback_data='item7')
        item8 = types.InlineKeyboardButton(
            'Фізіологічний шампуть WILD', callback_data='item8')
        item9 = types.InlineKeyboardButton(
            'Фізіологічний шампуть PURE', callback_data='item9')
        shampoo.row(item7)
        shampoo.row(item8)
        shampoo.row(item9)
        bot.edit_message_text('Фізіологічні шампуні',
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=shampoo)
    elif callback.data == 'chapter4':
        care = types.InlineKeyboardMarkup()
        item10 = types.InlineKeyboardButton(
            'Захисна сироватка GLOW', callback_data='item10')
        item11 = types.InlineKeyboardButton(
            'SHINE твердий бальзам кондиціонер', callback_data='item11')
        item12 = types.InlineKeyboardButton(
            'SILK твердий бальзам кондиціонер', callback_data='item12')
        care.row(item10)
        care.row(item11)
        care.row(item12)
        bot.edit_message_text('Догляд',
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=care)


