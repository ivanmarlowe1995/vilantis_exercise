from datetime import datetime
from models.shared_models import db


class CountryRelationRevised(db.Model):

    __table_args__ = {'schema': 'edw'}

    id = db.Column(db.Integer, primary_key=True)
    allow_pirates_to_pirates = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text, nullable=False)
    min_rep_level_to_occur = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    random = db.Column(db.Boolean, nullable=False)
    rep_change = db.Column(db.Numeric(32, 10), nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


class CountryRelationScore(db.Model):

    __table_args__ = {'schema': 'edw'}

    country_id = db.Column(db.String(32), primary_key=True)
    country_a = db.Column(db.String(50), nullable=False)
    country_b = db.Column(db.String(50), nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())
    relationship_score = db.Column(db.Numeric(32, 10), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id
