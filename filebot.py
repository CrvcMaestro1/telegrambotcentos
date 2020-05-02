# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os
from datetime import datetime


TOKEN = 'TOKEN_BOT'  # token brindado por BotFather

LOG_DIR = "/home/registro.txt" # directorio para log
USERS_DIR = "/home/usuarios.txt" # directorio para usuarios

knownUsers = []  # registro temporal de usuarios

commands = {  
    'start': 'Empezar a mensajear con el bot',
    'ayuda': 'Da informacion sobre los comandos disponibles',
    'cd': 'Cambia el directorio actual',
    'exec': 'Ejecuta un comando',
    'execlist': 'Ejecuta una lista de comandos',
    'reboot': 'Reinicia el servidor'
}

markup = types.ReplyKeyboardMarkup()
markup.row('/start', '/ayuda', '/cd')
markup.row('/exec', '/execlist', '/reboot')

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            fecha = datetime.fromtimestamp(m.json['date'])
            f = open(LOG_DIR, "a+")
            f.write(str(m.chat.first_name) + " [" + str(m.chat.id) + "]" + "[" + str(fecha) + "] : " + m.text + "\n")
            f.close()


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # actualizar el listener del bot con el que acabamos de desarrollar


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    f = open(USERS_DIR, "r")
    content = f.readlines()
    for c in content:
        knownUsers.append(c.split(';')[1].split('\n')[0])
    if str(cid) not in knownUsers:
        knownUsers.append(cid)
        f = open(USERS_DIR, "a+")
        f.write(str(m.chat.first_name) + ";" + str(m.chat.id) + "\n")
        f.close()
        bot.send_message(cid, "¡Bienvenido!", reply_markup=markup)
        command_help(m) 
    else:
        bot.send_message(cid,
                         "Ya habías empezado a hablar conmigo anteriormente. Busca el símbolo de comandos y revisa los comandos disponibles.",
                         reply_markup=markup)


# help page
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=markup)


# Reinicia servidor
@bot.message_handler(commands=['reboot'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Reiniciando servidor...")
    bot.send_chat_action(cid, 'typing')
    time.sleep(3)
    os.system("reboot")
	

# Ejecuta un comando
@bot.message_handler(commands=['exec'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Ejecutando: " + m.text[len("/exec"):])
    bot.send_chat_action(cid, 'typing') 
    time.sleep(2)
    f = os.popen(m.text[len("/exec"):])
    result = f.read()
    bot.send_message(cid, "Resultado: " + result, reply_markup=markup)


# Cambia de directorio
@bot.message_handler(commands=['cd'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Cambio a directorio: " + m.text[len("/cd"):])
    bot.send_chat_action(cid, 'typing') 
    time.sleep(2)
    os.chdir(m.text[len("/cd"):].strip())
    f = os.popen("pwd")
    result = f.read()
    bot.send_message(cid, "Directorio actual: " + result, reply_markup=markup)


# Ejecuta una lista de comandos
@bot.message_handler(commands=['execlist'])
def command_long_text(m):
    cid = m.chat.id
    comandos = m.text[len("/execlist\n"):].split('\n')
    for com in comandos:
        bot.send_message(cid, "Ejecutando: " + com)
	bot.send_chat_action(cid, 'typing')
	time.sleep(2)
	f = os.popen(com)
	result = f.read()
	bot.send_message(cid, "Resultado: " + result, )
    bot.send_message(cid, "Comandos ejecutados.", reply_markup=markup)


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "Hola")
def command_text_hi(m):
    bot.send_message(m.chat.id, "¡Hola " + str(m.chat.first_name) + "!", reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id, "No te entiendo, prueba con /ayuda", reply_markup=markup)


bot.polling()
