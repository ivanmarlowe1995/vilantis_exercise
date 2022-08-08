from datetime import datetime
from models.shared_models import db


class ClickHistory(db.Model):

    __table_args__ = {'schema': 'edw'}

    id = db.Column(db.Integer, primary_key=True)
    user_ip_address = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    request_type = db.Column(db.String(100), nullable=False)
    request_referrer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id
