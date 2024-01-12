import logging
import streamlit as st
from annotated_text import annotated_text

log_format = "%(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


def generate_text_cloud(intro: str, data: dict) -> None:
    annotated_pairs = []
    for key, value in data.items():
        annotated_pairs.append((key, str(value)))
    annotated_text(intro + " ", *annotated_pairs)
