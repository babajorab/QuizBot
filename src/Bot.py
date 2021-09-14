import os
from Token import TOKEN
from Database import Database
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

#Loging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#Messages
Welcome = '../Messages/Welcome.txt'
ReceiveUserName = '../Messages/ReceiveUserName.txt'
ReceivePassword = '../Messages/ReceivePassword.txt'
UserNameNotExist = '../Messages/UserNameNotExist.txt'
WrongPassword = '../Messages/WrongPassword.txt'
EnterAgainPassword = '../Messages/EnterAgainPassword.txt'
EnterWrongPasswordMuch = '../Messages/EnterWrongPasswordMuch.txt'
CurrectPassword = '../Messages/CurrectPassword.txt'
NotTakeTest = '../Messages/NotTakeTest.txt'
SelectOption = '../Messages/SelectOption.txt'
Help = '../Messages/Help.txt'

#Database
QuizPath = '../Database/Quiz'
UserData = '../Database/Users/Data.xlsx'

#Formating
ResultFormat = 'txt'

#Global variable
STATE = None
USERNAME = 1
PASSWORD = 2
COUNT_WRONG = 0

#Connection To Database
database = Database(UserData)

def text(update, context):
    if STATE == USERNAME:
        recieve_username(update, context)
    
    elif STATE == PASSWORD:
        receive_password(update, context)

    else:
        help(update, context)
        

def result_quiz(update, context):
    butten = []
    for item in get_quizes():
        butten.append([InlineKeyboardButton(item, callback_data=item)])

    reply_markup = InlineKeyboardMarkup(butten)
    update.message.reply_text(read_file(Welcome), reply_markup=reply_markup) 
    

def button(update, context):
    global STATE
        
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=read_file(SelectOption) + " " +  query.data)
    context.user_data['quiz'] = query.data

    context.bot.sendMessage(chat_id = update.effective_message.chat_id, text= read_file(ReceiveUserName))
    STATE = USERNAME


def recieve_username(update, context):
    global STATE, database
    username = update.message.text
    
    if database.exist_username(username):
        STATE = PASSWORD
        context.user_data['username'] = username
        update.message.reply_text(read_file(ReceivePassword))
                
    else:
        update.message.reply_text(read_file(UserNameNotExist))
        STATE = None
        

def send_result(update, context):
    username = context.user_data['username'] 
    file_path = '../Database/Quiz/{0}/{1}.{2}'.format(context.user_data['quiz'], username, ResultFormat)
      
    if(os.path.isfile(file_path)):
        update.message.reply_text(read_file(CurrectPassword) + "    " + database.get_name(username))
        context.bot.sendDocument(chat_id = update.message.chat_id, document=open(file_path,'rb'))
    else:
        update.message.reply_text(read_file(NotTakeTest))


def receive_password(update, context):
    global STATE, COUNT_WRONG, database
    
    password = update.message.text
    
    if database.get_password(context.user_data['username']) == password:
        send_result(update, context)

    else:
        COUNT_WRONG += 1

        #more wrong password
        if COUNT_WRONG == 3:
            update.message.reply_text(read_file(EnterWrongPasswordMuch))

        else:
            update.message.reply_text(read_file(WrongPassword))
            update.message.reply_text(read_file(EnterAgainPassword))
            return

    STATE = None
    COUNT_WRONG = 0
        
        
def help(update, context):
    update.message.reply_text(read_file(Help))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def read_file(path):
    with open(path, 'r', encoding="utf-8") as file:
        text = file.read()
        return text

def get_quizes():
    return [dir for dir in os.listdir(QuizPath)]

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", help))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("ResultQuiz", result_quiz))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

