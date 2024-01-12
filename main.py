import json
import logging
import os
from scrape_infinite_scroll import scrape_infinite_scroll
from scrape_job_details import scrape_job_details
from encrypt_data import encrypt_data

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

scrape_infinite_scroll(output='data/current_snapshot.json', max_index=5000, website='https://justjoin.it/?index=')
scrape_job_details(output1='data/current_snapshot.json', output2='data/sink.json')
encrypt_data('data/current_snapshot.json')
encrypt_data('data/sink.json')