import time

import rpc
import logging

from context import lab_logging

def print_result(result):
    print("Result: {}".format(result.value))

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
thread = cl.append_async('bar', base_list, print_result)

thread.start()
print('The main program continues to run in foreground.')

while not cl.thread_finished:
    print("Warten...")
    time.sleep(1)

cl.stop()
