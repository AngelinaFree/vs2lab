import pickle
import sys
import time

import zmq

import constPipe

topic = str(sys.argv[1])

address2 = "tcp://" + constPipe.SRC2 + ":" + constPipe.PORT2  # 2nd task src

context = zmq.Context()
sub_socket = context.socket(zmq.SUB)  # create a sub socket
sub_socket.setsockopt(zmq.SUBSCRIBE, topic.encode())

sub_socket.connect(address2)  # connect to task source 2

word_count = {}

while True:
    word = sub_socket.recv().split(' ')[1]  # receive work from a source (pickle: trusted peers only)

    word_count[word] = word_count.get(word, 0) + 1
    print(f"Reducer: {word_count[word]}x {word}")