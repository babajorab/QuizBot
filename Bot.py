from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import Info

def start(update, context):
    with open('welcome.txt', 'r', encoding="utf-8") as file:
        text = file.read()
        update.message.reply_text(text)


def help(update, context):
    update.message.reply_text('Help!')


def username(update, context):
    update.message.reply_text("you enter username")

def password(update, context):
    update.message.reply_text("you enter password")


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def get_list_quiz(path):
    #print(get_list_quiz('Database'))
    return [dir for dir in os.listdir(path)]


def main():
    updater = Updater(Info.TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("user", username))
    dp.add_handler(CommandHandler("pass", password))
    dp.add_handler(MessageHandler(Filters.text, start))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
