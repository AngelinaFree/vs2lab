import pickle
import sys
from time import sleep

import zmq

import constPipe

print('Reducer started')


context = zmq.Context()
pull_socket = context.socket(zmq.PULL)

host, port = constPipe.reducer_connections[int(sys.argv[1]) - 1]

pull_socket.bind(f'tcp://{host}:{port}')

word_count = {}

try:
    while True:
        word = pickle.loads(pull_socket.recv())  # receive work from a source (pickle: trusted peers only)
        word_count[word] = word_count.get(word, 0) + 1
        print(f'{word} : {word_count[word]}')
        pull_socket.setsockopt(zmq.RCVTIMEO, 5000)
except zmq.Again:
    pass

print('\nFinished')
print('----------------')
for word, count in word_count.items():
    print(f'{word}: {count}')