import random
import string
from urllib.parse import urljoin

from flask import flash, redirect, render_template, Markup


from . import app, db, BASE_URL, SHORT_LENGTH
from .forms import URLForm
from .models import URLMap


def get_unique_short_id():
    """Генерация короткой ссылки по умолчанию."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(SHORT_LENGTH))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Генерация короткой ссылки при вводе пользователем."""
    form = URLForm()
    if form.validate_on_submit():
        original_inp = form.original_link.data
        short_inp = form.custom_id.data or get_unique_short_id()
        if URLMap.query.filter_by(short=short_inp).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        new_url = URLMap(
            original=original_inp,
            short=short_inp
        )
        db.session.add(new_url)
        db.session.commit()
        short_link = urljoin(BASE_URL, new_url.short)
        flash(Markup
              (f'Ваша новая ссылка готова: <a href="'
               f'{short_link}">{short_link}</a>'))

    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_to_original(short):
    """Переадресация по адресу оригинальной ссылки."""
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)


if __name__ == '__main__':
    app.run()
