def average_vector(text, nlp):
    """
    Get the vector for the given text.

    This is calculated based on an average of SpaCy's word embeddings.

    Ignore tokens which do not have a known vector, and punctuation. If this
    filtering removes all tokens, then fall back to SpaCy's implementation
    which includes everything.

    :param text: Text string to process.
    :param nlp: Loaded SpaCy model for vectors.
    :returns: Average vector for the document.
    """
    doc = nlp(text, disable=["tagger", "parser", "ner"])
    token_vectors = [t.vector for t in doc if t.has_vector and not t.is_punct]

    if len(token_vectors) == 0:
        return doc.vector
    return sum(token_vectors) / len(token_vectors)
