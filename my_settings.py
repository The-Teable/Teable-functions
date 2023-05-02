# my_settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'teable_dev',
        'USER': 'root',
        'PASSWORD': ' ',
        # 'HOST': '/opt/bitnami/mysql/tmp/mysql.sock',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

SECRET_KEY = ' '
