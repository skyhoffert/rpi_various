#!/usr/bin/python3

import datetime
import json
import pickle
import queue
import socket
import sys
import threading
import time

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

    # set up timers
    time_last = time.time()
    time_now = time.time()
    time_between_samples = config['s_between_samples']

    try:
        while True:
            # wait for next sampling to occur
            while time_now - time_last < time_between_samples:
                time_now = time.time()

            # reset variables
            time_last = time_now
            data_temp = 0

            # if there is something in the temperature queue
            if not queue_temperature.empty():
                # pop until we get the most recent sample
                while not queue_temperature.empty():
                    data_temp = queue_temperature.get()
    
            # save data to file
            now = datetime.datetime.utcnow()
    
            with open('./logs/{}_{}_{}.log'.format(now.year, now.month, now.day), 'a') as out:
                # log time as {hour}:{minute}:{second}:{millis},
                out.write('{}:{}:{}:{:.0f},'.format(now.hour, now.minute, now.second, now.microsecond/1000))
                out.write('{:0.0f},'.format(data_temp*1000))
                out.write('\n')
        
    # catch a keyboard interrupt to kill the script
    except KeyboardInterrupt:
        stop_flag = True

    t_read_temp.join()

    print('\nCaught Interrupt. Exiting...')

if __name__ == '__main__':
    main()
    sys.exit()
