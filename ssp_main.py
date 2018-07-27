#!/usr/bin/python3

import json
import pickle
import queue
import socket
import sys
import threading

def thr_read_temp(port, rxbuffsize, q, stop_flag):
    # open UDP socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.1)
    addr = ('127.0.0.1', port)
    sock.bind(addr)

    # run until stop flag is raised
    while not stop_flag():
        # wait for data
        try:
            data, address = sock.recvfrom(rxbuffsize)
        except:
            continue

        # unpickle
        data = pickle.loads(data)

        # send it to the temp queue
        q.put(data)

def main():
    # open and parse the config file
    with open('config.json') as f:
        config = json.load(f)

    # thread stop flag
    stop_flag = False

    # create queues
    queue_temperature = queue.Queue()

    # stand up threads
    t_read_temp = threading.Thread(target=thr_read_temp, args=(config['ports']['temperature_1'], config['rx_buffer_size'], queue_temperature, lambda: stop_flag))
    t_read_temp.start()

    try:
        while True:
            if not queue_temperature.empty():
                data_temp = queue_temperature.get()
                print('Temperature: {}'.format(data_temp))
    except KeyboardInterrupt:
        stop_flag = True

    t_read_temp.join()

    print('\nCaught Interrupt. Exiting...')

if __name__ == '__main__':
    main()
    sys.exit()
