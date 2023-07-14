import telebot
import re

from main import *

bot = telebot.TeleBot('')


class Person:
    def __init__(self, p, q, d):
        self.p = p
        self.q = q
        self.d = d


users = {}


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, f"Welcome to RSA-bot {message.from_user.first_name}!!!")
        bot.send_message(message.from_user.id, "Write /help to get all information about commands")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/gen {length} - generating a private and public key with the selected "
                                               "length\n/enc {module} {open_exponent} {data} - encrypting selected "
                                               "data with entered public key\n/"
                                               "dec {data} - decrypting selected data with private key")
    elif re.search(r'^/gen \d+$', message.text) is not None:
        s = message.text.split(" ")
        n, e, d, p, q = Gen(int(s[1]))
        user_id = message.from_user.id
        users[user_id] = Person(p, q, d)
        bot.send_message(message.from_user.id, "Your public key:\nModule and open exponent in space\n" + str(n) + " " + str(e))
    elif re.search(r'^/enc \d+ \d+ \d+$', message.text) is not None:
        s = message.text.split(" ")
        msg = Encr(int(s[3]), int(s[2]), int(s[1]))
        bot.send_message(message.from_user.id, "Your encrypted data:\n" + str(msg))
    elif re.search(r'^/dec \d+$', message.text) is not None:
        s = message.text.split(" ")
        user_id = message.from_user.id
        if user_id not in users:
            bot.send_message(message.from_user.id, "You did not have private key!!!")
            bot.send_message(message.from_user.id, "Write /help to get all information about commands")
        else:
            msg = Decr(int(s[1]), users[user_id].d, users[user_id].p, users[user_id].q)
            bot.send_message(message.from_user.id, "Your decrypted data:\n" + str(msg))
    else:
        bot.send_message(message.from_user.id, "I don't understand You. Try to write /help.")


bot.polling(none_stop=True, interval=0)
