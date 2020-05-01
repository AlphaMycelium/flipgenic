import os

import ngtpy
import spacy
import sqlalchemy

from flipgenic.db_models import Base
from flipgenic.response import get_response
from flipgenic.train import learn_response


class Responder:
    """
    Connects to database files and generates responses.

    :param db_path: Path to the database folder which will hold files
        related to this responder. Will be created if it doesn't exist.
    :param spacy_model: Name of the spaCy model to load. This must be
        downloaded before use.
    """

    def __init__(self, db_path, model_name="en_core_web_md"):
        # Create the directory if it doesn't exist
        os.makedirs(db_path, exist_ok=True)
        self.db_path = db_path

        self._ngt = self._load_ngt()
        self._db_session = self._load_db()
        self._nlp = self._load_nlp(model_name)

    def get_response(self, text):
        """
        Find the best response to the given input text.

        :param text: Input text to respond to.
        :returns: Tuple of (response, distance).
        """
        session = self._db_session()
        response = get_response(text, self._ngt, session, self._nlp)
        session.close()
        return response

    def learn_response(self, responding_to, response):
        """
        Learn the given text as the response to an input.

        :param response: The response to be learned.
        :param responding_to: The text this is in response to.
        """
        session = self._db_session()
        learn_response(responding_to, response, session, self._ngt, self._nlp)
        session.close()

    def _load_ngt(self):
        """Create and open the NGT index."""
        path = os.path.join(self.db_path, "ngt")
        if not os.path.exists(path):
            ngtpy.create(path, dimension=300)  # Spacy word vectors are 300D

        return ngtpy.Index(path)

    def _load_db(self):
        """Create and open the SQLite responses database."""
        path = os.path.join(self.db_path, "responses.sqlite3")
        engine = sqlalchemy.create_engine("sqlite:///" + path)
        Base.metadata.create_all(engine)  # Create tables

        return sqlalchemy.orm.sessionmaker(bind=engine)

    def _load_nlp(self, model_name):
        """Load the SpaCy model."""
        return spacy.load(model_name, disable=["ner", "textcat"])
