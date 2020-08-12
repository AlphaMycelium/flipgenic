<p align="center">
  <img
    src="images/header.png"
    alt="Flipgenic: High-speed conversational dialogue engine"
  />
</p>

---

## What is it?

Flipgenic is a Python package which helps you in creating chatbots which
respond using a database of known conversations. It learns how to talk based on
messages it receives, or messages from a dataset which are pre-trained into it.

## How do I use it?

Here is a very basic example:

```python
# python -m pip install flipgenic
# python -m spacy download en_core_web_md

from flipgenic import Responder

# Create and connect to database
# This can take a while to load the spaCy models
responder = Responder('/path/to/data/folder/')

# Initialize the database with a single response
responder.learn_response('Hello', 'Hi!')

response = None
while True:
    text = input('> ')

    if response:
        # Learn the input as a response to the previous output
        responder.learn_response(response, text)

    # Generate a response
    response, distance = responder.get_response(text)
    print(response, f'({distance})')
```

**For more, see [ReadTheDocs](https://flipgenic.readthedocs.io/en/latest/quickstart.html).**

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
