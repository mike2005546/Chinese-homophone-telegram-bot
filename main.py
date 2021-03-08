import json
import logging
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


# Import json
with open('json/characters.json', 'r', encoding='utf8') as f:
    characters = json.load(f)

with open('json/sounds.json', 'r', encoding='utf8') as f:
    sounds = json.load(f)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


# Check if text contains chinese word only = True
def check_text_chinese(text):
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zh_pattern.search(text)
    return match


# Check if text has more than one word
def check_text_length(text):
    if len(text) > 1:
        return False
    else:
        return True


def sound(text):
    sound = []
    for i in range(len(characters[text])):
        sound.append(characters[text][i])
    return sound

def word(sound):
    words = []
    for i in range(len(sounds[sound])):
        words.append(sounds[sound][i])
    return words

def start(update: Update, context: CallbackContext):
    update.message.reply_text('想搵咩同音字？')

def reply(update: Update, context: CallbackContext):
    text = update.message.text
    url = 'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=' + text

    keyboard = []
    keyboard.append([InlineKeyboardButton(text="往漢語多功能字庫查看", url=url)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if check_text_chinese(text):
        if check_text_length(text):
            if text in str(characters):
                update.message.reply_text(text + '有' + str(len(characters[text])) + '個讀音', reply_markup=reply_markup)

                pronounce = sound(text)
                for i in range(len(pronounce)):
                    str1 = '、'.join(word(pronounce[i]))
                    update.message.reply_text(pronounce[i] + '\n' + str1)
            else:
                update.message.reply_text('字庫暫時未有呢個字...')
        else:
            update.message.reply_text('請只輸入一個中文字')
    else:
        update.message.reply_text('請輸入中文字')

    
def main():

    updater = Updater('642941204:AAFYJi5AvqYMwJmaf-OW2c6otEEVSU8Sudg')

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, reply))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
