import requests
from celery import Celery, shared_task

from settings import API_KEY, TICKER, URL, REDIS

app = Celery('tasks', broker=f'redis://{REDIS}', backend=f'redis://{REDIS}', include=['tasks'],
             argv=['--loglevel=INFO'])

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, get_candle.s(), name=f'Get ticker info: {TICKER}')


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 15})
def get_candle(*args):
    request_url = f'{URL}&symbol={TICKER}&apikey={API_KEY}'
    r = requests.get(request_url)
    if r.status_code != 200:
        raise Exception(f'Exchange response status code: {r.status_code}')
    data = r.json()
    task_id = app.current_worker_task.request.id
    print(task_id)
    return data
