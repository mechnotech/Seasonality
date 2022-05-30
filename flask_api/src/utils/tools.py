import json
from datetime import datetime
from http import HTTPStatus
from typing import Tuple, Union, Optional, Any, List

from flask import make_response, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import abort
import pandas as pd

from dbs.db import db, cache
from utils.models import HistoryUpdater


def show_error(text: Optional[Any], http_code: int):
    return abort(make_response(jsonify({'msg': text}), http_code))


def get_start_dates():
    result = db.session.execute("""
    SELECT *
    FROM price_history
    WHERE trading_day in (
    SELECT min(trading_day) as start_day
    FROM price_history
    WHERE EXTRACT(MONTH from trading_day) = 1 and EXTRACT(DAY from trading_day) in (1, 2, 3, 4, 5, 6, 7)
    GROUP BY EXTRACT(YEAR from trading_day));
    """)

    first_trading_days = [x[2] for x in result]

    return first_trading_days


def get_records_by_date_pair(pair: Tuple[datetime, Union[datetime, None]]):
    if isinstance(pair[1], datetime):
        second_arg = f"'{pair[1]}'"
    else:
        second_arg = 'now()'
    period = db.session.execute(f"""
    SELECT *
    FROM price_history
    WHERE trading_day >= '{pair[0]}' AND trading_day < {second_arg};
    """)
    period = {x[2]: x[3] for x in period}

    return period


def pairing_date(list_date: List[datetime]):
    pair_list = []
    if len(list_date) > 1:
        for i in range(len(list_date)):
            next_i = i + 1
            if next_i == len(list_date):
                pair_list.append((list_date[i], 'Now'))
                return pair_list
            pair_list.append((list_date[i], list_date[next_i]))
        return pair_list
    return list_date[0], 'Now'


def calc_pseudo_seasonality(periods):
    for period, records in periods.items():
        start_price = records[period[0]]
        for key_date, price in records.items():
            shift = (price - start_price) / start_price * 100
            records[key_date] = round(shift, 2)
    return periods


def get_year_records(pairs: List[Tuple[datetime, Union[datetime, None]]]):
    result = {}
    for pair in pairs:
        result[pair] = get_records_by_date_pair(pair)
    return result


def get_seasonality_df(periods):
    to_df = {}
    for k, v in periods.items():
        to_df.update(v)

    work_df = pd.DataFrame(to_df.items(), columns=['Date', 'Shift'])
    return work_df


def seasonality():
    dates = get_start_dates()
    date_pairs = pairing_date(dates)
    periods = get_year_records(date_pairs)
    shifted_records = calc_pseudo_seasonality(periods)

    df = get_seasonality_df(shifted_records)
    df['day_of_year'] = df['Date'].dt.dayofyear
    df['Date'] = df['Date'].astype(str)

    current_year = dates.pop(-1).year
    dates = dates[::-1]
    calc_year = dates[0].year
    result = {'This year': df.query(f'Date > "{current_year}"').groupby(['Date']).mean().to_dict()['Shift']}
    for i in range(5, len(dates), 5):
        result[f'{i} years'] = df.query(
            f'Date < "{calc_year}" and Date > "{dates[i].year}"'
        ).groupby(['day_of_year']).mean().round(decimals=2).to_dict()['Shift']

    return result


def post_load(obj):
    if not request.json:
        return abort(make_response(jsonify({'msg': 'Пустой запрос'}), HTTPStatus.BAD_REQUEST))
    try:
        entity = obj(**request.json)
    except ValidationError as e:
        return show_error(e.errors(), HTTPStatus.BAD_REQUEST)
    return entity


def get_from_redis(task: HistoryUpdater):
    task_data = None
    for k in cache.scan_iter(match='*' + str(task.task_id)):
        task_data = cache.get(name=k)
    if not task_data:
        show_error(f'Task ID {task.task_id} data not found', HTTPStatus.NOT_FOUND)
    return json.loads(task_data)


def put_to_database(task_data):
    pass
