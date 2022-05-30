import datetime

from sqlalchemy import UniqueConstraint

from dbs.db import db, metadata


class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    id = db.Column(db.BIGINT, primary_key=True, unique=True, nullable=False)
    ticker_name = db.Column(db.String(10), nullable=False)
    trading_day = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    open_price = db.Column(db.FLOAT, nullable=False)
    max_price = db.Column(db.FLOAT, nullable=False)
    min_price = db.Column(db.FLOAT, nullable=False)
    close_price = db.Column(db.FLOAT, nullable=False)
    __table_args__ = (UniqueConstraint('ticker_name', 'trading_day', name='_ticker_day_uc'),
                      )

    def __repr__(self):
        return f'<Price {self.ticker_name}>'
