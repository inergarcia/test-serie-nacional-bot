import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bs4 import BeautifulSoup
import requests
import datetime
import re
import fun
import math

URL = "http://beisbolencuba.com"

title = []
num_partidos = []
team  = []
carreras = []
new_carreras = []


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


#def start(update, context):
#    update.message.reply_text('Estadisticas de la Serie Nacional' + '\n' + '/help')

def start(update, context):
    keyboard = [[InlineKeyboardButton("Partidos", callback_data="1"),
                 InlineKeyboardButton("Partidos de Hoy", callback_data="2")],
                [InlineKeyboardButton("Posisiones Play Off Final", callback_data="3")],
                [InlineKeyboardButton("Posisiones Play Off Semifinal", callback_data="4")],
                [InlineKeyboardButton("Posisiones 2da Etapa", callback_data="5")],
                [InlineKeyboardButton("Posisiones 1ra Etapa", callback_data="6")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Estadisticas de la Serie Nacional!!!");
    update.message.reply_text('Selecione una opcion:', reply_markup=reply_markup)

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
    title = []
    num_partidos = []
    team  = []
    carreras = []
    new_carreras = []

    req = requests.get(URL)

    status_code = req.status_code
    cadena = ''

    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        entradas = html.find_all('table', {'class' : 'fpgame'})
    
        for ent in entradas:
            titulo = ent.find('a').getText()
            title.append(titulo)
            games = ent.find_all('table', {'class' : 'fpgt'})
            num_partidos.append(len(games))
            
            for game in games:
                equipo = game.find_all('span')
                marca = game.find_all('b')
                
                for e in equipo:
                    team.append(e.getText())
                for m in marca:
                    carreras.append(m.getText())

        
    else:
        #update.message.reply_text("Error code " + str(status_code))
        return  "Error code " + str(status_code)

    res = ''
    for ele in carreras:
        if len(str(ele)) <= 2:
            new_carreras.append(ele)

    index = 0

    for i in range(0, len(title)):
        n = num_partidos[i]
        cadena = title[i] + '\n'

        for x in range(0, 2*n, 1):
            cadena = cadena + team[index] + ' ' + new_carreras[index] + '\n'
            index = index + 1
            if (index) % 2 == 0:
                cadena = cadena + '\n'
        #update.message.reply_text(cadena)
        res = res + cadena + '\n'
        return res

def getPlayHoy():
    title = []
    num_partidos = []
    team  = []
    carreras = []
    new_carreras = []
    cadena = ''

    fecha_hoy = datetime.datetime.now()

    req = requests.get(URL)

    status_code = req.status_code


    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        entradas = html.find_all('table', {'class' : 'fpgame'})
    
        for ent in entradas:
            titulo = ent.find('a').getText()
            title.append(titulo)
            games = ent.find_all('table', {'class' : 'fpgt'})
            num_partidos.append(len(games))
            
            for game in games:
                equipo = game.find_all('span')
                marca = game.find_all('b')
                
                for e in equipo:
                    team.append(e.getText())
                for m in marca:
                    carreras.append(m.getText())

        
    else:
        #update.message.reply_text("Error code " + str(status_code))
        return "Error code " + str(status_code)

    for ele in carreras:
        if len(str(ele)) <= 2:
            new_carreras.append(ele)

    index = 0
    flag = False
    cat = ''
    for i in range(0, len(title)):
        n = num_partidos[i]
        
        if fun.esta(fun.formatFecha(fecha_hoy), title[i]):
            flag = True
        else:
            flag = False

        if flag:    
            cadena = title[i] + '\n'
        
        for x in range(0, 2*n, 1):
            if flag:
                cadena = cadena + team[index] + ' ' + new_carreras[index] + '\n'
            index = index + 1
            if flag:
                if index % 2 == 0:
                    cadena = cadena + '\n'
        if flag:
            cat = cat + cadena + '\n'
            #update.message.reply_text(cadena)
    if len(cat) == 0:
        return "No hay partidos hoy"
    return cat

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
                    cat = ' ' + cat + str(TABLE[f][c]) + '   '
                else:
                    cat = cat + str(TABLE[f][c]) + ' '
            men = men + cat + '\n'

        #update.message.reply_text(men)
        return men
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
    updater = Updater("1026034352:AAGeZU17EPC4H7E-cNbQKlX58yQJ3ZmLGdw", use_context=True)


    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))   


    dp.add_handler(MessageHandler(Filters.text, echo))

   
    dp.add_error_handler(error)

    
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
