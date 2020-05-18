from flipgenic import Responder

responder = Responder('/home/danth/flipgenic_test')

response = None
while True:
    text = input('> ')

    if text.strip() == '++train++':
        responder.learn_response(
            input('A: '),
            input('B: ')
        )
        print('Learned!')
    else:
        if response:
            # Learn as response to previous output
            responder.learn_response(response, text)

        response, confidence = responder.get_response(text)
        print(response, f'({confidence})')
