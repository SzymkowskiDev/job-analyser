import logging
import json
import csv
import os
import datetime
import copy

log_format = "%(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


def load_file(input_filename: str, create=True, log_success=True) -> dict or list:
    """
    Loads csv as list and json as dict and returns it with provided name (output)
    Parameter output_filename is for file that is created if doesn't exist
    Set create to False if you want an error when input_filename file does not exist
    """
    file_type = input_filename.split(".")[1]
    file_existance = os.path.exists(input_filename)
    # JSON
    if file_type == "json":
        if file_existance:
            with open(input_filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if log_success:
                    logging.info(f"'{input_filename}' loaded successfully with ({len(data)} items)")
            return data
        else:
            if create is True:
                data = {}
                with open(input_filename,'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                logging.info(f"'{input_filename}' did not exist so created one named '{input_filename}'")
                return data
            else:
                logging.error(f"'{input_filename}' does not exist!")
                return None
    # CSV
    elif file_type == "csv":
        if file_existance:
            data = []
            with open(input_filename, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    data.append(row)
            if log_success:
                logging.info(f"'{input_filename}' loaded successfully with ({len(data)} items)")
            return data
        else:
            if create is True:
                data = []
                with open(input_filename, 'w', encoding='utf-8', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(data)
                    logging.info(f"'{input_filename}' did not exist so created one named '{input_filename}'")
                    return data
            else:
                logging.error(f"'{input_filename}' does not exist!")
                return None
    elif (file_type != "json" or file_type != "csv") and file_existance:
        logging.error(f"Unsupported input file type.")
        return None


def persist_file(input_data: dict or list, output_filename: str, log_success: bool = True) -> dict or list:
    """
    Saves input_data as output_filename and returns the data
    """
    if isinstance(input_data, dict):
        # JSON
        with open(output_filename,'w', encoding='utf-8') as f:
            json.dump(input_data, f, ensure_ascii=False)
        if log_success:
            logging.info(f"{len(input_data)} persisted successfully as '{output_filename}'")
        return input_data
    elif isinstance(input_data, list):
        # CSV
        with open(output_filename, mode='w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f)
            try:
                list_of_headers = list(input_data[0].keys())
            except IndexError:
                list_of_headers = ['url','job_title','created_at','applied','third_party_url']
            csv_writer.writerow(list_of_headers)
            for item in input_data:
                row = []
                for attribute in list_of_headers:
                    row.append(item[attribute])
                csv_writer.writerow(row)
        if log_success:
            logging.info(f"{len(input_data)} items persisted successfully as '{output_filename}'")
        return input_data
    else:
        logging.error(f"Unsupported input data type: {type(input_data)}.")
        return None


def merge_dicts_without_overwrite(dict1: dict, dict2: dict) -> dict:
    "Merges dicts without overwriting duplicates (leaves existing ones untouched)"
    logging.info("merge_dicts_without_overwrite() started")
    merged_dict = copy.deepcopy(dict1)
    duplicate_count = 0
    added_count = 0
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        for key, value in dict2.items():
            if key not in merged_dict:
                merged_dict[key] = value
                added_count += 1
            else:
                duplicate_count += 1
        logging.info(f"{duplicate_count} is the duplicate count")
        logging.info(f"{added_count} is the added count")
        logging.info(f"{len(merged_dict)} length of resulting merged dictionary")
        return merged_dict
    else:
        logging.error(f"dict1 is of type: {type(dict1)} and dict2 is of type: {type(dict2)}")
    