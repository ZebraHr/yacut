from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from . import MIN_LENGHT, MAX_LENGHT, LENGTH_LIMIT


class URLForm(FlaskForm):
    """Форма для генерации короткой ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(MIN_LENGHT, MAX_LENGHT)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(MIN_LENGHT, LENGTH_LIMIT), Optional()]
    )
    submit = SubmitField('Создать')
