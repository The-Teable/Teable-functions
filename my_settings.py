# my_settings.py
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'teable_dev',
    'USER': 'root',
    'PASSWORD': 'SkaksdmlTea',
    # 'HOST': '/opt/bitnami/mysql/tmp/mysql.sock',
    'HOST': 'localhost',
    'PORT': '1234',
  }
}

SECRET_KEY = 'django-insecure-^qucw5$yj*wf4n6ywawt-zq997c5zjs@w#)g4b-&e(sg^&zt1k'