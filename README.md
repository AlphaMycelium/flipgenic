![Flipgenic: High-speed conversational dialogue engine](images/header.png)

**For how to get started, see
[ReadTheDocs](https://flipgenic.readthedocs.io/en/latest/quickstart.html).**

## How does it work?

A Flipgenic chatbot learns how to respond based on messages it receives, or
messages from a dataset which are pre-trained into it. Input messages (well,
a 300-dimensional [vector representation](https://spacy.io/api/token#vector)
of them) are stored along with any learned responses to that text. If someone
inputs the first message again, it will find the stored response and re-use it.

Input messages are converted to a 300-dimensional vector using
[SpaCy](https://spacy.io/api/token#vector). Then, this vector is used to
query the closest match from an [NGT](https://github.com/yahoojapan/NGT)
index containing the vectors of previously-learned messages. Each object ID
from the index corresponds to one or more known responses, stored in a
basic SQLite database. The most common response is selected, or one at random
if there is no mode.
