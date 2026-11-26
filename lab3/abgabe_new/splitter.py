import pickle
import random
import string
import sys
import time

import zmq

import constPipe

print('Splitter started')

if len(sys.argv) > 1:
    file_path = './' + str(sys.argv[1])
    generate = False
else:
    generate = True

host = constPipe.SRC1  # check task src host
port = constPipe.PORT1 # check task src port

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + host + ":" + port  # how and where to bind
push_socket.bind(address)  # bind socket to address

time.sleep(1)  # give all workers time to connect (needed for an even distribution)

if not generate:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            push_socket.send(pickle.dumps(line))
else:
    length = 1000
    random_string = ''.join(random.choices(string.ascii_letters + string.digits + '\n' + ' ', k=length))
    sentences = random_string.split('\n')
    for line in sentences:
        push_socket.send(pickle.dumps(line))

push_socket.close()
context.term()