import telebot
import catalog


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


# Handler for all messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Hello!")
    else:
        bot.send_message(message.from_user.id, "I don't "
                         "understand this command.")


# Reply Buttons
catalog.start()


# Reply on Catalog button click
catalog.check_reply()


# Chapter -> Items (InlineButtons menu updating)
catalog.callback_chapter()


# Starting the bot
if __name__ == '__main__':
    bot.polling(none_stop=True)
