import logging

from axyn.chatbot.ngtinit import reactions_index, statements_index
from axyn.chatbot.vector import average_vector
from axyn.models import Reaction, Statement

# Set up logging
logger = logging.getLogger(__name__)


def get_index_id(vector, index):
    """
    Get the NGT ID of the given vector.

    If the vector is not in the index, it will be added and the index built
    and saved.

    :param vector: Vector to get ID of.
    :param index: NGT index to query.
    :returns: NGT object id.
    """
    # Check if the index already contains this vector
    result = index.search(vector, 1)
    if len(result) > 0 and result[0][1] == 0:
        # This vector already exists, return its id
        return result[0][0]
    else:
        # Add vector to the index
        ngt_id = index.insert(vector)
        index.build_index()
        index.save()
        return ngt_id


def train_statement(text, responding_to, session):
    """
    Train the given statement into the index.

    :param text: Text to add.
    :param responding_to: The text this statement was in response to.
    :param session: Database session to use for insertions.
    """
    vector = average_vector(responding_to)
    ngt_id = get_index_id(vector, statements_index)

    session.add(Statement(ngt_id=ngt_id, text=text))
    session.commit()


def train_reaction(emoji, responding_to, session):
    """
    Train the given reaction into the index.

    :param text: Reaction emoji to add.
    :param responding_to: The text this reaction was added to.
    :param session: Database session to use for insertions.
    """
    vector = average_vector(responding_to)
    ngt_id = get_index_id(vector, reactions_index)

    session.add(Reaction(ngt_id=ngt_id, emoji=emoji))
    session.commit()
