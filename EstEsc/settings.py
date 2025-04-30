import os
from pathlib import Path

# Definir o diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Tentar carregar variáveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))
except ImportError:
    pass

# Definir ambiente
DJANGO_ENV = os.getenv('DJANGO_ENV', 'production')

# Chave secreta para o Django
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'unsafe-secret')

# Debug
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost', 'web-production-35f4b.up.railway.app', 'ow4crw.stackhero-network.com']

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'home',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Middleware WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# URL Conf
ROOT_URLCONF = 'EstEsc.urls'

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração de WSGI
WSGI_APPLICATION = 'EstEsc.wsgi.application'

# Configuração do banco de dados
if DJANGO_ENV == 'production':
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('STACKHERO_MYSQL_DB_NAME'),
        'USER': os.getenv('STACKHERO_MYSQL_USER'),
        'PASSWORD': os.getenv('STACKHERO_MYSQL_ROOT_PASSWORD'),
        'HOST': os.getenv('STACKHERO_MYSQL_HOST'),
        'PORT': os.getenv('STACKHERO_MYSQL_PORT'),
        'OPTIONS': {
            'ssl': {'ca': os.getenv('STACKHERO_MYSQL_SSL_CA')},
        },
    }
}

else:  # Desenvolvimento local
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway',
        'USER': 'vecchio',
        'PASSWORD': 'V3cc#!o55#',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Validadores de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuração de idioma e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Configuração de arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Modelo de usuário personalizado
AUTH_USER_MODEL = 'home.Usuario'

# Configurações de login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
