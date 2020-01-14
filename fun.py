import re
import datetime
import emoji

def formatFecha(fecha):
    if fecha == None:
        return '---'
    else:   
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

def emojize_cat(cadena):
    if re.search("PRI", cadena) != None:
        cat = cadena.replace("PRI", emoji.emojize(':fallen_leaf:PRI'))
        cadena = cat
    if re.search("MAY", cadena) != None:
        cat = cadena.replace("MAY", emoji.emojize(':tornado:MAY'))
        cadena = cat
    if re.search("IND", cadena) != None:
        cat = cadena.replace("IND", emoji.emojize('🦁IND'))
        cadena = cat
    if re.search("ART", cadena) != None:
        cat = cadena.replace("ART", emoji.emojize(':bow_and_arrow:ART'))
        cadena = cat
    if re.search("MTZ", cadena) != None:
        cat = cadena.replace("MTZ", emoji.emojize(':crocodile:MTZ'))
        cadena = cat
    if re.search("IJV", cadena) != None:
        cat = cadena.replace("IJV", emoji.emojize(':pirate_flag:IJV'))
        cadena = cat
    if re.search("CFG", cadena) != None:
        cat = cadena.replace("CFG", emoji.emojize(':elephant:CFG'))
        cadena = cat
    if re.search("VCL", cadena) != None:
        cat = cadena.replace("VCL", emoji.emojize(':leopard:VCL'))
        cadena = cat
    if re.search("SSP", cadena) != None:
        cat = cadena.replace("SSP", emoji.emojize(':rooster:SSP'))
        cadena = cat
    if re.search("CAV", cadena) != None:
        cat = cadena.replace("CAV", emoji.emojize(':tiger_face:CAV'))
        cadena = cat
    if re.search("CMG", cadena) != None:    
        cat = cadena.replace("CMG", emoji.emojize(':ox:CMG'))
        cadena = cat
    if re.search("LTU", cadena) != None:
        cat = cadena.replace("LTU", emoji.emojize(':axe:LTU'))
        cadena = cat
    if re.search("GRA", cadena) != None:
        cat = cadena.replace("GRA", emoji.emojize(':horse_face:GRA'))
        cadena = cat
    if re.search("HOL", cadena) != None:
        cat = cadena.replace("HOL", emoji.emojize(':dog_face:HOL'))
        cadena = cat
    if re.search("SCU", cadena) != None:
        cat = cadena.replace("SCU", emoji.emojize(':honeybee:SCU'))
        cadena = cat
    if re.search("GTM", cadena) != None:
        cat = cadena.replace("GTM", emoji.emojize(':moai:GTM'))
        cadena = cat
    return cadena

def getPartidos(table, fecha):
    partidos = ''
    flag = False

    for table in table:
        th = table.find_all('th')
        td = table.find_all('td')

        cat = ''
        
        for i, th in enumerate(th):
            if i == 2:
                break
            else:
                if esta(formatFecha(fecha), th.getText()):
                    flag = True
                cat = cat + th.getText() + '\n'
            
        L = []      
        for td in td:
            L.append(td.getText())
                
        cat = cat + ' ' + L[2] + ' ' + L[3] + '\n'
        cat = cat + ' ' + L[6] + ' ' + L[7] + '\n'
        partidos = partidos + cat
        if flag:
            return cat
    
    if fecha != None:
        return "No hay partidos hoy"    
    else:
        return partidos