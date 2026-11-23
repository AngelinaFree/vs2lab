import pickle
import re

import zmq

import constPipe

print('Mapper started')

address_1 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1  # Splitter

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
pull_socket.connect(address_1)

sockets = []
for host, port in constPipe.reducer_connections:
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect(f'tcp://{host}:{port}')
    sockets.append(push_socket)

while True:
    sentence = pickle.loads(pull_socket.recv())  # pickle: trusted peers only
    sentence = re.sub(r'[^\w\s]', '', sentence)
    words = sentence.lower().split()

    for word in words:
        filter = 0
        for char in word:
            filter += ord(char)
        print(f'Send \"{word}\" to reducer {filter % len(sockets) + 1}')
        sockets[filter % len(sockets)].send(pickle.dumps(word))