import logging
from logging.handlers import RotatingFileHandler

# file handler
handler = RotatingFileHandler('app.logs', mode='a', maxBytes=10*1024*1024, backupCount=9)

# log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)






