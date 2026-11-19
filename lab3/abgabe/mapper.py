import pickle

import zmq

import constPipe

address1 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1  # 1st task src

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket

pull_socket.connect(address1)  # connect to task source 1


host = constPipe.SRC2  # check task src host
port = constPipe.PORT2 # check task src port

context = zmq.Context()
pub_socket = context.socket(zmq.PUB)  # create a pub socket

address = "tcp://" + host + ":" + port  # how and where to bind
pub_socket.bind(address)  # bind socket to address

while True:
    for word in pickle.loads(pull_socket.recv()).split(' '):  # receive work from a source (pickle: trusted peers only)
        code = ord(word[0])
        topic = str(code % 2)

        pub_socket.send_string("%s %s" % (topic, word))