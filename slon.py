from flask import Flask, request, jsonify
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response: {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ],
            'elephant_count': 0
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in ['ладно', 'куплю', 'покупаю', 'хорошо', 'ок', 'давай']:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете! Вот ссылка: https://market.yandex.ru/search?text=слон'
        res['response']['end_session'] = True
        return

    sessionStorage[user_id]['elephant_count'] += 1
    count = sessionStorage[user_id]['elephant_count']

    if count == 1:
        text = f"Ну пожалуйста! Купи слона! Они такие милые!"
    elif count == 2:
        text = "Слоны - самые умные животные после человека! Тебе точно нужен слон!"
    elif count == 3:
        text = "Представляешь, как круто будет говорить друзьям, что у тебя есть собственный слон?"
    else:
        text = f"Я уже {count} раз просила! Ну купи слона!"

    res['response']['text'] = text
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:] + [session['suggests'][0]]

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно, куплю",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run(port=5000)
