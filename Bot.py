from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import Info
import logging


STATE = None
USERNAME = 1
PASSWORD = 2




def text(update, context):
    if STATE == USERNAME:
        recieve_username(update, context)
    
    if STATE == PASSWORD:
        pass

    
def start(update, context):
    global STATE
    update.message.reply_text(read_file('Messages/Welcome.txt'))
    update.message.reply_text(read_file('Messages/ReceiveUserName.txt'))
    STATE = USERNAME

def help(update, context):
    update.message.reply_text('Help!')


def recieve_username(update, context):
    global STATE
    username = update.message.text

    #if(database.exist_username(username))
    if(username == "sm"):
        pass
        
        
    else:
        update.message.reply_text(read_file('Messages/UserNameNotExist.txt'))
        STATE = None
        
        
    update.message.reply_text("your username is : " + username)
    










def password(update, context):
    update.message.reply_text("you enter password")







def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def read_file(path):
    with open(path, 'r', encoding="utf-8") as file:
        text = file.read()
        return text

def get_list_quiz(path):
    #print(get_list_quiz('Database'))
    return [dir for dir in os.listdir(path)]


def main():
    updater = Updater(Info.TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

