from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from config import Config
import base64
import requests
from io import BytesIO
from dotenv import load_dotenv
import time

dotenv_path = '.env'
load_dotenv(dotenv_path)

updater = Updater(Config.TELEGRAM_SECRET_KEY,
                  use_context=True)
max_retries = 3
sleep_time = 5

app_url = Config.APP_BASE_URL
creds = {'username': '', 'password': ''}
image_data = {
    'image_bytes': None,
    'id': None
}


def get_labels():
    num_retries = 0
    tasks = {'label': [], 'id': []}
    while num_retries < max_retries:
        try:
            labels_url = app_url + 'api/labels'
            res = requests.get(labels_url)
            if res.status_code == 200:
                tasks = res.json()
                tasks['label'].append('Exit')
                tasks['id'].append(None)
                break
        except:
            num_retries += 1
            print('Error while getting labels. Retrying...', '\nNumber of retries left: ', max_retries - num_retries, '\n')
            time.sleep(sleep_time)

    return tasks

tasks = get_labels()

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

def get_image():
    url = app_url + 'api/images'
    res = requests.get(url, auth=(creds['username'], creds['password']))
    if res.status_code != 200:
        return None, None
    res_json = res.json()
    if not res_json['image_id']:
        return None, None
    img = res_json['image']
    image_data = base64.b64decode(img)
    image_file = BytesIO(image_data)
    img_id = res_json['image_id']

    return image_file, img_id

def my_tasks(update: Update, context: CallbackContext):
    global tasks
    
    new_tasks = get_labels()
    if set(new_tasks['label']) != set(tasks['label']):
        tasks['label'] = new_tasks['label']
        tasks['id'] = new_tasks['id']
        update_tasks_handler(update, context)

    kbd_layout = [[x] for x in tasks['label']]
    kbd = ReplyKeyboardMarkup(kbd_layout)

    img, img_id = get_image()
    image_data['image_bytes'] = img 
    image_data['id'] = img_id

    if not img_id:
        update.message.reply_text('Sorry, currently there are no more images for you to annotate. Please come back later.')
    else:
        update.message.reply_photo(photo=img, reply_markup=kbd)


def exit(update: Update, context: CallbackContext):
    start(update, context)

def annotate_image(label_id):
    url = app_url + 'api/annotations'
    data = {
        'image_id': image_data['id'],
        'label_id': label_id
    }
    res = requests.post(url, json=data, auth=(creds['username'], creds['password']))

def annotate(update: Update, context: CallbackContext):
    update.message.reply_text(f"Image was labeled as '{update.message.text}'")
    if update.message.text == 'Exit':
        exit(update, context)
        return
    label_id = tasks['id'][tasks['label'].index(update.message.text)]
    annotate_image(label_id)
    my_tasks(update, context)

def update_tasks_handler(update, context):
    global tasks_handler

    updater.dispatcher.remove_handler(tasks_handler)
    updater.dispatcher.remove_handler(password_handler)
    updater.dispatcher.remove_handler(login_handler)

    tasks_handler = MessageHandler(Filters.regex(f'^({"|".join(tasks["label"])})$'), annotate)

    updater.dispatcher.add_handler(tasks_handler)
    updater.dispatcher.add_handler(password_handler)
    updater.dispatcher.add_handler(login_handler)

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("Registration"), register))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("My Tasks"), my_tasks))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("Login"), enter_username))

tasks_handler = MessageHandler(Filters.regex(f'^({"|".join(tasks["label"])})$'), annotate)
password_handler = MessageHandler(Filters.text, enter_password)
login_handler = MessageHandler(Filters.text, login)

updater.dispatcher.add_handler(tasks_handler)
updater.dispatcher.add_handler(password_handler)
updater.dispatcher.add_handler(login_handler)

updater.start_polling()
