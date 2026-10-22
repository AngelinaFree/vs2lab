import logging
import threading
import unittest

import aufgabe1
import dictionary
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    # Threading Server
    _server = aufgabe1.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = aufgabe1.Client()  # create new client for each test

    def test_srv_get_correct(self):  
        msg = self.client.call("GET jan")
        self.assertEqual(msg, 'jan: 123456789')

    def test_srv_get_Upper(self):  
            msg = self.client.call("GET JAN")
            self.assertEqual(msg, 'jan: 123456789')

    def test_srv_get_wrong(self):
            msg = self.client.call("GET David")
            self.assertEqual(msg, 'No entry for "david"')

    def test_srv_get_all(self):
            msg = self.client.call("GETALL")
            self.assertEqual(msg, dictionary.to_string())

    def test_srv_bad_request(self):
                msg = self.client.call("get jan")
                self.assertEqual(msg, 'bad request')

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate

    


if __name__ == '__main__':
    unittest.main()
