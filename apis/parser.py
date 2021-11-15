from io import StringIO
import selenium
from selenium import webdriver
# from lxml import html, etree
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teable-functions.settings")
import django
django.setup()

options = webdriver.ChromeOptions()
options.add_argument('headless')