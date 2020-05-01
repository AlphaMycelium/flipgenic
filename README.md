![Flipgenic: High-speed conversational dialogue engine](images/header.png)

## What is it?

Flipgenic is a Python package which helps you in creating chatbots which
respond using a database of known conversations. It learns how to talk based on
messages it receives, or messages from a dataset which are pre-trained into it.

## How do I use it?

**See [ReadTheDocs](https://flipgenic.readthedocs.io/en/latest/quickstart.html).**

## How does it work?

Input messages (well, a 300-dimensional
[vector representation](https://spacy.io/api/token#vector) of them) are stored
along with any learned responses to that text. If someone inputs the first
message again, the stored response will be found and re-used.

Input messages are converted to a 300-dimensional vector using
[SpaCy](https://spacy.io/api/token#vector). Then, this vector is used to
query the closest match from an [NGT](https://github.com/yahoojapan/NGT)
index containing the vectors of previously-learned messages. Each object ID
from the index corresponds to one or more known responses, stored in a
basic SQLite database. The most common response is selected, or one at random
if there is no mode.
