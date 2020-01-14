import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bs4 import BeautifulSoup
import requests
import datetime
import re
import fun
import math
import os
import emoji

URL = "http://beisbolencuba.com"

title = []
num_partidos = []
team  = []
carreras = []
new_carreras = []


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



def start(update, context):
    manito = emoji.emojize(':backhand_index_pointing_right:')
    cartel = '\u26BE' + 'Serie Nacional de Béisbol' + '\u26BE' + '\n\n'
    cartel = cartel + manito + '  Estadísticas' + '\n'
    cartel = cartel + manito + '  Partidos' + '\n'
    cartel = cartel + manito + '  Posisiones' + '\n'
    update.message.reply_text(cartel)

    key = [[KeyboardButton('/menu')]]
    key_markup = ReplyKeyboardMarkup(key, one_time_keyboard = False, resize_keyboard = True)
    context.bot.send_message(chat_id = update.effective_chat.id, text='Menu', reply_markup=key_markup)
 
def menu(update, context):
    keyboard = [[InlineKeyboardButton("Partidos", callback_data="1"),
                 InlineKeyboardButton("Partidos de Hoy", callback_data="2")],
                [InlineKeyboardButton("Posisiones Play Off Final", callback_data="3")],
                [InlineKeyboardButton("Posisiones Play Off Semifinal", callback_data="4")],
                [InlineKeyboardButton("Posisiones 2da Etapa", callback_data="5")],
                [InlineKeyboardButton("Posisiones 1ra Etapa", callback_data="6")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Selecione una opción:', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query

    if query.data == '1':
        query.edit_message_text(text=getPlayStatus())
    if query.data == '2':
        query.edit_message_text(text=getPlayHoy())
    if query.data == '3':
        query.edit_message_text(text=getTableposition(0))
    if query.data == '4':
        query.edit_message_text(text=getTableposition(1))
    if query.data == '5':
        query.edit_message_text(text=getTableposition(2))
    if query.data == '6':
        query.edit_message_text(text=getTableposition(3))

def getPlayStatus():

    req = requests.get(URL)

    status_code = req.status_code

    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        table = html.find_all('table', {'class' : 'fpgame'})
        
        return fun.emojize_cat(fun.getPartidos(table, None))

    else:
        return  "Error code " + str(status_code)

def getPlayHoy():
    req = requests.get(URL)

    status_code = req.status_code

    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        table = html.find_all('table', {'class' : 'fpgame'})
        fecha_hoy = datetime.datetime.now()
        return fun.emojize_cat(fun.getPartidos(table, fecha_hoy))
    else:
        return  "Error code " + str(status_code)

def getTableposition(n_table):
    req = requests.get(URL)
    status_code = req.status_code

    TABLE = [ [0 for c in range(0,10)] for f in range(0,100)]
    men = ''


    if status_code == 200:
        html = BeautifulSoup(req.text, 'html.parser')

        table_pos = html.find_all('table', {'class': 'bpos'})
    

        L = fun.getTable(n_table, table_pos, TABLE) 
        fun.Space_Matrix(TABLE, L[0], L[1])

        for f in range(0, L[0]):
            cat = ''
            for c in range(0, L[1]):
                if f == 0 and c == 0:
                    cat = ' ' + cat + str(TABLE[f][c]) + '        '
                else:
                    cat = cat + str(TABLE[f][c]) + ' '
            men = men + cat + '\n'

        #update.message.reply_text(men)
        return fun.emojize_cat(men)
    else:
        #update.message.reply_text("Error code:" + str(status_code))
        return  "Error code:" + str(status_code)


def help(update, context):
    update.message.reply_text("/start");


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def echo(update, context):
    update.message.reply_text("/start");




def main():
    
    TOKEN_TEST = os.environ.get('TOKEN_TEST')
    
    if TOKEN_TEST == None:
        from env import TOKEN_TEST
    
    updater = Updater(TOKEN_TEST, use_context=True)


    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))   


    dp.add_handler(MessageHandler(Filters.text, echo))

   
    dp.add_error_handler(error)

    
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
