from configparser import ConfigParser

conf = ConfigParser()
conf.read('config.ini')

KEY = conf['CONSUMER']['KEY']
SECRET = conf['CONSUMER']['SECRET']

ACCESS_KEY = conf['ACCESS']['KEY']
ACCESS_TOKEN = conf['ACCESS']['TOKEN']