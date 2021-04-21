"""Settings module."""

from starlette.config import Config

config = Config('.env')

MONGODB_HOST = config('MONGODB_HOST', default='mongo')
MONGODB_PORT = config('MONDODB_PORT', cast=int, default=27017)
DATA_PATH = config('DATA_PATH', default='/data/rivm2016.csv')
