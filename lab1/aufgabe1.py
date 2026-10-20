"""
Client and server using classes
"""

import logging
import socket

import const_cs

import dictionary
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        self.sock.listen(1)
        self._logger.info("Server listening...")
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                self._logger.info("Client connected")
                while True:  # forever
                    data = connection.recv(1024)
                    self._logger.info("Data recieved")
                    if not data:
                        break  # stop if client stopped

                    message = data.decode('ascii').split()
                    if not message:
                        continue
                    if 'GETALL' == message[0]:
                        answer = self.getALL()
                    elif 'GET' == message[0] and len(message) == 2:
                        answer = self.get(message[1])
                    else:
                        self._logger.info("Bad Request")
                    connection.send(answer.encode('ascii'))
                connection.close()  # close the connection
                self._logger.info("Connection closed")
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")

    def get(self, name):
        try:
            return f'{name}: ' + dictionary.dictonary[name.lower()]
        except:
            return f'No entry for \"{name}\"'

    def getALL(self):
            answer = ''
            for name, number in dictionary.dictonary.items():
                answer += f'{name}: {number}\n'
            return answer




class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in):
        """ Call server """
        self.logger.info("Sending data")
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        self.logger.info("Waiting for response")
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        self.logger.info("Data recieved")
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def close(self):
        """ Close socket """
        self.sock.close()
