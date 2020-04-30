import logging

import spacy

logger = logging.getLogger(__name__)


# This module exists to ensure we only load the model once
# for use in all modules.
logger.info("Loading NLP model")
nlp = spacy.load("en_core_web_md", disable=["ner", "textcat"])
