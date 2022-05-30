# Запустить один раз после инсталляции
# и выполнения миграции: alembic upgrade head !
from datetime import datetime

from app import app
from db_models.models import PriceHistory
from dbs.db import init_db
from dbs.db import db


def table_exist():
    for t in db.metadata.sorted_tables:
        if t.name == 'price_history':
            return True
    return False


def table_not_empty():
    result = PriceHistory.query.first()
    return result


def from_csv():
    with open('dataset/KC-057.csv', 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            row = line.split(',')
            dc_row = {
                'ticker_name': row[0],
                'trading_day': datetime.strptime(row[1], "%m/%d/%Y"),
                'open_price': row[2],
                'max_price': row[3],
                'min_price': row[4],
                'close_price': row[5],
            }
            yield dc_row


def to_postgres(batch):
    db.session.bulk_save_objects(batch)
    db.session.commit()


def csv_to_postgres():
    batch = []
    counter = 0
    for row in from_csv():

        history_record = PriceHistory(**row)
        batch.append(history_record)
        counter += 1
        if counter == 99:
            to_postgres(batch)
            batch.clear()
            counter = 0
    if batch:
        to_postgres(batch)


if __name__ == '__main__':
    init_db(app)
    app.app_context().push()
    if table_exist() and not table_not_empty():
        csv_to_postgres()
        print('....Dataset loaded.....')
    else:
        print('Database not empty: exiting')
