import re

from flask import jsonify, request
from urllib.parse import urljoin

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id
from . import BASE_URL


@app.route('/api/id/', methods=['POST'])
def create_short():
    """Генерация новой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    long_url = data['url']
    if 'custom_id' not in data or data[
       'custom_id'] is None or data['custom_id'] == '':
        data['custom_id'] = get_unique_short_id()
    short_url = data['custom_id']
    if re.match(r"^[A-Za-z0-9]+$", short_url) is None:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=short_url).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if len(short_url) > 16:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )
    new_url = URLMap(
        original=long_url,
        short=short_url
    )
    db.session.add(new_url)
    db.session.commit()
    short_link = urljoin(BASE_URL, new_url.short)
    return jsonify({'url': data['url'], 'short_link': short_link}), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Получение ссылки по идентификатору."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
