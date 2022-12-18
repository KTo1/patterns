import os
import logging


savraska_log = logging.getLogger('savraska.main')
formatter = logging.Formatter("<%(asctime)s> <%(levelname)s> <%(module)s> <%(message)s>")

logs_dir = 'logs'
file_name = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(file_name, logs_dir)
file_name = os.path.join(file_name, 'savraska.log')

file_hand = logging.FileHandler(file_name, encoding='utf-8')
file_hand.setLevel(logging.DEBUG)
file_hand.setFormatter(formatter)

if not savraska_log.handlers:
    savraska_log.addHandler(file_hand)

savraska_log.setLevel(logging.DEBUG)