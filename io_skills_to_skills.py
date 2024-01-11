import json
import logging
import os
from util import load_file, persist_file, merge_dicts_without_overwrite
from collections import Counter

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def io_skills_to_skills(input_skills: list, n_skills = 15) -> list:
    sink = load_file(input_filename='data/sink.json', create=True, log_success=True)
    sink_filtered = {}
    list_of_skills = []
    for job_url, job_details in sink.items():
        required_skills = job_details.get('required_skills')
        result = set(input_skills).intersection(set(required_skills)) == set(input_skills)
        if result:
            sink_filtered.update({job_url: job_details})
            list_of_skills = list_of_skills + required_skills    
    logging.info(f"{len(list_of_skills)} skills in list_of_skills")
    lowercase_list = [s.lower() for s in list_of_skills]
    frequency_counts = Counter(lowercase_list)
    sorted_counts = dict(frequency_counts.most_common())
    lowercase_input_skills = [s.lower() for s in input_skills]
    sorted_counts_filtered = {}
    for skill, count in sorted_counts.items():
        if skill not in lowercase_input_skills:
            sorted_counts_filtered.update({skill: count})
            logging.debug(f"{skill} removed from end result")
    sorted_counts = sorted_counts_filtered
    persist_file(input_data=sorted_counts, output_filename='data/io_skills_to_skills/sink_skill_counts.json')
    n_most_frequent_skills = {}
    counter = 0
    for skill, count in sorted_counts.items():
        counter += 1
        if counter > n_skills:
            break
        else:
            n_most_frequent_skills.update({skill: count})
    logging.info(f"{n_most_frequent_skills} are skills that would give you more job hunting opportunities given that you already know {input_skills}")
    if len(sink_filtered) < 30:
        logging.warning(f"Sample size less than 30! ({len(sink_filtered)})")
    return n_most_frequent_skills


if __name__ == '__main__':
    io_skills_to_skills(input_skills=['SQL', 'Python', 'AWS'], n_skills = 15)