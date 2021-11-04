# my_settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'teable_dev',
        'USER': 'root',
        'PASSWORD': 'SkaksdmlTea',
        'HOST': '/opt/bitnami/mariadb/tmp/mysql.sock',
        # 'HOST': '127.0.0.1',
        'PORT': '1234',
    }
}

SECRET_KEY = 'django-insecure-^qucw5$yj*wf4n6ywawt-zq997c5zjs@w#)g4b-&e(sg^&zt1k'
