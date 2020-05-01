from flipgenic.db_models import Response
from flipgenic.vector import average_vector


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


def learn_response(responding_to, response, session, index, nlp):
    """
    Learn the given response.

    :param response: Response to learn.
    :param responding_to: The text this statement was in response to.
    :param session: Database session to use for insertions.
    :param index: NGT index to use for insertions.
    """
    vector = average_vector(responding_to, nlp)
    ngt_id = get_index_id(vector, index)

    session.add(Response(ngt_id=ngt_id, response=response))
    session.commit()
