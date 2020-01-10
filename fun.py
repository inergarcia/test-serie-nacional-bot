import re
import datetime

def formatFecha(fecha):
    dia = fecha.day
    mes = fecha.month
    ano = fecha.year
    dateFormat = []
    str_dia = str_mes = str_ano = ''
    if dia < 10:
        str_dia = '0' + str(dia)
    else:
        str_dia = str(dia)

    if mes < 10:
        str_mes = '0' + str(mes)
    else:
        str_mes = str(mes)

    str_ano = str(ano)

    return str_dia + '/' + str_mes + '/' + str_ano

def esta(patron, cadena):
    return re.search(patron, cadena) != None

#number:numero de la tabla 
#table:lista con todas las tablas
#TABLE: donde se guarda la tabla
def getTable(number, table, TABLE):
    fila = columna = 0
    flag = False
    for t, tp in enumerate(table):
        if t == number:
            flag = True
            table_tr = tp.find_all('tr')
            fila = len(list(table_tr)) 
            for f, tr in enumerate(table_tr):
                table_th = tr.find_all('th')
                table_td = tr.find_all('td')
                if len(list(table_th)):
                    columna = len(list(table_th))
                    for c, th in enumerate(table_th):
                        TABLE[f][c] = th.getText()
                else:
                    for c, td in enumerate(table_td):
                        TABLE[f][c] = td.getText()
        if flag:
            return [fila, columna]

def Space(cadena):
    return cadena.replace(u'\xa0', u'')

def Space_Matrix(Matrix, fila, columna):
    for i in range(0, fila):
        for j in range(0, columna):
            Matrix[i][j] = Space(Matrix[i][j])
