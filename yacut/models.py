from datetime import datetime

from yacut import db
from . import LENGTH_LIMIT, MAX_LENGHT


class URLMap(db.Model):
    """Модель для оригинальной и короткой ссылок."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGHT), nullable=False)
    short = db.Column(db.String(LENGTH_LIMIT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            original=self.original,
        )

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
