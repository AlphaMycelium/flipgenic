Quickstart
**********

Firstly, install Flipgenic `from pypi <https://pypi.org/project/flipgenic/>`_.

Create an instance of ``Responder``. This class will handle connection
to the database, and provides methods for learning and recalling
responses::

  from flipgenic import Responder
  responder = Responder('/path/to/storage/directory/')

Learn Responses
===============

Responses can be taught by passing a pair of statements, the second
in response to the first::

  responder.learn_response('Hello', 'Hi')

This is most commonly used in two ways:

- **Learn a large set of responses taken from a corpus.** This is helpful
  to build up the database when you first create a chatbot.
- **Learn each user input as a response to the last output in that
  conversation.** This extends your database as the bot is used, and
  adapts it to talk in a similar style to its users.


Get a Response
==============

A response can be recalled as follows::

  response, distance = responder.get_response('Hello')

``distance`` is the distance between the vectors of the input text, and
the text the selected response was originally responding to.

- The lower the value, the closer the match, and therefore the response
  has a higher chance of making sense in the conversation.
- If it is an exact match, it will be 0.
- The distance can theoretically be any positive number, however they
  tend to range from 0 up to around 5.
- If no responses are found (usually meaning the database is completely
  empty), the distance will be infinite.

By checking this value against a threshold of your choosing, you can
opt not to output uncertain responses - or to replace them with a
default message.
