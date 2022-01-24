from .base import *

DEBUG = False

import  dj_database_url 
DATABASES [ 'default' ]  =   dj_database_url . configuración ()
	
# Respete el encabezado 'X-Forwarded-Proto' para request.is_secure() 
SECURE_PROXY_SSL_HEADER  =  ( 'HTTP_X_FORWARDED_PROTO' ,  'https' )

# Permitir todos los encabezados de host 
ALLOWED_HOSTS  =  [ '*' ]

try:
    from .local import *
except ImportError:
    pass
