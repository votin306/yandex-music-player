from locale import strcoll
import pygame
from urllib3 import HTTPSConnectionPool
from yaml import load
from yandex_music import Client, DownloadInfo, exceptions
import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import * 
import json
from threading import Thread
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, uic
from PyQt5.QtMultimedia import *
from PyQt5.QtWebEngineWidgets import *
from player import ui_login, ui

def login_yandex_show():
    ui_login.show()

def login_yandex_close():
    ui_login.close()

def login_yandex():
        link_post = 'https://oauth.yandex.com/token'
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        client_id = '23cabbbdc6cd418abb4b39c32c41195d'
        client_secret = '53bc75238f0c4d08a118e51fe9203300'
        header = {
            'user-agent': user_agent
        }
        try:
            request_post = f"grant_type=password&client_id={client_id}&client_secret={client_secret}&username={ui_login.login.text()}&password={ui_login.pwrd.text()}"
            request_auth = requests.post(link_post, data=request_post, headers=header)
            if request_auth.status_code == 200:
                json_data = request_auth.json()
                token = json_data.get('access_token')
                client = Client(token).init() #Создаем пользователя
                ui_login.state.setText("Успешно ;)") 
                ui.auth_yandex.setText(ui_login.login.text())
                with open("login_token.json", "w") as write_file: #Создаем Json для того что бы мы всё время не вводили пароль с логином
                    data = {'token':token,'username':ui_login.login.text()}
                    json.dump(data, write_file)
            else:
                ui_login.state.setText("Ошибка (проверь данные)  :(")
                print('Не удалось получить токен')
        except requests.exceptions.ConnectionError:
            ui_login.state.setText("Ошибка (проверь интернет)  :(")
            print('Интернета нетю (а вот, а всё, а надо было раньше инетом пользоваться :3 )')
        except UnicodeEncodeError: 
            ui_login.state.setText("Ошибка (русские символы)  :(")
            print('Чето чел попутал все берега. На русских символах пишет логин, гений одним словом ;)')
        return '';
