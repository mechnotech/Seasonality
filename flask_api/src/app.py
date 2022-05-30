from flasgger import Swagger
from flask import Flask

from dbs.db import init_db
from settings import config

from views.history.history import history

app = Flask(__name__)
app.config.from_pyfile('settings.py', silent=True)
init_db(app)
app.app_context().push()

swagger = Swagger(app, template_file='project_description/openapi.yaml')

app.register_blueprint(history, url_prefix='/api/v1/history')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', port=config.api_port,
    )
