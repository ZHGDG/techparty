import sae
import config
from bottle import debug, run
from web import APP

application = sae.create_wsgi_app(APP)


