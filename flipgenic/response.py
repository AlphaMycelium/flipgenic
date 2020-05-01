import random
from statistics import StatisticsError, mode

from mathparse import mathparse

from flipgenic.db_models import Response
from flipgenic.vector import average_vector


def process_as_math(text):
    """
    Attempt to process the text as a mathematical evaluation using mathparse.

    :returns: Response text, or None if the input cannot be parsed as math.
    """
    try:
        expression = mathparse.extract_expression(text, language="ENG")
        result = mathparse.parse(expression, language="ENG")
        return f"{expression} = {result}"
    except:
        return None


def get_closest_vector(text, index, nlp):
    """
    Get the closest matching response from the index.

    :param text: Text we are comparing against.
    :param index: NGT index to query from.
    :param nlp: Loaded SpaCy model for vectors.
    :returns: Tuple of (id, distance).
    """
    text_vector = average_vector(text, nlp)

    # Nearest neighbour search to find the closest stored vector
    results = index.search(text_vector, 1)
    return results[0] if len(results) else (None, None)


def get_response(text, index, session, nlp):
    """
    Generate a response to the given text.

    :param text: Text to respond to.
    :param index: NGT index to use for queries.
    :param session: Database session to use for queries.
    :param nlp: Loaded SpaCy model for vectors.
    :returns: Tuple of (response, distance).
    """
    math_response = process_as_math(text)
    if math_response:
        # The text can be handled as a mathematical evaluation
        return math_response, 1

    # Find closest matching vector
    match_id, distance = get_closest_vector(text, index, nlp)
    if match_id is None:
        return None, 0

    # Get all response texts associated with this input
    matches = session.query(Response).filter(Response.ngt_id == match_id).all()
    responses = [match.response for match in matches]

    try:
        # Select most common response
        response = mode(responses)
    except StatisticsError:
        # Select a random response
        response = random.choice(responses)

    return response, distance
