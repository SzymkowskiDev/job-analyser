import json
import logging
import os
from util import load_file, persist_file, merge_dicts_without_overwrite
from collections import Counter

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def io_skills_to_titles(input_skills: list, n_titles = 15) -> list:
    sink = load_file(input_filename='data/sink.json', create=True, log_success=True)
    sink_filtered = {}
    title_list = []
    for job_url, job_details in sink.items():
        required_skills = job_details.get('required_skills')
        result = set(input_skills).intersection(set(required_skills)) == set(input_skills)
        if result:
            sink_filtered.update({job_url: job_details})
            title_list.append(job_details.get('job_title'))

    frequency_counts = Counter(title_list)
    sorted_counts = dict(frequency_counts.most_common())
    persist_file(input_data=sorted_counts, output_filename='data/io_skills_to_titles/sink_title_counts.json')
    n_most_frequent_skills = {}
    counter = 0
    for skill, count in sorted_counts.items():
        counter += 1
        if counter > n_titles:
            break
        else:
            n_most_frequent_skills.update({skill: count})
    logging.info(f"{n_most_frequent_skills} {len(n_most_frequent_skills)} most frequent skills for {input_skills} and sample size: {len(sink_filtered)}")
    if len(sink_filtered) < 30:
        logging.warning(f"Sample size less than 30! ({len(sink_filtered)})")
    return n_most_frequent_skills


if __name__ == '__main__':
    io_skills_to_titles(input_skills=['React'])