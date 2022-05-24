from yandex_music import Client, exceptions
import requests
from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])
ui = uic.loadUi("login.ui")
ui.setWindowTitle("Авторизация")

def login_yandex():
        link_post = 'https://oauth.yandex.com/token'
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        client_id = '23cabbbdc6cd418abb4b39c32c41195d'
        client_secret = '53bc75238f0c4d08a118e51fe9203300'
        header = {
            'user-agent': user_agent
        }
        try:
            request_post = f"grant_type=password&client_id={client_id}&client_secret={client_secret}&username={ui.login.text()}&password={ui.pwrd.text()}"
            request_auth = requests.post(link_post, data=request_post, headers=header)
            if request_auth.status_code == 200:
                json_data = request_auth.json()
                token = json_data.get('access_token')
                client = Client(token).init()
                ui.state.setText("Успешно ;)")

            else:
                ui.state.setText("Ошибка (проверь данные)  :(")
                print('Не удалось получить токен')
        except requests.exceptions.ConnectionError:
            ui.state.setText("Ошибка (проверь интернет)  :(")
            print('Интернета нетю (а вот, а всё, а надо было раньше инетом пользоваться :3 )')
        except UnicodeEncodeError: 
            ui.state.setText("Ошибка (русские символы)  :(")
            print('Чето чел попутал все берега. На русских символах пишет логин, гений одним словом)')
        return '';

ui.show()
app.exec()
