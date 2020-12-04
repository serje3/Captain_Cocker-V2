import os

from utils import databases


TOKEN=os.environ.get('TOKEN')
AUTHKEY = os.environ.get('AUTHKEY')
URL = os.environ.get('URL')
PORT = os.environ.get('PORT')


DATABASE_TYPE = databases['postgres']
DATABASE_CONF = os.environ.get('POSTGRESQL_CONF')












