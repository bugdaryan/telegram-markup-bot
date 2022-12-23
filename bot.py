from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from config import Config
import requests

updater = Updater(Config.TELEGRAM_SECRET_KEY,
                  use_context=True)

app_url = 'http://localhost:5000/'
tasks = ['Dog', 'Cat', 'Fish', 'Exit']
creds = {'username': '', 'password': ''}

def reset_creds():
    creds['username'] = ''
    creds['password'] = ''


def start(update: Update, context: CallbackContext):
    """
    method to handle the /start command and create keyboard
    """

    kbd_layout = [['Login'], ['Registration'], ['Exit']]
    kbd = ReplyKeyboardMarkup(kbd_layout)
    update.message.reply_text(text="Select Options", reply_markup=kbd)

def enter_username(update: Update, context: CallbackContext):
    reset_creds()
    
    update.message.reply_text(text="Enter your username", reply_markup=ReplyKeyboardRemove())


def enter_password(update: Update, context: CallbackContext):
    if creds['username'] == '':
        creds['username'] = update.message.text
        update.message.reply_text(text="Enter your password", reply_markup=ReplyKeyboardRemove())
    else:
        login(update, context)


def login(update: Update, context: CallbackContext):
    creds['password'] = update.message.text
    url = app_url + 'api/login'
    res = requests.get(url, auth=(creds['username'], creds['password']))
    if res.status_code == 200:
        kbd_layout = [['My Tasks'], ['Exit']]
        kbd = ReplyKeyboardMarkup(kbd_layout)
        update.message.reply_text(text="You have successfully logged in", reply_markup=kbd)
    elif res.status_code == 401:
        update.message.reply_text(text="Incorrect username or password. Try again. \n\nEnter your username")
        reset_creds()
    else:
        update.message.reply_text(text="Something went wrong. Try again later")


def register(update: Update, context: CallbackContext):
    
    url = app_url + 'api/register'
    res = requests.post(url)
    if res.status_code != 201:
        update.message.reply_text(text="Something went wrong. Try again later")
        return
    res_json = res.json()
    username = res_json['username']
    password = res_json['password']
    kbd_layout = [['Login'], ['Registration'], ['Exit']]

    kbd = ReplyKeyboardMarkup(kbd_layout)


    reply = f'''You have successfully registered
Your login is {username}
Your password is {password}'''

    update.message.reply_text(text=reply, reply_markup=kbd)

def my_tasks(update: Update, context: CallbackContext):
    kbd_layout = [[x] for x in tasks]
    kbd = ReplyKeyboardMarkup(kbd_layout)
    update.message.reply_photo(photo=open('Dog.jpg', 'rb'), reply_markup=kbd)


def exit(update: Update, context: CallbackContext):
    start(update, context)


def echo(update: Update, context: CallbackContext):
    """
    message to handle any "Option [0-9]" Regrex.
    """
    if update.message.text == 'Exit':
        exit(update, context)
        return
    update.message.reply_text("You just clicked on '%s'" % update.message.text)
    my_tasks(update, context)

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("Registration"), register))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("My Tasks"), my_tasks))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("Login"), enter_username))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(r"(?=("+'|'.join(tasks)+r"))"), echo))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("Exit"), exit))
updater.dispatcher.add_handler(MessageHandler(Filters.text, enter_password))
updater.dispatcher.add_handler(MessageHandler(Filters.text, login))
updater.start_polling()
