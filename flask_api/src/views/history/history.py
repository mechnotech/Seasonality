from http import HTTPStatus

from flask import Blueprint

from utils.models import HistoryUpdater
from utils.tools import (

    post_load, seasonality, get_from_redis, put_to_database,

)

history = Blueprint('history', __name__)


@history.route('pull/', methods=['POST'])
def history_pull():
    task = post_load(obj=HistoryUpdater)
    result = get_from_redis(task)
    put_to_database(result)
    return {'msg': result['result']}, HTTPStatus.CREATED


@history.route('seasonality/', methods=['GET'])
def season_get():
    result = seasonality()
    return {'msg': result}
