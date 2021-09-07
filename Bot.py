from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import Info
import logging


#Messages
Welcome = 'Messages/Welcome.txt'
ReceiveUserName = 'Messages/ReceiveUserName.txt'
ReceivePassword = 'Messages/ReceivePassword.txt'
UserNameNotExist = 'Messages/UserNameNotExist.txt'
WrongPassword = 'Messages/WrongPassword.txt'


STATE = None
USERNAME = 1
PASSWORD = 2

COUNT_WRONG = 0

def text(update, context):
    if STATE == USERNAME:
        recieve_username(update, context)
    
    elif STATE == PASSWORD:
        receive_password(update, context)

    else:
        help(update, context)
        
    
def start(update, context):
    global STATE
    update.message.reply_text(read_file(Welcome))
    update.message.reply_text(read_file(ReceiveUserName))
    STATE = USERNAME


def recieve_username(update, context):
    global STATE
    username = update.message.text

    #FIXED
    #if database.exist_username(username)
    if(username == "sm"):
        STATE = PASSWORD
        context.user_data['username'] = username
        update.message.reply_text(read_file(ReceivePassword))
                
    else:
        update.message.reply_text(read_file(UserNameNotExist))
        STATE = None
        


def receive_password(update, context):
    global STATE, COUNT_WRONG
    
    password = update.message.text
    username = context.user_data['username'])

    #FIXED
    #if database.check_user_pass(username, password)
    if(password == '1234'):
        pass

    elif COUNT_WRONG == 3:
        #M start again
        STATE = None
        COUNT_WRONG = 0
        
    else:
        COUNT_WRONG += 1
        update.message.reply_text(read_file(WrongPassword))
        #M try again
        
        
    
    



def help(update, context):
    update.message.reply_text('Help!')

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

