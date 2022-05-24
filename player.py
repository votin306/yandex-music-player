import pygame
from yandex_music import Client, DownloadInfo, exceptions
import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
import json
from threading import Thread
from PyQt5 import QtCore, QtWidgets, uic
from command import login_yandex, login_yandex_close, login_yandex_show

token_account = 0
id_action_track = ''
id_action_album = ''

app = QtWidgets.QApplication([])
ui_login = uic.loadUi("login.ui")
ui = uic.loadUi("play.ui")
ui.setFixedSize(971,905)

def remove_char(s):
    result = s[1 : -1]
    return result

def chart_set_track(item): #Выбор трека из чарта и отображение инфы от песне
    client = Client(token_account)
    search_result = client.search(item.text())
    result_info_album = search_result.best.result.albums
    id_album = [artist.id for artist in result_info_album]
    id_action_album = str(str(id_album))
    id_track = search_result.best.result.id
    id_action_track = str(id_track)
    track = client.tracks(f'{id_track}')[0]
    name_artist = [artists.name for artists in track.artists]
    year_track = [album.year for album in track.albums]
    ui.artist_set_track.setText(",".join(name_artist))
    ui.name_set_track.setText(track.title)
    ui.year_track.setText(str(year_track))
    ui.album_titile.setText(str([album.title for album in track.albums]))
    try:
        ui.like_set_track.clicked.connect(client.users_likes_tracks_add(id_track))
    except TypeError: pass
    except exceptions.UnauthorizedError: pass
    
def thread_chart_set_track(item): #Поток для верхней задачи
    th = Thread(target=chart_set_track, args=[item]).start()

def load_love_track(): #Загузка любимых песен
    try:    
        client = Client(token_account)
        for count in client.users_likes_tracks():
            track = client.tracks(f'{count.track_id}')[0]
            ui.love_track.addItem(f"{track.title} - {', '.join(artist.name for artist in track.artists)}")
    except exceptions.NetworkError:
        pass
    finally:
        ui.staus_app.setText("Ок")

def thread_load_love_track(): #Поток ввехней задачи
    th = Thread(target=load_love_track).start()

def load_chart(): #Загрузка чарта при запуске
    ui.staus_app.setText("Загрузка любимых треков")
    try:
        client = Client(token_account)
        chart = client.chart('world').chart
        for track_short in chart.tracks:
            track, chart = track_short.track, track_short.chart
            artists = ''
            if track.artists:
                artists = ' - ' + ', '.join(artist.name for artist in track.artists)
            track_text = f'{track.title}{artists}'
            track_text = f'{track_text}'
            ui.list_chart.addItem(track_text)
    except exceptions.NetworkError:
        pass
    
def thread_load_chart(): #Поток верху
    th = Thread(target=load_chart).start()

def play(item): #Играть песню с плейлита
    client = Client(token_account)
    search_result = client.search(item.text())
    id_track = search_result.best.result.id
    track = client.tracks(f'{id_track}')[0]
    #track.download("1.mp3")
    track.download_cover("1.png")
    pixmap = QPixmap('1.png')
    pixmap = pixmap.scaled(171, 171)
    ui.image.setPixmap(pixmap)
    ui.name_set_track.setText(f"{track.title}")
    ui.artist_set_track.setText(', '.join([artist.name for artist in track.artists]))
    ui.year_track.setText(remove_char(str([album.year for album in track.albums])))
    ui.album_titile.setText(remove_char(str([album.title for album in track.albums])[1 : -1]))
    ui.genere.setText(remove_char(str([album.genre for album in track.albums])[1 : -1]))
    
def thread_play(item):
    th = Thread(target=play, args=[item]).start()

def set_volume():
    ui.vol_label.setText(str(ui.vol.value()))

ui_login.login_button.clicked.connect(login_yandex)
ui_login.exit_button.clicked.connect(login_yandex_close)
ui.auth_yandex.clicked.connect(login_yandex_show)
ui.list_chart.itemClicked.connect(thread_chart_set_track)
ui.love_track.itemClicked.connect(thread_play)
ui.vol.valueChanged.connect(set_volume)
#ui.pause.clicked.connect(pause)
#ui.stop.clicked.connect(stop)
#ui.play.clicked.connect(resume)

if ui_login.__init__:
    try:
        with open("login_token.json", "r") as write_file:
            token = json.load(write_file) 
            client = Client(token["token"]).init()
            token_account = token["token"]
            if token["username"] == '': ui.auth_yandex.setText("Не авторизирован")
            else: ui.auth_yandex.setText(token["username"])
    except exceptions.NetworkError:
        ui.auth_yandex.setText("Нет интернета")
        ui.staus_app.setText("Нет интернета")
    client = Client(token_account)
    thread_load_chart()
    thread_load_love_track()
    ui.vol_label.setText(str(ui.vol.value()))

ui.show()
app.exec()
