import json
import logging
import os
from util import load_file, persist_file, merge_dicts_without_overwrite
from collections import Counter

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def filter_job_titles(sink, title):
    sink_filtered = {}
    title_list = []
    for job_url, job_details in sink.items():
        job_title = job_details.get('job_title')
        if title.lower() in job_title.lower():
            sink_filtered.update({job_url: job_details})
            title_list.append(job_title)
    logging.info(f"{len(sink_filtered)} job offers had {title} in title")
    logging.info(title_list)
    return sink_filtered


def get_skill_frequencies(sink_filtered):
    list_of_skills = []
    for job_url, job_details in sink_filtered.items():
        required_skills = job_details.get('required_skills')
        if required_skills:
            list_of_skills = list_of_skills + required_skills
    logging.info(f"{len(list_of_skills)} skills in list_of_skills")
    lowercase_list = [s.lower() for s in list_of_skills]
    frequency_counts = Counter(lowercase_list)
    sorted_counts = dict(frequency_counts.most_common())
    persist_file(input_data=sorted_counts, output_filename='data/io_title_to_skills/sink_title_counts.json')
    return sorted_counts


def io_title_to_skills(title='Data Engineer', n_skills=15):
    n_most_frequent_skills = None
    sink = load_file(input_filename='data/sink.json', create=True, log_success=True)
    sink_filtered = filter_job_titles(sink, title)
    persist_file(input_data=sink_filtered, output_filename='data/io_title_to_skills/sink_title.json')
    sorted_counts = get_skill_frequencies(sink_filtered)
    n_most_frequent_skills = {}
    counter = 0
    for skill, count in sorted_counts.items():
        counter += 1
        if counter > n_skills:
            break
        else:
            n_most_frequent_skills.update({skill: count})
    logging.info(f"{n_most_frequent_skills} {len(n_most_frequent_skills)} most frequent skills for {title} and sample size: {len(sink_filtered)}")
    if len(sink_filtered) < 30:
        logging.warning(f"Sample size less than 30! ({len(sink_filtered)})")
    return n_most_frequent_skills
    

if __name__ == '__main__':
    io_title_to_skills(title='devops', n_skills=15)


