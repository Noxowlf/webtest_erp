from .base import *

DEBUG = False

import  dj_database_url 
DATABASES [ 'default' ] = dj_database_url.config ()
	
# Respete el encabezado 'X-Forwarded-Proto' para request.is_secure() 
SECURE_PROXY_SSL_HEADER = ( 'HTTP_X_FORWARDED_PROTO' ,  'https' )

# Permitir todos los encabezados de host 
ALLOWED_HOSTS = ['*']


import os

env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

try:
    from .local import *
except ImportError:
    pass
