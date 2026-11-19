import pickle
import random
import sys
import time
import re

import zmq

import constPipe

file_path = './' + str(sys.argv[1])

host = constPipe.SRC1  # check task src host
port = constPipe.PORT1 # check task src port

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + host + ":" + port  # how and where to bind
push_socket.bind(address)  # bind socket to address

time.sleep(1)  # give all workers time to connect (needed for an even distribution)

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        push_socket.send(pickle.dumps(line))