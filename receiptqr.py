from dotenv import load_dotenv,find_dotenv
from pyzbar.pyzbar import decode
from fake_headers import Headers
from telebot import types
from random import choice
from os import environ
import cv2 as cv
import requests
import telebot
import time
import re
import os


if __name__ == '__main__':
    try:
        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file)
        telegram_api = environ.get('api_tg_qr')
        bot = telebot.TeleBot(telegram_api)
    except Exception as e:
        input(e)
        exit()


def decode_qr(photo_path:str):
    img=cv.imread(photo_path)
    objs=decode(img)
    os.remove(photo_path)
    if len(objs) > 0:
        dataqr = objs[0].data.decode('utf-8')
        return True, dataqr
    return False, "Cant't find qr"


# def check_admin(fn):
#     def wrapped(message: types.Message):
#         peerid = message.from_user.id
#         if not peerid == int(environ.get('admin_peerid')):
#             return
#         return fn(message)
#     return wrapped


def generate_namefile():
    symb = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    name = ''.join([choice(symb) for _ in range(8)])
    return f"{name}.jpg"


def save_photo(fileID):
    try:
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        name_file = generate_namefile()
        with open(name_file, 'wb') as new_file:
            new_file.write(downloaded_file)
        return True, name_file
    except Exception as e:
        return False, e


def get_name_oofd(name_raw:str):
    match = re.match(r'\d{0,3}\. \d{0,13} ', name_raw)
    if match:
        name_raw = name_raw[match.end()::]
    findre = r'(.*?)\(\d{0,10}\)'
    result = re.findall(findre, name_raw)
    if len(result) < 1:
        return name_raw
    else:
        return result[0]


def get_info_receipt(url:str):
    if not 'consumer.oofd' in url:
        return 'get receipt from oofd system'
    URL_API = 'https://consumer.oofd.kz/api/tickets/ticket/'
    session = requests.session()
    headers = Headers().generate()
    session.headers.update(headers)
    try:
        resp = session.get(url, verify=False)

        token = resp.url.split('/')[-1]
        url = f'{URL_API}{token}'
        resp = session.get(url, verify= False)
        ticket = resp.json()['ticket']

        result = []
        for item in ticket['items']:
            commodity = item['commodity']
            name_raw = commodity['name']
            name = get_name_oofd(name_raw)
            allsum = commodity['sum']
            quantity = commodity['quantity']
            text = f'{name} ({allsum}тг) {quantity}шт'
            result.append(text)
        return '\n'.join(result)
    except Exception as e:
        return e
    

@bot.message_handler(content_types=['photo'])
# @check_admin
def handle_start_help(message: types.Message):
    fileID = message.photo[-1].file_id
    peerid = message.from_user.id
    success, text = save_photo(fileID)
    if success:
        sucess_find_qr, text = decode_qr(text)
        if sucess_find_qr:
            bot.send_message(peerid, f"text qr:\n{text}")
            text = get_info_receipt(text)
    bot.send_message(peerid, text)


@bot.message_handler()
# @check_admin
def handle_start_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Give me the fucking qr photo')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(15)
