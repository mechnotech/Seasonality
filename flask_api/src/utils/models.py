import orjson
from pydantic import BaseModel, UUID4


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode('utf-8')


class AdvancedJsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class HistoryUpdater(AdvancedJsonModel):
    task_id: UUID4
    ticker: str
