import os

import ngtpy
import spacy
import sqlalchemy

from flipgenic.db_models import Base, Response
from flipgenic.vector import average_vector
from flipgenic.response import get_response


class Responder:
    """
    Connects to database files and generates responses.

    :param db_path: Path to the database folder which will hold files
        related to this responder. Will be created if it doesn't exist.
    :param model: SpaCy model, or the name of one to be loaded.
    """

    def __init__(self, db_path, model="en_core_web_md"):
        # Create the directory if it doesn't exist
        os.makedirs(db_path, exist_ok=True)
        self.db_path = db_path

        self._ngt = self._load_ngt()
        self._db_session = self._load_db()
        self._nlp = self._load_nlp(model)

        self._to_learn = list()

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

    def add_response(self, responding_to, response):
        """
        Add a response to the batch, to be committed later.

        responding_to is transformed into a vector now, but it is not
        added to the index until you commit it.

        :param response: The response to be learned.
        :param responding_to: The text this is in response to.
        """
        vector = average_vector(responding_to, self._nlp)
        self._to_learn.append((vector, response))

    def _get_ngt_id(self, vector):
        """
        Get the NGT id of the given vector.

        This is performed first by searching ``self._unbuilt_ids`` for a match, and
        then querying the index if none is found.

        If there is still no match, then the vector will be inserted into the index,
        however the index is not rebuilt. This means that the vector will not be found
        if this method is called again. Therefore, we use a dictionary of unbuilt IDs
        to avoid adding the same vector twice. The dictionary can be emptied once the
        index has been updated.

        :param vector: Vector to get the ID of.
        """
        # Convert the numpy array to bytes so we can use it as a dictionary key
        vector_hash = vector.tobytes()
        if vector_hash in self._unbuilt_ids:
            # Vector is in unbuilt_ids, return it
            return self._unbuilt_ids[vector_hash]

        # Query the index for this vector
        result = self._ngt.search(vector, 1)
        if len(result) > 0 and result[0][1] == 0:
            # This vector already exists, return its id
            return result[0][0]
        else:
            # Add vector to the index
            ngt_id = self._ngt.insert(vector)
            self._unbuilt_ids[vector_hash] = ngt_id
            return ngt_id

    def commit_responses(self):
        """
        Ingest added responses into the database and index.
        """
        self._unbuilt_ids = dict()
        session = self._db_session()

        for vector, response in self._to_learn:
            session.add(Response(
                ngt_id=self._get_ngt_id(vector),
                response=response
            ))

        self._ngt.build_index()
        self._ngt.save()
        session.commit()
        session.close()

        del self._unbuilt_ids
        self._to_learn = list()

    def learn_response(self, responding_to, response):
        """
        Learn the given text as the response to an input.

        This is a shortcut to calling add_response followed by commit_responses,
        and therefore any other added responses will also be committed.

        :param response: The response to be learned.
        :param responding_to: The text this is in response to.
        """
        self.add_response(responding_to, response)
        self.commit_responses()

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

    def _load_nlp(self, model):
        """Load the SpaCy model."""
        if type(model) == str:
            return spacy.load(model, disable=["ner", "textcat"])
        return model
