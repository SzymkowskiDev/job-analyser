import json
import logging
import os

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def generate_report(input_file = 'job_bank.json', output_file = 'stats.csv'):
    pass