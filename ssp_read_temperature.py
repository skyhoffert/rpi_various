#!/usr/bin/python3

'''
Launches a program that reads from a temperature sensor and sends that data to a UDP port on localhost.
'''

import json
import pickle
import random
import socket
import sys
import time

# TODO -- remove this once real sensor reading is implemented
def faux_read():
    mu = 20.2 # degrees C
    stddev = 0.1
    return random.gauss(mu, stddev)

# read from the connected temperature sensor
def read_sensor():
    # TODO
    return faux_read()

# send a sampled temperature to a UDP socket
def send_temp(data, socket=None, address=None):
    if not socket or not address:
        return False
    
    sent = socket.sendto(data, address)

def main():
    # open and parse the config file
    with open('config.json') as f:
        config = json.load(f)

    # attempt to set up UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)
    addr = ('127.0.0.1', config['ports']['temperature_1'])

    # start the timer
    time_last = time.time()
    time_now = time.time()
    time_between_samples = config['s_between_samples']
    
    try:
        while True:
            # wait for next sampling to occur
            while time_now - time_last < time_between_samples:
                time_now = time.time()

            # reset the timer
            time_last = time_now

            # read from the sensor
            temp = read_sensor()
            temp = pickle.dumps(temp)

            # send to main program (if running)
            send_temp(temp, socket=sock, address=addr)
    except KeyboardInterrupt:
        pass

    print('\nCaught Interrupt. Exiting...')

if __name__ == '__main__':
    main()
    sys.exit()
