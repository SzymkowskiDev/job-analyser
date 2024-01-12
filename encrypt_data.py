import logging
import json
import csv
import os
import datetime
import copy
from util import load_file, persist_file


log_format = "%(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


def hash_sensitive_data(data: dict) -> dict:
    logging.info(f"{len(data)} length of data before encryption")
    encrypted_data = {}
    for job_url, job_details in data.items():
        job_details.update({"company": str(hash(job_details.get("company")))})
        job_details.update({"description": str(hash(job_details.get("description")))})
        encrypted_data.update({str(hash(job_url)): job_details})
    logging.info(f"{len(encrypted_data)} length of data after encryption")
    return encrypted_data


def encrypt_data(input_filename):
    data = load_file(input_filename)
    encrypted_data = hash_sensitive_data(data) 
    persist_file(input_data=encrypted_data,output_filename=input_filename)


if __name__ == '__main__':
    encrypt_data('data/current_snapshot.json')
    encrypt_data('data/sink.json')
